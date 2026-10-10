from lxml import html
import json,re
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')
root=html.fromstring(Path('src/english.html').read_text(encoding='utf-8'))
items=[]
def add(s):
 s=re.sub(r'\s+',' ',s or '').strip()
 if s and re.search('[A-Za-z]',s) and s not in items: items.append(s)
for e in root.iter():
 if not isinstance(e.tag,str) or e.tag in ['script','style','noscript']:continue
 add(e.text)
 if e.tag not in ['script','style']:add(e.tail)
 for k in ['alt','aria-label','title','placeholder']:add(e.get(k))
Path('src/text-inventory.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
for i,s in enumerate(items): print(str(i)+': '+s)
