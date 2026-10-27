(() => {
  'use strict';

  const menuButton = document.querySelector('.menu-toggle');
  const menu = document.getElementById('main-nav');
  const closeMenu = () => {
    if (!menuButton || !menu) return;
    menu.classList.remove('is-open');
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open navigation');
  };
  if (menuButton && menu) {
    menuButton.addEventListener('click', () => {
      const isOpen = menuButton.getAttribute('aria-expanded') !== 'true';
      menu.classList.toggle('is-open', isOpen);
      menuButton.setAttribute('aria-expanded', String(isOpen));
      menuButton.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    });
    menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('click', event => {
      if (!menu.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        closeMenu();
        menuButton.focus();
      }
    });
    // Do not retain an open phone menu after rotating or crossing a breakpoint.
    if (window.matchMedia) {
      const navigationBreakpoint = window.matchMedia('(max-width: 980px)');
      if (navigationBreakpoint.addEventListener) navigationBreakpoint.addEventListener('change', closeMenu);
      else if (navigationBreakpoint.addListener) navigationBreakpoint.addListener(closeMenu);
    }
  }

  const filterButtons = Array.from(document.querySelectorAll('[data-filter]'));
  const projects = Array.from(document.querySelectorAll('.project-card'));
  const groups = Array.from(document.querySelectorAll('[data-project-group]'));
  const projectCount = document.getElementById('project-count');
  const search = document.getElementById('project-search');
  const empty = document.getElementById('empty-projects');
  const resetButtons = Array.from(document.querySelectorAll('[data-reset-projects]'));
  const resetView = document.getElementById('reset-project-view');
  const detailsToggle = document.getElementById('toggle-project-details');
  let activeFilter = 'all';
  const normalise = value => value.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  const searchable = new Map(projects.map(project => [project, normalise(project.dataset.search || '')]));
  const visibleProjects = () => projects.filter(project => !project.hidden);
  const updateDetailsToggle = () => {
    if (!detailsToggle) return;
    const visible = visibleProjects();
    const allOpen = visible.length > 0 && visible.every(project => project.querySelector('details')?.open);
    detailsToggle.disabled = visible.length === 0;
    detailsToggle.setAttribute('aria-pressed', String(allOpen));
    detailsToggle.textContent = allOpen ? 'Collapse all details ' : 'Expand all details ';
    const icon = document.createElement('span');
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = allOpen ? '−' : '+';
    detailsToggle.appendChild(icon);
  };
  const applyFilters = () => {
    const terms = normalise(search?.value || '').split(' ').filter(Boolean);
    let visible = 0;
    projects.forEach(project => {
      const matchesCategory = activeFilter === 'all' || project.dataset.category === activeFilter;
      const matchesSearch = terms.every(term => searchable.get(project).includes(term));
      const show = matchesCategory && matchesSearch;
      project.hidden = !show;
      if (show) visible += 1;
    });
    groups.forEach(group => {
      const visibleInGroup = Array.from(group.querySelectorAll('.project-card')).filter(project => !project.hidden).length;
      group.hidden = visibleInGroup === 0;
      const count = group.querySelector('.group-count');
      if (count) {
        count.textContent = String(visibleInGroup).padStart(2, '0');
        count.setAttribute('aria-label', `${visibleInGroup} project${visibleInGroup === 1 ? '' : 's'}`);
      }
    });
    filterButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === activeFilter)));
    if (projectCount) projectCount.textContent = `Showing ${visible} of ${projects.length} projects`;
    if (empty) empty.hidden = visible !== 0;
    if (resetView) resetView.hidden = activeFilter === 'all' && !(search?.value.trim());
    updateDetailsToggle();
    updateProgress();
  };
  filterButtons.forEach(button => button.addEventListener('click', () => {
    activeFilter = button.dataset.filter;
    applyFilters();
  }));
  search?.addEventListener('input', applyFilters);
  resetButtons.forEach(button => button.addEventListener('click', () => {
    activeFilter = 'all';
    if (search) search.value = '';
    applyFilters();
    search?.focus();
  }));
  detailsToggle?.addEventListener('click', () => {
    const expand = detailsToggle.getAttribute('aria-pressed') !== 'true';
    visibleProjects().forEach(project => {
      const details = project.querySelector('details');
      if (details) details.open = expand;
    });
    updateDetailsToggle();
    updateProgress();
  });

  const copyButton = document.getElementById('copy-email');
  const copyStatus = document.getElementById('copy-status');
  copyButton?.addEventListener('click', async () => {
    if (!copyStatus) return;
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText('vedantak070@gmail.com');
      copyStatus.textContent = 'Email address copied.';
    } catch {
      copyStatus.textContent = 'Select the email address above to copy it.';
    }
  });

  const progress = document.getElementById('reading-progress');
  function updateProgress() {
    if (!progress) return;
    const distance = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = distance > 0 ? Math.min(1, Math.max(0, window.scrollY / distance)) : 0;
    progress.style.transform = `scaleX(${ratio})`;
  }
  let progressQueued = false;
  window.addEventListener('scroll', () => {
    if (progressQueued) return;
    progressQueued = true;
    window.requestAnimationFrame(() => {
      updateProgress();
      progressQueued = false;
    });
  }, {passive: true});
  window.addEventListener('resize', updateProgress, {passive: true});
  document.querySelectorAll('details').forEach(details => details.addEventListener('toggle', () => {
    updateDetailsToggle();
    updateProgress();
  }));
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(updateProgress);
    document.fonts.addEventListener?.('loadingdone', updateProgress);
  }

  if ('IntersectionObserver' in window) {
    const navLinks = Array.from(document.querySelectorAll('[data-nav]'));
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        navLinks.forEach(link => {
          const active = link.getAttribute('href') === `#${entry.target.id}`;
          link.classList.toggle('is-active', active);
          if (active) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, {rootMargin: '-15% 0px -65% 0px', threshold: 0});
    document.querySelectorAll('main > section[id]').forEach(section => observer.observe(section));
  }

  applyFilters();
  document.documentElement.classList.add('js');

  // Appearance motion never hides content; phones avoid extra scroll animation.
  if ('IntersectionObserver' in window && window.matchMedia &&
      !window.matchMedia('(max-width: 767px)').matches &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const appearanceObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('motion-enter');
        appearanceObserver.unobserve(entry.target);
      });
    }, {threshold: 0.1, rootMargin: '0px 0px -18px 0px'});
    document.querySelectorAll('.project-card, .expertise-group, .certification-card, .experience-card')
      .forEach(element => appearanceObserver.observe(element));
  }
})();
