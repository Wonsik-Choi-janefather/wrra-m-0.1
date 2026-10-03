"""SOURCE-conditioned finite state preparation and frozen same-state currents."""
from pathlib import Path
import importlib.util,sys,json,hashlib,copy
import numpy as np
ROOT=Path(__file__).resolve().parent
UP=ROOT.parent
P6=UP/'review_0_4_0_6_r1/studies/v0_6_r1/code'
P8=UP/'shutter_v0_8'

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
sys.path.insert(0,str(P6));v6=load('v6compute09',P6/'compute.py')
b8=load('bridge08',P8/'address_bridge.py')

def validate(c):
    for key in ['preparation_strength_scan','Q2_GeV2','source_controls']:
        if not isinstance(c[key],list) or not c[key]:raise ValueError('nonempty '+key+' required')
    for key in ['preparation_strength_scan','Q2_GeV2']:
        if len(c[key])!=len(set(c[key])):raise ValueError('duplicate '+key)
    names=[]
    for case in c['source_controls']:
        name=case['name']
        if not isinstance(name,str) or not name or name in names:raise ValueError('source case names')
        names.append(name)
        b8.parent.validate_controls(case['controls'],1000000)
    if 'baseline' not in names or next(x for x in c['source_controls'] if x['name']=='baseline')['controls']!={}:raise ValueError('uncontrolled named baseline required')
    if c['reference_preparation_strength'] not in c['preparation_strength_scan']:raise ValueError('reference strength missing from scan')
    for x in c['preparation_strength_scan']+[c['reference_preparation_strength']]:
        if isinstance(x,bool) or not isinstance(x,(int,float)) or not np.isfinite(x) or not 0<=x<=1:raise ValueError('preparation strength')
    if type(c['selector_prime']) is not int or not b8.parent.is_prime(c['selector_prime']):raise ValueError('selector must be prime')
    if type(c['excited_mode_index']) is not int or c['excited_mode_index']<1:raise ValueError('excited mode')
    for q in c['Q2_GeV2']:
        if isinstance(q,bool) or not isinstance(q,(int,float)) or not np.isfinite(q) or q<0:raise ValueError('Q2')
    if not c['Q2_GeV2']:raise ValueError('empty Q2 grid')


def residue_fraction(n,phi_vector,p):
    n=np.asarray(n);phi_vector=np.asarray(phi_vector)
    if n.ndim!=1 or not n.size or n.dtype.kind not in 'iu' or np.any(n<2) or np.any(n[1:]<=n[:-1]):raise ValueError('sorted distinct integer addresses >=2 required')
    if phi_vector.shape!=n.shape or not np.all(np.isfinite(phi_vector)):raise ValueError('finite aligned phi vector required')
    if not b8.parent.is_prime(p):raise ValueError('prime selector required')
    weight=np.abs(phi_vector)**2;total=float(weight.sum())
    if not np.isfinite(total) or not total>0:raise ValueError('zero phi has no conditional state')
    mask=b8.parent.valuations(n,p)%2==1
    return float(weight[mask].sum()/total)


def prepare(g,excited,selector_fraction,strength):
    if isinstance(selector_fraction,bool) or isinstance(strength,bool) or not isinstance(selector_fraction,(int,float)) or not isinstance(strength,(int,float)) or not np.isfinite(selector_fraction) or not 0<=selector_fraction<=1 or not np.isfinite(strength) or not 0<=strength<=1:raise ValueError('preparation inputs')
    g=np.asarray(g);excited=np.asarray(excited)
    if g.ndim!=1 or not g.size or excited.shape!=g.shape or not np.all(np.isfinite(g)) or not np.all(np.isfinite(excited)):raise ValueError('finite aligned internal modes required')
    if abs(np.vdot(g,g)-1)>2e-11 or abs(np.vdot(excited,excited)-1)>2e-11 or abs(np.vdot(g,excited))>2e-11:raise ValueError('normalized orthogonal modes required')
    a=strength*selector_fraction
    return (1-a)*np.outer(g,g.conj())+a*np.outer(excited,excited.conj()),a


def state_current_context(c,v):
    # Frozen geometry, counterterm and calibration; no call to currents.prepare for this vector.
    v=np.asarray(v)
    if v.shape!=c['g'].shape or not np.all(np.isfinite(v)) or abs(np.vdot(v,v)-1)>2e-11:raise ValueError('normalized finite internal vector required')
    # The inherited density/link implementation is defined on real frozen modes.
    # Reject unsupported complex states instead of silently omitting conjugation.
    if np.iscomplexobj(v) and np.any(v.imag!=0):raise ValueError('current adapter supports real frozen modes only')
    v=v.real
    out=copy.copy(c);n=c['nspace'];F=c['F'];Q=c['Q'];a=F@(Q@v).reshape(3,n).T
    b=F@(Q@(c['m']['bounded']@v)).reshape(3,n).T
    def density(slots):return np.column_stack([np.einsum('na,ab,nb->n',a,s,a) for s in slots])
    out['g']=v;out['norm_density']=np.sum(a*a,axis=1);out['link_density']=np.sum(a*b,axis=1)
    out['charge_density']={name:density(slots) for name,slots in c['charge_slots'].items()}
    out['mag_density']={name:density(slots) for name,slots in c['mag_slots'].items()}
    out['weak_density']=density(c['vslots']);out['axial_density']=density(c['aslots'])
    return out


def mixed_currents(ground,excited,weight,q):
    a=v6.currents.ground(ground,q);b=v6.currents.ground(excited,q)
    return {name:{key:(1-weight)*a[name][key]+weight*b[name][key] for key in a[name]} for name in ['proton','neutron','weak']}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def run():
    cfg=json.loads((ROOT/'inputs.json').read_text());validate(cfg)
    h=json.loads((P8/'handoff.json').read_text());inp=json.loads((P6/'inputs.json').read_text())
    m,p,e,V,g,c=v6.construct(inp);mode=cfg['excited_mode_index']
    if mode>=len(e):raise ValueError('mode outside frozen basis')
    excited=V[:,mode];ce=state_current_context(c,excited)
    H=p['delta_MeV']*(m['h0']-p['x']*m['bounded']);gap=float(p['delta_MeV']*(e[mode]-e[0]))
    rows=[];checks={}
    frozen=json.loads((P6/'results.json').read_text())
    charge_ops={(q,name):v6.currents.full_charge(c,q,name) for q in cfg['Q2_GeV2'] for name in ['proton','neutron']}
    for q in cfg['Q2_GeV2']:
        for name in ['proton','neutron']:
            op=charge_ops[q,name]
            checks[f'ground_charge_operator_{name}_{q}']=abs(g@op@g-v6.currents.ground(c,q)[name]['GE'])<2e-10
            checks[f'excited_charge_operator_{name}_{q}']=abs(excited@op@excited-v6.currents.ground(ce,q)[name]['GE'])<2e-10
    for case in cfg['source_controls']:
        n,vec,probs=b8.branches(h['N'],h['alpha'],h['beta'],case['controls'])
        f=residue_fraction(n,vec['phi'],cfg['selector_prime'])
        for strength in cfg['preparation_strength_scan']:
            rho,w=prepare(g,excited,f,strength)
            tag=case['name']+'_'+str(strength)
            checks[tag+'_positive']=np.linalg.eigvalsh(rho).min()>-2e-11
            checks[tag+'_trace']=abs(np.trace(rho)-1)<2e-11
            checks[tag+'_stationary_same_H']=np.linalg.norm(H@rho-rho@H)<2e-8
            excitation=float(np.trace(rho@H).real-p['delta_MeV']*e[0])
            checks[tag+'_energy']=abs(excitation-w*gap)<2e-8
            curves=[]
            for q in cfg['Q2_GeV2']:
                ff=mixed_currents(c,ce,w,q)
                checks[tag+f'_CVC_{q}']=abs(ff['weak']['GEV']-(ff['proton']['GE']-ff['neutron']['GE']))<2e-10
                for name in ['proton','neutron']:
                    op=charge_ops[q,name]
                    checks[tag+f'_trace_current_{name}_{q}']=abs(np.trace(rho@op).real-ff[name]['GE'])<2e-10
                if q==0:
                    checks[tag+'_charge_anchors']=abs(ff['proton']['GE']-1)<2e-10 and abs(ff['neutron']['GE'])<2e-10
                curves.append({'Q2_GeV2':q,**ff})
            rows.append({'case':case['name'],'strength':strength,'phi_fraction':probs['phi'],'D_fraction':probs['D'],
              'return_fraction':probs['initial_reflection']+probs['normal_return'], 'selector_fraction_in_phi':f,'excited_population':w,
              'conditional_excitation_MeV':excitation,'curves':curves})
    # Frozen calibration is reproduced only for zero-strength preparation; no refitting.
    z=v6.currents.ground(c,0)
    for name,key in [('proton','GM_muN'),('neutron','GM_muN'),('weak','GAV')]:
        checks[f'frozen_0_6_{name}_{key}']=abs(z[name][key]-frozen['zero_momentum'][name][key])<2e-10
    if not all(checks.values()):raise AssertionError([k for k,v in checks.items() if not v])
    out={'version':'upstream-0.9','construction_inputs':cfg,'internal_dimension':len(g),'excitation_gap_MeV':gap,
         'frozen_charge_width_fm':c['ell_fm'],'frozen_counterterm_radius_fm2':c['counterterm_radius_fm2'],
         'rows':rows,'checks':{k:bool(v) for k,v in checks.items()},'checks_passed':int(sum(checks.values())),
         'parent_sha256':{'upstream_0_8_handoff':sha(P8/'handoff.json'),'upstream_0_6_inputs':sha(P6/'inputs.json'),'upstream_0_6_results':sha(P6/'results.json')},
         'scope':'finite conditional nucleon preparation and current execution; not a derived species abundance or physical origin of preparation channel',
         'remaining':{'neutron_magnetic_radius_fm':frozen['unfitted_diagnostic']['neutron_magnetic_radius_fm'],'reference_fm':frozen['unfitted_diagnostic']['PDG_reference_fm'],
           'physical_time_unit':None,'source_energy_supply':None,'species_origin':None,'finite_Q2_external_validation':'inherited open mismatch/curvature ledger retained'}}
    (ROOT/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    handoff={'version':'upstream-0.9','preparation_map':'address dephasing; v_3(n) odd prepares mixture (1-lambda)|g><g|+lambda|e1><e1|; other addresses prepare |g><g|',
             'trace_contract':'conditional phi density has trace 1; unnormalized density has trace f_phi; D and R remain outside nucleon preparation',
             'energy_contract':'excitation above frozen ground computed from same H; energy supply and creation rest mass are not supplied by dimensionless phi norm',
             'physical_time_unit':None,'species_selection':'externally specified proton/neutron channel','next_stage':'0.10 integrate SOURCE-filter-record-preparation-current ledgers; preserve open interfaces',
             'results_sha256':sha(ROOT/'results.json')}
    (ROOT/'handoff.json').write_text(json.dumps(handoff,indent=2)+'\n')
    print('0.9 checks passed:',out['checks_passed']);reference=next(x for x in rows if x['case']=='baseline' and x['strength']==cfg['reference_preparation_strength']);print('reference:',json.dumps({k:reference[k] for k in ['selector_fraction_in_phi','excited_population','conditional_excitation_MeV']}))
if __name__=='__main__':run()
