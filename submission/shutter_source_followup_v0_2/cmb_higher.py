"""Exact finite shared-phase SOURCE moments through actual CAMB transfers.
New joint preparation: seven collinear harmonics with a uniformly rotated axis.
This is a conditional UNLENSED SOURCE NG calculation, not a Planck NG fit.
"""
import math,json,itertools
import numpy as np
from numpy.polynomial.legendre import leggauss,legvander
from scipy.special import roots_legendre
from common import IN,OUT,CFG,csvwrite,save,checks_pass

def wigner000(a,b,c):
    if (a+b+c)%2 or c>a+b or c<abs(a-b):return 0.
    g=(a+b+c)//2
    lf=lambda n:math.lgamma(n+1)
    logarithm=(lf(2*g-2*a)+lf(2*g-2*b)+lf(2*g-2*c)-lf(2*g+1))/2
    logarithm+=lf(g)-lf(g-a)-lf(g-b)-lf(g-c)
    return (-1.)**g*math.exp(logarithm)

def main():
    d=np.load(IN/'D_lens_a2.5.npz');r=np.load(IN/'R_lens_a2.5.npz')
    prior=np.load(IN/'SOURCE_lens_a2.5.npz')
    standard=np.load(IN/'standard_lens_a2.5.npz')
    address=json.loads((IN/'address_results.json').read_text())
    case=next(x for x in address['cases'] if x['branch']=='dark_weight_only')
    ell=d['ell'].astype(int);n=np.arange(1,8);J=128
    assert np.array_equal(ell,np.arange(2,6001)) and np.allclose(d['k'],.05*n,rtol=0,atol=1e-14)
    fields=['T','E','phi'];units=np.array([2.7255e6,2.7255e6,1.])
    coefficient=np.zeros((3,2,len(ell),7))
    for amplitude in case['amplitudes']:
        mode=amplitude['mode']-1;component=0 if amplitude['component']=='cosine' else 1
        for x,name in enumerate(fields):
            coefficient[x,component,:,mode]=units[x]*(amplitude['S_D']*d[name][:,mode]+amplitude['delta_R']*r[name][:,mode])

    def axial(register_dimension):
        theta=2*math.pi*np.arange(register_dimension)/register_dimension
        co=np.cos(n[:,None]*theta);si=np.sin(n[:,None]*theta)
        amplitudes=[]
        prefactor=np.sqrt(4*math.pi*(2*ell+1))
        for x in range(3):
            even=coefficient[x,0]@co+coefficient[x,1]@si
            odd=coefficient[x,0]@si-coefficient[x,1]@co
            parity=ell%2==0
            amplitudes.append(np.where(parity[:,None],
                ((-1.)**(ell//2))[:,None]*even,
                ((-1.)**((ell+1)//2))[:,None]*odd)*prefactor[:,None])
        return np.array(amplitudes)

    def gaussian_moment_body_coefficients(field,use):
        # 14 independent ternary variables have Gaussian moments through order 4.
        # Retaining a random common axis STILL gives nonzero sky connected 4-point.
        ls=ell[use];out=np.zeros((len(ls),14))
        pref=np.sqrt(4*math.pi*(2*ls+1))/math.sqrt(2)
        even=ls%2==0;se=(-1.)**(ls//2);so=(-1.)**((ls+1)//2)
        co=coefficient[field,0,use];si=coefficient[field,1,use]
        out[:,0::2]=pref[:,None]*np.where(even[:,None],se[:,None]*co,-so[:,None]*si)
        out[:,1::2]=pref[:,None]*np.where(even[:,None],se[:,None]*si,so[:,None]*co)
        return out

    A=axial(J)
    Cl=np.mean(A*A,axis=2)/(2*ell+1)[None,:]
    source_cl_T=prior['CMB_Dl'][ell,0]*2*math.pi/(ell*(ell+1))
    source_cl_E=prior['CMB_Dl'][ell,1]*2*math.pi/(ell*(ell+1))
    source_cl_phi=prior['phi_Dl'][ell]*2*math.pi/(ell.astype(float)*(ell+1))**2
    checks={}
    # Haar moments through fourth order have an exact finite weighted
    # orientation quadrature: degree <=4*lmax and azimuth |m|<=4*lmax.
    # Count this additional ensemble representation instead of a free infinite
    # orientation memory. It is not a microscopic preparation derivation.
    orientation_mu_nodes=2*int(ell.max())+1
    orientation_phi_nodes=4*int(ell.max())+1
    orientation_mu,orientation_weights=roots_legendre(orientation_mu_nodes)
    probabilities=orientation_weights/2
    orientation_entropy=float(-np.sum(probabilities*np.log(probabilities))+math.log(orientation_phi_nodes))
    orientation_count=orientation_mu_nodes*orientation_phi_nodes
    checks['finite_orientation_weights_positive']=bool(probabilities.min()>0)
    checks['finite_orientation_weights_normalized']=abs(probabilities.sum()-1)<1e-14
    checks['finite_orientation_second_moment']=abs(float(probabilities@orientation_mu**2)-1/3)<1e-11
    for x,reference in enumerate([source_cl_T,source_cl_E,source_cl_phi]):
        checks[f'actual_CAMB_{fields[x]}_power_reproduced']=np.max(abs(Cl[x]-reference))/max(reference.max(),1e-100)<1e-12
    te=np.mean(A[0]*A[1],axis=1)/(2*ell+1)
    reference_te=prior['CMB_Dl'][ell,3]*2*math.pi/(ell*(ell+1))
    checks['actual_TE_cross_power_reproduced']=np.max(abs(te-reference_te))/max(abs(reference_te).max(),1e-100)<1e-12
    deflection=math.sqrt(float(np.sum((2*ell+1)/(4*math.pi)*ell*(ell+1)*Cl[2])))
    deflection_arcsec=deflection*180/math.pi*3600
    checks['actual_SOURCE_lensing_RMS_reproduced']=abs(deflection_arcsec/0.009556588544185153-1)<1e-11
    # Covariance alone does not determine these connected higher moments.
    phase_control_errors={}
    for dim in CFG['cmb']['phase_dimensions_for_controls']:
        if dim==J:continue  # avoid reporting a self-comparison as a new control
        B=axial(dim)
        for order in [2,3,4]:
            reference=np.mean(A**order,axis=2);actual=np.mean(B**order,axis=2)
            error=float(np.max(abs(actual-reference))/max(abs(reference).max(),1e-100))
            phase_control_errors[f'J{dim}_order{order}']=error
            checks[f'phase_quadrature_J{dim}_order{order}']=error<1e-10
    # Independently check Wigner 000 normalization with angular quadrature.
    for triangle in [(2,2,2),(2,3,3),(10,10,20),(30,40,50)]:
        mu,w=leggauss(sum(triangle)//2+2);P=legvander(mu,max(triangle))
        integral=float(np.sum(w*np.prod(P[:,triangle],axis=1))/2)
        ref=wigner000(*triangle)**2
        checks['Gaunt_quadrature_'+'_'.join(map(str,triangle))]=abs(integral-ref)/ref<1e-10

    # Isotropic rotational B_l1l2l3=wigner(000)*<A_l1 A_l2 A_l3>.
    # Reduced b=B/h with h=sqrt(prod(2l+1)/(4pi))*wigner(000).
    selected=[x for x in CFG['cmb']['multipoles_selected'] if x<=CFG['cmb']['bispectrum_ell_max']]
    triangles=list(itertools.combinations_with_replacement(selected,3))
    field_triples=[(0,0,0),(1,1,1),(0,0,1),(0,1,1),(0,0,2),(0,1,2),(2,2,2)]
    bispectrum=[]
    for tri in triangles:
        w3j=wigner000(*tri)
        if w3j==0:continue
        norm=math.sqrt(np.prod([2*l+1 for l in tri])/(4*math.pi))
        for xyz in field_triples:
            moment=float(np.mean(A[xyz[0],tri[0]-2]*A[xyz[1],tri[1]-2]*A[xyz[2],tri[2]-2]))
            bispectrum.append(dict(fields='-'.join(fields[x] for x in xyz),ell1=tri[0],ell2=tri[1],ell3=tri[2],
                Wigner_000=w3j,body_third_moment=moment,rotational_B=w3j*moment,reduced_b=moment/norm,
                unit='*'.join('microK' if x<2 else 'dimensionless_phi' for x in xyz)))
    csvwrite('CMB_selected_reduced_bispectra.csv',bispectrum)
    # All equilateral multipoles up to 6000; odd parity vanishes.
    eq=[]
    for i,l in enumerate(ell):
        w3j=wigner000(int(l),int(l),int(l))
        norm=math.sqrt((2*l+1.)**3/(4*math.pi))
        for x in range(3):
            third=float(np.mean(A[x,i]**3))
            eq.append(dict(field=fields[x],ell=int(l),rotational_B=w3j*third,
                reduced_b=third/norm if w3j!=0 else 0.,parity_allowed=l%2==0))
    csvwrite('CMB_equilateral_bispectra_ell2_6000.csv',eq)

    # Rotationally invariant angular band-power covariance: exact finite phases.
    chosen=np.array(CFG['cmb']['multipoles_selected']);ix=chosen-2
    power=A[:,ix]**2/(2*chosen+1)[None,:,None]
    power_centered=power-power.mean(2,keepdims=True)
    power_rows=[];power_covs=[]
    for x in range(3):
        covariance=power_centered[x]@power_centered[x].T/J
        gaussian=np.diag(2*Cl[x,ix]**2/(2*chosen+1))
        connected=covariance-gaussian
        scale=max(np.diag(covariance).max(),1e-100)
        checks[f'power_covariance_PSD_{fields[x]}']=np.linalg.eigvalsh(covariance).min()/scale>-1e-11
        power_covs.append(covariance)
        for i,l in enumerate(chosen):
            for j,m in enumerate(chosen):
                power_rows.append(dict(field=fields[x],ell1=int(l),ell2=int(m),
                    exact_power_covariance=float(covariance[i,j]),
                    Gaussian_Wick_power_covariance=float(gaussian[i,j]),
                    connected_power_covariance=float(connected[i,j])))
    csvwrite('CMB_connected_angular_power_covariance.csv',power_rows)
    # Exact one-point sky statistics after averaging phase and common-axis angle.
    # Gauss N=2*Lmax+1 integrates fourth-degree bandlimited polynomials exactly.
    point_rows=[];point_cache={}
    ternary_nodes=np.array([0.,math.sqrt(3),-math.sqrt(3)])
    ternary_weights=np.array([2/3,1/6,1/6])
    for order,target in [(1,0),(2,1),(3,0),(4,3)]:
        checks[f'finite_Gaussian_moment_reference_order{order}']=abs(float(ternary_weights@ternary_nodes**order)-target)<1e-14
    for lmax in CFG['cmb']['point_moment_lmax']:
        use=ell<=lmax;ls=ell[use]
        mu,w=leggauss(2*lmax+1)
        P=legvander(mu,lmax)[:,ls]*np.sqrt((2*ls+1)/(4*math.pi))[None,:]
        for x in range(3):
            point=P@A[x,use]
            mean=float(np.sum(w[:,None]*point)/(2*J))
            centered=point-mean
            m2=float(np.sum(w[:,None]*centered**2)/(2*J))
            m3=float(np.sum(w[:,None]*centered**3)/(2*J))
            m4=float(np.sum(w[:,None]*centered**4)/(2*J));k4=m4-3*m2*m2
            expected=float(np.sum((2*ls+1)/(4*math.pi)*Cl[x,use]))
            checks[f'sky_variance_matches_Cl_{fields[x]}_L{lmax}']=abs(m2/expected-1)<1e-10
            if x<2:
                baseline=standard['unlensed_Dl'][ls,x]*2*math.pi/(ls*(ls+1))
            else:
                baseline=standard['pp_Dl'][ls]*2*math.pi/(ls.astype(float)*(ls+1))**2
            baseline_var=float(np.sum((2*ls+1)/(4*math.pi)*baseline))
            combined_var=m2+baseline_var
            body=gaussian_moment_body_coefficients(x,use)
            reference_power=np.sum(body**2,axis=1)/(2*ls+1)
            checks[f'common_axis_reference_Cl_{fields[x]}_L{lmax}']=np.max(abs(reference_power-Cl[x,use]))/max(Cl[x,use].max(),1e-100)<1e-12
            conditional_variance=np.sum((P@body)**2,axis=1)
            reference_var=float((w/2)@conditional_variance)
            reference_k4=3*float((w/2)@(conditional_variance-reference_var)**2)
            checks[f'common_axis_reference_variance_{fields[x]}_L{lmax}']=abs(reference_var/m2-1)<1e-10
            point_rows.append(dict(field=fields[x],lmax=lmax,SOURCE_RMS=math.sqrt(m2),
                SOURCE_third_moment=m3,SOURCE_connected_fourth_moment=k4,
                SOURCE_skewness=m3/m2**1.5,SOURCE_excess_kurtosis=k4/m2**2,
                common_axis_Gaussian_moment_reference_skewness=0.,
                common_axis_Gaussian_moment_reference_excess_kurtosis=reference_k4/reference_var**2,
                isotropic_angular_Gaussian_reference_skewness=0.,
                isotropic_angular_Gaussian_reference_excess_kurtosis=0.,
                Gaussian_baseline_RMS=math.sqrt(baseline_var),
                Gaussian_baseline_plus_SOURCE_skewness=m3/combined_var**1.5,
                Gaussian_baseline_plus_SOURCE_excess_kurtosis=k4/combined_var**2,
                unit='microK' if x<2 else 'dimensionless_phi',
                baseline_status='Independent Gaussian reference, not full lensed/foreground NG likelihood'))
            point_cache[(lmax,x)]=(mu,w,point)
    csvwrite('CMB_bandlimited_sky_cumulants.csv',point_rows)
    # Independent sky cubic integral versus the reduced-bispectrum contraction.
    lmax=8;mu,w=leggauss(2*lmax+1);ls=np.arange(2,lmax+1)
    sky=legvander(mu,lmax)[:,ls]*np.sqrt((2*ls+1)/(4*math.pi))[None,:]@A[0,ls-2]
    direct=float(np.sum(w[:,None]*sky**3)/(2*J));contraction=0.
    for tri in itertools.product(ls,repeat=3):
        w3j=wigner000(*map(int,tri))
        if w3j==0:continue
        third=float(np.mean(A[0,tri[0]-2]*A[0,tri[1]-2]*A[0,tri[2]-2]))
        contraction+=third*math.sqrt(np.prod([2*l+1 for l in tri])/(4*math.pi)**3)*w3j**2
    checks['bispectrum_reconstructs_sky_third_moment']=abs(direct-contraction)/max(abs(direct),1e-100)<1e-10

    # Full SOURCE initial-state cumulants including mixed D/R orders.
    profile=np.load(IN/'finite_preparation.npz')['dimensionless_fluctuation'][1:]
    profile=profile-profile.mean(1,keepdims=True)
    var=profile@profile.T/J;init=[]
    for order in [3,4]:
        for slots in itertools.product([0,1],repeat=order):
            moment=float(np.mean(np.prod(profile[list(slots)],axis=0)))
            connected=moment
            if order==4:
                a,b,c,d0=slots
                connected-=var[a,b]*var[c,d0]+var[a,c]*var[b,d0]+var[a,d0]*var[b,c]
            norm=math.prod(math.sqrt(var[i,i]) for i in slots)
            init.append(dict(fields=''.join('D' if i==0 else 'R' for i in slots),order=order,
                raw_moment=moment,connected_moment=connected,standardized_connected_moment=connected/norm))
    csvwrite('SOURCE_initial_connected_moments.csv',init)
    # Review correction: Gaussian-moment INITIAL harmonics with a common random
    # axis are not the same object as an isotropic Gaussian ANGULAR reference.
    # Mixing anisotropic Gaussian covariances produces kappa4=3 Var_mu[V(mu)].
    checks['common_axis_alone_has_nonzero_connected_fourth']=all(row['common_axis_Gaussian_moment_reference_excess_kurtosis']>0 for row in point_rows)
    checks['shared_phase_nonzero_bispectrum']=max(abs(row['reduced_b']) for row in bispectrum if row['fields']=='T-T-T')>0
    checks['angular_parity_selection']=all(abs(row['rotational_B'])==0 for row in eq if not row['parity_allowed'])
    coeff_profile=np.fft.rfft(profile,axis=1)/J
    resonance_rows=[]
    for a,b in itertools.combinations_with_replacement(range(1,8),2):
        if a+b<=7:
            product=coeff_profile[0,a]*coeff_profile[0,b]*coeff_profile[0,a+b].conjugate()
            resonance_rows.append(dict(n1=a,n2=b,n3=a+b,D_complex_resonant_product_real=float(product.real),
                D_complex_resonant_product_imag=float(product.imag)))
    csvwrite('SOURCE_three_harmonic_resonances.csv',resonance_rows)
    np.savez_compressed(OUT/'CMB_higher_moment_arrays.npz',ell=ell,Cl_T_E_phi=Cl,
        harmonic_coefficients=coefficient,selected_ell=chosen,selected_axial_amplitudes=A[:,ix],
        selected_power_covariance=np.array(power_covs))
    source_T_eq=[x for x in eq if x['field']=='T']
    peak=max(source_T_eq,key=lambda x:abs(x['reduced_b']))
    result=dict(validation_inputs=dict(actual_modes=7,ell_min=2,ell_max=6000,phase_states=128,
        transfer='Actual cached patched CAMB D/R T,E,phi at accuracy 2.5; no new background fit or Boltzmann rerun'),
        WRRA_transformation=CFG['cmb'],outputs=dict(initial_connected_moments=init,
            bandlimited_sky_cumulants=point_rows,equilateral_T_peak=peak,
            selected_rotational_bispectrum_rows=len(bispectrum),all_equilateral_rows=len(eq),
            connected_power_covariance_rows=len(power_rows),SOURCE_deflection_RMS_arcsec=deflection_arcsec,
            phase_quadrature_errors=phase_control_errors,
            counted_orientation_representation=dict(mu_nodes=orientation_mu_nodes,
                azimuth_nodes=orientation_phi_nodes,weighted_axis_states=orientation_count,
                axis_entropy_nats=orientation_entropy,
                joint_axis_and_128_phase_states=orientation_count*128,
                joint_preparation_entropy_nats=orientation_entropy+math.log(128),
                scope='Finite quadrature exact for moments up to fourth order at ell<=6000; additional ensemble representation, no free repeated preparation'),
            independent_bispectrum_sky_check=dict(direct_third_moment=direct,reconstructed=contraction),
            joint_preparation_dependence='Isotropic Gaussian ANGULAR reference has zero connected third/fourth. Gaussian-moment initial harmonics retaining the common axis still have nonzero sky connected fourth; the new finite comparator calculates this explicitly.',
            finite_Gaussian_moment_comparator=dict(independent_ternary_variables=14,nodes=ternary_nodes.tolist(),
                weights=ternary_weights.tolist(),initial_variable_states=3**14,
                initial_variable_entropy_nats=float(-14*np.sum(ternary_weights*np.log(ternary_weights))),
                status='Finite first-four-Gaussian-moment comparator, not a full Gaussian distribution; common orientation retained')),
        refutation_conditions=['Failure to reproduce actual SOURCE C_l and phi normalization','Finite-phase/angle quadrature nonconvergence','Measured custom-shape bispectrum or connected power covariance incompatible with frozen preparation','Confusion between initial-profile cumulants and projected sky cumulants'],
        conclusion='Actual seven-mode CMB projection of conditional non-Gaussian SOURCE moments executed, including rotational bispectra and connected angular power covariance. A custom NG map likelihood and nonlinear non-Gaussian lens remapping are not executed.',
        checks=checks_pass(checks))
    save('CMB_higher_results.json',result);print('CMB higher moments:',len(result['checks']),'checks passed',flush=True)
    return result

if __name__=='__main__':main()
