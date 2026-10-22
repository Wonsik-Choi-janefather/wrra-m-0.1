from pathlib import Path
import copy,json,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
base=dict(claim_id='synthetic_fixed_branch',version='test1',kind='fixed_prediction',mapping_confirmed=True,parameters_fitted_on_test=0,distribution='gaussian_known_covariance',observations=[0.,0.],predictions=[0.,0.],covariance=[[1.,0.],[0.,1.]],family_alpha=.001,family_tests=1,synthetic=True)
cases=[('nominal',{},0),('discrepancy',{'observations':[10.,10.]},1),('unconfirmed_mapping',{'mapping_confirmed':False,'observations':[10.,10.]},3),('test_refit',{'parameters_fitted_on_test':1},2),('bad_covariance',{'covariance':[[1.,2.],[2.,1.]]},2),('nan',{'observations':[float('nan'),0.]},2),('bad_distribution',{'distribution':'estimated_covariance'},2),('missing_version',{'version':''},2),('single_test',{'observations':[4.,0.],'family_alpha':.01},1),('family_100',{'observations':[4.,0.],'family_alpha':.01,'family_tests':100},0)]
results=[]
with tempfile.TemporaryDirectory() as td:
 for name,changes,expected in cases:
  d=copy.deepcopy(base);d.update(changes);path=Path(td)/(name+'.json');path.write_text(json.dumps(d));r=subprocess.run([sys.executable,str(P/'judge.py'),str(path)],capture_output=True,text=True);assert r.returncode==expected,(name,r.stdout);results.append(dict(case=name,expected_exit=expected,actual=json.loads(r.stdout)))
 a=dict(claim_id='comparison',version='test1',kind='paired_advantage',candidate_losses=[1.],reference_losses=[2.],scope='sample_aggregate',same_inputs=True,same_errors=False,same_split=True)
 path=Path(td)/'unmatched.json';path.write_text(json.dumps(a));r=subprocess.run([sys.executable,str(P/'judge.py'),str(path)],capture_output=True,text=True);assert r.returncode==2;results.append(dict(case='unmatched',expected_exit=2,actual=json.loads(r.stdout)))
(P/'test_results.json').write_text(json.dumps(dict(passed=len(results),total=len(results),cases=results),indent=2));print(json.dumps(dict(passed=len(results),total=len(results))))
