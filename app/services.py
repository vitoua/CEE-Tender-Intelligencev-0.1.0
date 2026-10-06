from datetime import datetime
from .models import Tender,TenderItem,Keyword,SourceRun
from .matching import match
async def sync_source(db,source):
 run=SourceRun(source=source);db.add(run);db.commit()
 try:
  if source=='prozorro':from .connectors.prozorro import fetch
  elif source=='ted':from .connectors.ted import fetch
  else:raise ValueError('Unknown source')
  rows=await fetch();extras=[(x.term,x.category,x.weight) for x in db.query(Keyword).filter_by(active=True)];count=0
  for n in rows:
   cat,score,hits=match(' '.join([n.title,n.description]+[i.description for i in n.items]),extras)
   if score<25:continue
   t=db.query(Tender).filter_by(source=n.source,external_id=n.external_id).first() or Tender(source=n.source,external_id=n.external_id)
   db.add(t)
   for k in ('country','title','buyer','description','value','currency','deadline','published_at','status','source_url'):setattr(t,k,getattr(n,k))
   t.category=cat;t.score=score;t.items.clear();db.flush()
   for i in n.items:t.items.append(TenderItem(description=i.description,quantity=i.quantity,unit=i.unit,cpv=i.cpv,matched_terms=', '.join(hits)))
   count+=1
  run.status='ok';run.imported=count;run.finished_at=datetime.utcnow();db.commit();return count
 except Exception as e:
  run.status='error';run.error=f'{type(e).__name__}: {e}';run.finished_at=datetime.utcnow();db.commit();raise
