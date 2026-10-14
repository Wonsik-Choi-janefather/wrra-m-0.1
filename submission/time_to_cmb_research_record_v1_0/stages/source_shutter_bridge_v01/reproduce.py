#!/usr/bin/env python3
"""Executed conditional SOURCE/index/profile -> metric -> shutter calibration.
Dependencies numpy. Existing archive data are bundled; no network access.
"""
from pathlib import Path
import csv,json,hashlib,math
import numpy as np
P=Path(__file__).resolve().parent

def csvfile(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

def main():
    cfg=json.loads((P/'frozen_inputs.json').read_text())
    c=cfg['c_m_s'];dt=cfg['dt_s'];d=c*dt
    shape=tuple(cfg['finite_index_shape']);NU=math.prod(shape)
    assert NU==cfg['N_U']
    addresses=np.arange(1,NU+1,dtype=np.int64);r=addresses-1
    i=r%shape[0];j=(r//shape[0])%shape[1];k=r//(shape[0]*shape[1])
    recovered=1+i+shape[0]*(j+shape[1]*k)
    assert np.array_equal(recovered,addresses)
    axes=[]
    for a,coord in enumerate((i,j,k)):
        nextcoord=(coord+1)%shape[a]
        # The periodic displacement is one positive graph edge, including seam.
        assert np.all((nextcoord-coord)%shape[a]==1)
        axes.append(dict(axis=a,index_extent=shape[a],edge_length_m=d,
                         edge_crossing_s=d/c,period_length_m=shape[a]*d,
                         axis_streaming_speed_m_s=d/dt))
    csvfile('address_metric_axes.csv',axes)
    samples=[]
    for a in (1,2,500,501,14500,14501,NU):
        q=a-1;xyz=(q%shape[0],(q//shape[0])%shape[1],q//(shape[0]*shape[1]))
        samples.append(dict(address=a,i=xyz[0],j=xyz[1],k=xyz[2],
                    X_m=xyz[0]*d,Y_m=xyz[1]*d,Z_m=xyz[2]*d))
    csvfile('address_mapping_samples.csv',samples)

    # This is the actual frozen arithmetic payload/profile from v0.29.1.
    file=P/'inputs/positive_profile_and_payload.npz'
    assert hashlib.sha256(file.read_bytes()).hexdigest()==cfg['profile_sha256']
    z=np.load(file);x=z['x'];N=len(x)
    assert np.allclose(np.diff(x),1/N,atol=1e-15,rtol=0)
    L=N*d;Lmacro=2*math.pi*cfg['Mpc_m']/cfg['old_mode_k_Mpc_inv']
    profiles=[];frozen_response=[]
    deltaA=2*math.cos(math.pi/8);eta=np.array(cfg['eta_J_m3'])
    for branch in ('weighted','unweighted'):
        W=z[branch+'_verified_W_s'];kernels=z[branch+'_positive_slot_kernels']
        payload=z[branch+'_sector_residue_slot_payload']
        I=z[branch+'_info_profile'];recon=W@kernels
        error=float(max(abs(I-recon)))
        assert error<1e-12 and np.min(I)>=0
        totals=payload.sum(axis=(1,2));sector=payload.sum(axis=1)@kernels
        stored_sector=z[branch+'_sector_profiles']
        sector_error=float(np.max(abs(sector-stored_sector)))
        # A tempting coarse mapping preserves totals but does NOT recover the
        # archived local sector allocation. Keep this failed comparison visible.
        assert np.max(abs(sector.sum(0)-I))<1e-12
        assert np.max(abs(stored_sector.sum(0)-I))<1e-12
        assert np.max(abs(stored_sector.mean(1)-totals))<1e-12
        baseline=I.mean();relative=I/baseline-1
        for name,length in [('shutter_calibrated_micro_profile',L),('old_k_fundamental_period_probe',Lmacro)]:
            density=I/length
            integral=density.sum()*length/N
            assert abs(integral-baseline)<1e-12
            newrelative=density/density.mean()-1
            assert np.max(abs(newrelative-relative))<1e-12
            profiles.append(dict(branch=branch,metric_choice=name,grid_points=N,
              period_length_m=length,cell_length_m=length/N,
              integral_information=float(integral),relative_information_RMS=float(np.sqrt(np.mean(relative**2))),
              original_profile_reconstruction_error=error,naive_local_sector_allocation_difference=sector_error,
              per_sector_max_local_difference=np.max(abs(sector-stored_sector),axis=1).tolist(),
              archived_sector_totals_preserved=True,naive_sector_mapping_reproduces_archive=bool(sector_error<1e-12),
              light_shutters_per_profile_cell=(length/N)/d,
              geometry_origin='Length renderer is declared/calibrated, not an independently derived SOURCE metric.'))
        # Actual v0.29.1 address-residue payload selects n mod 3 != 0.
        B=payload.sum(2);MC=B[:,np.arange(30)%3!=0].sum(1)
        response=eta*deltaA*MC;response[0]=0
        frozen_response.append(dict(branch=branch,controlled_payload=MC.tolist(),
          d_density_d_resource_probability_J_m3=response.tolist(),
          original_eps_delta_density_J_m3=(response*cfg['old_epsilon']).tolist()))
    csvfile('source_profile_length_audit.csv',profiles)

    # Family of graph metrics: same arithmetic data, different length readouts.
    # This demonstrates exactly what the light/shutter anchor fixes.
    choices=[]
    for factor in (.5,1,2):
        edge=d*factor
        choices.append(dict(edge_multiplier=factor,edge_m=edge,
          speed_on_fixed_shutter_m_s=edge/dt,
          compatible_time_s=edge/c,
          arithmetic_count=NU,arithmetic_payload_changed=False))
    csvfile('metric_identifiability.csv',choices)

    # A naive six-neighbour graph clock does not ensure 3D isotropic propagation.
    # This is a negative test of one proposed spatial extension, not of WRRA Core.
    diagonal_axis_walk_speed=c/math.sqrt(3)
    courant=c*dt/d
    checks=dict(all_addresses_bijective=True,all_periodic_edges_one_step=True,
      payload_hash_valid=True,stored_profile_reconstructed=True,
      stored_sector_totals_preserved=True,naive_slot_only_sector_profiles_reconstructed=False,information_integral_preserved=True,
      relative_variation_invariant=True,axis_light_shutter_match=True,
      old_spatial_scale_independently_identified=False,
      six_neighbour_constant_tick_3D_isotropy=False,
      naive_3D_central_wave_CFL_pass=bool(courant<=1/math.sqrt(3)))
    prior=json.loads((P/'inputs/prior_rerun_summary.json').read_text())
    result=dict(version='0.1',input=cfg,
      WRRA_transform='Inherited finite address factorization -> declared periodic index graph -> calibrated local edge metric c*dt; actual arithmetic payload -> frozen positive slot kernels -> X=Lx and I_L=I/L.',
      new_geometry_assumptions=['Fast-index 500x29x70 ordering promoted to a periodic graph. Original indices were not physical sites.',
        'One axis neighbour edge per shutter; equal calibrated edges dx=dy=dz=c*dt.',
        'Graph is a finite local renderer witness, not the size of the universe or one literal space cell per address established by the source.'],
      output=dict(light_step_m=d,light_step_pm=d*1e12,axes=axes,
        conditional_graph_volume_m3=NU*d**3,profile_grid_points=N,
        shutter_calibrated_profile_period_m=L,
        old_mode_fundamental_period_m=Lmacro,
        macro_to_micro_profile_length_ratio=Lmacro/L,
        old_mode_period_in_base_light_shutters=Lmacro/d,
        actual_profiles=profiles,actual_resource_responses=frozen_response),
      checks=checks,metric_family=choices,
      spatial_extension_negative_controls=dict(six_neighbour_equal_tick_diagonal_speed_m_s=diagonal_axis_walk_speed,
        diagonal_to_axis_speed_ratio=1/math.sqrt(3),
        three_dimensional_central_wave_courant=courant,maximum_stable_courant=1/math.sqrt(3),
        scope='Checks of explicitly proposed graph/finite-difference extensions only; neither was a claim of the prior 1D massless-shift implementation.'),
      prior_v0291_reexecution=prior,
      independent_source_metric_match_established=False,
      source_address_count_used_as_physical_universe_extent=False,
      unique_clock_from_NU_or_zeta_established=False,
      new_mode_CMB_implemented=False,
      refutation_conditions='Address duplication/loss, nonpositive or nonconserved information, wrong stored-profile reconstruction, edge/time mismatch, contradiction with an independently supplied address metric, or 3D anisotropy/instability when asserting isotropic propagation.',
      conclusion='Conditional calibrated SOURCE-to-shutter metric witness is executed. The total positive profile and aggregate resource responses are preserved. A naive slot-only local sector mapping fails to reproduce the archived allocation despite equal totals. Arithmetic count alone does not select a physical metric; local sector ownership, macro scale and 3D propagation remain open.')
    (P/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (P/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P))+'\n' for f in sorted(P.rglob('*')) if f.is_file() and f.name!='SHA256SUMS.txt'))
    print(json.dumps(dict(step_pm=d*1e12,profile_period_nm=L*1e9,profile_macro_ratio=Lmacro/L,
                         axes=axes,checks=checks),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
