"""Generate static Persian/English pages. Requires Python 3 and lxml.

Keep the English source intact; translate only text and accessible labels.
Native component IDs, selectors, analytics data and embedded scripts stay intact.
"""
from pathlib import Path
from lxml import html, etree
import json, re

ROOT = Path(__file__).resolve().parent.parent
inventory = json.loads((ROOT / 'src/text-inventory.json').read_text(encoding='utf-8'))
copy = {}
for line in (ROOT / 'src/fa-copy.txt').read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    index, translation = line.split('\t', 1)
    copy[inventory[int(index)]] = translation
assert len(copy) == len(inventory), 'Every source string needs an explicit translation or brand-name exception.'
copy.update({'Play product animation': 'پخش ویدئوی محصول',
             'Pause Highlights gallery': 'توقف گالری ویژگی‌ها',
             'Pause': 'توقف', 'Play': 'پخش', 'Open menu': 'باز کردن منو',
             'Close menu': 'بستن منو', 'Close Menu': 'بستن منو',
             'Open Menu': 'باز کردن منو', 'Pause animation': 'توقف انیمیشن',
             'Play animation': 'پخش انیمیشن', 'Pause video': 'توقف ویدئو',
             'Play video': 'پخش ویدئو', 'Search': 'جست‌وجو',
             'Apple Watch SE 3, aluminum case, midnight color, Modular watch face with day and date complication, right side exterior, Digital Crown, connected to Braided Solo Loop band, black color': 'اپل واچ SE ۳ میدنایت با صفحهٔ ماژولار و تاریخ، پیچ دیجیتال و بند بافتنی مشکی.',
             'Apple Watch SE 3, aluminum case, starlight color, Modular watch face with day and date complication, right side exterior, Digital Crown, connected to Braided Solo Loop band, magenta color': 'اپل واچ SE ۳ استارلایت با صفحهٔ ماژولار و تاریخ، پیچ دیجیتال و بند بافتنی سرخابی.'})
(ROOT / 'dist/assets/fa-strings.json').write_text(json.dumps(copy, ensure_ascii=False), encoding='utf-8')
digits = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
def norm(s): return re.sub(r'\s+', ' ', s or '').strip()
def translate(s):
    key = norm(s)
    if not key: return s
    target = copy.get(key)
    if target is None and not re.search('[A-Za-z]', key):
        target = key.translate(digits)
        target = re.sub(r'\$([۰-۹,٫.]+)', r'\1 دلار', target)
    if target is None: return s
    return re.sub(r'^\s*', '', s) if not target else re.match(r'^\s*', s)[0] + target + re.search(r'\s*$', s)[0]

original = (ROOT / 'src/english.html').read_text(encoding='utf-8')
description = 'اپل واچ SE ۳؛ سلامت، ورزش و ارتباطات، روی مچت. با قابلیت‌های ایمنی، شارژ سریع و دو رنگ خوش‌استایل.'
for language in ['en', 'fa']:
    doc = html.fromstring(original)
    persian = language == 'fa'
    if persian:
        for el in doc.iter():
            if not isinstance(el.tag, str): continue
            if el.tag not in ['script', 'style', 'noscript']:
                if el.text: el.text = translate(el.text)
                for attr in ['alt', 'aria-label', 'title', 'placeholder', 'data-aria-label', 'data-aria-label-small']:
                    if el.get(attr): el.set(attr, translate(el.get(attr)))
                if el.get('data-aria-map'):
                    labels = json.loads(el.get('data-aria-map'))
                    el.set('data-aria-map', json.dumps({k:translate(v) for k,v in labels.items()},ensure_ascii=False))
                if el.get('data-product-template'):
                    template = el.get('data-product-template')
                    if 'credit.display.smart' in template:
                        el.set('data-product-template','با تحویل دستگاه واجد شرایطت، تا ${credit.display.smart} برای خرید اپل واچ بعدی اعتبار بگیر.')
            # Tails belong to the parent and can contain visible copy after inline elements.
            if el.tail: el.tail = translate(el.tail)
            if el.get('lang'): el.set('lang', 'fa')
            if el.get('dir'): el.set('dir', 'rtl')
        doc.set('lang', 'fa')
        doc.set('xml:lang', 'fa')
        doc.set('dir', 'rtl')
        for meta in doc.xpath('//meta[@name="description" or @property="og:description" or @name="twitter:description"]'):
            meta.set('content', description)
        for meta in doc.xpath('//meta[@property="og:locale"]'): meta.set('content', 'fa_IR')
        for meta in doc.xpath('//meta[@property="og:title" or @name="twitter:title"]'): meta.set('content', 'اپل واچ SE ۳')
    # Remove fine print after translation: drop_tree merges text nodes, which
    # must keep their original inventory boundaries until localized.
    for section in doc.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " ac-gf-sosumi ")]'):
        section.drop_tree()
    for link in doc.xpath('//a[starts-with(@href, "#footnote-")]'):
        wrappers = link.xpath('ancestor::*[contains(concat(" ", normalize-space(@class), " "), " footnote ")]')
        (wrappers[-1] if wrappers else link).drop_tree()
    head = doc.find('head')
    head.append(html.Element('link', rel='stylesheet', href='/assets/localization.css'))
    for lang, href in [('fa','/'), ('en','/en/'), ('x-default','/')]:
        head.append(html.Element('link', rel='alternate', hreflang=lang, href=href))
    if persian:
        head.append(html.Element('link', rel='preload', href='/assets/pinar/Pinar-DS4-Regular.woff2', as_='font', type='font/woff2', crossorigin='anonymous'))
        head[-1].attrib['as'] = head[-1].attrib.pop('as_')
    # A separate, stable control: the native header must not rebuild it.
    header = doc.get_element_by_id('globalheader')
    control = html.Element('nav', attrib={'class':'locale-nav', 'aria-label': 'انتخاب زبان' if persian else 'Language'})
    link = html.Element('a', href='/en/' if persian else '/', attrib={'class':'locale-switch', 'lang':'en' if persian else 'fa', 'hreflang':'en' if persian else 'fa', 'aria-label':'Switch to English' if persian else 'تغییر زبان به فارسی', 'data-local-link':''})
    link.text = 'EN' if persian else 'فارسی'
    control.append(link)
    header.addnext(control)
    doc.find('body').append(html.Element('script', src='/assets/localization.js', defer='defer'))
    result = '<!DOCTYPE html>\n' + html.tostring(doc, encoding='unicode', method='html')
    destination = ROOT / ('dist/index.html' if persian else 'dist/en/index.html')
    destination.parent.mkdir(exist_ok=True, parents=True)
    destination.write_text(result, encoding='utf-8')
print(f'Generated Persian default and English route; {len(inventory)} source strings covered.')
