from pathlib import Path
import subprocess,sys,json,time
P=Path(__file__).resolve().parent;logs=P/'runs';logs.mkdir(exist_ok=True);rows=[]
if sys.flags.optimize:raise SystemExit('Run without -O: test assertions must remain enabled')
for script in ['original/code/compute.py','build.py','verify.py','test_contract.py','test_corruption.py','check_em.py']:
 start=time.time();p=subprocess.run([sys.executable,str(P/script)],capture_output=True,text=True)
 name=script.replace('/','_');(logs/(name+'.log')).write_text(p.stdout+p.stderr)
 rows.append({'command':[sys.executable,script],'exit':p.returncode,'seconds':time.time()-start});print(script,p.returncode,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
(logs/'REPRODUCTION.json').write_text(json.dumps(rows,indent=2))
