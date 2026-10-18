from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyBboxPatch
R=Path(__file__).resolve().parent
F=R/'figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'savefig.facecolor':'white'})
blue='#285e91'; orange='#db7b25'; teal='#17826e'; red='#b34846'; ink='#223347'
fig,axs=plt.subplots(1,2,figsize=(10.8,4.0))
for ax,b in zip(axs,[1,-1]):
 ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-1.8,5.5);ax.set_ylim(-1,3.3)
 for y in [0,1.2]:
  for x in range(4):ax.add_patch(Rectangle((x,y),.76,.76,facecolor=blue,alpha=.85))
 ax.add_patch(Rectangle((4,1.2 if b==1 else 0),.76,.76,facecolor=orange))
 ax.text(-.22,1.58,'Upper',ha='right',va='center',color=ink)
 ax.text(-.22,.38,'Lower',ha='right',va='center',color=ink)
 ax.text(2.35,2.65,'Upper extra: b = +1' if b==1 else 'Lower extra: b = -1',ha='center',weight='bold',color=ink)
 ax.text(2.35,-.55,'T(9,+1) = (5,4)' if b==1 else 'T(9,-1) = (4,5)',ha='center',color=ink)
fig.suptitle('Renderer selects the placement of remainder one',fontsize=17,weight='bold',color=ink,y=.98)
fig.text(.5,.025,'Nine units in either state. Same odd count; opposite ordered placement.',ha='center',fontsize=11,color=ink)
fig.subplots_adjust(left=.03,right=.98,top=.83,bottom=.13,wspace=.10)
fig.savefig(F/'remainder_placement.png',dpi=220);fig.savefig(F/'remainder_placement.svg');plt.close(fig)

fig,axs=plt.subplots(2,2,figsize=(10.8,6.1))
for ax,(b,c,label) in zip(axs.flat,[(1,-1,'Upper + Lower'),(-1,1,'Lower + Upper'),(1,1,'Upper + Upper'),(-1,-1,'Lower + Lower')]):
 u1,d1=(9+b)//2,(9-b)//2;u2,d2=(15+c)//2,(15-c)//2
 ax.barh([1,0],[u1,d1],color=blue,height=.32)
 ax.barh([1,0],[u2,d2],left=[u1,d1],color='#9db2c8',height=.32)
 ax.axvline(12,color=teal,linestyle='--',linewidth=1.3)
 for y,total in [(1,u1+u2),(0,d1+d2)]:ax.text(total+.22,y,str(total),va='center',fontsize=13,color=ink,weight='bold')
 ax.set_yticks([1,0],['Upper','Lower']);ax.set_xlim(0,15);ax.set_ylim(-.55,1.7)
 ax.set_xticks([0,4,8,12]);ax.tick_params(length=0);ax.grid(axis='x',alpha=.14)
 for sp in ax.spines.values():sp.set_visible(False)
 ax.set_title(label+'  |  residual = '+str(b+c),fontsize=12,weight='bold',color=teal if b+c==0 else red,pad=8)
 ax.text(.5,-.23,'Balanced closure candidate' if b+c==0 else 'Residual remains in this channel',transform=ax.transAxes,ha='center',color=teal if b+c==0 else red,fontsize=11)
fig.suptitle('Opposite placements balance; like placements retain a residual',fontsize=16,weight='bold',color=ink,y=.98)
fig.text(.5,.035,'Address 9 (dark) + address 15 (light): total = 24 in every case. Dashed line: 12 units.',ha='center',fontsize=10.5,color=ink)
fig.subplots_adjust(left=.09,right=.97,top=.83,bottom=.15,wspace=.29,hspace=.72)
fig.savefig(F/'conjugate_closure.png',dpi=220);fig.savefig(F/'conjugate_closure.svg');plt.close(fig)
print('Generated two exact arithmetic diagrams (PNG/SVG).')
