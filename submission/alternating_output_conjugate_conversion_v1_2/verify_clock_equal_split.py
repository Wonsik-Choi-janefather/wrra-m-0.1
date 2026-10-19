from decimal import Decimal
import json

def admitted(n):
    return n >= 9 and n % 2 == 1 and any(n%d == 0 for d in range(2,int(n**.5)+1))
def split(r):
    return (r//2,r//2) if r%2 == 0 and admitted(r//2) else None
odd=[n for n in range(9,100,2) if admitted(n)]
for n in odd:
    assert split(2*n)==(n,n)
    for x in (-1,1):
        for y in (-1,1):
            u=(n+x)//2+(n+y)//2; d=(n-x)//2+(n-y)//2
            assert u+d==2*n and u-d==x+y
assert split(24) is None
assert split(54)==(27,27)
# Explicit sequential output reservation for one matter-first pair.
actual=[0,0]; pending=[0,0]
actual[0]+=1; pending[1]+=1
assert actual[0]+pending[0]==actual[1]+pending[1]
actual[1]+=1; pending[1]-=1
assert actual==[1,1] and pending==[0,0]
dt=Decimal('1.4813019664158633e-21')
f=1/dt
assert abs(f/Decimal('6.750818015e20')-1)<Decimal('1e-9')
print(json.dumps({'equal_split_cases':len(odd),'placement_cases':len(odd)*4,'unequal_24_rejected':True,'sequential_pending_ledger':'PASS','clock_seconds':str(dt),'clock_hz':str(f),'checks':'formal consistency only'},indent=2))
