"""Finite WRRA record/reset witness. Run: python reproduce.py. No network."""
import json, math, itertools
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
checks={}
def check(name,condition):
    checks[name]=bool(condition)
    if not condition: raise AssertionError(name)
def entropy(p):
    p=np.asarray(p); p=p[p>0]; return float(-np.sum(p*np.log(p)))
def run():
    n=np.array([4.,6.,8.]); N=1015000; alpha=1.8996877935161325
    f=1+np.log(n)/(4*np.log(N)); w=n**(-alpha); w/=w.sum()
    t=np.array([f[1]-f[2],f[2]-f[0],f[0]-f[1]])
    delta=(t/w)*(.2/np.max(np.abs(t/w)))
    p=[]
    for sign in [1,-1]:
        z=.1+sign*delta; p.append(w[:,None]*np.array([.5+z,.5-z]).T)
    p=np.array(p); b=f[:,None]*np.array([0.,2.])[None,:]
    mean=(p*b).sum(axis=(1,2)); var=(p*b*b).sum(axis=(1,2))-mean**2
    response=1/(2-var); gap=float(abs(response[0]-response[1]))
    check('positive_preparations',np.all(p>0))
    check('normalization',np.max(abs(p.sum(axis=(1,2))-1))<1e-14)
    check('address_marginal',np.max(abs(p[0].sum(1)-p[1].sum(1)))<1e-14)
    check('carrier_marginal',np.max(abs(p[0].sum(0)-p[1].sum(0)))<1e-14)
    check('weighted_snapshot',np.max(abs((p[0]*f[:,None]).sum(0)-(p[1]*f[:,None]).sum(0)))<1e-14)
    check('equal_mean',abs(mean[0]-mean[1])<1e-14)
    check('stable_response',np.all(2-var>0))
    check('different_response',gap>1e-6)
    c=.2/np.max(np.abs(t/w))
    analytic_difference=-8*c*(f[0]-f[1])*(f[0]-f[2])*(f[1]-f[2])
    check('analytic_variance_difference',abs(var[0]-var[1]-analytic_difference)<1e-14)
    histories=list(itertools.product([0,1],repeat=4))
    labels=[sum(h)%2 for h in histories]
    enc=[(sum(h)%2,h[:3]) for h in histories]
    check('sixteen_histories',len(histories)==16)
    check('two_response_classes',len(set(labels))==2)
    check('eight_histories_per_class',labels.count(0)==labels.count(1)==8)
    check('reversible_factorization',len(set(enc))==16)
    check('decode_history',all(tuple(g)+(r^(sum(g)%2),)==h for h,(r,g) in zip(histories,enc)))
    check('xor_online_closure',all(((sum(h)%2)^a)==sum(h+(a,))%2 for h in histories for a in [0,1]))
    check('one_state_lower_bound',max(abs(response-response.mean()))>=gap/2-1e-14)
    # State (r,g,e): g and e have 8 values. Swap is a bijection on all 128 states.
    states=list(itertools.product(range(2),range(8),range(8)))
    swapped=[(r,e,g) for r,g,e in states]
    check('finite_swap_bijective',len(set(swapped))==128)
    check('finite_swap_involution',all((r,g,e)==(rr,ee,gg) for (r,g,e),(rr,gg,ee) in zip(states,swapped)))
    blank_inputs=[s for s in states if s[2]==0]
    blank_outputs=[(r,e,g) for r,g,e in blank_inputs]
    check('blank_environment_exact_reset',all(out[1]==0 and out[0]==inp[0] and out[2]==inp[1] for inp,out in zip(blank_inputs,blank_outputs)))
    check('blank_reset_retains_sixteen_distinctions',len(set(blank_outputs))==16)
    beta=1.; energy=np.arange(8,dtype=float); tau=np.exp(-beta*energy); tau/=tau.sum()
    uniform=np.ones(8)/8; Htau=entropy(tau); decrement=math.log(8)-Htau
    Q=float(np.dot(uniform-tau,energy)); D=float(np.sum(uniform*np.log(uniform/tau)))
    check('thermal_full_support',np.all(tau>0))
    check('imperfect_reset',0<tau[0]<1)
    check('finite_heat_equality',abs(beta*Q-decrement-D)<1e-13)
    check('positive_correction',D>0)
    sorted_joint=np.sort(np.outer(uniform,tau).ravel())[::-1]
    caps=np.array([sorted_joint[:8*k].sum() for k in range(1,9)])
    check('majorization_preimage_bound',np.max(abs(caps-np.cumsum(np.sort(tau)[::-1])))<1e-14)
    check('swap_attains_blank_probability_bound',abs(tau[0]-caps[0])<1e-14)
    check('residue_preserved_by_swap',all(a[0]==c[0] for a,c in zip(states,swapped)))
    check('thermal_support_obstruction',16*8>2*8)
    # Finite product ensemble before and after swap: joint entropy unchanged.
    before=np.einsum('r,g,e->rge',np.ones(2)/2,uniform,tau)
    after=before.transpose(0,2,1)
    check('total_entropy_preserved',abs(entropy(before.ravel())-entropy(after.ravel()))<1e-13)
    check('thermal_energy_ledger',abs(Q-(np.dot(after.sum((0,1)),energy)-np.dot(before.sum((0,1)),energy)))<1e-13)
    # Finite accumulation experiment: 3 tape cells, each holding one octal digit.
    # r, the occupancy pointer and the overflow flag are separate counted states.
    def accumulate(initial_digits, stream):
        tape=list(initial_digits)+[0]*(3-len(initial_digits)); q=len(initial_digits)
        rows=[{'stage':0,'occupied_cells':q,'tape':tape.copy(),'overflow':False,'incoming':0}]
        for stage,g in enumerate(stream,1):
            overflow=(q==3)
            if not overflow:tape[q]=g;q+=1
            rows.append({'stage':stage,'occupied_cells':q,'tape':tape.copy(),'overflow':overflow,'incoming':g if overflow else 0})
            if overflow:break  # STALL: keep the untransferred digit in its register.
        return rows
    empty_start=accumulate([], [1,6,3,5]); residual_start=accumulate([7],[1,6,3,5])
    check('overflow_stage_four',empty_start[-1]['stage']==4 and empty_start[-1]['overflow'])
    check('overflow_stage_three_with_initial_residue',residual_start[-1]['stage']==3 and residual_start[-1]['overflow'])
    check('stall_preserves_incoming',empty_start[-1]['incoming']==5 and empty_start[-1]['tape']==[1,6,3])
    full_inputs=list(itertools.product(range(8),repeat=4))
    from collections import Counter
    overwritten=Counter((b,c,d) for a,b,c,d in full_inputs)
    check('overwrite_eight_to_one',len(overwritten)==512 and set(overwritten.values())=={8})
    check('overflow_counting_obstruction',len(full_inputs)==4096 and 4096>512)
    for occupied in range(3):
        prefixes=list(itertools.product(range(8),repeat=occupied+1))
        final=[accumulate([],prefix)[-1] for prefix in prefixes]
        outputs={(x['occupied_cells'],tuple(x['tape']),x['overflow'],x['incoming']) for x in final}
        check('injective_accumulation_stage_'+str(occupied+1),len(outputs)==8**(occupied+1) and all(x['incoming']==0 and not x['overflow'] for x in final))
    result={'version':'0.2','inputs':{'N':N,'alpha':alpha,'history_bits':4,'baseline_stiffness':2,'beta':1,'query_tolerance':0},'mean_load':mean.tolist(),'variance':var.tolist(),'susceptibility':response.tolist(),'analytic_variance_difference':float(analytic_difference),'response_gap':gap,'one_state_minimax_error':gap/2,'history_states':16,'exact_response_states':2,'blank_environment_min_states':8,'thermal_reset':{'ground_probability':float(tau[0]),'bath_heat':Q,'memory_entropy_decrease_nats':decrement,'bath_relative_entropy_nats':D,'bath_entropy_nats':Htau},'checks':checks,'passed':sum(checks.values()),'total':len(checks)}
    result['accumulation']={'tape_states':512,'all_controlled_register_states_upper_bound':65536,'initially_empty':empty_start,'initial_residue':residual_start,'overwrite_preimage_multiplicity':8}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    fig,axes=plt.subplots(1,2,figsize=(9,3.3))
    L=np.arange(1,9); axes[0].plot(L,2.**L,'o-',label='Exact history'); axes[0].plot(L,np.ones(8)*2,'s-',label='Parity response')
    axes[0].set_yscale('log',base=2); axes[0].set_xlabel('Finite history length (bits)');axes[0].set_ylabel('Required distinguishable states');axes[0].legend()
    axes[1].bar(['Entropy decrease','Finite-bath correction','Heat / kT'],[decrement,D,Q],color=['#345e85','#ad764b','#547b69']);axes[1].tick_params(axis='x',labelsize=8); axes[1].set_ylabel('Dimensionless value (nats)')
    fig.tight_layout();fig.savefig(ROOT/'figure.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,3.4))
    stages=np.arange(5)
    ax.plot(stages,3*stages,'o--',color='#ad764b',label='Attempted cumulative load')
    ax.plot(stages,np.minimum(3*stages,9),'s-',color='#345e85',label='Admitted tape load (stall at stage 4)')
    ax.axhline(9,color='#555555',linestyle=':',label='Finite tape capacity: 9 bits')
    ax.annotate('Overflow: next transfer blocked',xy=(4,9),xytext=(1.2,11.4),arrowprops={'arrowstyle':'->','color':'#444444'},fontsize=9)
    ax.set_xticks(stages);ax.set_xlabel('Finite transfer stage');ax.set_ylabel('Distinguishability load (bits)')
    ax.set_ylim(-.5,13);ax.legend(loc='lower right',fontsize=8);fig.tight_layout()
    fig.savefig(ROOT/'accumulation.png',dpi=180);plt.close(fig)
    print(json.dumps(result,indent=2))
if __name__=='__main__': run()
