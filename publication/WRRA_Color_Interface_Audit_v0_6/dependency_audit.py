"""Verify external reads of the frozen color_check, not just its signature."""
from pathlib import Path
import ast,dis,types,itertools,math,json,hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'source/mcc_3_0/stage_3_particle_component_replay/run_stage3.py'

def global_reads(code):
    names={i.argval for i in dis.get_instructions(code) if i.opname in ('LOAD_GLOBAL','LOAD_NAME')}
    for child in code.co_consts:
        if isinstance(child,types.CodeType):names|=global_reads(child)
    return names

def run():
    expected=json.loads((ROOT/'SOURCE_SHA256.json').read_text())[str(SOURCE.relative_to(ROOT))]
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==expected
    fn=next(x for x in ast.parse(SOURCE.read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='color_check')
    module=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]))
    builtins={'range':range,'sum':sum,'complex':complex,'float':float,'max':max}
    namespace={'__builtins__':builtins,'np':np,'itertools':itertools,'math':math}
    exec(compile(module,str(SOURCE),'exec'),namespace)
    function=namespace['color_check'];reads=global_reads(function.__code__)
    allowed=set(builtins)|{'np','itertools','math'}
    result=function()
    checks={'frozen_source_identity':True,'all_external_names_allowlisted':reads<=allowed,
            'no_captured_state':not function.__code__.co_freevars,
            'isolated_namespace_reproduces_color_check':abs(result['norm']-1)<1e-12 and result['maximum_residual']<1e-12}
    output={'external_names':sorted(reads),'allowed_names':sorted(allowed),
      'scope':'Static recursive bytecode reads plus execution in a namespace containing only standard libraries and restricted builtins; ordinary unmodified library behavior is assumed. This is not a sandbox against malicious library replacement.',
      'checks':checks,'passed':sum(checks.values()),'total':len(checks),'color_output':result}
    (ROOT/'dependency_results.json').write_text(json.dumps(output,indent=2)+'\n')
    assert all(checks.values()),checks
    print(json.dumps(output,indent=2))

if __name__=='__main__':run()
