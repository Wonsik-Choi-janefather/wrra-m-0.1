"""Finite Klein cell complex, flat internal transport, density-state response.
Run: python audit_B.py. No network or fitted data. Output: evidence/results.json.
"""
from pathlib import Path
from fractions import Fraction
import json, math, hashlib, sys
import numpy as np
I=np.eye(2); J=np.diag([1.,-1.])
def R(t): return np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])
def rank_exact(a,p=None):
 a=[[int(x)%p if p else Fraction(int(x)) for x in row] for row in a]; nr=len(a); nc=len(a[0]); r=0
 for c in range(nc):
  k=next((k for k in range(r,nr) if a[k][c]),None)
  if k is None: continue
  a[r],a[k]=a[k],a[r]; t=a[r][c]
  a[r]=[(x*pow(t,-1,p))%p for x in a[r]] if p else [x/t for x in a[r]]
  for k in range(r+1,nr):
   if a[k][c]:
    t=a[k][c];a[k]=[(x-t*y)%p for x,y in zip(a[k],a[r])] if p else [x-t*y for x,y in zip(a[k],a[r])]
  r+=1
  if r==nr:break
 return r

def grid(m,n,klein=True,phi=.7,seam=None):
 def v(i,j):return (i%m)*n+j%n
 A=lambda i,j:v(i,j)
 B=lambda i,j:m*n+v(i,j)
 edges=[]; mats=[]
 for i in range(m):
  for j in range(n):
   edges.append((v(i,j),v(i+1, -j if klein and i==m-1 else j)))
   mats.append((J if seam is None else seam) if i==m-1 else I)
 Q=R(phi/n)
 for i in range(m):
  for j in range(n):edges.append((v(i,j),v(i,j+1)));mats.append(Q)
 faces=[]
 for i in range(m):
  for j in range(n):
   middle=(B(0,-j-1),-1) if klein and i==m-1 else (B(i+1,j),1)
   faces.append([(A(i,j),1),middle,(A(i,j+1),-1),(B(i,j),-1)])
 d1=np.zeros((m*n,2*m*n),dtype=np.int64);d2=np.zeros((2*m*n,m*n),dtype=np.int64)
 for e,(u,vv) in enumerate(edges):d1[u,e]-=1;d1[vv,e]+=1
 for f,es in enumerate(faces):
  for e,s in es:d2[e,f]+=s
 return edges,np.array(mats),faces,d1,d2

def face_defect(edges,U,faces):
 worst=0.
 for face in faces:
  P=I.copy();start=None;at=None
  for e,s in face:
   a,b=edges[e] if s==1 else edges[e][::-1]
   if start is None:start=a
   else:assert a==at
   at=b;P=(U[e] if s==1 else U[e].T)@P
  assert at==start
  worst=max(worst,float(np.max(np.abs(P-I))))
 return worst

def energy(rho,edges,U,c):return .5*sum(c[e]*float(np.sum((rho[v]-U[e]@rho[u]@U[e].T)**2)) for e,(u,v) in enumerate(edges))
def step(rho,edges,U,c,eta):
 out=rho.copy()
 for e,(u,v) in enumerate(edges):
  out[v]+=eta*c[e]*(U[e]@rho[u]@U[e].T-rho[v])
  out[u]+=eta*c[e]*(U[e].T@rho[v]@U[e]-rho[u])
 return out

def main():
 m,n=5,7;phi=.7;edges,U,faces,d1,d2=grid(m,n)
 checks={};out={'parameters':{'m':m,'n':n,'phi':phi,'kappa':1,'seed':20261008},'scope':'Exact finite-complex checks and floating-point state transport, not measured spacetime topology or gravitational prediction.'}
 checks['boundary_squared_zero']=bool(np.all(d1@d2==0))
 checks['each_edge_two_faces']=bool(np.all(np.count_nonzero(d2,axis=1)==2))
 rk1=rank_exact(d1);rk2=rank_exact(d2);rk12=rank_exact(d1,2);rk22=rank_exact(d2,2)
 betti=[m*n-rk1,2*m*n-rk1-rk2,m*n-rk2];betti2=[m*n-rk12,2*m*n-rk12-rk22,m*n-rk22]
 te,tU,tf,td1,td2=grid(m,n,False,0,seam=J)
 tr1=rank_exact(td1);tr2=rank_exact(td2);tbetti=[m*n-tr1,2*m*n-tr1-tr2,m*n-tr2]
 out['complex']={'vertices':m*n,'edges':2*m*n,'faces':m*n,'Euler_characteristic':0,'Klein_Betti_Q':betti,'Klein_Betti_F2':betti2,'torus_Betti_Q':tbetti,'rank_d1_Q':rk1,'rank_d2_Q':rk2}
 checks['homology_Klein_Q']=betti==[1,1,0];checks['homology_Klein_F2']=betti2==[1,2,1];checks['homology_torus_Q']=tbetti==[1,2,1]
 defect=face_defect(edges,U,faces);torusdef=face_defect(te,tU,tf)
 _,badU,_,_,_=grid(m,n,False,phi,seam=J)
 baddef=face_defect(te,badU,tf)
 out['holonomy']={'Klein_face_max_defect':defect,'torus_J_I_face_max_defect':torusdef,'incompatible_torus_face_defect':baddef,'Klein_relation_defect':float(np.max(np.abs(J@R(phi)@J-R(-phi)))),'torus_J_Rphi_relation_defect':float(np.max(np.abs(J@R(phi)-R(phi)@J)))}
 checks['flat_faces']=defect<1e-12;checks['torus_flat_counterexample']=torusdef<1e-12;checks['invalid_torus_detected']=baddef>.1
 rho=np.array([[.5,.25],[.25,.5]]);pure=np.full((2,2),.5);mixed=I/2
 delta=lambda x,W:float(np.sum((W@x@W.T-x)**2))
 out['loop_response']={'rho':rho.tolist(),'D_J':delta(rho,J),'D_J_pure':delta(pure,J),'D_J_mixed':delta(mixed,J),'D_J_squared':delta(rho,J@J),'D_torus_J':delta(rho,J)}
 checks['loop_exact_cases']=abs(delta(rho,J)-.5)<1e-15 and abs(delta(pure,J)-2)<1e-15 and delta(mixed,J)==0 and delta(rho,J@J)==0
 rng=np.random.default_rng(20261008);raw=rng.normal(size=(m*n,2,2));field=raw@raw.transpose(0,2,1);field/=np.trace(field,axis1=1,axis2=2)[:,None,None]
 cochain_error=0.
 for face in faces:
  total=np.zeros((2,2))
  for e,sign in face:
   u,v=edges[e] if sign==1 else edges[e][::-1];W=U[e] if sign==1 else U[e].T
   total=W@total@W.T+field[v]-W@field[u]@W.T
  cochain_error=max(cochain_error,float(np.max(np.abs(total))))
 checks['covariant_boundary_squared_zero']=cochain_error<1e-12
 out['cochain_max_error']=cochain_error
 angles=rng.uniform(-math.pi,math.pi,m*n);G=np.array([R(t)@(J if k%3==0 else I) for k,t in enumerate(angles)])
 Up=np.array([G[v]@U[e]@G[u].T for e,(u,v) in enumerate(edges)]);fp=G@field@G.transpose(0,2,1)
 c=rng.uniform(.5,1.5,len(edges));degrees=np.zeros(m*n)
 for e,(u,v) in enumerate(edges):degrees[u]+=c[e];degrees[v]+=c[e]
 eta=.9/float(degrees.max());E=energy(field,edges,U,c);Eg=energy(fp,edges,Up,c)
 gaugeD=delta(G[0]@rho@G[0].T,G[0]@J@G[0].T)
 step_error=float(np.max(np.abs(step(fp,edges,Up,c,eta)-G@step(field,edges,U,c,eta)@G.transpose(0,2,1))))
 out['gauge']={'energy_before':E,'energy_after':Eg,'energy_absolute_difference':abs(E-Eg),'loop_response_difference':abs(gaugeD-.5),'update_max_difference':step_error}
 checks['gauge_energy']=abs(E-Eg)<1e-12;checks['gauge_loop']=abs(gaugeD-.5)<1e-12;checks['gauge_update']=step_error<1e-12
 e=0;h=1e-5;cp=c.copy();cm=c.copy();cp[e]+=h;cm[e]-=h
 fd=(energy(field,edges,U,cp)-energy(field,edges,U,cm))/(2*h);u,v=edges[e];analytic=.5*float(np.sum((field[v]-U[e]@field[u]@U[e].T)**2))
 out['weight_response']={'edge':e,'analytic':analytic,'central_difference':fd,'absolute_error':abs(fd-analytic)};checks['weight_derivative']=abs(fd-analytic)<1e-8
 energies=[E];min_eig=1.;trace_error=0.
 for k in range(1000):
  field=step(field,edges,U,c,eta);energies.append(energy(field,edges,U,c));min_eig=min(min_eig,float(np.linalg.eigvalsh(field).min()));trace_error=max(trace_error,float(np.max(np.abs(np.trace(field,axis1=1,axis2=2)-1))))
 out['diffusion']={'steps':1000,'eta':eta,'max_degree':float(degrees.max()),'initial_energy':energies[0],'final_energy':energies[-1],'largest_energy_increment':float(np.max(np.diff(energies))),'minimum_eigenvalue_over_updates':min_eig,'max_trace_error':trace_error,'max_final_distance_from_mixed':float(np.max(np.abs(field-I/2)))}
 checks['energy_monotone']=bool(np.max(np.diff(energies))<1e-12);checks['PSD_trace_preserved']=min_eig>=-1e-12 and trace_error<1e-12
 # Full source register geometry: H spectator sheets, keep the zero-weight reference vertex.
 L,C,H=500,70,29;N=L*C*H
 l=np.tile(np.arange(L),C);z=np.repeat(np.arange(C),L)
 target=np.where(z==C-1,(-l)%L,l)+L*((z+1)%C)
 inverse=np.where(z==0,(-l)%L,l)+L*((z-1)%C)
 checks['full_sheet_seam_bijection']=bool(np.array_equal(np.sort(target),np.arange(L*C)) and np.array_equal(inverse[target],np.arange(L*C)))
 walk=np.arange(L*C)
 for _ in range(C):walk=target[walk]
 checks['full_sheet_single_return']=bool(np.array_equal(walk,(-l)%L+L*z))
 for _ in range(C):walk=target[walk]
 checks['full_sheet_double_return']=bool(np.array_equal(walk,np.arange(L*C)))
 out['source_register']={'L':L,'C':C,'H_spectator_sheets':H,'vertices':N,'edges':2*N,'faces':N,'active_arithmetic_addresses':N-1,'address_1_seam_step_destination':1+L*H,'reference_vertex_retained':True,'meaning':'Disjoint H-sheet cellulation indexed by the source tuples, not a connected universe or a derived carrier dimension.'}
 checks['excluded_reference_not_invariant_under_step']=out['source_register']['address_1_seam_step_destination']!=1
 checks={k:bool(v) for k,v in checks.items()};out['checks']=checks;out['status']='PASS' if all(checks.values()) else 'FAIL';out['versions']={'python':sys.version.split()[0],'numpy':np.__version__};out['audit_source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 dest=Path(__file__).parent/'evidence';dest.mkdir(exist_ok=True);(dest/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));assert all(checks.values())
if __name__=='__main__':main()
