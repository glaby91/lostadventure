from pathlib import Path
from collections import deque
from PIL import Image
import random,csv
W,H=40,25; START=(1,23); DOOR=(2,23); OUT=Path(__file__).resolve().parent
DIRS=((-1,0),(1,0),(0,-1),(0,1)); WALL={1,4,5,6,7}
def neigh(p):
 x,y=p
 return [(x+dx,y+dy) for dx,dy in DIRS if 1<=x+dx<W-1 and 1<=y+dy<H-1]
def build(seed):
 rng=random.Random(seed); opened={START,DOOR}; frontier=[]; frontier_set=set()
 def add_fringe(p):
  for q in neigh(p):
   if q not in opened and q!=DOOR and q not in frontier_set and abs(q[0]-DOOR[0])+abs(q[1]-DOOR[1])!=1:
    frontier.append(q);frontier_set.add(q)
 add_fringe(START)
 while frontier:
  i=rng.randrange(len(frontier));p=frontier[i];frontier[i]=frontier[-1];frontier.pop();frontier_set.discard(p)
  if p in opened or abs(p[0]-DOOR[0])+abs(p[1]-DOOR[1])==1:continue
  if sum(q in opened for q in neigh(p))!=1:continue
  opened.add(p);add_fringe(p)
 return opened

def simulate(opened,food):
 pos=START;remain=set(food);moves=0
 while remain:
  d={pos:0};prev={pos:None};q=deque([pos])
  while q:
   p=q.popleft()
   for z in neigh(p):
    if z in opened and z not in d:d[z]=d[p]+1;prev[z]=p;q.append(z)
  target=min(remain,key=lambda p:(d.get(p,10**6),p[1],p[0]))
  path=[];p=target
  while p!=pos:path.append(p);p=prev[p]
  for p in reversed(path):
   pos=p;moves+=1;remain.discard(pos)
 d={pos:0};q=deque([pos])
 while q:
  p=q.popleft()
  for z in neigh(p):
   if z in opened and z not in d:d[z]=d[p]+1;q.append(z)
 return moves+d[DOOR],moves,d[DOOR]

best=None
for seed in range(1000):
 opened=build(seed)
 deg={p:sum(q in opened for q in neigh(p)) for p in opened}
 food={p for p,n in deg.items() if n==1 and p not in (START,DOOR)}
 total,collect,exitdist=simulate(opened,food)
 # Maximize the forced tree sweep first, then the greedy simulation distance.
 score=(len(opened),total,len(food))
 if best is None or score>best[0]:best=(score,seed,opened,food,deg,collect,exitdist)
score,seed,opened,food,deg,collect,exitdist=best
v=[1]*(W*H)
for x,y in opened:v[y*W+x]=0
for x,y in food:v[y*W+x]=2
v[DOOR[1]*W+DOOR[0]]=3
(OUT/'TABLE63.LAB').write_text('\r\n'.join(map(str,v))+'\r\n',encoding='ascii')
# Write the deterministic shortest-target simulation route used for the score.
pos=START;remain=set(food);route=[pos]
while remain:
 d={pos:0};prev={pos:None};q=deque([pos])
 while q:
  p=q.popleft()
  for z in neigh(p):
   if z in opened and z not in d:d[z]=d[p]+1;prev[z]=p;q.append(z)
 target=min(remain,key=lambda p:(d.get(p,10**6),p[1],p[0]));path=[];p=target
 while p!=pos:path.append(p);p=prev[p]
 for p in reversed(path):pos=p;route.append(pos);remain.discard(pos)
d={pos:0};prev={pos:None};q=deque([pos])
while q:
 p=q.popleft()
 for z in neigh(p):
  if z in opened and z not in d:d[z]=d[p]+1;prev[z]=p;q.append(z)
p=DOOR;path=[]
while p!=pos:path.append(p);p=prev[p]
for p in reversed(path):route.append(p)
assert len(route)-1==score[1] and route[-1]==DOOR
with (OUT/'parcours_force.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['pas','x','y','case'])
 for i,(x,y) in enumerate(route):w.writerow([i,x+1,y+1,'Miam' if (x,y) in food else 'sortie' if (x,y)==DOOR else 'passage'])
# CPC render
S=2; GL={143:[255]*8,231:[0,60,126,255,255,126,60,0],207:[170,85,170,85,170,85,170,85]};COL={'bg':(0,0,0),'wall':(99,0,247),'food':(1,247,0),'door':(159,65,159)}
im=Image.new('RGB',(W*8*S,H*8*S),COL['bg']);px=im.load()
def draw(x,y,gid,color):
 for gy,row in enumerate(GL[gid]):
  for gx in range(8):
   if row&(128>>gx):
    for dy in range(S):
     for dx in range(S):px[x*8*S+gx*S+dx,y*8*S+gy*S+dy]=COL[color]
for y in range(H):
 for x in range(W):
  a=v[y*W+x]
  if a==1:draw(x,y,143,'wall')
  elif a==2:draw(x,y,231,'food')
  elif a==3:draw(x,y,207,'door')
im.save(OUT/'TABLE63_preview.png',optimize=True)
with (OUT/'simulation.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['niveau','cases_accessibles','miams','coeurs','sortie','deplacements_simules','collisions','resultat','seed'])
 w.writerow(['TABLE63',len(opened),len(food),0,f'{DOOR[0]+1},{DOOR[1]+1}',score[1],0,'sortie atteinte',seed])
print(f'seed={seed} open={len(opened)} miams={len(food)} leaves={len(food)} moves={score[1]} collect={collect} exit={exitdist} door={DOOR} route={len(route)-1} lower_bound={2*(len(opened)-1)-1}')
