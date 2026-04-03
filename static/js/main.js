/* ============================================================
   RoleFit — Main JavaScript
   GSAP ScrollTrigger + ScrollSmoother + UI interactions
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ----- Loading Screen (shows only once per session) ----- */
  const loader = document.getElementById('loading-screen');
  if (loader) {
    if (sessionStorage.getItem('rf_loaded')) {
      loader.classList.add('hidden');
    } else {
      setTimeout(() => {
        loader.classList.add('hidden');
        sessionStorage.setItem('rf_loaded', '1');
      }, 2200);
    }
  }

  /* ----- Navbar scroll shadow ----- */
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  /* ----- File upload UX ----- */
  const fileInput = document.getElementById('resume');
  const fileNameEl = document.querySelector('.file-name-display');
  const uploadArea = document.querySelector('.file-upload-area');

  if (fileInput && fileNameEl) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length) {
        fileNameEl.textContent = fileInput.files[0].name;
        fileNameEl.classList.add('visible');
      } else {
        fileNameEl.classList.remove('visible');
      }
    });
  }

  if (uploadArea) {
    ['dragenter', 'dragover'].forEach(e =>
      uploadArea.addEventListener(e, () => uploadArea.classList.add('dragover'), { passive: true })
    );
    ['dragleave', 'drop'].forEach(e =>
      uploadArea.addEventListener(e, () => uploadArea.classList.remove('dragover'), { passive: true })
    );
  }

  /* ----- Form submit → show analyzing overlay ----- */
  const form = document.querySelector('.analyze-form');
  const overlay = document.querySelector('.analyzing-overlay');
  const submitBtn = document.querySelector('.submit-btn');

  if (form && overlay) {
    form.addEventListener('submit', () => {
      overlay.classList.add('active');
      if (submitBtn) submitBtn.classList.add('loading');
    });
  }

  /* ----- Terms modal ----- */
  document.querySelectorAll('[data-modal]').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.getElementById(trigger.dataset.modal);
      if (target) target.classList.add('active');
    });
  });

  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.modal-overlay').classList.remove('active');
    });
  });

  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) overlay.classList.remove('active');
    });
  });

  /* ----- Smooth scroll for anchor links ----- */
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(link.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  /* ----- GSAP ScrollTrigger animations ----- */
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    /* Hero entrance */
    const heroTl = gsap.timeline({ defaults: { ease: 'power3.out', duration: 0.8 } });
    heroTl
      .from('.hero-badge', { y: 20, opacity: 0 })
      .from('.hero h1', { y: 30, opacity: 0 }, '-=0.5')
      .from('.hero-subtitle', { y: 20, opacity: 0 }, '-=0.5')
      .from('.hero-actions', { y: 20, opacity: 0 }, '-=0.4');

    /* Stats reveal animation */
    ScrollTrigger.batch('.stat-item', {
      onEnter: batch => gsap.fromTo(batch,
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, stagger: 0.1, duration: 0.6, ease: 'power2.out' }
      ),
      start: 'top 85%',
      once: true
    });

    /* Generic reveal for sections */
    gsap.utils.toArray('.gs-reveal').forEach(el => {
      gsap.fromTo(el,
        { y: 40, opacity: 0, visibility: 'hidden' },
        {
          y: 0, opacity: 1, visibility: 'visible',
          duration: 0.8, ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            once: true
          }
        }
      );
    });

    /* Step cards stagger */
    ScrollTrigger.batch('.step-card', {
      onEnter: batch => gsap.fromTo(batch,
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, stagger: 0.15, duration: 0.7, ease: 'power2.out' }
      ),
      start: 'top 85%',
      once: true
    });

    /* Form card entrance */
    gsap.from('.form-card', {
      y: 50, opacity: 0, duration: 0.9, ease: 'power2.out',
      scrollTrigger: { trigger: '.form-card', start: 'top 85%', once: true }
    });

    /* Result cards (results page) */
    ScrollTrigger.batch('.result-card', {
      onEnter: batch => gsap.fromTo(batch,
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, stagger: 0.12, duration: 0.7, ease: 'power2.out' }
      ),
      start: 'top 90%',
      once: true
    });

    /* Score ring animation on results page */
    const ringFill = document.querySelector('.ring-fill');
    if (ringFill) {
      const scoreEl = document.querySelector('.score-value');
      const scoreVal = scoreEl ? parseFloat(scoreEl.textContent) : 0;
      const circumference = 440;
      const offset = circumference - (circumference * scoreVal / 100);
      ringFill.style.strokeDashoffset = circumference;

      ScrollTrigger.create({
        trigger: '.score-section',
        start: 'top 80%',
        once: true,
        onEnter: () => {
          gsap.to(ringFill, { attr: { 'stroke-dashoffset': offset }, duration: 1.5, ease: 'power2.out' });
        }
      });
    }
  }
});
