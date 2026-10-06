from datetime import datetime
import httpx
from .base import TenderData,Item
URL='https://api.ted.europa.eu/v3/notices/search';FIELDS=['publication-number','notice-title','buyer-name','buyer-country','total-value','total-value-cur','publication-date','deadline','classification-cpv']
def first(v):
 if isinstance(v,dict): return first(v.get('eng') or next(iter(v.values()),''))
 if isinstance(v,list): return first(v[0]) if v else ''
 return str(v or '')
def dt(v):
 try:return datetime.fromisoformat(first(v)[:10])
 except:return None
async def fetch(limit=100):
 body={'query':'FT~"SSD" OR FT~"NVMe" OR FT~"DDR4" OR FT~"DDR5" OR FT~"memory card"','fields':FIELDS,'limit':limit,'scope':'ACTIVE','paginationMode':'PAGE','page':1}
 async with httpx.AsyncClient(timeout=45) as c:r=await c.post(URL,json=body);r.raise_for_status();data=r.json()
 out=[]
 for x in data.get('notices') or data.get('results') or []:
  n=first(x.get('publication-number'));cpvs=x.get('classification-cpv') or []
  try:value=float(first(x.get('total-value')).replace(',','.'))
  except:value=None
  items=[Item(first(x.get('notice-title')),cpv=first(c)) for c in (cpvs if isinstance(cpvs,list) else [cpvs])]
  out.append(TenderData('ted',n,first(x.get('buyer-country'))[:3] or 'EU',first(x.get('notice-title')),first(x.get('buyer-name')),'',value,first(x.get('total-value-cur')),dt(x.get('deadline')),dt(x.get('publication-date')),'active',f'https://ted.europa.eu/en/notice/-/detail/{n}',items))
 return out
