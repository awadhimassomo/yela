// PRELOADER
window.addEventListener('load', () => {
  setTimeout(() => {
    const p = document.getElementById('preloader');
    if (p) {
      p.style.opacity = '0';
      setTimeout(() => p.style.display = 'none', 600);
    }
    scrollToHashTarget();
  }, 1800);
});

function scrollToHashTarget() {
  if (!window.location.hash) return;
  const target = document.querySelector(window.location.hash);
  if (!target) return;
  const navOffset = nav ? nav.offsetHeight : 0;
  const top = target.getBoundingClientRect().top + window.scrollY - navOffset;
  window.scrollTo({ top, behavior: 'smooth' });
}

// CUSTOM CURSOR
const cur = document.getElementById('cursor');
const ring = document.getElementById('cursor-ring');
if (cur && ring) {
  let mx = 0, my = 0, rx = 0, ry = 0;
  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    cur.style.left = mx + 'px'; cur.style.top = my + 'px';
  });
  function animRing() {
    rx += (mx - rx) * 0.1; ry += (my - ry) * 0.1;
    ring.style.left = rx + 'px'; ring.style.top = ry + 'px';
    requestAnimationFrame(animRing);
  }
  animRing();
  document.querySelectorAll('a, button, .program-card, .team-card, .gallery-item').forEach(el => {
    el.addEventListener('mouseenter', () => {
      cur.style.transform = 'translate(-50%,-50%) scale(2)';
      cur.style.background = 'var(--coral)';
      ring.style.transform = 'translate(-50%,-50%) scale(1.5)';
      ring.style.opacity = '0.2';
    });
    el.addEventListener('mouseleave', () => {
      cur.style.transform = 'translate(-50%,-50%) scale(1)';
      cur.style.background = 'var(--saffron)';
      ring.style.transform = 'translate(-50%,-50%) scale(1)';
      ring.style.opacity = '0.5';
    });
  });
}

// NAVBAR SCROLL
const nav = document.getElementById('navbar');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  });
}

// HAMBURGER
const ham = document.getElementById('hamburger');
const mob = document.getElementById('mobileMenu');
if (ham && mob) {
  let menuOpen = false;
  ham.addEventListener('click', () => {
    menuOpen = !menuOpen;
    mob.classList.toggle('open', menuOpen);
    ham.children[0].style.transform = menuOpen ? 'rotate(45deg) translate(5px,5px)' : '';
    ham.children[1].style.opacity = menuOpen ? '0' : '1';
    ham.children[2].style.transform = menuOpen ? 'rotate(-45deg) translate(5px,-5px)' : '';
  });
  document.querySelectorAll('.mobile-link').forEach(a => {
    a.addEventListener('click', () => {
      menuOpen = false; mob.classList.remove('open');
      ham.children[0].style.transform = '';
      ham.children[1].style.opacity = '1';
      ham.children[2].style.transform = '';
    });
  });
}

// SCROLL REVEAL
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      if (e.target.classList.contains('reveal-right')) animateAboutStats();
    }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => revealObserver.observe(el));

// ABOUT STAT COUNTERS
let aboutStatsRun = false;
function animateAboutStats() {
  if (aboutStatsRun) return; aboutStatsRun = true;
  const targets = [{ id: 'stat1', end: 800 }, { id: 'stat2', end: 7 }, { id: 'stat3', end: 48 }];
  targets.forEach(({ id, end }) => {
    const el = document.getElementById(id);
    if (!el) return;
    let val = 0; const step = end / 60;
    const t = setInterval(() => {
      val += step;
      if (val >= end) { val = end; clearInterval(t); }
      el.textContent = Math.floor(val);
    }, 16);
  });
}

// IMPACT COUNTERS
const impactSec = document.getElementById('impact');
if (impactSec) {
  const impactObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        document.querySelectorAll('.counter').forEach(c => {
          const target = parseInt(c.dataset.target);
          let val = 0; const step = target / 80;
          const t = setInterval(() => {
            val += step;
            if (val >= target) { val = target; clearInterval(t); }
            c.textContent = Math.floor(val);
          }, 16);
        });
        impactObs.disconnect();
      }
    });
  }, { threshold: 0.3 });
  impactObs.observe(impactSec);
}

// TESTIMONIALS SLIDER
let testiIdx = 0;
const track = document.getElementById('testiTrack');
const dots = document.querySelectorAll('.testi-dot');
const totalSlides = dots.length;

function goTesti(idx) {
  testiIdx = Math.max(0, Math.min(idx, totalSlides - 1));
  if (track) track.style.transform = `translateX(-${testiIdx * 100}%)`;
  dots.forEach((d, i) => d.classList.toggle('active', i === testiIdx));
}
dots.forEach(d => d.addEventListener('click', () => goTesti(parseInt(d.dataset.idx))));

let autoTesti = setInterval(() => goTesti((testiIdx + 1) % totalSlides), 5000);
if (track) {
  track.addEventListener('mouseenter', () => clearInterval(autoTesti));
  track.addEventListener('mouseleave', () => {
    autoTesti = setInterval(() => goTesti((testiIdx + 1) % totalSlides), 5000);
  });
  let touchX = 0;
  track.addEventListener('touchstart', e => touchX = e.touches[0].clientX, { passive: true });
  track.addEventListener('touchend', e => {
    const diff = touchX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) goTesti(diff > 0 ? testiIdx + 1 : testiIdx - 1);
  }, { passive: true });
}

// AUTO-DISMISS DJANGO MESSAGES
document.querySelectorAll('.django-message').forEach(msg => {
  setTimeout(() => {
    msg.style.transition = 'opacity 0.5s ease';
    msg.style.opacity = '0';
    setTimeout(() => msg.remove(), 500);
  }, 5000);
});
