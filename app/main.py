from io import BytesIO
from fastapi import FastAPI,Depends,Form,HTTPException,Request
from fastapi.responses import HTMLResponse,RedirectResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openpyxl import Workbook
from .db import Base,engine,get_db,SessionLocal
from .models import User,Tender,Keyword,SourceRun
from .auth import hash_password,verify_password
from .config import settings
from .i18n import tr
from .services import sync_source
app=FastAPI(title='CEE Tender Intelligence',version='0.1.0');app.mount('/static',StaticFiles(directory='app/static'),name='static');templates=Jinja2Templates(directory='app/templates')
@app.on_event('startup')
def startup():
 Base.metadata.create_all(engine);db=SessionLocal()
 if not db.query(User).filter_by(email=settings.admin_email).first():db.add(User(email=settings.admin_email,name='Administrator',password_hash=hash_password(settings.admin_password),role='superadmin'))
 if not db.query(Keyword).count():
  for a,b,c in [('goodram','SSD',40),('kioxia','SSD',40),('enterprise ssd','SSD',25),('rdimm','DRAM',25),('lrdimm','DRAM',25),('pendrive','Flash',20)]:db.add(Keyword(term=a,category=b,weight=c))
 db.commit();db.close()
def current(request,db):
 uid=request.cookies.get('uid');return db.get(User,int(uid)) if uid and uid.isdigit() else None
def required(request:Request,db=Depends(get_db)):
 u=current(request,db)
 if not u:raise HTTPException(401)
 return u
def labels(request):return tr(request.query_params.get('lang') or request.cookies.get('lang') or settings.app_language)
@app.get('/health')
def health():return {'status':'ok'}
@app.get('/login',response_class=HTMLResponse)
def login_page(request:Request):return templates.TemplateResponse('login.html',{'request':request})
@app.post('/login')
def login(request:Request,email:str=Form(),password:str=Form(),db=Depends(get_db)):
 u=db.query(User).filter_by(email=email,active=True).first()
 if not u or not verify_password(password,u.password_hash):return templates.TemplateResponse('login.html',{'request':request,'error':'Invalid credentials'},status_code=400)
 r=RedirectResponse('/',303);r.set_cookie('uid',str(u.id),httponly=True,samesite='lax');return r
@app.get('/logout')
def logout():
 r=RedirectResponse('/login',303);r.delete_cookie('uid');return r
@app.get('/',response_class=HTMLResponse)
def index(request:Request,country:str='',category:str='',min_score:int=25,db=Depends(get_db)):
 u=current(request,db)
 if not u:return RedirectResponse('/login',303)
 q=db.query(Tender)
 if country:q=q.filter(Tender.country==country)
 if category:q=q.filter(Tender.category==category)
 rows=q.filter(Tender.score>=min_score).order_by(Tender.deadline.asc().nullslast()).limit(500).all()
 return templates.TemplateResponse('index.html',{'request':request,'u':u,'rows':rows,'t':labels(request),'runs':db.query(SourceRun).order_by(SourceRun.id.desc()).limit(4).all()})
@app.get('/tenders/{tid}',response_class=HTMLResponse)
def detail(tid:int,request:Request,db=Depends(get_db),u=Depends(required)):
 x=db.get(Tender,tid)
 if not x:raise HTTPException(404)
 return templates.TemplateResponse('detail.html',{'request':request,'u':u,'x':x,'users':db.query(User).filter_by(active=True).all(),'t':labels(request)})
@app.post('/tenders/{tid}/status')
def set_status(tid:int,status:str=Form(),assigned_to_id:str=Form(''),db=Depends(get_db),u=Depends(required)):
 x=db.get(Tender,tid);x.status=status;x.assigned_to_id=int(assigned_to_id) if assigned_to_id else None;db.commit();return RedirectResponse(f'/tenders/{tid}',303)
@app.post('/sync/{source}')
async def sync(source:str,request:Request,db=Depends(get_db),u=Depends(required)):
 if u.role not in ('superadmin','admin'):raise HTTPException(403)
 await sync_source(db,source);return RedirectResponse('/',303)
@app.get('/export.xlsx')
def export(country:str='',category:str='',db=Depends(get_db),u=Depends(required)):
 q=db.query(Tender)
 if country:q=q.filter_by(country=country)
 if category:q=q.filter_by(category=category)
 rows=q.all();wb=Workbook();ws=wb.active;ws.title='Tenders';ws.append(['ID','Source','Country','Title','Buyer','Value','Currency','Deadline','Category','Score','Status','URL'])
 for x in rows:ws.append([x.id,x.source,x.country,x.title,x.buyer,x.value,x.currency,x.deadline,x.category,x.score,x.status,x.source_url])
 wi=wb.create_sheet('Items');wi.append(['Tender ID','Description','Quantity','Unit','CPV','Matched terms'])
 for x in rows:
  for i in x.items:wi.append([x.id,i.description,i.quantity,i.unit,i.cpv,i.matched_terms])
 b=BytesIO();wb.save(b);b.seek(0);return StreamingResponse(b,media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',headers={'Content-Disposition':'attachment; filename=tenders.xlsx'})
@app.get('/admin',response_class=HTMLResponse)
def admin(request:Request,db=Depends(get_db),u=Depends(required)):
 if u.role not in ('superadmin','admin'):raise HTTPException(403)
 return templates.TemplateResponse('admin.html',{'request':request,'u':u,'users':db.query(User).all(),'keywords':db.query(Keyword).order_by(Keyword.category).all(),'t':labels(request)})
@app.post('/admin/users')
def add_user(name:str=Form(),email:str=Form(),password:str=Form(),role:str=Form(),countries:str=Form(''),db=Depends(get_db),u=Depends(required)):
 if u.role!='superadmin':raise HTTPException(403)
 db.add(User(name=name,email=email,password_hash=hash_password(password),role=role,countries=countries));db.commit();return RedirectResponse('/admin',303)
@app.post('/admin/keywords')
def add_keyword(term:str=Form(),category:str=Form(),weight:int=Form(15),db=Depends(get_db),u=Depends(required)):
 if u.role not in ('superadmin','admin'):raise HTTPException(403)
 db.add(Keyword(term=term,category=category,weight=weight));db.commit();return RedirectResponse('/admin',303)
