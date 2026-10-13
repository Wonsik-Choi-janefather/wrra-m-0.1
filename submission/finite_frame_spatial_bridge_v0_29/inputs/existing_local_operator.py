"""Conditional volume-operator localization. No fitted sound speed or inferred spatial map."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
NU=1_015_000
def validate(v,v0,prob,u):
 v=np.asarray(v,float);v0=np.asarray(v0,float);prob=np.asarray(prob,float)
 if v.ndim!=1 or v0.shape!=v.shape or prob.shape!=(len(v),3):raise ValueError("Cell-array shape")
 if np.any(v<=0) or np.any(v0<=0) or not np.isfinite(u) or u<=0:raise ValueError("Positive units/volumes required")
 if not all(np.isfinite(x).all() for x in (v,v0,prob)):raise ValueError("Finite values required")
 if np.any(prob<0) or not np.allclose(prob.sum(axis=1),1,atol=1e-12,rtol=0):raise ValueError("Local branch populations must normalize")
 return v,v0,prob
def ledger(v,v0,prob,u):
 v,v0,prob=validate(v,v0,prob,u)
 fixed=prob[:,0]+prob[:,1];vac=prob[:,2]
 E=u*(v0*fixed+v*vac)
 rho=E/v;p=-u*vac
 # Volume-only response, fixed local reference volume and fixed populations.
 response=-u*v0*fixed/v**2
 # Adiabatic ca²=0 only when rho evolves; vacuum-only case is undefined.
 ca2=np.where(fixed>0,0,np.nan)
 return {"energy":E,"rho":rho,"pressure":p,"density_dv":response,"ca2_fixed_populations":ca2}
def linear_response(v,v0,prob,u,delta_v,delta_prob=None):
 v,v0,prob=validate(v,v0,prob,u)
 dv=np.asarray(delta_v,float)
 if dv.shape!=v.shape:raise ValueError("delta volume shape")
 dp=np.zeros_like(prob) if delta_prob is None else np.asarray(delta_prob,float)
 if dp.shape!=prob.shape or not np.allclose(dp.sum(axis=1),0,atol=1e-12,rtol=0):
  raise ValueError("Population perturbations must preserve local normalization")
 f=prob[:,0]+prob[:,1]
 dr=-u*v0*f/v**2*dv+u*v0/v*(dp[:,0]+dp[:,1])+u*dp[:,2]
 pressure=-u*dp[:,2]
 return dr,pressure
def audit_input(file,out):
 z=np.load(file,allow_pickle=False)
 v,v0,P=validate(z["cell_volumes"],z["reference_volumes"],z["branch_populations"],float(z["u_star"]))
 if len(v)!=NU:raise ValueError("Declared NU mismatch")
 metadata=json.loads(Path(str(file)+".json").read_text())
 for key in ("address_to_volume_rule","population_rule","source_sha256","spatial_embedding_rule"):
  if not metadata.get(key):raise ValueError("Missing executable provenance rule: "+key)
 if "delta_volume" not in z:raise ValueError("Arithmetic mapper must provide its actual delta_volume output")
 dv=z["delta_volume"]
 if abs(float(np.sum(dv)))>1e-10*max(1,float(np.sum(v))):
  raise ValueError("Local fluctuation must conserve declared total volume")
 before=ledger(v,v0,P,float(z["u_star"]))
 dr,dp=linear_response(v,v0,P,float(z["u_star"]),dv)
 report={"N_U":len(v),"total_volume":float(sum(v)),"u_star":float(z["u_star"]),
  "metadata":metadata,"input_sha256":hashlib.sha256(Path(file).read_bytes()).hexdigest(),
  "deltaV_independently_fitted":False,
  "density_mapping":"delta rho_i=-u_star*v0_i*(P1_i+P2_i)/v_i^2*delta v_i",
  "pressure_mapping_fixed_populations":"delta p_i=0",
  "camB_rest_frame_sound_speed_uniquely_derived_from_H_only":False,
  "ca2_zero_condition":"fixed populations and reference volumes, evolving nonzero resident sector",
  "transport_metric_and_gauge_closure_verified":False,
  "official_CMB_prediction_ready":False}
 out=Path(out);out.mkdir(exist_ok=True,parents=True)
 np.savez_compressed(out/"linear_response.npz",rho=before["rho"],pressure=before["pressure"],delta_rho=dr,delta_pressure=dp)
 (out/"bridge_audit.json").write_text(json.dumps(report,indent=2))
 return report

def demo(out):
 # A declared synthetic perturbation for implementation tests, NOT WRRA arithmetic output.
 # Keep global V fixed and use the existing500x29x70 finite index size.
 idx=np.arange(NU,dtype=np.int64)
 v=np.ones(NU);v0=np.ones(NU);P=np.tile([.05,.268,.682],(NU,1));u=1.
 dv=1e-4*np.cos(2*np.pi*(idx%500)/500);dv-=np.mean(dv)
 a=ledger(v,v0,P,u);b=ledger(v+dv,v0,P,u);dr,dp=linear_response(v,v0,P,u,dv)
 # Same homogeneous H with two gradient completions. Both extra energies vanish uniformly.
 # In normalized demo units Egrad=(g/2)*sum((delta v_(i+1)-delta v_i)^2).
 periodic=np.roll(dv,1)-dv
 grad=[float(g*.5*np.sum(periodic**2)) for g in (0.,1.)]
 report={"N_U":NU,"synthetic_mode_amplitude":1e-4,"not_an_arithmetic_volume_prediction":True,
  "max_volume_sum_drift":float(abs(np.sum(dv))),
  "max_linear_vs_exact_density_error":float(np.max(abs((b["rho"]-a["rho"])-dr))),
  "exact_pressure_unchanged":bool(np.array_equal(a["pressure"],b["pressure"])),
  "density_response_sign_for_positive_deltaV":float(dr[0]),
  "homogeneous_global_H_diagonal":(u*np.array([sum(v0),sum(v0),sum(v)])).tolist(),
  "zero_new_fit_parameters_in_this_test":True,
  "counterexample_uniform_energy_of_both_gradient_completions":0,
  "gradient_energy_for_same_nonuniform_mode_g0_g1":grad,
  "conclusion":"Global H fixes a conditional thermodynamic response, not a unique spatial generator or propagation law."}
 out=Path(out);out.mkdir(exist_ok=True,parents=True)
 (out/"demo_checks.json").write_text(json.dumps(report,indent=2))
 return report
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--input");p.add_argument("--demo",action="store_true")
 p.add_argument("--out",default=str(Path(__file__).resolve().parent/"results"))
 a=p.parse_args()
 if not a.input and not a.demo:p.error("Need actual address-volume input, or explicitly --demo")
 print(json.dumps(demo(a.out) if a.demo else audit_input(a.input,a.out),indent=2))
