/* Reference hero controls. Other galleries use the original native components. */
(() => {
  const hero = document.querySelector('.reference-hero');
  const film = hero?.querySelector('video');
  const control = hero?.querySelector('.rh-pause');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const reference = new URLSearchParams(location.search).has('reference');
  const small = matchMedia('(max-width: 734px)');
  const medium = matchMedia('(max-width: 1068px)');
  let userPaused = reference || reduced.matches;
  let visible = true;
  if (film && control) {
    const updateControl = () => {
      control.setAttribute('aria-pressed', String(film.paused));
      const persian = document.documentElement.lang === 'fa';
      control.setAttribute('aria-label', persian ? (film.paused ? 'پخش ویدئوی محصول' : 'توقف ویدئوی محصول') : (film.paused ? 'Play product animation' : 'Pause product animation'));
    };
    const ready = () => {
      film.currentTime = 2.8;
      if (!userPaused && visible) film.play().catch(updateControl);
      else film.pause();
      updateControl();
    };
    const selectMedia = () => {
      const size = small.matches ? 'small_2x' : medium.matches ? 'medium_2x' : 'large_2x';
      const src = '/assets/hero-' + size + '.mp4';
      if (film.getAttribute('src') !== src) { film.setAttribute('src', src); film.load(); }
      else if (film.readyState >= 1) ready();
    };
    film.addEventListener('loadedmetadata', ready);
    film.addEventListener('play', updateControl);
    film.addEventListener('pause', updateControl);
    control.addEventListener('click', () => {
      userPaused = !film.paused;
      if (userPaused) film.pause();
      else film.play().catch(updateControl);
    });
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      if (!visible) film.pause();
      else if (!userPaused && film.readyState >= 2) film.play().catch(updateControl);
    }).observe(hero);
    reduced.addEventListener('change', event => {
      if (event.matches) { userPaused = true; film.pause(); }
    });
    small.addEventListener('change', selectMedia);
    medium.addEventListener('change', selectMedia);
    selectMedia();
  }
  const normalizeLinks = parent => parent.querySelectorAll('a[href^="/"]').forEach(link => {
    const href = link.getAttribute('href');
    if (link.hasAttribute('data-local-link')) return;
    if (!/^\/(v|ac|assets)\//.test(href)) link.href = 'https://www.apple.com' + href;
  });
  normalizeLinks(document);
  const nav = document.getElementById('globalheader');
  if (nav) new MutationObserver(() => normalizeLinks(nav)).observe(nav, {subtree: true, childList: true});
})();
