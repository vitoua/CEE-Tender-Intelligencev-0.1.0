WORDS={'DRAM':['ddr3','ddr4','ddr5','sodimm','udimm','rdimm','lrdimm','ecc memory','pamięć ram','оперативна пам'], 'SSD':['ssd','nvme','solid state','dysk półprzewodnikowy','твердотільний','u.2','u.3','e1.s','e3.s','sas ssd'], 'Flash':['usb flash','pendrive','flash drive','microsd','micro sd','sd card','karta pamięci','карта пам'], 'NAND':['nand','emmc','ufs','bics flash']}
NEG=['furniture','chair','meble','krzesło','меблі']
def match(text,extra=()):
 low=(text or '').lower()
 if any(x in low for x in NEG): return 'Other',0,[]
 scores={}; hits=[]
 for cat,terms in WORDS.items():
  f=[x for x in terms if x in low]
  if f:scores[cat]=25+15*len(f);hits+=f
 for term,cat,w in extra:
  if term.lower() in low:scores[cat]=scores.get(cat,0)+w;hits.append(term)
 if not scores:return 'Other',0,[]
 cat=max(scores,key=scores.get);return cat,min(100,scores[cat]),sorted(set(hits))
