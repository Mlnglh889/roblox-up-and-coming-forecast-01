import json,os
I=os.getenv('MAKEFUN_INPUT_DIR','/input');O=os.getenv('MAKEFUN_OUTPUT_DIR','/output')
ms=[json.loads(x) for x in open(I+'/history.ndjson') if x.strip()]
# Rank-persistence with recency-weighted rank stability: recent chart positions
# receive the highest mass; stable games retain a slightly sharper distribution.
last=ms[-1]['up_and_coming']; hist={}
for m in ms:
 for r in m['up_and_coming']:
  hist.setdefault(r['universe_id'],[]).append(r['rank'])
def score(r):
 a=hist[r['universe_id']][-6:]
 return sum((i+1)*(-abs(x-r['rank'])) for i,x in enumerate(a))
chart=sorted(last,key=lambda r:r['rank'])
# Preserve a broad unnamed share because this chart churns and new games enter.
P=.62; probs=[]
for k in range(1,11):
 w=[]
 for r in chart:
  d=int(r['rank'])-k
  w.append(pow(2.71828,-abs(d)/(1.15 if d<=0 else 1.45))*(1+max(-.15,min(.15,score(r)/1000))))
 z=sum(w)
 for r,q in zip(chart,w):
  p=int(q/z*P*1000000)/1000000
  if p:probs.append({'universe_id':r['universe_id'],'place':k,'p':p})
top=[r['universe_id'] for r in chart[:10]]
os.makedirs(O,exist_ok=True)
json.dump({'probabilities':probs,'top10':top},open(O+'/'+json.loads(open(I+'/task.json').read())['output'],'w'),separators=(',',':'))
print('forecast',len(probs),top)
# revision: recency-weighted rank kernel with explicit newcomer mass
