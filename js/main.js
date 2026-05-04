(function () {
  const cfg = window.MONTHLY_BIBLE_STUDY_CONFIG || { partifulUrl: 'https://partiful.com/', galleryPhotos: [] };

  /** Sync all Partiful links from config */
  document.querySelectorAll('a[href="https://partiful.com/"]').forEach(function (a) {
    a.href = cfg.partifulUrl || a.href;
  });

  /** Mobile navigation */
  const toggle = document.querySelector('.nav__toggle');
  const navList = document.getElementById('nav-panel');
  if (toggle && navList) {
    toggle.addEventListener('click', function () {
      const open = navList.classList.toggle('nav__list--open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    navList.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.matchMedia('(max-width: 767px)').matches) {
          navList.classList.remove('nav__list--open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  /** Photo gallery */
  const galleryRoot = document.getElementById('photo-gallery');
  const lightbox = document.getElementById('lightbox');
  const lbImg = lightbox && lightbox.querySelector('.lightbox__img');
  const lbCaption = lightbox && lightbox.querySelector('.lightbox__caption');
  const lbClose = lightbox && lightbox.querySelector('.lightbox__close');

  function openLightbox(item) {
    if (!lightbox || !lbImg || !lbCaption) return;
    lbImg.src = item.src;
    lbImg.alt = item.alt || '';
    lbCaption.textContent = item.caption || '';
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
    lbClose.focus();
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.hidden = true;
    lbImg.removeAttribute('src');
    document.body.style.overflow = '';
  }

  if (galleryRoot && cfg.galleryPhotos && cfg.galleryPhotos.length) {
    cfg.galleryPhotos.forEach(function (item, i) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'photo-tile';
      btn.setAttribute('aria-label', 'View photo: ' + (item.caption || 'Image ' + (i + 1)));

      const img = document.createElement('img');
      img.src = item.src;
      img.alt = item.alt || '';
      img.loading = 'lazy';
      img.decoding = 'async';
      img.width = 400;
      img.height = 300;

      const cap = document.createElement('span');
      cap.className = 'photo-tile__cap';
      cap.textContent = item.caption || '';

      btn.appendChild(img);
      btn.appendChild(cap);
      btn.addEventListener('click', function () {
        openLightbox(item);
      });
      galleryRoot.appendChild(btn);
    });
  }

  if (lbClose) {
    lbClose.addEventListener('click', closeLightbox);
  }
  if (lightbox) {
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lightbox && !lightbox.hidden) closeLightbox();
  });
})();
