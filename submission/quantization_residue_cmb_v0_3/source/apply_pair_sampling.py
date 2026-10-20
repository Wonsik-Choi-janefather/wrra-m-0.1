from pathlib import Path
import sys
p=Path(sys.argv[1])/"fortran/results.f90"
s=p.read_text()
needle="        if (Accuracy%lSampleBoost >= 50) then"
block='        ! WRRA paired-parity multipole sampling; retained transfer values are actual.\n        if (abs(Accuracy%lSampleBoost-49._dl)<1.e-6_dl) then\n            lind=0\n            do lvar=lmin,min(100,max_l)\n                lind=lind+1\n                ls(lind)=lvar\n            end do\n            step=max(2,mod(State%CP%min_l_logl_sampling,1000))\n            do lvar=101+2*(State%CP%min_l_logl_sampling/1000),max_l,step\n                lind=lind+1\n                ls(lind)=lvar\n                if(lvar+1<=max_l) then\n                    lind=lind+1\n                    ls(lind)=lvar+1\n                end if\n            end do\n            if(ls(lind)<max_l-1) then\n                lind=lind+1\n                ls(lind)=max_l-1\n            end if\n            if(ls(lind)<max_l) then\n                lind=lind+1\n                ls(lind)=max_l\n            end if\n            this%nl=lind\n            allocate(this%l(lind))\n            this%l=ls(1:lind)\n            return\n        end if\n\n'
assert needle in s and "WRRA paired-parity" not in s
p.write_text(s.replace(needle,block+needle,1))
