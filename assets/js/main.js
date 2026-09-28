/* Fialho Barbearia
   Interações da página. Tudo aqui é melhoria progressiva: sem JavaScript,
   o menu fica sempre visível e todos os links continuam funcionando. */

(function () {
  'use strict';

  var root = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------- Menu (celular e tablet) ---------- */

  function initMenu() {
    var toggle = document.querySelector('[data-menu-toggle]');
    var menu = document.querySelector('[data-menu]');
    if (!toggle || !menu) return;

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', String(open));
      menu.classList.toggle('is-open', open);
    }

    function isOpen() {
      return toggle.getAttribute('aria-expanded') === 'true';
    }

    toggle.addEventListener('click', function () {
      setOpen(!isOpen());
    });

    menu.addEventListener('click', function (event) {
      if (event.target.closest('a')) setOpen(false);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen()) {
        setOpen(false);
        toggle.focus();
      }
    });

    document.addEventListener('click', function (event) {
      if (isOpen() && !event.target.closest('[data-header]')) setOpen(false);
    });

    window.matchMedia('(min-width: 980px)').addEventListener('change', function (event) {
      if (event.matches) setOpen(false);
    });
  }

  /* ---------- Revelação na rolagem ---------- */

  function initReveal() {
    var items = document.querySelectorAll('[data-reveal]');
    if (!items.length || reduceMotion.matches || !('IntersectionObserver' in window)) return;

    root.classList.add('motion-ok');

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    items.forEach(function (item) {
      observer.observe(item);
    });
  }

  /* ---------- Barra fixa no celular ---------- */

  function initStickyCta() {
    var bar = document.querySelector('[data-sticky-cta]');
    var hero = document.querySelector('.hero__actions');
    if (!bar || !hero || !('IntersectionObserver' in window)) return;

    bar.hidden = false;

    var selectors = ['.club__actions', '.visit__actions', '.closing', '.footer'];
    var state = { pastHero: false, nearAction: selectors.map(function () { return false; }) };

    function update() {
      var near = state.nearAction.some(Boolean);
      var visible = state.pastHero && !near;
      bar.classList.toggle('is-visible', visible);
      root.classList.toggle('has-sticky-cta', visible);
    }

    new IntersectionObserver(function (entries) {
      var entry = entries[0];
      state.pastHero = !entry.isIntersecting && entry.boundingClientRect.top < 0;
      update();
    }).observe(hero);

    // A barra some onde a página já oferece um botão de ação próprio
    var elements = selectors.map(function (selector) {
      return document.querySelector(selector);
    });

    var actionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        state.nearAction[elements.indexOf(entry.target)] = entry.isIntersecting;
      });
      update();
    });

    elements.forEach(function (element) {
      if (element) actionObserver.observe(element);
    });

    update();
  }

  initMenu();
  initReveal();
  initStickyCta();
})();
