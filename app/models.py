from datetime import datetime
from sqlalchemy import Boolean,Column,DateTime,Float,ForeignKey,Integer,String,Text,UniqueConstraint
from sqlalchemy.orm import relationship
from .db import Base
class User(Base):
 __tablename__='users'; id=Column(Integer,primary_key=True); email=Column(String,unique=True,index=True); name=Column(String); password_hash=Column(String); role=Column(String,default='kam'); active=Column(Boolean,default=True); countries=Column(String,default='')
class Tender(Base):
 __tablename__='tenders'; __table_args__=(UniqueConstraint('source','external_id'),); id=Column(Integer,primary_key=True); source=Column(String,index=True); external_id=Column(String,index=True); country=Column(String,index=True); title=Column(Text); buyer=Column(Text); description=Column(Text,default=''); value=Column(Float); currency=Column(String); deadline=Column(DateTime); published_at=Column(DateTime); status=Column(String,default='new'); source_url=Column(Text); category=Column(String,index=True); score=Column(Integer,default=0,index=True); assigned_to_id=Column(Integer,ForeignKey('users.id')); created_at=Column(DateTime,default=datetime.utcnow); assignee=relationship('User'); items=relationship('TenderItem',cascade='all, delete-orphan',back_populates='tender')
class TenderItem(Base):
 __tablename__='tender_items'; id=Column(Integer,primary_key=True); tender_id=Column(Integer,ForeignKey('tenders.id')); description=Column(Text); quantity=Column(Float); unit=Column(String); cpv=Column(String); matched_terms=Column(Text,default=''); tender=relationship('Tender',back_populates='items')
class Keyword(Base):
 __tablename__='keywords'; id=Column(Integer,primary_key=True); term=Column(String,unique=True); category=Column(String); weight=Column(Integer,default=15); active=Column(Boolean,default=True)
class SourceRun(Base):
 __tablename__='source_runs'; id=Column(Integer,primary_key=True); source=Column(String); started_at=Column(DateTime,default=datetime.utcnow); finished_at=Column(DateTime); status=Column(String,default='running'); imported=Column(Integer,default=0); error=Column(Text,default='')
