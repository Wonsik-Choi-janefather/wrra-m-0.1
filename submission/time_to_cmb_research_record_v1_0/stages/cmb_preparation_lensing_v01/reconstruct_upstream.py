"""Reconstruct address -> residue/supply -> physical background, without density swaps."""
from pathlib import Path
import runpy,json,csv,hashlib
import numpy as np
import camb
from camb import constants as c
from calculate_reference import params as reference_params
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
CFG=json.loads((ROOT/'inputs/source_frozen_inputs.json').read_text())
ETA=np.array(CFG['eta_J_m3']);EPS=CFG['inherited_supply_epsilon']
U100=3*(100000/c.Mpc)**2*c.c**2/(8*np.pi*c.G)
FAMILY={'unweighted':[0,0,0],'weighted':[0,.25,.1],'dark_weight_only':[0,.25,0]}

def savecsv(name,rows):
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    p=ROOT/'inputs/addresses.npz'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==CFG['input_sha256']['inputs/addresses.npz']
    archive=np.load(p);n=archive['addresses'][1:];w=archive['address_weights'][1:];e=archive['sector_effects'][1:].T
    assert len(archive['addresses'])==1015000 and archive['addresses'][0]==1
    logn=np.log(n)/np.log(n[-1]);base=e*w[None,:];derivative=base*logn[None,:]
    funcs=runpy.run_path(str(ROOT/'inputs/original_positive_readout.py'))
    _,K=funcs['modular_positive_kernel'](1024);prob=.5+EPS*(K-1)
    mask=np.arange(30)%3!=0;A8=1-np.cos(np.pi/8);gap=2*np.cos(np.pi/8)
    # Fixed thermal budget, identical to the original observable completion.
    pp=reference_params('unweighted','standard',2.5)
    pp.set_cosmology(H0=100,ombh2=.0224,omch2=.12,mnu=.06,nnu=3.044,tau=.0544,TCMB=2.7255,
        bbn_predictor='PRIMAT_Yp_DH_ErrorMC_2024.dat')
    thermal=camb.get_background(pp)
    thermal_wh2={name:float(thermal.get_Omega(name)) for name in ['photon','neutrino','nu']}
    cases=[];checks={};arrays={};residue_rows=[];group_rows=[];mode_rows=[]
    old=json.loads((ROOT/'inputs/closed_ledger.json').read_text())
    for label,lam in FAMILY.items():
        contrib=base+np.array(lam)[:,None]*derivative
        B,total,split=funcs['residue_payload'](contrib,n)
        direct=np.array([np.bincount(n%30,weights=q,minlength=30) for q in contrib])
        mu=B.sum((1,2));u0=ETA*mu
        controlled=B[:,mask].sum(2);M=controlled.sum(1);U=mu-M
        du=EPS*ETA[:,None]*gap*(controlled@K[mask]-M[:,None]);du[0]=0
        source_before=ETA*np.array([mu[0],U[1]+A8*M[1],U[2]+A8*M[2]])
        supplier_before=ETA[:,None]*gap*(controlled@prob[mask]);supplier_before[0]=0
        after=u0[:,None]+du
        balance=float(np.max(abs(source_before[:,None]+supplier_before-after)))
        pressure_balance=float(np.max(abs(-(source_before[2]+supplier_before[2])+after[2])))
        h2=float(u0.sum()/U100+sum(thermal_wh2.values()));H0=100*np.sqrt(h2)
        Fourier=np.fft.rfft(du,axis=1)/du.shape[1]
        amplitudes=[]
        for mode in range(1,8):
            for component,vector in [('cosine',2*Fourier[:,mode].real),('sine',-2*Fourier[:,mode].imag)]:
                row=dict(branch=label,mode=mode,component=component,k_Mpc_inv=.05*mode,
                    delta_u_D_at_a1_J_m3=float(vector[1]),delta_u_R_J_m3=float(vector[2]),
                    S_D=float(vector[1]/u0[1]),delta_R=float(vector[2]/u0[2]))
                amplitudes.append(row);mode_rows.append(row)
        case=dict(branch=label,lambda_P_D_R=lam,mean_load_P_D_R=mu.tolist(),u0_P_D_R_J_m3=u0.tolist(),
            controlled_load=M.tolist(),uncontrolled_load=U.tolist(),
            background=dict(H0=float(H0),ombh2=float(u0[0]/U100),omch2=float(u0[1]/U100)),
            frame_density_balance_J_m3=balance,frame_pressure_balance_J_m3=pressure_balance,
            mean_density_perturbation_J_m3=float(np.max(abs(du.mean(1)))),
            slot_split_error=float(split),address_vs_routed_residue_error=float(np.max(abs(direct-B.sum(2)))),
            source_probability_range=[float(prob.min()),float(prob.max())],amplitudes=amplitudes,
            density_swapped_after_readout=False,new_eta=False,new_supply_amplitude=False,
            preparation_status='Inherited addressed supply probability and conditional regular early extension',
            selection_status='Inherited branch' if label!='dark_weight_only' else 'New observationally informed candidate in the existing sector-specific weight family; not uniquely forced')
        cases.append(case);arrays[label+'_payload']=B;arrays[label+'_du_J_m3']=du
        arrays[label+'_source_before_J_m3']=source_before;arrays[label+'_supplier_before_J_m3']=supplier_before
        for s,name in enumerate(['P','D','R']):
            for r in range(30):
                residue_rows.append(dict(branch=label,sector=name,residue=r,controlled=bool(r%3!=0),
                    baseline_load=float(np.sum(base[s,n%30==r])),
                    log_weight_increment=float(lam[s]*np.sum(derivative[s,n%30==r])),
                    final_load=float(direct[s,r]),energy_J_m3=float(ETA[s]*direct[s,r])))
            group_rows.append(dict(branch=label,sector=name,uncontrolled_load=float(U[s]),controlled_load=float(M[s]),
                initial_source_mean_J_m3=float(source_before[s]),
                initial_supplier_mean_J_m3=float(supplier_before[s].mean()),final_total_mean_J_m3=float(u0[s])))
        checks[label+'_address_route']=case['address_vs_routed_residue_error']<1e-12
        checks[label+'_mean_direct_load']=bool(np.max(abs(mu-contrib.sum(1)))<1e-12)
        checks[label+'_frame_energy_pressure']=max(balance,pressure_balance)<2e-24
        checks[label+'_no_zero_mode_added']=case['mean_density_perturbation_J_m3']<1e-30
        checks[label+'_probability_positive']=bool(0<prob.min() and prob.max()<1)
        checks[label+'_slot_split']=split<1e-10
        checks[label+'_all_positive_density']=bool(np.min(after)>0)
        if label!='dark_weight_only':
            ref=next(x['observables'] for x in old['cases'] if x['id']==label+'_uniform_g_parity')
            checks[label+'_previous_energy_ledger']=bool(np.max(abs(u0/np.array(ref['u_P_D_R_today_J_m3'])-1))<1e-12)
    # Primitive frame permutation, inherited 8->72 supply exchange.
    indexes=np.arange(512);left=4*8+2;right=4*72+1
    indexes[left],indexes[right]=indexes[right],indexes[left]
    A=np.repeat(1-np.cos(2*np.pi*np.arange(128)/128),4)
    excitation=np.tile([0,0,1,1],128);energy=A+gap*excitation
    checks['frame_permutation_unitary']=bool(np.array_equal(indexes[indexes],np.arange(512)))
    checks['source_supply_Hamiltonian_commutes']=bool(np.max(abs(energy[indexes]-energy))<1e-14)
    checks['uniform_resource_mean_identity']=abs(A8+.5*gap-1)<1e-15
    # Hybrid candidate reproduces address-generated sector marginals; slots must be rerouted.
    arrays_h=arrays['dark_weight_only_payload'];weighted=arrays['weighted_payload'];unweighted=arrays['unweighted_payload']
    checks['candidate_dark_marginal_reproduces_weighted']=bool(np.max(abs(arrays_h[1].sum(1)-weighted[1].sum(1)))<1e-12)
    checks['candidate_vacuum_marginal_reproduces_unweighted']=bool(np.max(abs(arrays_h[2].sum(1)-unweighted[2].sum(1)))<1e-12)
    reroute_change=float(np.max(abs(arrays_h[1]-weighted[1])))
    # Attribute the dark correction to exact addresses, rather than a density knob.
    inc=.25*derivative[1];total_inc=float(inc.sum())
    ranking=np.argsort(inc)[-20:][::-1]
    top=[dict(address=int(n[i]),residue=int(n[i]%30),base_dark_load=float(base[1,i]),
        dark_load_increment=float(inc[i]),increment_fraction=float(inc[i]/total_inc)) for i in ranking]
    boundaries=[2,10,100,1000,10000,100000,1000000,1015001];bands=[]
    for a,b in zip(boundaries[:-1],boundaries[1:]):
        sel=(n>=a)&(n<b);v=float(inc[sel].sum())
        bands.append(dict(address_min=a,address_max=b-1,count=int(sel.sum()),
            dark_increment=v,fraction_of_increment=v/total_inc))
    correction=dict(base_mu_D=float(base[1].sum()),log_moment_D=float(derivative[1].sum()),
        lambda_D=.25,delta_mu_D=total_inc,delta_u_D_J_m3=float(ETA[1]*total_inc),
        relative_dark_energy_increment=total_inc/float(base[1].sum()),
        controlled_increment_fraction=float(inc[n%3!=0].sum()/total_inc),
        uncontrolled_increment_fraction=float(inc[n%3==0].sum()/total_inc),top_addresses=top,bands=bands,
        formula='mu_D(lambda_D)=sum e_D(n)w_n + lambda_D*sum e_D(n)w_n*ln(n)/ln(N_U)')
    checks={k:bool(v) for k,v in checks.items()}
    result=dict(version='address_to_CMB_bridge_0.1',date='2026-10-14',address_count=1015000,active_address_count=len(n),
        family_rule='e_s(n)*w_n*(1+lambda_s*ln(n)/ln(N_U)); original address 1 exclusion retained',
        thermal_wh2=thermal_wh2,U100_J_m3=U100,cases=cases,dark_correction=correction,
        changed_dark_slot_payload_when_R_weight_changes=reroute_change,checks=checks,all_checks_pass=all(checks.values()),
        candidate_rule_origin='Existing sector-specific weight family; lambda=(0,.25,0) selected following the observed ledger-exchange diagnosis',
        no_optimizer=True,no_readout_density_swap=True,
        still_open=['Physical interpretation and applicability of the calibrated weight choice','Upstream derivation of primordial preparation','SOURCE-specific lensing'])
    assert result['all_checks_pass'],[k for k,v in checks.items() if not v]
    (OUT/'address_results.json').write_text(json.dumps(result,indent=2))
    np.savez_compressed(OUT/'address_residue_supply_profiles.npz',**arrays)
    savecsv('sector_residue_trace.csv',residue_rows);savecsv('source_supply_mean_ledger.csv',group_rows)
    savecsv('generated_SOURCE_harmonics.csv',mode_rows);savecsv('dark_increment_by_address_band.csv',bands)
    savecsv('dark_increment_top_addresses.csv',top)
    print(json.dumps(dict(cases=[dict(branch=x['branch'],u0=x['u0_P_D_R_J_m3'],background=x['background']) for x in cases],
        dark_delta_mu=total_inc,reroute_change=reroute_change,checks_passed=sum(checks.values()))),flush=True)

if __name__=='__main__':main()
