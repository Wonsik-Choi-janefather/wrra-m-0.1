#!/usr/bin/env python3
"""Finite WRRA prime-family binding ansatz and shared spin-flavor currents.

The principal state fit uses supplied nucleon masses and magnetic moments.
Observed axial coupling is only a comparison for that fit. Transferred beta
rates retain the parent 0.2 lifetime normalization, including its axial input.
Spatial S3 labels are an abstract L=0, even-parity representation, not a
solved radial QCD wavefunction. No prime labels are newly identified here.
"""
from pathlib import Path
import hashlib,itertools,json,math
import numpy as np
from scipy.optimize import brentq
import parent_kernel as parent

ROOT=Path(__file__).resolve().parent

def perm_matrix(perm):
    return np.eye(64).reshape(4,4,4,64).transpose((*perm,3)).reshape(64,64)

def fixed_basis(projector,rank):
    columns=[]
    for j in range(projector.shape[1]):
        v=projector[:,j].copy()
        for old in columns:v-=old*np.vdot(old,v).real
        norm=np.linalg.norm(v)
        if norm>1e-9:
            v/=norm
            if v[np.argmax(np.abs(v))]<0:v*=-1
            columns.append(v)
        if len(columns)==rank:break
    assert len(columns)==rank
    return np.column_stack(columns)

def finite_states():
    eye=np.eye(64);pauli=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1])]
    Js=[sum(parent.at_slot(np.kron(np.eye(2),s/2),i) for i in range(3)) for s in pauli]
    Is=[sum(parent.at_slot(np.kron(s/2,np.eye(2)),i) for i in range(3)) for s in pauli]
    J2=sum(j@j for j in Js);I2=sum(i@i for i in Is)
    half=(3.75*eye-J2)/3@(3.75*eye-I2)/3
    perms=list(itertools.permutations(range(3)));Ps=[perm_matrix(p) for p in perms]
    signs=[(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3)) for p in perms]
    sym=sum(Ps)/6;anti=sum(s*P for s,P in zip(signs,Ps))/6;mixed=eye-sym-anti
    seq=list(itertools.product(range(4),repeat=3))
    def sector(ku):return np.diag([float(sum(x<2 for x in s)==ku and sum(1 if x%2==0 else -1 for x in s)==1) for s in seq])
    Sp=fixed_basis((half@sector(2)@sym).real,1)[:,0]
    Ep=fixed_basis((half@sector(2)@mixed).real,2)
    tp=np.array([[0,1],[0,0]]);sz=np.diag([1,-1])
    V=sum(parent.at_slot(np.kron(tp,np.eye(2)),i) for i in range(3)).real
    Az=sum(parent.at_slot(np.kron(tp,sz),i) for i in range(3)).real
    Sn=V.T@Sp;En=V.T@Ep
    space=np.eye(3)
    pS=np.kron(Sp,space[:,0]);nS=np.kron(Sn,space[:,0])
    pM=sum(np.kron(Ep[:,j],space[:,j+1]) for j in range(2))/math.sqrt(2)
    nM=sum(np.kron(En[:,j],space[:,j+1]) for j in range(2))/math.sqrt(2)
    Pbasis=np.column_stack([pS,pM]);Nbasis=np.column_stack([nS,nM])
    Vbig=np.kron(V,np.eye(3));Abig=np.kron(Az,np.eye(3))
    U=sum(parent.at_slot(np.diag([1,-1,0,0]),i) for i in range(3)).real
    D=sum(parent.at_slot(np.diag([0,0,1,-1]),i) for i in range(3)).real
    Ubig=np.kron(U,np.eye(3));Dbig=np.kron(D,np.eye(3))
    Qbig=np.kron(sum(parent.at_slot(np.diag([2/3,2/3,-1/3,-1/3]),i) for i in range(3)),np.eye(3))
    representations=[];symmetry_errors=[]
    for perm,P in zip(perms,Ps):
        Erep=Ep.T@P@Ep;Srep=np.zeros((3,3));Srep[0,0]=1;Srep[1:,1:]=Erep
        total=np.kron(P,Srep)
        symmetry_errors.extend(np.linalg.norm(total@s-s) for s in (pS,nS,pM,nM))
        representations.append({'permutation':list(perm),'spatial_representation':Srep.tolist(),'E_rep_orthogonal_error':float(np.linalg.norm(Erep.T@Erep-np.eye(2))),'neutron_rep_agreement':float(np.linalg.norm(En.T@P@En-Erep))})
    matrices={'vector':Pbasis.T@Vbig@Nbasis,'axial':Pbasis.T@Abig@Nbasis,
              'proton_up_spin':Pbasis.T@Ubig@Pbasis,'proton_down_spin':Pbasis.T@Dbig@Pbasis,
              'neutron_up_spin':Nbasis.T@Ubig@Nbasis,'neutron_down_spin':Nbasis.T@Dbig@Nbasis,
              'proton_isoscalar_spin':(Pbasis.T@np.kron(2*Js[2],np.eye(3))@Pbasis).real,
              'neutron_isoscalar_spin':(Nbasis.T@np.kron(2*Js[2],np.eye(3))@Nbasis).real,
              'proton_collective_isovector_spin':(Pbasis.T@np.kron(4*Is[2]@Js[2],np.eye(3))@Pbasis).real,
              'neutron_collective_isovector_spin':(Nbasis.T@np.kron(4*Is[2]@Js[2],np.eye(3))@Nbasis).real}
    checks={
      'J_I_half_projectors_idempotent':np.linalg.norm(half@half-half)<1e-12,
      'S3_projectors_complete_orthogonal':np.linalg.norm(sym+anti+mixed-eye)<1e-12 and max(np.linalg.norm(a@b) for a,b in ((sym,anti),(sym,mixed),(anti,mixed)))<1e-12,
      'spin_isospin_half_in_all_configs':all(np.linalg.norm(np.kron(op,np.eye(3))@s-.75*s)<1e-12 for op in (J2,I2) for s in (pS,pM,nS,nM)),
      'two_config_bases_orthonormal':np.linalg.norm(Pbasis.T@Pbasis-np.eye(2))<1e-12 and np.linalg.norm(Nbasis.T@Nbasis-np.eye(2))<1e-12,
      'spin_flavor_space_exchange_symmetric':max(symmetry_errors)<1e-12,
      'spatial_representation_orthogonal':max(r['E_rep_orthogonal_error'] for r in representations)<1e-12,
      'same_spatial_rep_for_proton_neutron':max(r['neutron_rep_agreement'] for r in representations)<1e-12,
      'charges_one_zero_in_both_configs':np.linalg.norm(Qbig@Pbasis-Pbasis)<1e-12 and np.linalg.norm(Qbig@Nbasis)<1e-12,
      'vector_block_identity':np.linalg.norm(matrices['vector']-np.eye(2))<1e-12,
      'axial_block_five_thirds_one_third':np.linalg.norm(matrices['axial']-np.diag([5/3,1/3]))<1e-12,
      'proton_spin_blocks':np.linalg.norm(matrices['proton_up_spin']-np.diag([4/3,2/3]))<1e-12 and np.linalg.norm(matrices['proton_down_spin']-np.diag([-1/3,1/3]))<1e-12,
      'neutron_spin_blocks':np.linalg.norm(matrices['neutron_up_spin']-np.diag([-1/3,1/3]))<1e-12 and np.linalg.norm(matrices['neutron_down_spin']-np.diag([4/3,2/3]))<1e-12,
      'collective_static_magnetic_blocks':all(np.linalg.norm(matrices[name]-sgn*np.eye(2))<1e-12 for name,sgn in [('proton_isoscalar_spin',1),('neutron_isoscalar_spin',1),('proton_collective_isovector_spin',1),('neutron_collective_isovector_spin',-1)]),
    }
    color=parent.spin_flavor()
    checks['color_antisymmetric_singlet']=color['checks']['color_exchange_antisymmetric'] and color['checks']['color_singlet_total_generators_zero']
    def rows(s):
        return [{'spin_flavor':list(seq[index//3]),'space':['S','E1','E2'][index%3],'amplitude':float(s[index])} for index in np.flatnonzero(abs(s)>1e-12)]
    result={'dimensions':{'spin_flavor':64,'spatial_label':3,'color':27,'noncolor':192,'full_formal_product':5184},
      'spatial_scope':'abstract orthonormal L=0 even-parity S3 representation S plus E; compatible permutation labels, no radial shape or QCD binding solution',
      'spin_flavor_basis':['3u_up','3u_down','5d_up','5d_down'],'spatial_representations':representations,
      'state_basis':{name:rows(s) for name,s in [('proton_S',pS),('proton_M',pM),('neutron_S',nS),('neutron_M',nM)]},
      'current_blocks':{k:v.tolist() for k,v in matrices.items()},'maximum_exchange_error':float(max(symmetry_errors)),
      'checks':{k:bool(v) for k,v in checks.items()}}
    return result,matrices

def mix(q):return np.array([math.sqrt(1-q),math.sqrt(q)])
def expect(M,q):c=mix(q);return float(c@M@c)
def hamiltonian(delta,coupling,rprod,mass):
    raw=delta*np.array([[0.,-coupling*math.sqrt(rprod)],[-coupling*math.sqrt(rprod),1.]])
    eig,vec=np.linalg.eigh(raw);state=vec[:,0]
    if state[0]<0:state*=-1
    H=raw+(mass-eig[0])*np.eye(2)
    return {'raw_matrix_MeV':raw.tolist(),'matrix_with_mass_anchor_MeV':H.tolist(),'raw_ground_energy_MeV':float(eig[0]),'ground_mass_MeV':float(mass),'excited_mass_MeV':float(mass+eig[1]-eig[0]),'internal_gap_MeV':float(eig[1]-eig[0]),'ground_vector':state.tolist(),'mixed_weight_q':float(state[1]**2),'off_diagonal_magnitude_MeV':float(-raw[0,1])}

def angular(g):
    lam=-g;den=1+3*g*g
    return {'signed_lambda':lam,'a':(1-g*g)/den,'A':-2*lam*(lam+1)/den,'B':2*lam*(lam-1)/den}

def main():
    inp=json.loads((ROOT/'inputs.json').read_text(encoding='utf8'))
    masses=inp['masses'];mp=masses['proton'];mn=masses['neutron'];me=masses['electron']
    observed=inp['magnetic_moments_muN'];alpha=inp['inherited']['alpha'];kappa=inp['inherited']['kappa']
    # Same additive 45/75 mass response as particle trial 0.1. These are
    # effective Dirac response energies, not MS-bar current-quark masses.
    mu_mass=(2*mp-mn)/3;md_mass=(2*mn-mp)/3;A=(mp+mn)/6
    mu_u=2/3*mp/mu_mass;mu_d=-1/3*mp/md_mass
    sf,blocks=finite_states()
    p_mu=mu_u*blocks['proton_up_spin']+mu_d*blocks['proton_down_spin']
    n_mu=mu_u*blocks['neutron_up_spin']+mu_d*blocks['neutron_down_spin']
    diff=observed['proton']-observed['neutron'];summ=observed['proton']+observed['neutron']
    q=brentq(lambda q:expect(p_mu-n_mu,q)-diff,0.,.5,xtol=1e-15)
    c0=(summ-expect(p_mu+n_mu,q))/2
    g=expect(blocks['axial'],q);v=expect(blocks['vector'],q)
    q_closed=(5/3-diff/(mu_u-mu_d))/(4/3)
    rp=parent.euler_activity(3,alpha)*parent.euler_activity(5,alpha)
    coupling=math.sqrt(q*(1-q))/(1-2*q)/math.sqrt(rp)
    H_p=hamiltonian(A,coupling,rp,mp);H_n=hamiltonian(A,coupling,rp,mn)
    Q0=mn-mp-me;fc=parent.phase(Q0,me,True)
    phys=inp['weak_constants'];GF=phys['GF_GeV_minus2']*1e-6
    pref=GF**2*phys['Vud']**2*me**5/(2*math.pi**3*phys['hbar_MeV_s'])
    base_rate=pref*(v*v+3*g*g)*fc;rate=kappa*kappa*rp*base_rate
    # Axial observation enters only after the magnetic principal fit above.
    g_obs=abs(inp['axial_comparison']['signed_lambda']);q_axial=(5/3-g_obs)/(4/3)
    c1=(diff-g_obs*(mu_u-mu_d))/2
    joint_coupling=math.sqrt(q_axial*(1-q_axial))/(1-2*q_axial)/math.sqrt(rp)
    joint_Hp=hamiltonian(A,joint_coupling,rp,mp);joint_Hn=hamiltonian(A,joint_coupling,rp,mn)
    joint_q=joint_Hp['mixed_weight_q'];joint_g=expect(blocks['axial'],joint_q)
    p_joint=p_mu+c0*blocks['proton_isoscalar_spin']+c1*blocks['proton_collective_isovector_spin']
    n_joint=n_mu+c0*blocks['neutron_isoscalar_spin']+c1*blocks['neutron_collective_isovector_spin']
    joint_rate=kappa*kappa*rp*pref*(1+3*joint_g**2)*fc
    cases=[]
    for pu,pd in ((3,5),(3,7),(5,7),(3,11),(5,11)):
        activity=parent.euler_activity(pu,alpha)*parent.euler_activity(pd,alpha)
        H=hamiltonian(A,coupling,activity,mp);qc=H['mixed_weight_q'];gc=expect(blocks['axial'],qc)
        rc=kappa*kappa*activity*pref*(1+3*gc*gc)*fc
        cases.append({'up_prime':pu,'down_prime':pd,'proton_address':pu*pu*pd,'neutron_address':pu*pd*pd,'activity_product':activity,'q':qc,'axial':gc,'mean_life_s':1/rc,'mu_proton_muN':expect(p_mu,qc)+c0,'mu_neutron_muN':expect(n_mu,qc)+c0,'scope':'controlled labels with common response energies, weak constants, magnetic fit and parent kappa fixed; not identified particles'})
    scale_cases=[dict(delta_choice_MeV=d,**hamiltonian(d,coupling,rp,mp)) for d in (100.,A,1000.)]
    joint_cases=[]
    for pu,pd in ((3,5),(3,7),(5,7),(3,11),(5,11)):
        activity=parent.euler_activity(pu,alpha)*parent.euler_activity(pd,alpha)
        H=hamiltonian(A,joint_coupling,activity,mp);qc=H['mixed_weight_q'];gc=expect(blocks['axial'],qc)
        rc=kappa*kappa*activity*pref*(1+3*gc*gc)*fc
        joint_cases.append({'up_prime':pu,'down_prime':pd,'proton_address':pu*pu*pd,'neutron_address':pu*pd*pd,'activity_product':activity,'q':qc,'axial':gc,'mean_life_s':1/rc,'mu_proton_muN':expect(p_joint,qc),'mu_neutron_muN':expect(n_joint,qc),'scope':'controlled labels with joint C,c0,c1, response energies and parent kappa fixed; not identified particles'})
    family=[]
    for qc in (0.,q,q_axial,.5):
        gc=5/3-4*qc/3
        c1c=(diff-gc*(mu_u-mu_d))/2
        family.append({'q':qc,'axial':gc,'needed_isovector_c1_muN':c1c,'common_c0_muN':c0,'mu_proton_muN':expect(p_mu,qc)+c0+c1c,'mu_neutron_muN':expect(n_mu,qc)+c0-c1c})
    positive_target_cases=[{'axial_comparison_magnitude':g_obs+x,'q_if_axial_anchored':(5/3-g_obs-x)/(4/3)} for x in (-inp['axial_comparison']['uncertainty'],0.,inp['axial_comparison']['uncertainty'])]
    rho=np.outer(mix(q),mix(q));tr=parent.transport(rate,mn)
    tr['checks']={k:bool(value) for k,value in tr['checks'].items()}
    checks={**sf['checks'],
      'magnetic_numeric_inverse_equals_closed_form':abs(q-q_closed)<1e-12,
      'positive_density_normalized':np.linalg.eigvalsh(rho).min()>-1e-12 and abs(np.trace(rho)-1)<1e-12,
      'magnetic_moments_returned_by_common_fit':abs(expect(p_mu,q)+c0-observed['proton'])<1e-12 and abs(expect(n_mu,q)+c0-observed['neutron'])<1e-12,
      'direct_current_equals_state_axial_formula':abs(g-(5/3-4*q/3))<1e-12,
      'Hamiltonian_eigenstate_returns_magnetic_q':abs(H_p['mixed_weight_q']-q)<1e-12 and abs(H_n['mixed_weight_q']-q)<1e-12,
      'same_internal_state_for_isospin_pair':np.linalg.norm(np.array(H_p['ground_vector'])-np.array(H_n['ground_vector']))<1e-12,
      'mass_offsets_return_nucleon_anchors':all(np.max(abs(np.linalg.eigvalsh(H['matrix_with_mass_anchor_MeV'])[0]-mass))<1e-9 for H,mass in ((H_p,mp),(H_n,mn))),
      'vector_current_remains_one':abs(v-1)<1e-12,
      'scale_family_same_ground_state':max(abs(H['mixed_weight_q']-q) for H in scale_cases)<1e-12,
      'EM_isovector_family_shares_same_moments':all(abs(row['mu_proton_muN']-observed['proton'])<1e-12 and abs(row['mu_neutron_muN']-observed['neutron'])<1e-12 for row in family),
      'axial_observed_q_and_c1_reconcile_common_moments':abs(expect(p_mu,q_axial)+c0+c1-observed['proton'])<1e-12 and abs(expect(n_mu,q_axial)+c0-c1-observed['neutron'])<1e-12,
      'parent_phase_two_integrations_agree':abs(fc-parent.phase(Q0,me,True,'gauss'))/fc<2e-9,
      'state_rate_transfer_no_new_lifetime_refit':abs(rate/ (1/inp['inherited']['neutron_mean_life_s'])-(1+3*g*g)/(1+3*g_obs*g_obs))<1e-10,
      'joint_eigenstate_returns_calibrated_axial':abs(joint_q-q_axial)<1e-12 and abs(joint_g-g_obs)<1e-12,
      'joint_collective_currents_return_both_moments':abs(expect(p_joint,joint_q)-observed['proton'])<1e-12 and abs(expect(n_joint,joint_q)-observed['neutron'])<1e-12,
      'joint_inherited_lifetime_anchor_returned':abs(1/joint_rate-inp['inherited']['neutron_mean_life_s'])<1e-9,
      'both_current_models_same_charge_and_vector':np.linalg.norm(blocks['vector']-np.eye(2))<1e-12,
      **{('transport_'+k):val for k,val in tr['checks'].items()}}
    checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
    result={'title':'WRRA-M internal fold mixing and shared nucleon currents v0.3','date':'2026-10-02','author':'Wonsik Choi',
      'hypothesis':'same retained prime-composite address admits internal permutation-sector mixing; a finite Euler-family coupling enters a two-state binding ansatz whose eigenstate is read by distinct electromagnetic and weak currents',
      'inputs':inp,'input_sha256':hashlib.sha256((ROOT/'inputs.json').read_bytes()).hexdigest(),
      'finite_state_construction':sf,
      'effective_mass_current_choice':{'up_response_energy_MeV':mu_mass,'down_response_energy_MeV':md_mass,'A_MeV':A,'mu_up_Dirac_muN':mu_u,'mu_down_Dirac_muN':mu_d,'status':'declared additive mass-response and one-body Dirac-moment ansatz; not current-quark masses or complete nucleon binding energies'},
      'principal_magnetic_fit':{'input_roles':'mp,mn fix two response energies; observed mu_p-mu_n fixes q with c1=0; observed mu_p+mu_n fixes c0; observed lambda excluded from this state fit',
        'q_mixed_config':q,'theta_degrees':math.degrees(math.asin(math.sqrt(q))),'state_density_config':rho.tolist(),'isoscalar_shift_each_baryon_c0_muN':c0,'isovector_correction_choice_c1_muN':0.,
        'mu_proton_muN':expect(p_mu,q)+c0,'mu_neutron_muN':expect(n_mu,q)+c0,'vector':v,'axial_magnitude':g,'state_axial_dressing_relative_to_five_thirds':g/(5/3),'angular_coefficients':angular(g)},
      'binding_ansatz':{'formula':'H_B=(m_B-e_min)*I+Delta*[[0,-C*sqrt(r_up*r_down)],[-C*sqrt(r_up*r_down),1]]','Delta_reference_MeV':A,'dimensionless_C_from_magnetic_fit':coupling,'activity_product_3_5':rp,'proton':H_p,'neutron':H_n,'scale_cases':scale_cases,'status':'finite positive-gap constitutive Hamiltonian; mass offsets are inherited anchors; Delta=A is a stated scale choice, not an observed excitation or microscopic QCD determination'},
      'axial_comparison':{'calculated_magnitude':g,'observed_magnitude':g_obs,'absolute_difference':g-g_obs,'relative_difference':g/g_obs-1,'status':'principal c1=0 magnetic state does not reproduce the observed axial magnitude; no refit performed','q_if_axial_is_anchored':q_axial,'theta_if_axial_is_anchored_degrees':math.degrees(math.asin(math.sqrt(q_axial))),'required_c1_each_baryon_opposite_muN':c1,'equivalent_magnetic_isovector_gain':diff/(g_obs*(mu_u-mu_d)),'target_uncertainty_cases':positive_target_cases},
      'magnetic_identifiability_family':{'formula':'mu_p-mu_n=(mu_u-mu_d)*(5/3-4q/3)+2*c1; sum=mu_u+mu_d+2*c0','rows':family,'conclusion':'with an unconstrained isovector electromagnetic response c1, the two magnetic moments alone do not identify q or axial dressing; the principal inverse is conditional on c1=0'},
      'rate_transfer':{'Q_MeV':Q0,'phase_C':fc,'physical_kernel_mean_life_s':1/base_rate,'parent_kappa':kappa,'fixed_parent_kappa_mean_life_s':1/rate,'rate_relative_to_parent':rate/(1/inp['inherited']['neutron_mean_life_s']),'scope':'same parent 0.2 Coulomb/allowed-beta approximation and kappa; parent kappa already used observed lambda and neutron lifetime, so this is a transfer test, not an independent lifetime anchor'},
      'joint_calibrated_internal_state':{'q':joint_q,'theta_degrees':math.degrees(math.asin(math.sqrt(joint_q))),'dimensionless_C':joint_coupling,'c0_muN':c0,'c1_muN':c1,'proton_H':joint_Hp,'neutron_H':joint_Hn,'axial':joint_g,'mu_proton_muN':expect(p_joint,joint_q),'mu_neutron_muN':expect(n_joint,joint_q),'mean_life_with_inherited_kappa_s':1/joint_rate,'magnetic_operator_formula':'M=mu_u U+mu_d D+c0*(2J_z)+c1*(2I_z)*(2J_z)','proton_magnetic_block':p_joint.tolist(),'neutron_magnetic_block':n_joint.tolist(),'calibration_roles':'observed lambda fixes q and C; magnetic sum fixes c0, magnetic difference fixes c1; parent kappa retained without another lifetime fit','scope':'explicit calibrated internal-state realization; collective static magnetic response coefficients are not newly derived exchange/sea dynamics'},
      'joint_prime_family_cases':joint_cases,
      'prime_family_cases':cases,'transport':tr,
      'next_constraints':['derive isovector electromagnetic exchange/sea response c1 and weak dressing from a shared specified internal Hamiltonian','supply radial/spatial response and a physical excitation constraint before fixing absolute internal Delta','separate parent radiative/recoil normalization from arithmetic coupling before testing a second measured decay channel'],
      'verification':{'checks':checks,'passed':sum(checks.values()),'total':len(checks),'all_passed':all(checks.values()),'meaning':'mathematical and numerical implementation checks; not empirical agreement with every response'}}
    (ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'q':q,'theta_deg':result['principal_magnetic_fit']['theta_degrees'],'gA':g,'eta_state':g/(5/3),'C':coupling,'c0':c0,'required_c1_for_axial':c1,'rate_transfer':result['rate_transfer'],'checks':result['verification']},indent=2))

if __name__=='__main__':main()

