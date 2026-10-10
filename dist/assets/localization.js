/* Localize strings the native components insert after page load. */
(() => {
  document.querySelector('.locale-switch')?.addEventListener('click', event => {
    const link = event.currentTarget;
    const url = new URL(link.href);
    url.search = location.search;
    url.hash = location.hash;
    link.href = url.href;
  });
  if (document.documentElement.lang !== 'fa') return;
  fetch('/assets/fa-strings.json').then(response => {
    if (!response.ok) throw new Error('Persian copy unavailable');
    return response.json();
  }).then(strings => {
    const normalize = value => value.replace(/\s+/g, ' ').trim();
    const translate = value => {
      const key = normalize(value);
      if (strings[key]) return value.match(/^\s*/)[0] + strings[key] + value.match(/\s*$/)[0];
      if (/^Footnote \d+$/.test(key)) return 'پاورقی ' + key.match(/\d+/)[0].replace(/\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);
      return value;
    };
    const update = root => {
      if (root.nodeType === Node.TEXT_NODE) {
        if (root.parentElement?.closest('script,style,[lang="en"],.locale-nav')) return;
        const next = translate(root.nodeValue);
        if (next !== root.nodeValue) root.nodeValue = next;
        return;
      }
      if (root.nodeType !== Node.ELEMENT_NODE && root !== document.body) return;
      if (root.matches?.('script,style,.locale-nav')) return;
      for (const attr of ['aria-label','alt','title','placeholder']) {
        if (!root.hasAttribute?.(attr)) continue;
        const value = root.getAttribute(attr), next = translate(value);
        if (value !== next) root.setAttribute(attr,next);
      }
      for (const child of root.childNodes) update(child);
    };
    update(document.body);
    new MutationObserver(records => {
      for (const record of records) {
        if (record.type === 'attributes' || record.type === 'characterData') update(record.target);
        else for (const node of record.addedNodes) update(node);
      }
    }).observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['aria-label','alt','title','placeholder']});
  }).catch(error => console.error(error));
})();
