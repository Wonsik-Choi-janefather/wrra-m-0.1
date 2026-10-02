#!/usr/bin/env python3
"""WRRA-M upstream 0.4: retained spatial modes and a field-dependent mixing link.

Known axial/magnetic inputs calibrate C, c0 and eta once.  Electromagnetic
response is then -dH/db, with b=mu_N B measured in MeV; it is not an added
state-independent c1.  The Gaussian/Jacobi construction is a disclosed
finite effective completion, not a solution of full QCD or compactification.
"""
from pathlib import Path
import copy, hashlib, itertools, json, math
import numpy as np
from numpy.polynomial.hermite import hermgauss
from scipy.linalg import expm
import inherited_v0_3_r1 as old

ROOT=Path(__file__).resolve().parent
SX=np.array([[0.,1.],[1.,0.]])

def check_inputs(inp):
    legacy=copy.deepcopy(inp)
    legacy['axial_comparison']=legacy['axial_calibration']
    old.validate_inputs(legacy)
    c=inp['internal_completion']
    ell=c['ell_dimensionless']
    if not math.isfinite(ell) or ell<=0: raise ValueError('ell must be finite and positive')
    if c['quadrature_order']<5 or not isinstance(c['quadrature_order'],int):
        raise ValueError('quadrature order must be an integer >= 5 (degree-eight leakage norm)')
    if c['delta_mode']!='mass_reference': raise ValueError('only the declared mass_reference delta is supported')
    if c['magnetic_link_model']!='linear_field_deformation': raise ValueError('unsupported magnetic link model')
    if any(not math.isfinite(x) or x<=0 for x in c['delta_sensitivity_MeV']):
        raise ValueError('positive finite gaps required')
    if any(not math.isfinite(x) or x<=0 for x in c['response_field_steps_MeV']):
        raise ValueError('positive finite response steps required')

def gauss6(order=5,ell=1.):
    z,w=hermgauss(order)
    indices=np.array(list(itertools.product(range(order),repeat=6)))
    points=z[indices]*ell
    weights=np.prod(w[indices],axis=1)/math.pi**3
    return points,weights

def shapes(points,ell=1.):
    x,y=points[:,:3],points[:,3:]
    return np.column_stack(((np.sum(x*x,axis=1)-np.sum(y*y,axis=1)),2*np.sum(x*y,axis=1)))/(math.sqrt(3)*ell**2)

def state_from_rows(rows,space):
    v=np.zeros(64)
    for r in rows:
        if r['space']==space:
            a,b,c=r['spin_flavor'];v[16*a+4*b+c]=r['amplitude']
    return v

def spatial_completion(sf,inp):
    ell=inp['internal_completion']['ell_dimensionless']
    points,w=gauss6(inp['internal_completion']['quadrature_order'],ell)
    raw=shapes(points,ell)
    # J maps three particle coordinates to orthonormal Jacobi coordinates.
    J=np.array([[1.,-1.,0.],[1/math.sqrt(3),1/math.sqrt(3),-2/math.sqrt(3)]])/math.sqrt(2)
    pairs=points.reshape(-1,2,3)
    physical=[];equations=[]
    for r in sf['spatial_representations']:
        perm=r['permutation'];inverse=np.argsort(perm)
        R=np.eye(3)[inverse]
        A=J@R@J.T
        transformed=np.einsum('ab,nbk->nak',A,pairs).reshape(-1,6)
        D=raw.T@(w[:,None]*shapes(transformed,ell))
        target=np.array(r['spatial_representation'])[1:,1:]
        physical.append(D)
        # aligned shape columns raw @ O, D O = O target
        equations.append(np.kron(np.eye(2),D)-np.kron(target.T,np.eye(2)))
    _,singular,vt=np.linalg.svd(np.vstack(equations))
    O=vt[-1].reshape(2,2,order='F')*math.sqrt(2)
    if O.flat[np.argmax(abs(O))]<0:O=-O
    alignment_error=max(np.linalg.norm(D@O-O@np.array(r['spatial_representation'])[1:,1:]) for D,r in zip(physical,sf['spatial_representations']))
    e=raw@O
    f=np.column_stack((np.ones(len(w)),e))
    gram=f.T@(w[:,None]*f)
    X=[f.T@(w[:,None]*e[:,a,None]*f) for a in range(2)]
    states=sf['state_basis']
    Sp=state_from_rows(states['proton_S'],'S')
    Sn=state_from_rows(states['neutron_S'],'S')
    Ep=np.column_stack([state_from_rows(states['proton_M'],'E'+str(a+1))*math.sqrt(2) for a in range(2)])
    En=np.column_stack([state_from_rows(states['neutron_M'],'E'+str(a+1))*math.sqrt(2) for a in range(2)])
    lower=sum(old.parent.at_slot(np.kron(np.eye(2),np.array([[0,0],[1,0]])),s) for s in range(3))
    spin_pairs=[(Sp,Ep),(Sn,En),(lower@Sp,lower@Ep),(lower@Sn,lower@En)]
    T=[sum(np.outer(s,E[:,a])+np.outer(E[:,a],s) for s,E in spin_pairs)/math.sqrt(2) for a in range(2)]
    W=sum(np.kron(t,x) for t,x in zip(T,X))
    pS=np.kron(Sp,[1,0,0]);nS=np.kron(Sn,[1,0,0])
    pM=sum(np.kron(Ep[:,a],np.eye(3)[:,a+1]) for a in range(2))/math.sqrt(2)
    nM=sum(np.kron(En[:,a],np.eye(3)[:,a+1]) for a in range(2))/math.sqrt(2)
    bp=np.column_stack((pS,pM));bn=np.column_stack((nS,nM))
    Wp=bp.T@W@bp;Wn=bn.T@W@bn
    charge=np.kron(sum(old.parent.at_slot(np.diag([2/3,2/3,-1/3,-1/3]),s) for s in range(3)),np.eye(3))
    Sz=np.kron(sum(old.parent.at_slot(np.kron(np.eye(2),np.diag([1,-1])),s) for s in range(3)),np.eye(3))
    Iz=np.kron(sum(old.parent.at_slot(np.kron(np.diag([1,-1]),np.eye(2)),s) for s in range(3)),np.eye(3))
    pauli=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
    spin=[np.kron(sum(old.parent.at_slot(np.kron(np.eye(2),a/2),s) for s in range(3)),np.eye(3)) for a in pauli]
    isospin=[np.kron(sum(old.parent.at_slot(np.kron(a/2,np.eye(2)),s) for s in range(3)),np.eye(3)) for a in pauli]
    Wmag=Iz@Sz@W
    group_errors=[]
    for r in sf['spatial_representations']:
        U=np.kron(old.perm_matrix(r['permutation']),np.array(r['spatial_representation']))
        group_errors.append(np.linalg.norm(U@W@U.T-W))
    # Bare multiplication is NOT closed under the retained three spatial modes.
    # Its norm on M is calculated before projection using exact Gaussian moments.
    psiM=e@Ep.T/math.sqrt(2)
    bare_out=sum(e[:,a,None]*(psiM@T[a].T) for a in range(2))
    total_norm2=float(np.sum(w*np.sum(bare_out**2,axis=1)))
    projected_norm2=float(np.linalg.norm(W@pM)**2)
    # Dimensionless six-dimensional oscillator K = -ell^2 laplacian/2 + rho^2/(2ell^2).
    # The traceless degree-two harmonic polynomials obey K(P phi_S)=5 P phi_S.
    Araw=[np.diag([1,1,1,-1,-1,-1])/(math.sqrt(3)*ell**2),np.block([[np.zeros((3,3)),np.eye(3)],[np.eye(3),np.zeros((3,3))]])/(math.sqrt(3)*ell**2)]
    Aaligned=[sum(O[b,a]*Araw[b] for b in range(2)) for a in range(2)]
    harmonic_laplacian=np.array([2*np.trace(a) for a in Aaligned])
    euler=np.column_stack([2*np.einsum('ni,ij,nj->n',points,a,points) for a in Aaligned])
    Kf=np.column_stack((3*np.ones(len(w)),3*e+euler-ell**2*harmonic_laplacian/2))
    Kblock=f.T@(w[:,None]*Kf)
    checks={
      'spatial_gram_identity':np.linalg.norm(gram-np.eye(3))<2e-12,
      'physical_E_intertwines_spin_flavor_E':alignment_error<2e-12,
      'alignment_orthogonal':np.linalg.norm(O.T@O-np.eye(2))<2e-12,
      'spatial_S_E_matrix_elements':max(np.linalg.norm(X[a][0,1:]-np.eye(2)[a]) for a in range(2))<2e-12,
      'spatial_even_parity':np.max(abs(shapes(-points,ell)-raw))<2e-12,
      'spatial_ell_scaling':np.max(abs(shapes(points*1.7,ell*1.7)-raw))<2e-12,
      'projected_link_hermitian':np.linalg.norm(W-W.T)<2e-12,
      'link_permutation_invariant':max(group_errors)<2e-12,
      'link_conserves_charge':np.linalg.norm(charge@W-W@charge)<2e-12,
      'link_conserves_spin_projection':np.linalg.norm(Sz@W-W@Sz)<2e-12,
      'link_is_spin_rotation_scalar':max(np.linalg.norm(j@W-W@j) for j in spin)<2e-12,
      'link_is_isospin_scalar':max(np.linalg.norm(j@W-W@j) for j in isospin)<2e-12,
      'spatial_quadratic_harmonic_and_L_zero':max(abs(harmonic_laplacian))<2e-12 and np.max(abs(euler-2*e))<2e-12,
      'oscillator_mode_gap_two_units':np.linalg.norm(Kblock-np.diag([3,5,5]))<2e-12,
      'magnetic_link_hermitian_charge_conserving':np.linalg.norm(Wmag-Wmag.T)<2e-12 and np.linalg.norm(charge@Wmag-Wmag@charge)<2e-12,
      'both_nucleon_link_blocks_sigma_x':max(np.linalg.norm(Wp-SX),np.linalg.norm(Wn-SX))<2e-12,
      'magnetic_link_isovector_signs':max(np.linalg.norm(bp.T@Wmag@bp-SX),np.linalg.norm(bn.T@Wmag@bn+SX))<2e-12,
      'retained_nucleon_subspace_invariant':max(np.linalg.norm(W@b-b@SX) for b in (bp,bn))<2e-12,
      'unprojected_leakage_disclosed':total_norm2>projected_norm2+1e-3,
    }
    return {'ell_dimensionless':ell,'quadrature_nodes':len(w),'quadrature_order':inp['internal_completion']['quadrature_order'],
       'normalization':'phi_S=(pi ell^2)^(-3/2) exp[-(x^2+y^2)/(2 ell^2)]; phi_E=(X_raw O) phi_S',
       'alignment_O':O.tolist(),'alignment_error':alignment_error,'spatial_gram':gram.tolist(),
       'spatial_X_blocks':[m.tolist() for m in X],'proton_W_block':Wp.tolist(),'neutron_W_block':Wn.tolist(),
       'dimensionless_oscillator_block':Kblock.tolist(),
       'maximum_link_permutation_error':max(group_errors),
       'unprojected_M_norm_squared':total_norm2,'retained_M_norm_squared':projected_norm2,
       'discarded_M_norm_squared':total_norm2-projected_norm2,
       'scope':'Explicit Gaussian/Jacobi effective modes with retained-space projection. Bare polynomial multiplication has higher-mode leakage; it is not silently treated as a closed untruncated binding theory.',
       'checks':{k:bool(v) for k,v in checks.items()}},Wp

def response_energies(inp,blocks):
    mp=inp['masses']['proton'];mn=inp['masses']['neutron']
    eu=(2*mp-mn)/3;ed=(2*mn-mp)/3
    mu_u=2/3*mp/eu;mu_d=-1/3*mp/ed
    Dp=mu_u*blocks['proton_up_spin']+mu_d*blocks['proton_down_spin']
    Dn=mu_u*blocks['neutron_up_spin']+mu_d*blocks['neutron_down_spin']
    return eu,ed,mu_u,mu_d,Dp,Dn

def calibration(inp,blocks,W):
    _,_,mu_u,mu_d,Dp,Dn=response_energies(inp,blocks)
    g=abs(inp['axial_calibration']['signed_lambda'])
    q=(5/3-g)/(4/3);x=math.sqrt(q*(1-q))/(1-2*q)
    ri=inp['inherited'];R=old.euler_activity(3,ri['alpha'],ri['N'])*old.euler_activity(5,ri['alpha'],ri['N'])
    c0=(sum(inp['magnetic_moments_muN'].values())-mu_u-mu_d)/2
    c1=(inp['magnetic_moments_muN']['proton']-inp['magnetic_moments_muN']['neutron']-(mu_u-mu_d)*g)/2
    coherence=old.expect(W,q)
    return {'C':x/math.sqrt(R),'c0':c0,'eta':c1/(x*coherence),'q_calibration':q,'x_calibration':x,
        'c1_target_muN':c1,'activity_reference':R,'coherence':coherence}

def spectrum(raw):
    val,vec=np.linalg.eigh(raw)
    if vec[0,0]<0:vec[:,0]*=-1
    # Choose excited vector (-sqrt(q),sqrt(1-q)) to make transitions reproducible.
    if vec[1,1]<0:vec[:,1]*=-1
    return val,vec

def evaluate(inp,blocks,W,pars,primes=(3,5),delta=None,field=0.,model='link'):
    ri=inp['inherited'];R=math.prod(old.euler_activity(p,ri['alpha'],ri['N']) for p in primes)
    x=pars['C']*math.sqrt(R)
    mp,mn=(inp['masses'][k] for k in ('proton','neutron'))
    if delta is None:delta=(mp+mn)/6
    raw=delta*np.array([[0.,-x],[-x,1.]])
    ev,states=spectrum(raw);ground=states[:,0];q=float(ground[1]**2)
    _,_,mu_u,mu_d,Dp,Dn=response_energies(inp,blocks)
    g=float(ground@blocks['axial']@ground);v=float(ground@blocks['vector']@ground)
    results={}
    for name,sign,mass,D in [('proton',1,mp,Dp),('neutron',-1,mn,Dn)]:
        Mex=sign*pars['eta']*x*W if model=='link' else sign*pars['c1_target_muN']*np.eye(2)
        M=D+pars['c0']*np.eye(2)+Mex
        H0=raw+(mass-ev[0])*np.eye(2)
        H=H0-field*M
        vals,vec=spectrum(H)
        groundB=vec[:,0]
        transformed=states.T@M@states
        trans=float(transformed[0,1]);gap=float(ev[1]-ev[0])
        curvature=2*trans**2/gap
        results[name]={'hamiltonian_zero_MeV':H0.tolist(),'magnetic_operator_muN':M.tolist(),
          'magnetic_exchange_operator_muN':Mex.tolist(),'ground_moment_muN':float(transformed[0,0]),
          'excited_moment_muN':float(transformed[1,1]),'transition_moment_muN':trans,
          'reduced_internal_susceptibility_MeV_minus1':curvature,
          'c1_expectation_signed_muN':float(ground@Mex@ground),
          'field_b_MeV':field,'field_energy_MeV':float(vals[0]),
          'field_ground_moment_muN':float(groundB@M@groundB),
          'field_q':float(groundB[1]**2),'ground_mass_MeV':float(np.linalg.eigvalsh(H0)[0])}
    wc=inp['weak_constants'];me=inp['masses']['electron'];Q=mn-mp-me
    phase=old.phase(Q,me,wc['alpha_em'])
    pref=(wc['GF_GeV_minus2']*1e-6)**2*wc['Vud']**2*me**5/(2*math.pi**3*wc['hbar_MeV_s'])
    rate=ri['kappa']**2*R*pref*(v*v+3*g*g)*phase
    return {'primes':list(primes),'activity':R,'delta_MeV':delta,'x':x,'off_diagonal_t_MeV':delta*x,
      'q':q,'ground_vector':ground.tolist(),'gap_MeV':float(ev[1]-ev[0]),'charge_proton':1.,'charge_neutron':0.,
      'vector':v,'axial_magnitude':g,'mean_life_s':1/rate,'phase_space':phase,'nucleons':results}

def field_checks(inp,blocks,W,pars,result):
    checks={};rows=[]
    for h in inp['internal_completion']['response_field_steps_MeV']:
        plus=evaluate(inp,blocks,W,pars,field=h);minus=evaluate(inp,blocks,W,pars,field=-h)
        for name in ('proton','neutron'):
            b=result['nucleons'][name];p=plus['nucleons'][name];m=minus['nucleons'][name]
            first=-(p['field_energy_MeV']-m['field_energy_MeV'])/(2*h)
            # Differentiate Hellmann-Feynman moment rather than cancelling two mass anchors.
            second=(p['field_ground_moment_muN']-m['field_ground_moment_muN'])/(2*h)
            operator=-(np.array(p['hamiltonian_zero_MeV'])-h*np.array(p['magnetic_operator_muN'])-(np.array(m['hamiltonian_zero_MeV'])+h*np.array(m['magnetic_operator_muN'])))/(2*h)
            checks[f'{name}_energy_derivative_h{h}']=abs(first-b['ground_moment_muN'])<2e-7
            checks[f'{name}_moment_derivative_h{h}']=abs(second-b['reduced_internal_susceptibility_MeV_minus1'])<2e-9
            checks[f'{name}_operator_derivative_h{h}']=np.linalg.norm(operator-np.array(b['magnetic_operator_muN']))<2e-9
            rows.append({'nucleon':name,'h_MeV':h,'minus_energy_derivative':first,'moment_derivative':second})
    return rows,checks

def controls(inp,blocks,W,pars,baseline):
    rows=[];checks={}
    def add(name,change):
        c=copy.deepcopy(inp);change(c);check_inputs(c);r=evaluate(c,blocks,W,pars)
        rows.append({'name':name,'q':r['q'],'axial':r['axial_magnitude'],'mean_life_s':r['mean_life_s'],
         'mu_p':r['nucleons']['proton']['ground_moment_muN'],'mu_n':r['nucleons']['neutron']['ground_moment_muN'],'activity':r['activity']})
        return r
    n=add('N=100',lambda c:c['inherited'].update(N=100))
    checks['finite_cutoff_changes_coupling_state_and_rate']=abs(n['q']-baseline['q'])>1e-4 and abs(n['mean_life_s']-baseline['mean_life_s'])>1e-2
    a=add('alpha+0.05',lambda c:c['inherited'].update(alpha=c['inherited']['alpha']+.05))
    checks['alpha_changes_coupling_state_and_response']=abs(a['q']-baseline['q'])>1e-3 and abs(a['nucleons']['proton']['ground_moment_muN']-baseline['nucleons']['proton']['ground_moment_muN'])>1e-3
    z=add('alpha_em=0',lambda c:c['weak_constants'].update(alpha_em=0.))
    checks['EM_phase_input_changes_rate_without_recalibration']=z['mean_life_s']>baseline['mean_life_s'] and abs(z['q']-baseline['q'])<1e-12
    k=add('kappa*1.02',lambda c:c['inherited'].update(kappa=c['inherited']['kappa']*1.02))
    checks['kappa_square_rate_scaling']=abs(k['mean_life_s']/baseline['mean_life_s']-1/1.02**2)<1e-12
    m=add('mn+0.01_MeV',lambda c:c['masses'].update(neutron=c['masses']['neutron']+.01))
    checks['mass_input_changes_moments_phase_and_rate']=abs(m['mean_life_s']-baseline['mean_life_s'])>1 and abs(m['nucleons']['proton']['ground_moment_muN']-baseline['nucleons']['proton']['ground_moment_muN'])>1e-6
    for key,magnitude in [('eta',1.1),('C',1.1)]:
        pp=dict(pars);pp[key]*=magnitude;r=evaluate(inp,blocks,W,pp)
        checks[key+'_changes_response']=abs(r['nucleons']['proton']['ground_moment_muN']-baseline['nucleons']['proton']['ground_moment_muN'])>1e-3
        if key=='eta':checks['eta_leaves_zero_field_axial_fixed']=abs(r['axial_magnitude']-baseline['axial_magnitude'])<1e-12
        else:checks['C_changes_shared_state_axial']=abs(r['axial_magnitude']-baseline['axial_magnitude'])>1e-3
    invalid=[]
    changes=[('ell_zero',lambda c:c['internal_completion'].update(ell_dimensionless=0.)),('negative_gap',lambda c:c['internal_completion'].update(delta_sensitivity_MeV=[-1.])),('N_bool',lambda c:c['inherited'].update(N=True)),('N_too_small',lambda c:c['inherited'].update(N=10)),('axial_boundary',lambda c:c['axial_calibration'].update(signed_lambda=-1.)),('negative_EM',lambda c:c['weak_constants'].update(alpha_em=-.1)),('closed_beta',lambda c:c['masses'].update(neutron=938.3))]
    for name,change in changes:
        c=copy.deepcopy(inp);change(c)
        try:check_inputs(c)
        except ValueError:ok=True
        else:ok=False
        checks['reject_'+name]=ok;invalid.append({'name':name,'rejected':ok})
    return rows,invalid,checks

def main():
    inp=json.loads((ROOT/'inputs.json').read_text());check_inputs(inp)
    sf,blocks=old.finite_states()
    spatial,W=spatial_completion(sf,inp)
    pars=calibration(inp,blocks,W)
    result=evaluate(inp,blocks,W,pars)
    scalar=evaluate(inp,blocks,W,pars,model='scalar')
    derivative,checks=field_checks(inp,blocks,W,pars,result)
    control,invalid,cc=controls(inp,blocks,W,pars,result);checks.update(cc)
    checks.update({'inherited_'+k:v for k,v in sf['checks'].items()})
    checks.update(spatial['checks'])
    checks['calibrated_axial_returned']=abs(result['axial_magnitude']-abs(inp['axial_calibration']['signed_lambda']))<1e-12
    checks['joint_magnetic_inputs_returned']=all(abs(result['nucleons'][n]['ground_moment_muN']-inp['magnetic_moments_muN'][n])<1e-12 for n in ('proton','neutron'))
    checks['c1_emerges_from_field_derivative']=all(abs(result['nucleons'][n]['c1_expectation_signed_muN']-s*pars['c1_target_muN'])<1e-12 for n,s in [('proton',1),('neutron',-1)])
    checks['mass_anchors_returned']=max(abs(result['nucleons'][n]['ground_mass_MeV']-inp['masses'][n]) for n in ('proton','neutron'))<1e-9
    checks['parent_reference_matches_frozen_file']=(inp['parent_calibration_reference']==json.loads((ROOT/'frozen_parent_reference.json').read_text()))
    ref=inp['parent_calibration_reference'];frozen=copy.deepcopy(inp)
    frozen['masses']=ref['masses'];frozen['weak_constants']=ref['weak_constants'];frozen['inherited']=ref['inherited']
    frozen['axial_calibration']['signed_lambda']=-ref['axial_magnitude']
    refpars=calibration(frozen,blocks,W);reference=evaluate(frozen,blocks,W,refpars)
    checks['frozen_parent_lifetime_reproduced']=abs(reference['mean_life_s']-ref['inherited']['neutron_mean_life_s'])<1e-8
    # Commuting charge and isoscalar mixing permit unitary expectation transport.
    H=np.array(result['nucleons']['proton']['hamiltonian_zero_MeV'])
    rho=np.outer(result['ground_vector'],result['ground_vector'])
    U=expm(-1j*(H-np.trace(H)/2*np.eye(2))/result['delta_MeV'])
    evolved=U@rho@U.conj().T
    checks['internal_actual_trace_and_positivity']=abs(np.trace(evolved)-1)<1e-12 and np.linalg.eigvalsh(evolved).min()>-1e-12
    checks['internal_energy_conserved']=abs(np.trace(H@evolved)-np.trace(H@rho))<1e-9
    tr=old.parent.transport(1/result['mean_life_s'],inp['masses']['neutron'])
    tr['checks']={k:bool(v) for k,v in tr['checks'].items()}
    checks.update({'transport_'+k:bool(v) for k,v in tr['checks'].items()})
    scales=[evaluate(inp,blocks,W,pars,delta=d) for d in inp['internal_completion']['delta_sensitivity_MeV']]
    checks['gap_changes_leave_static_joint_readouts_fixed']=all(abs(r['q']-result['q'])<1e-12 and abs(r['nucleons']['proton']['ground_moment_muN']-result['nucleons']['proton']['ground_moment_muN'])<1e-12 for r in scales)
    checks['gap_response_susceptibility_inverse_scaling']=all(abs(r['nucleons']['proton']['reduced_internal_susceptibility_MeV_minus1']*r['delta_MeV']-result['nucleons']['proton']['reduced_internal_susceptibility_MeV_minus1']*result['delta_MeV'])<1e-12 for r in scales)
    checks['scalar_and_link_same_ground_moments']=all(abs(scalar['nucleons'][n]['ground_moment_muN']-result['nucleons'][n]['ground_moment_muN'])<1e-12 for n in ('proton','neutron'))
    checks['scalar_and_link_different_excited_and_transition_response']=all(abs(scalar['nucleons'][n]['excited_moment_muN']-result['nucleons'][n]['excited_moment_muN'])>1e-3 and abs(scalar['nucleons'][n]['transition_moment_muN']-result['nucleons'][n]['transition_moment_muN'])>1e-3 for n in ('proton','neutron'))
    checks={k:bool(v) for k,v in checks.items()}
    if not all(checks.values()):raise AssertionError({k:v for k,v in checks.items() if not v})
    families=[evaluate(inp,blocks,W,pars,primes=p) for p in ((3,5),(3,7),(5,7),(3,11),(5,11))]
    out={'title':'WRRA-M internal spatial coupling and joint currents upstream v0.4','author':'Wonsik Choi','date':'2026-10-02',
      'input_roles':'masses, moments and axial ratio are joint calibration inputs; prime labels, finite cutoff and linear field law are declared WRRA constitutive choices; parent weak normalization is frozen',
      'inputs':inp,'input_sha256':hashlib.sha256((ROOT/'inputs.json').read_bytes()).hexdigest(),
      'spatial_completion':spatial,'calibrated_parameters':pars,'baseline':result,'scalar_c1_control':scalar,
      'field_derivative_checks':derivative,'fixed_parameter_prime_cases':families,'delta_sensitivity':scales,
      'fixed_parameter_input_controls':control,'invalid_input_controls':invalid,
      'parent_reference':reference,'conserved_transport':tr,
      'scope':'A finite projected Gaussian/Jacobi effective model. eta is calibrated transverse magnetic information. Reduced internal curvature is conditional on Delta and no explicit b^2 term; it is not identified with a measured Compton polarizability or observed excited baryon.',
      'checks':checks,'checks_passed':sum(checks.values()),'checks_total':len(checks)}
    (ROOT/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'checks_passed':len(checks),'calibration':pars,'baseline':result},ensure_ascii=False,indent=2))
    return out

if __name__=='__main__':main()
