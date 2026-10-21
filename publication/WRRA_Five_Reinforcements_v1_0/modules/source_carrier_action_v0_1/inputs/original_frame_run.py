"""Finite energy-conserving frame candidate, under declared resource preparation.
No cosmological optimizer. Registers/initial resources are counted explicitly.
This closes one frame and the conditional total fluid budget, not quantum collapse.
"""
from pathlib import Path
import json,runpy
import numpy as np
ROOT=Path(__file__).resolve().parent
ETA=np.array([7.5615824991e-10,7.2857613288e-10,7.6461028188e-10])
NU=np.array([0.,0.,3.]);D=128;k0=8;k1=72
A=1-np.cos(2*np.pi*np.arange(D)/D);delta=A[k1]-A[k0]

def main():
    checks={};cases=[];arrays={}
    engine=runpy.run_path(str(ROOT/'observable_engine.py'))
    thermal=engine['thermal_budget']()
    previous=json.loads((ROOT/'inputs/previous_observable_ledger.json').read_text())
    p6=json.loads((ROOT/'inputs/p6_results.json').read_text())
    payload=np.load(ROOT/'inputs/positive_profile_and_payload.npz')
    # Mode(128) x supply bit(2) x NEW blank P7-style degenerate record(2).
    # Other two bits of g, original residue r and bath e remain spectators.
    def index(k,b,r):return 4*k+2*b+r
    permutation=np.arange(4*D);a=index(k0,1,0);b=index(k1,0,1)
    permutation[a],permutation[b]=permutation[b],permutation[a]
    U=np.eye(4*D)[permutation]
    Am=np.repeat(A,4);Bexc=np.tile([0.,0.,1.,1.],D)
    memory=np.tile([0.,1.,0.,1.],D)
    initial_modes=np.repeat(np.arange(D),4)
    checks['finite_unitary_permutation']=np.array_equal(permutation[permutation],np.arange(4*D))
    checks['mode_complement_identity']=abs(A[k0]+A[k1]-2)<1e-14
    checks['two_distinguishable_source_modes']=k1!=k0
    # Explicit resource preparation already present in P7's uniform g witness.
    uniform_g=np.ones(8)/8;g=np.arange(8)
    tau_g=np.exp(-g);tau_g/=tau_g.sum()
    priors={'uniform_g_parity':float(uniform_g[g%2==1].sum()),
            'P7_Gibbs_g_parity_control':float(tau_g[g%2==1].sum())}
    checks['uniform_g_parity_half']=priors['uniform_g_parity']==.5
    checks['thermal_control_not_recalibrated']=abs(priors['P7_Gibbs_g_parity_control']-1/(1+np.e))<1e-14
    # Finite full-unitary energy and pressure closure at three physical volumes.
    for s in (1,2):
        for V in (.125,1.,8.):
            coeff=ETA[s]*V**(NU[s]/3)
            H=coeff*(Am+delta*Bexc)
            pressure=-(NU[s]/3)*H/V
            checks[f's{s}_V{V}_energy_conserving_unitary']=np.max(abs(H[permutation]-H))<1e-23
            checks[f's{s}_V{V}_pressure_conserving_unitary']=np.max(abs(pressure[permutation]-pressure))<1e-23
    # Logical P6 observable is carried through U; it is not replaced by the
    # source-only physical readout. All finite partition moments are invariant.
    logical_after=Am[permutation]
    checks['logical_observable_conjugation']=np.max(abs(logical_after[permutation]-Am))<1e-14
    # Freeze frame command after one accepted pulse; never apply U twice as
    # a claimed irreversible reset (U^2=I). Reuse needs a new counted resource.
    source_after_mode_at_a=initial_modes[permutation[a]]
    checks['exchange_moves_excited_supply_to_record']=source_after_mode_at_a==k1 and Bexc[permutation[a]]==0 and memory[permutation[a]]==1
    for branch in ('weighted','unweighted'):
        B=payload[branch+'_sector_residue_slot_payload'].sum(2)
        mu=B.sum(1);uniform_mass=B[:,np.arange(30)%3==0].sum(1)
        controlled_mass=mu-uniform_mass
        L0=np.array([mu[0],uniform_mass[1]+A[k0]*controlled_mass[1],uniform_mass[2]+A[k0]*controlled_mass[2]])
        ref=next(x for x in p6['cases'] if x['branch']==branch)
        checks[branch+'_initial_means_reproduced']=np.max(abs(L0-ref['mean_P_D_R_load']))<1e-12
        needed=ETA*(mu-L0)
        # This is the NEW resource assumption: a finite supply bit carrying
        # half of the exact 8->72 gap, addressed only on the existing mod3
        # complement. Its mean fills the uniform-reference budget headroom.
        checks[branch+'_uniform_supply_equals_reference_headroom']=np.max(abs(needed[1:]-.5*delta*ETA[1:]*controlled_mass[1:]))<1e-23
        for prior,p in priors.items():
            gamma=np.zeros(4*D);gamma[index(k0,0,0)]=1-p;gamma[index(k0,1,0)]=p
            final=gamma[permutation]
            mode_probs=np.bincount(initial_modes,weights=final,minlength=D)
            source_response=float(final@Am)
            record_probability=float(final@memory)
            supply_before=float(gamma@Bexc);supply_after=float(final@Bexc)
            # Information retained in source+record: use the conjugate original
            # observable, with same dimensionless P6 prior, fields and bias.
            original_mean=float(gamma@Am);logical_mean=float(final@logical_after)
            orig_second=float(gamma@(Am**2));new_second=float(final@(logical_after**2))
            checks[branch+'_'+prior+'_logical_P6_moments_preserved']=abs(logical_mean-original_mean)<1e-14 and abs(orig_second-new_second)<1e-14
            checks[branch+'_'+prior+'_source_supply_energy_balance']=abs(source_response+delta*supply_after-A[k0]-delta*supply_before)<1e-14
            checks[branch+'_'+prior+'_supply_ends_ground']=supply_after==0
            checks[branch+'_'+prior+'_record_probability_from_existing_prior']=abs(record_probability-p)<1e-14
            checks[branch+'_'+prior+'_finite_probability_support']=np.min(final)>=0 and abs(final.sum()-1)<1e-14
            # Full reference mixture: uniform-address group has no exchange;
            # mod3 complement has the supplied bit and the resonant pair U.
            Lafter=np.array([mu[0],uniform_mass[1]+controlled_mass[1]*source_response,
                            uniform_mass[2]+controlled_mass[2]*source_response])
            reservoir0=np.array([0.,p*delta*controlled_mass[1],p*delta*controlled_mass[2]])
            Ltotal0=L0+reservoir0
            checks[branch+'_'+prior+'_total_load_is_invariant']=np.max(abs(Ltotal0-Lafter))<1e-12
            if prior=='uniform_g_parity':
                checks[branch+'_full_budget_equals_existing_uniform_reference']=np.max(abs(Ltotal0-mu))<1e-12
            for V in (.125,1.,8.):
                factor=ETA*V**(NU/3)
                src_before=factor*L0;sup_before=factor*reservoir0;src_after=factor*Lafter
                pbefore=-NU*(src_before+sup_before)/(3*V)
                pafter=-NU*src_after/(3*V)
                checks[branch+'_'+prior+f'_V{V}_whole_energy_pressure']=np.max(abs(src_before+sup_before-src_after))<1e-23 and np.max(abs(pbefore-pafter))<1e-23
            # The total background is frozen at both frame endpoints. Its D
            # part is dust and R part vacuum, using the inherited volume laws.
            aa=np.geomspace(1e-8,1,240)
            u=(ETA*Ltotal0)[None,:]*aa[:,None]**(NU-3)
            pfluid=-NU*u/3
            du_dloga=(NU-3)*u
            residual=du_dloga+3*(u+pfluid)
            checks[branch+'_'+prior+'_background_conservation']=np.max(abs(residual)/u)<1e-14
            caseid=branch+'_'+prior
            print('Computing total source+supplier '+caseid,flush=True)
            row,sub,dl=engine['calculate'](caseid,Ltotal0,thermal)
            checks.update(sub)
            row['state_preparation']='declared finite supply from '+prior+'; after one energy-conserving frame exchange, not I/128'
            row['readout_operator']='source A plus addressed finite supply Hamiltonian; same total energy before/after frame'
            if prior=='uniform_g_parity':
                old=next(x for x in previous['cases'] if x['id']==branch+'_uniform')
                checks[branch+'_whole_CMB_background_matches_reference']=abs(row['H0_derived_km_s_Mpc']-old['H0_derived_km_s_Mpc'])<1e-9
            cases.append({'id':caseid,'branch':branch,'supply_prior':prior,'supply_excited_probability':p,
                 'initial_source_loads':L0.tolist(),'initial_supply_loads':reservoir0.tolist(),
                 'initial_total_loads':Ltotal0.tolist(),'final_source_loads':Lafter.tolist(),
                 'final_supply_loads':[0.,0.,0.],
                 'initial_supply_energy_J_V0':(ETA*reservoir0).tolist(),
                 'original_P6_bias_j':(-np.array(ref['mean_P_D_R_load'])).tolist(),
                 'logical_P6_mean_error':abs(logical_mean-original_mean),
                 'record_excited_probability_on_controlled_addresses':record_probability,
                 'single_outcome_derived':False,'reusable_reset_cycle_closed':False,
                 'source_mode_populations_after':{'8':float(mode_probs[k0]),'72':float(mode_probs[k1])},
                 'source_is_uniform_density_matrix':False,'observables':row})
            arrays[caseid+'_controlled_register_probabilities_before']=gamma
            arrays[caseid+'_controlled_register_probabilities_after']=final
    checks={k:bool(v) for k,v in checks.items()}
    result={'version':'0.28','input':'existing arithmetic loads, eta, Kc/2, mod3 preparation, P7 g priors; original uniform-reference energy budget',
       'new_construction_assumptions':['P7 g parity is coupled to an addressed two-level supply Hamiltonian with gap exactly equal to the 8-to72 source energy difference',
                                      'only existing mod3-complement addresses use the exchange gate',
                                      'one new initially blank energy-degenerate logical record bit, distinct from the old 22keV phenotype record',
                                      'one accepted frame gate; after-event free evolution, no uncounted repeated fresh resources',
                                      'supply D/R parts inherit the same volume law as the corresponding source; not the old all-pressureless measurement supplier'],
       'finite_register_account':{'carrier_slots':128,'supply_g_states':8,'g_parity_energy_bit':2,
                                 'g_other_two_bits_retained':True,'new_blank_record_states':2,
                                 'existing_P7_residue_and_environment':'unchanged spectator registers; not relabeled as the new record'},
       'transformation':'exact energy-gap matching -> finite controlled unitary -> source/supply/record energy and information -> inherited total fluid background -> conditional CAMB/BAO/BBN',
       'closed':['one frame source+finite supply energy exchange','same-energy pressure at both endpoints','full logical P6 moments and bias under conjugated information observables','total-background conservation under the adopted standard fluid completion','conditional total-budget observables'],
       'still_open':['physical origin/selection of supply preparation','autonomous pulse triggering and reusable reset/control work cycle','single-outcome quantum selection','3D primordial perturbations and anisotropic stress from arithmetic states','official Planck likelihood and statistical rejection'],
       'negative_control':'fixed P7 Gibbs g parity input changes total resource budget and yields different spectra; uniform supply is not forced by unitary invariance alone',
       'new_fit':False,'new_eta':False,'curve_matching_optimizer_used':False,
       'cases':cases,'checks':checks,'checks_passed':sum(checks.values()),
       'refutation_conditions':['gate fails to commute with full source+supply Hamiltonian','reservoir counted twice or omitted before the frame','lost P6 moments in global information account','whole volume-energy derivative/continuity fails','fixed input resource state incompatible with observations under proper likelihood'],
       'scope':'conditional finite-frame resource closure, not complete cosmological microdynamics'}
    (ROOT/'results/closed_ledger.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    np.savez_compressed(ROOT/'results/finite_registers.npz',permutation=permutation,**arrays)
    assert all(checks.values()),{k:v for k,v in checks.items() if not v}
    print('Checks '+str(sum(checks.values()))+'/'+str(len(checks)),flush=True)
    for x in cases:
        o=x['observables'];print(x['id'],o['H0_derived_km_s_Mpc'],o['TT_first_three_peak_ell'],o['planck_public_bin_diagnostic']['all']['RMS_in_public_bin_sigma'],flush=True)

if __name__=='__main__':main()
