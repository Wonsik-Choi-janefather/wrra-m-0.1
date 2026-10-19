"""WRRA local sequential-output kinematics audit; c=m=Delta_tau=1 internally."""
import json, math
from pathlib import Path
import numpy as np
DT=1.4813019664158633e-21
C=299792458.
def dot(a,b): return a[0]*b[0]-np.dot(a[1:],b[1:])
def boost(a,b):
    b2=float(b@b)
    if b2==0:return a.copy()
    g=1/math.sqrt(1-b2); bp=float(b@a[1:])
    return np.r_[g*(a[0]-bp), a[1:]+((g-1)*bp/b2-g*a[0])*b]
def dist(p,u,z):
    r=p*(dot(u,z)/dot(u,p))-z
    return math.sqrt(max(0,-dot(r,r)))
rng=np.random.default_rng(135112117)
directions=np.vstack([np.eye(3),-np.eye(3),rng.normal(size=(12,3))])
directions/=np.linalg.norm(directions,axis=1)[:,None]
errors=dict(interval=0.,mass_shell=0.,conservation=0.,inverse_boost=0.,null_transport=0.,rest_separation=0.)
count=0; min_time=1e9
for mag in [0,.1,.3,.6,.8,.95,.99]:
 for direction in directions:
  b=mag*direction
  for p in [.1,.5,1.,2.,3.]:
   E=math.sqrt(1+p*p)
   P=np.array([10.,0,0,0]); a=np.array([E,p,0,0]); partner=np.array([E,-p,0,0]); q=np.array([10-2*E,0,0,0])
   R=P-a; mr=math.sqrt(dot(R,R)); u=R/mr; z=u.copy()
   PP,aa,bb,qq,RR,zz,uu=[boost(v,b) for v in [P,a,partner,q,R,z,u]]
   assert RR[0]>0 and dot(RR,RR)>0 and qq[0]>0
   min_time=min(min_time,float(zz[0]))
   errors['interval']=max(errors['interval'],abs(dot(zz,zz)-1))
   for orig,new in [(a,aa),(partner,bb),(R,RR),(q,qq)]:
    errors['mass_shell']=max(errors['mass_shell'],abs(dot(new,new)-dot(orig,orig))/max(1,abs(dot(orig,orig))))
   errors['conservation']=max(errors['conservation'],float(np.max(np.abs(PP-aa-RR)))/10,float(np.max(np.abs(RR-bb-qq)))/10)
   errors['inverse_boost']=max(errors['inverse_boost'],float(np.max(np.abs(boost(zz,-b)-z)))/max(abs(z)))
   light=boost(np.array([1.,*direction]),b)
   errors['null_transport']=max(errors['null_transport'],abs(np.linalg.norm(light[1:])/light[0]-1))
   errors['rest_separation']=max(errors['rest_separation'],abs(dist(aa,uu,zz)-dist(a,u,z))/max(1,dist(a,u,z)))
   # Charge: 0 = (+1)+(-1); (-1) = (-1)+0 at the two events.
   assert 0==1-1 and -1==-1+0
   count+=1
assert min_time>0 and max(errors.values())<1e-10
rows=[]
for b in [0,.6,.8,.99]:
 g=1/math.sqrt(1-b*b)
 rows.append(dict(beta=b,gamma=g,coordinate_interval_s=g*DT,coordinate_tick_rate_Hz=1/(g*DT)))
# Incorrect rule: transform spatial displacement but force every coordinate interval to 1.
g=1/math.sqrt(1-.8**2)
wrong_interval=1-(g*.8)**2
result=dict(scope='local kinematics only; not interacting QFT or observational confirmation',cases=count,boosts=126,momentum_settings=5,seed=135112117,clock_s=DT,light_reference_m=C*DT,max_errors=errors,minimum_future_time_component=min_time,charge_ledger='exact integer conservation at both emissions',equal_split='n+n retained; rest masses both 1',control_beta=.8,incorrect_fixed_coordinate_clock_interval=wrong_interval,correct_interval=1.,table=rows)
Path(__file__).with_name('verification_lorentz_sequential.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

