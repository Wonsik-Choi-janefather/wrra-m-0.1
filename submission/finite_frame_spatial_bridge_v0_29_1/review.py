"""Independent review of the physical frame, numerical outputs and claim scope."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.special import logsumexp
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'frame_baseline'
ETA=np.array([7.5615824991e-10,7.2857613288e-10,7.6461028188e-10])

def main():
    checks={};details={}
    # Review current original files against their confirmed release manifest;
    # return only aggregate status, no unrelated content in the review package.
    manifest=json.loads((OLD/'manifest_sha256.json').read_text())
    matched=0
    for rel,sha in manifest.items():
        assert hashlib.sha256((OLD/rel).read_bytes()).hexdigest()==sha,'Release integrity mismatch'
        matched+=1
    checks['prior_release_integrity']=matched==len(manifest)
    parent=json.loads((ROOT/'inputs/physical_frame_ledger.json').read_text())
    z=np.load(ROOT/'inputs/finite_registers.npz');perm=z['permutation']
    A=1-np.cos(2*np.pi*np.arange(128)/128)
    Am=np.repeat(A,4);Bexc=np.tile([0.,0.,1.,1.],128)
    gap=A[72]-A[8];H=Am+gap*Bexc
    checks['gate_is_true_bijection']=np.array_equal(np.sort(perm),np.arange(512))
    checks['gate_is_unitary_involution']=np.array_equal(perm[perm],np.arange(512))
    checks['entire_source_supply_spectrum_preserved']=np.array_equal(H,H[perm])
    spectra=[]
    for x in parent['cases']:
        ident=x['id'];gamma0=z[ident+'_controlled_register_probabilities_before']
        gamma1=z[ident+'_controlled_register_probabilities_after']
        checks[ident+'_global_spectrum_entropy_preserved']=np.array_equal(np.sort(gamma0),np.sort(gamma1))
        checks[ident+'_energy_preserved_on_full_register']=abs(gamma0@H-gamma1@H)<1e-14
        checks[ident+'_physical_source_differs_from_logical_probe']=abs(gamma1@Am-gamma1@Am[perm])>.1
        # Exact finite-field partition invariance, not just a zero-field mean.
        probes=[np.array(v) for v in ([0.,0.,0.],[.1,-.3,.2],[-.2,.4,-.1])]
        errors=[]
        for f in (np.array([0.,1.05,0.]),np.array([.5,0.,.9])):
            alphabet=np.column_stack([np.ones(512)*f[0],Am*f[1],Am*f[2]])
            after_alphabet=alphabet[perm]
            for field in probes:
                s0=gamma0>0;s1=gamma1>0
                v0=logsumexp(np.log(gamma0[s0])-alphabet[s0]@field)
                v1=logsumexp(np.log(gamma1[s1])-after_alphabet[s1]@field)
                errors.append(abs(v0-v1))
        checks[ident+'_finite_field_partition_preserved']=max(errors)<1e-14
        o=x['observables']
        checks[ident+'_same_baryon_density_in_BBN']=abs(o['ombh2']-.0223958067929491)<1e-14
        if ident.endswith('uniform_g_parity'):
            dl=np.loadtxt(ROOT/'results'/f'{ident}_Dl.csv',delimiter=',',skiprows=1)
            cl=np.load(ROOT/'results'/f'{ident}_Cl.npz')
            ell=np.arange(len(dl));fac=ell*(ell+1)/(2*np.pi)
            checks[ident+'_raw_Cl_matches_Dl']=np.allclose(cl['tt'][2:]*fac[2:],dl[2:,1],rtol=1e-10,atol=1e-12)
            spectra.append({'id':ident,'H0':o['H0_derived_km_s_Mpc'],
                            'first_TT_peak':o['TT_first_three_peak_ell'][0],
                            'public_bin_RMS':o['planck_public_bin_diagnostic']['all']['RMS_in_public_bin_sigma']})
    mode=json.loads((ROOT/'results/single_mode_ledger.json').read_text())
    checks['one_mode_checks_completed']=all(mode['checks'].values())
    checks['no_official_likelihood_claim']=mode['official_Planck_minus2logL'] is None and all(x['observables']['official_minus2logL'] is None for x in parent['cases'])
    # Review fixes applied to the wording: Omega is imposed flatness, helium
    # mass fraction differs from nucleon fraction, and published spectra belong
    # to the previous standard completion, not the new interacting mode.
    details['reference_reproduction']=spectra
    b=parent['cases'][0]['observables']['BBN']
    details['BBN']={'mass_fraction':b['Y_He_mass_fraction'],'nucleon_fraction':b['Y_p_nucleon_fraction'],
                    'D_over_H':b['D_over_H'],'scope':'inherited PRIMAT table interpolation'}
    details['D_H_comparison_to_user_quoted_benchmark']={'benchmark':2.54e-5,'quoted_sigma':.04e-5,
        'observational_sigma_difference':abs(b['D_over_H']-2.54e-5)/.04e-5,
        'note':'conditional arithmetic against the quoted benchmark, not a new verified observational dataset or formal rejection'}
    claims=[
      {'claim':'finite frame source/supply energy and pressure closure','status':'supported under declared resource Hamiltonian and preparation'},
      {'claim':'logical P6 moments unchanged','status':'supported for full conjugated joint observables; false if interpreted as unchanged source-only A'},
      {'claim':'uniform preparation uniquely follows from arithmetic','status':'not established; fixed alternative g prior produces different backgrounds'},
      {'claim':'one conditional interacting scalar mode conserved','status':'supported with explicit spatial preparation, GR and transfer recipient choice'},
      {'claim':'physical 3D positions and primordial spectrum derived','status':'not established'},
      {'claim':'new interacting mode already produced the displayed CMB spectra','status':'false; recorded CMB is the prior standard completion'},
      {'claim':'official Planck fit, BAO likelihood and BBN matched','status':'not established by current diagnostics'},
      {'claim':'single quantum outcome or all UV divergences resolved','status':'not established'}]
    checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
    result={'reviewed_scope':'arithmetic inputs -> finite information/energy frame -> total fluid background -> recorded observables -> one conditional spatial mode',
            'previous_checks_reproduced_as_release_evidence':parent['checks_passed'],
            'current_release_files_verified':matched,'independent_review_checks':checks,
            'checks_passed':sum(checks.values()),'details':details,'claims':claims,
            'assessment':'conditional toy-model computational closure and known-value reproduction achieved; physical spatial preparation and interaction realization remain explicit open assumptions',
            'outgoing_email_sent':False}
    (ROOT/'results/review_ledger.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print('Independent review '+str(sum(checks.values()))+'/'+str(len(checks)))

if __name__=='__main__':main()
