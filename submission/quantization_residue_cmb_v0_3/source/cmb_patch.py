from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).parent/'build/camb-2.0.4'
p=root/'fortran/DarkEnergyFluid.f90'
s=p.read_text()
declaration='''
    ! Conserved dust + spatially modulated vacuum, in geodesic synchronous gauge.
    ! Ordinary clxc is the dust contrast; these two variables are delta_R and v_D.
    type, extends(TDarkEnergyModel) :: TSourceVacuum
        real(dl) :: delta_R_initial = 0._dl
        real(dl) :: force_multiplier = 1._dl
        real(dl) :: start_factor = 1._dl
        logical :: discrete_modes = .false.
        real(dl), private :: grhoc0, grhov0
    contains
        procedure, nopass :: PythonClass => TSourceVacuum_PythonClass
        procedure, nopass :: SelfPointer => TSourceVacuum_SelfPointer
        procedure :: Init => TSourceVacuum_Init
        procedure :: BackgroundDensityAndPressure => TSourceVacuum_Background
        procedure :: PerturbationInitial => TSourceVacuum_Initial
        procedure :: PerturbedStressEnergy => TSourceVacuum_Stress
        procedure :: PerturbationEvolve => TSourceVacuum_Evolve
    end type TSourceVacuum
'''
s=s.replace('    contains\n\n    subroutine TDarkEnergyFluid_ReadParams',declaration+'\n    contains\n\n    subroutine TDarkEnergyFluid_ReadParams',1)
methods='''
    function TSourceVacuum_PythonClass() result(name)
    character(len=:), allocatable :: name
    name='SourceVacuum'
    end function

    subroutine TSourceVacuum_SelfPointer(cptr,P)
    use iso_c_binding
    type(c_ptr) :: cptr
    type(TSourceVacuum), pointer :: typed
    class(TPythonInterfacedClass), pointer :: P
    call c_f_pointer(cptr,typed)
    P=>typed
    end subroutine

    subroutine TSourceVacuum_Init(this,State)
    class(TSourceVacuum),intent(inout)::this
    class(TCAMBdata),intent(in),target::State
    this%is_cosmological_constant=.false.
    this%num_perturb_equations=2
    select type(State)
    class is(CAMBdata)
        this%grhoc0=State%grhoc
        this%grhov0=State%grhov
    end select
    end subroutine

    subroutine TSourceVacuum_Background(this,grhov,a,grhov_t,w)
    class(TSourceVacuum),intent(inout)::this
    real(dl),intent(in)::grhov,a
    real(dl),intent(out)::grhov_t
    real(dl),intent(out),optional::w
    grhov_t=grhov*a*a
    if(present(w)) w=-1._dl
    end subroutine

    subroutine TSourceVacuum_Initial(this,y,a,tau,k)
    class(TSourceVacuum),intent(in)::this
    real(dl),intent(out)::y(:)
    real(dl),intent(in)::a,tau,k
    y(1)=this%delta_R_initial
    ! Regular radiation-era solution v=-k*(rho_R/rho_D)*delta_R*tau/5.
    y(2)=-this%force_multiplier*k*this%grhov0/this%grhoc0*a**3*y(1)*tau/5
    end subroutine

    subroutine TSourceVacuum_Stress(this,dgrhoe,dgqe, &
        a,dgq,dgrho,grho,grhov_t,w,gpres_noDE,etak,adotoa,k,kf1,ay,ayprime,w_ix)
    class(TSourceVacuum),intent(inout)::this
    real(dl),intent(out)::dgrhoe,dgqe
    real(dl),intent(in)::a,dgq,dgrho,grho,grhov_t,w,gpres_noDE,etak,adotoa,k,kf1
    real(dl),intent(in)::ay(*)
    real(dl),intent(inout)::ayprime(*)
    integer,intent(in)::w_ix
    dgrhoe=grhov_t*ay(w_ix)
    ! The added momentum is dust momentum, not vacuum velocity.
    dgqe=this%grhoc0/a*ay(w_ix+1)
    end subroutine

    subroutine TSourceVacuum_Evolve(this,ayprime,w,w_ix,a,adotoa,k,z,y)
    class(TSourceVacuum),intent(in)::this
    real(dl),intent(inout)::ayprime(:)
    real(dl),intent(in)::a,adotoa,w,k,z,y(:)
    integer,intent(in)::w_ix
    ayprime(w_ix)=0._dl
    ayprime(w_ix+1)=-adotoa*y(w_ix+1) &
        -this%force_multiplier*k*this%grhov0/this%grhoc0*a**3*y(w_ix)
    end subroutine
'''
s=s.replace('    end module DarkEnergyFluid',methods+'\n    end module DarkEnergyFluid')
p.write_text(s)
p=root/'fortran/equations.f90';s=p.read_text()
s=s.replace('    module GaugeInterface\n','    module GaugeInterface\n    use DarkEnergyFluid, only: TSourceVacuum\n',1)
s=s.replace('    clxcdot = -k*z\n','''    clxcdot = -k*z
    select type(de=>State%CP%DarkEnergy)
    class is(TSourceVacuum)
        clxcdot=clxcdot-k*ay(EV%w_ix+1)
    end select
''',1)
# Diagnostics should also use the actual dust velocity.
s=s.replace('            EV%OutputTransfer(Transfer_Newt_vel_cdm) = -k*sigma/adotoa', '''            EV%OutputTransfer(Transfer_Newt_vel_cdm) = -k*sigma/adotoa
            select type(de=>State%CP%DarkEnergy)
            class is(TSourceVacuum)
                EV%OutputTransfer(Transfer_Newt_vel_cdm) = -k*(sigma+ay(EV%w_ix+1))/adotoa
            end select''')
p.write_text(s)
p=root/'camb/dark_energy.py';s=p.read_text();s+='''

@fortran_class
class SourceVacuum(DarkEnergyModel):
    """Experimental conserved dust/vacuum SOURCE response; see accompanying assumptions."""
    _fortran_class_module_ = "DarkEnergyFluid"
    _fortran_class_name_ = "TSourceVacuum"
    _fields_ = (("delta_R_initial", c_double), ("force_multiplier", c_double), ("start_factor", c_double), ("discrete_modes", c_bool))
''';p.write_text(s)
p=root/'fortran/cmbmain.f90';s=p.read_text()
s=s.replace('    use DarkEnergyInterface\n','    use DarkEnergyInterface\n    use DarkEnergyFluid, only: TSourceVacuum\n',1)
s=s.replace('        call Evolve_q%GetArray(.false.)', '''        select type(de=>CP%DarkEnergy)
        class is(TSourceVacuum)
            if(de%discrete_modes) then
                call Evolve_q%Init()
                call Evolve_q%Add(0.05_dl,3.2_dl,63)
            end if
        end select
        call Evolve_q%GetArray(.false.)''',1)
needle='    subroutine SetkValuesForInt(ThisCT)'
i=s.index(needle);j=s.index('    if (',i)
s=s[:j]+'''    select type(de=>CP%DarkEnergy)
    class is(TSourceVacuum)
        if(de%discrete_modes) then
            call ThisCT%q%Init()
            call ThisCT%q%Add(0.05_dl,3.2_dl,63)
            call Init_ClTransfer(ThisCT)
            return
        end if
    end select

'''+s[j:]
p.write_text(s)
s=s.replace('    WantLateTime = CP%DoLensing .or. State%num_redshiftwindows > 0 .or. CP%CustomSources%num_custom_sources > 0', '''    WantLateTime = CP%DoLensing .or. State%num_redshiftwindows > 0 .or. CP%CustomSources%num_custom_sources > 0
    select type(de=>CP%DarkEnergy)
    class is(TSourceVacuum)
        if(de%discrete_modes) WantLateTime=.true.
    end select''',1)
s=s.replace('    GetTauStart = taustart', '''    select type(de=>CP%DarkEnergy)
    class is(TSourceVacuum)
        taustart=taustart*de%start_factor
    end select
    GetTauStart = taustart''',1)
p.write_text(s)
# Additional native outputs for an independent audit, not symbolic CDM-comoving formulas.
p=root/'camb/model.py';s=p.read_text()
s=s.replace('    "lens_potential_source",\n]', '''    "lens_potential_source",
    "source_delta_R", "source_v_D", "source_z", "source_d_delta_D", "source_d_v_D", "source_d_eta",
]''',1);p.write_text(s)
p=root/'fortran/camb_python.f90';s=p.read_text()
s=s.replace('    subroutine GetOutputEvolutionFork(Data, EV, times, outputs, nsources, ncustomsources)\n', '''    subroutine GetOutputEvolutionFork(Data, EV, times, outputs, nsources, ncustomsources)
    use DarkEnergyFluid, only: TSourceVacuum
''',1)
s=s.replace('        if (ncustomsources > 0) then\n            outputs(Transfer_max + 9 + nsources:', '''        outputs(Transfer_max+9+nsources:Transfer_max+14+nsources,j,EV%q_ix)=0
        select type(de=>Data%CP%DarkEnergy)
        class is(TSourceVacuum)
            outputs(Transfer_max+9+nsources,j,EV%q_ix)=y(EV%w_ix)
            outputs(Transfer_max+10+nsources,j,EV%q_ix)=y(EV%w_ix+1)
            outputs(Transfer_max+11+nsources,j,EV%q_ix)=-yprime(ix_clxc)/EV%q-y(EV%w_ix+1)
            outputs(Transfer_max+12+nsources,j,EV%q_ix)=yprime(ix_clxc)
            outputs(Transfer_max+13+nsources,j,EV%q_ix)=yprime(EV%w_ix+1)
            outputs(Transfer_max+14+nsources,j,EV%q_ix)=yprime(ix_etak)/EV%q
        end select
        if (ncustomsources > 0) then
            outputs(Transfer_max + 15 + nsources:''',1)
s=s.replace('                Transfer_max + 9 + nsources + ncustomsources - 1, j, EV%q_ix)', '                Transfer_max + 15 + nsources + ncustomsources - 1, j, EV%q_ix)',1)
p.write_text(s)
print('SOURCE patch applied')
