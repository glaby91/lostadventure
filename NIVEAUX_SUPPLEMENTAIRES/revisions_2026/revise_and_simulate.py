from pathlib import Path
from collections import deque
from PIL import Image,ImageDraw,ImageFont
import csv
W,H,S=40,25,2
ROOT=Path(__file__).resolve().parent.parent;ORIG=ROOT/'tables';OUT=Path(__file__).resolve().parent;TABLES=OUT/'tables';IMAGES=OUT/'images'
TABLES.mkdir(parents=True,exist_ok=True);IMAGES.mkdir(parents=True,exist_ok=True)
COL={'bg':(0,0,0),'wall':(99,0,247),'food':(1,247,0),'door':(159,65,159),'heart':(247,239,0)}
GL={143:[255]*8,231:[0,60,126,255,255,126,60,0],207:[170,85,170,85,170,85,170,85],244:[0,0,24,60,126,255,255,0],245:[0,0,255,255,126,60,24,0],246:[128,224,248,254,248,224,128,0],247:[2,14,62,254,62,14,2,0],228:[108,254,254,254,124,56,16,0]}
TILE={1:(143,'wall'),2:(231,'food'),3:(207,'door'),4:(244,'wall'),5:(245,'wall'),6:(246,'wall'),7:(247,'wall'),8:(228,'heart')}
WALLS={1,4,5,6,7};START=(1,23)
FONT={'L':['#..','#..','#..','#..','###'],'O':['###','#.#','#.#','#.#','###'],'S':['###','#..','###','..#','###'],'T':['###','.#.','.#.','.#.','.#.'],'A':['.#.','#.#','###','#.#','#.#'],'D':['##.','#.#','#.#','#.#','##.'],'V':['#.#','#.#','#.#','#.#','.#.'],'E':['###','#..','##.','#..','###'],'N':['#.#','##.','#.#','#.#','#.#'],'R':['##.','#.#','##.','##.','#.#'],'U':['#.#','#.#','#.#','#.#','###'],'F':['###','#..','##.','#..','#..'],'W':['#.#','#.#','#.#','###','#.#'],'I':['###','.#.','.#.','.#.','###'],'J':['..#','..#','..#','#.#','###'],'Y':['#.#','#.#','.#.','.#.','.#.']}
WORDS={15:'RUN',20:'SOS',25:'FUN',30:'WIN',35:'JOY',40:'RUN',45:'SOS',50:'FUN'}
def bfs(v,start):
 d={start:0};prev={};q=deque([start])
 while q:
  x,y=q.popleft()
  for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   nx,ny=p
   if 0<=nx<W and 0<=ny<H and v[ny*W+nx] not in WALLS and p not in d:
    d[p]=d[(x,y)]+1;prev[p]=(x,y);q.append(p)
 return d,prev
def route(prev,start,end):
 p=end;r=[p]
 while p!=start:p=prev[p];r.append(p)
 return r[::-1]
def add_word(v,level,word):
 # The generator's 15x11 gallery coordinates.
 x0=2 if (level//2)%2==0 else W-2-15
 y0=2 if (level//4)%2==0 else H-2-11
 width=len(word)*4-1;rx=x0+2;ry=y0+3
 assert rx+width<=x0+14 and ry+5<=y0+10
 # Keep existing Miam, clear only old gallery walls for a small floor pocket.
 for y in range(ry,ry+5):
  for x in range(rx,rx+width):
   if v[y*W+x] not in (2,):v[y*W+x]=0
 for i,ch in enumerate(word):
  for yy,row in enumerate(FONT[ch]):
   for xx,c in enumerate(row):
    if c=='#':v[(ry+yy)*W+rx+i*4+xx]=2
 return word

def simulate(v):
 pos=START;lives=3;miams={(i%W,i//W) for i,a in enumerate(v) if a==2};hearts={(i%W,i//W) for i,a in enumerate(v) if a==8};moves=hits=0;completed=False
 if v[START[1]*W+START[0]] in WALLS:return {'completed':False,'reason':'départ bloqué','moves':0,'hits':0,'lives':lives}
 while miams or hearts:
  d,prev=bfs(v,pos);targets=hearts or miams
  reachable=[p for p in targets if p in d]
  if not reachable:return {'completed':False,'reason':'objet inaccessible','moves':moves,'hits':hits,'lives':lives}
  target=min(reachable,key=lambda p:(d[p],p[1],p[0]));path=route(prev,pos,target)
  for nxt in path[1:]:
   tile=v[nxt[1]*W+nxt[0]]
   if tile in WALLS:
    hits+=1;lives-=1
    if lives<=0:return {'completed':False,'reason':'vies épuisées','moves':moves,'hits':hits,'lives':lives}
    continue
   pos=nxt;moves+=1
   if pos in miams:miams.remove(pos);v[pos[1]*W+pos[0]]=0
   elif pos in hearts:hearts.remove(pos);v[pos[1]*W+pos[0]]=0;lives+=1
   if tile==3 and not miams:completed=True;break
  if completed:break
 if not completed:
  d,prev=bfs(v,pos);doors=[(i%W,i//W) for i,a in enumerate(v) if a==3]
  reachable=[p for p in doors if p in d]
  if not reachable:return {'completed':False,'reason':'sortie inaccessible','moves':moves,'hits':hits,'lives':lives}
  target=min(reachable,key=lambda p:d[p])
  for nxt in route(prev,pos,target)[1:]:
   if v[nxt[1]*W+nxt[0]] in WALLS:hits+=1;lives-=1
   else:pos=nxt;moves+=1
  completed=pos==target and not miams
 return {'completed':completed,'reason':'sortie atteinte' if completed else 'échec','moves':moves,'hits':hits,'lives':lives}

def render(v,path):
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
   if a in TILE:draw(x,y,*TILE[a])
 for x in range(W):draw(x,0,143,'wall');draw(x,H-1,143,'wall')
 for y in range(H):draw(0,y,143,'wall');draw(W-1,y,143,'wall')
 im.save(path,optimize=True)

rows=[]
for level in range(11,51):
 orig=ORIG/f'TABLE{level}.LAB';v=list(map(int,orig.read_text().split()))[:1000]
 if len(v)!=1000:raise ValueError(f'{level}: {len(v)} cells')
 word=WORDS.get(level)
 if word:add_word(v,level,word)
 # Difficulty policy: two hearts on the earlier maps, fewer in the middle, none in the ten hardest.
 hearts_n=2 if level<=20 or level in (22,26,30,34,38) else 0
 d,_=bfs(v,START)
 hpositions=[]
 cand=[p for p in d if v[p[1]*W+p[0]]==0 and d[p]>8]
 cand.sort(key=lambda p:(-d[p],p[1],p[0]))
 for p in cand:
  if len(hpositions)>=hearts_n:break
  if all(abs(p[0]-q[0])+abs(p[1]-q[1])>=12 for q in hpositions):hpositions.append(p);v[p[1]*W+p[0]]=8
 # Decorate selected existing walls using codes 4-7; they remain lethal wall variants.
 variant_count=0
 for y in range(1,H-1):
  for x in range(1,W-1):
   if v[y*W+x]==1 and (x*7+y*11+level)%29==0:
    v[y*W+x]=4+(x+y+level)%4;variant_count+=1
 # Make TABLE41-50 the ten hard maps: 25+ Miam, no hearts; all earlier counts rise as before.
 if level>=41:
  target=25+(level-41)
  d,_=bfs(v,START);current=v.count(2)
  cand=[p for p in d if v[p[1]*W+p[0]]==0 and d[p]>4]
  cand.sort(key=lambda p:(d[p],p[1],p[0]))
  # Favor distant branches, but spread the items instead of stacking at the end.
  rngseed=level*91
  import random;rng=random.Random(rngseed);rng.shuffle(cand)
  cand.sort(key=lambda p:(-(d[p]+rng.random()*8),p[1],p[0]))
  for x,y in cand[:max(0,target-current)]:v[y*W+x]=2
 # Simulate with real editor rules. Copy before simulation because collected items clear.
 pre=v.copy();result=simulate(v.copy())
 d0,_=bfs(pre,START)
 exitp=next(( (i%W,i//W) for i,a in enumerate(pre) if a==3),None)
 exitdist=d0.get(exitp,-1) if exitp else -1
 row={'niveau':level,'mot_miam':word or '', 'miams':pre.count(2),'coeurs':pre.count(8),'portes':pre.count(3),'murs_4_7':sum(a in (4,5,6,7) for a in pre),'distance_sortie':exitdist,'simulation_pas':result['moves'],'collisions':result['hits'],'vies_fin':result['lives'],'simulation':result['reason']}
 rows.append(row)
 (TABLES/f'TABLE{level}.LAB').write_text('\r\n'.join(map(str,pre))+'\r\n',encoding='ascii')
 render(pre,IMAGES/f'TABLE{level}.png')
# Rank difficulty from collectible count, simulated route length and current help hearts;
# remove hearts from the ten hardest, then rerun those exact level simulations.
def rank_score(r):return int(r['miams'])*10+int(r['simulation_pas'])-int(r['coeurs'])*70
for _ in range(3):
 hard_now=sorted(rows,key=rank_score,reverse=True)[:10]
 changed=False
 for r in hard_now:
  if int(r['coeurs'])==0:continue
  level=int(r['niveau']);p=TABLES/f'TABLE{level}.LAB';v=list(map(int,p.read_text().split()))[:1000]
  v=[0 if a==8 else a for a in v]
  result=simulate(v.copy());p.write_text('\\r\\n'.join(map(str,v))+'\\r\\n',encoding='ascii');render(v,IMAGES/f'TABLE{level}.png')
  r['coeurs']=0;r['simulation_pas']=result['moves'];r['collisions']=result['hits'];r['vies_fin']=result['lives'];r['simulation']=result['reason'];changed=True
 if not changed:break
# final ten hardest from the revised 40
hard=sorted(rows,key=rank_score,reverse=True)[:10]
# simulation report and 40-map contact sheet
with (OUT/'simulation_40.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter=';');w.writeheader();w.writerows(rows)
thumbw,thumbh=320,200;cw,ch=336,226
sheet=Image.new('RGB',(4*cw,10*ch),(16,18,28));dr=ImageDraw.Draw(sheet);font=ImageFont.load_default()
for i,level in enumerate(range(11,51)):
 x=(i%4)*cw+8;y=(i//4)*ch+8
 thumb=Image.open(IMAGES/f'TABLE{level}.png').convert('RGB').resize((thumbw,thumbh),Image.Resampling.NEAREST)
 sheet.paste(thumb,(x,y));r=rows[i];label=f"TABLE{level}  M{r['miams']} C{r['coeurs']} W{r['murs_4_7']}"
 dr.text((x,y+202),label,fill='white',font=font)
sheet.save(OUT/'apercu_40_tables_revisees.png',optimize=True)
# Rank the ten hardest by simulated route length, Miam count and lack of hearts.
hard=hard
with (OUT/'simulation_10_super_durs.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter=';');w.writeheader();w.writerows(hard)
print('SUMMARY')
for r in rows:print(r)
print('TEN_HARDEST',[(r['niveau'],r['miams'],r['coeurs'],r['simulation_pas'],r['collisions'],r['simulation']) for r in hard])
print('FILES',OUT)
