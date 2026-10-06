import asyncio
from app.db import Base,engine,SessionLocal
from app.services import sync_source
async def main():
 Base.metadata.create_all(engine);db=SessionLocal()
 for source in ('prozorro','ted'):
  try:print(source,await sync_source(db,source))
  except Exception as e:print(source,'ERROR',e)
 db.close()
asyncio.run(main())
