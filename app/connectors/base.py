from dataclasses import dataclass,field
from datetime import datetime
@dataclass
class Item: description:str; quantity:float|None=None; unit:str|None=None; cpv:str|None=None
@dataclass
class TenderData:
 source:str; external_id:str; country:str; title:str; buyer:str=''; description:str=''; value:float|None=None; currency:str|None=None; deadline:datetime|None=None; published_at:datetime|None=None; status:str='active'; source_url:str=''; items:list[Item]=field(default_factory=list)
