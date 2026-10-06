from datetime import datetime
import httpx
from .base import TenderData,Item
BASE='https://public.api.openprocurement.org/api/2.5/tenders'
def dt(v):
 try:return datetime.fromisoformat(v.replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
async def fetch(limit=60):
 out=[]
 async with httpx.AsyncClient(timeout=30,follow_redirects=True) as c:
  r=await c.get(BASE,params={'limit':limit});r.raise_for_status()
  for row in r.json().get('data',[]):
   d=(await c.get(f"{BASE}/{row['id']}"));d.raise_for_status();x=d.json().get('data',{});v=x.get('value') or {};p=x.get('tenderPeriod') or {};e=x.get('procuringEntity') or {}
   items=[Item(i.get('description',''),i.get('quantity'),(i.get('unit') or {}).get('name'),(i.get('classification') or {}).get('id')) for i in x.get('items',[])]
   tid=x.get('tenderID',row['id']);out.append(TenderData('prozorro',tid,'UKR',x.get('title',''),e.get('name',''),x.get('description',''),v.get('amount'),v.get('currency'),dt(p.get('endDate','')),dt(x.get('dateCreated','')),x.get('status',''),f'https://prozorro.gov.ua/tender/{tid}',items))
 return out
