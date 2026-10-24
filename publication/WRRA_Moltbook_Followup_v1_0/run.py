"""Run modules in the order authorized by the research author."""
from pathlib import Path
import json
import cosmos,life,neuro,energy

P=Path(__file__).resolve().parent
if __name__=='__main__':
    for name,module in [('cosmos',cosmos),('life',life),('neuro',neuro),('energy',energy)]:
        result=module.run()
        (P/(name+'_results.json')).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        print(name,'calculated')
