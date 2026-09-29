/* =========================================================
   GEMU-style Surface Site — 交互脚本
   原生 JS，无任何依赖。全部使用严格相等，DOM 取用前先判空。
   模块：
     1. 页头滚动态 & 滚动进度条
     2. 移动端抽屉菜单
     3. 滚动揭示动画 (IntersectionObserver)
     4. FAQ 手风琴（高度过渡）
     5. 证言轮播
     6. 返回顶部 & 当前年份
     7. 导航高亮（当前区块）
   ========================================================= */
(function () {
  'use strict';

  /* 兜底：无论 <head> 内联脚本是否被执行（某些环境 CSP 会拦截），
     都确保 html 拥有 js 类，否则 .reveal 的初始隐藏不会生效，动画整体失效 */
  document.documentElement.classList.add('js');

  /* ---------- 工具 ---------- */
  const $  = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.prototype.slice.call((ctx || document).querySelectorAll(sel));

  /* =======================================================
     1. 页头滚动态 & 滚动进度条
     ======================================================= */
  const header   = $('#header');
  const progress = $('#progress');
  const toTop    = $('#toTop');
  const heroImg   = $('.hero__bg img');
  const heroInner = $('.hero__inner');
  const hasHeroFx = !!(heroImg && heroInner);
  const reduceMotion = window.matchMedia &&
                       window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let ticking = false;

  function onScrollFrame() {
    const y = window.scrollY || window.pageYOffset;

    // 页头背景切换
    if (header) {
      if (y > 40) { header.classList.add('is-stuck'); }
      else { header.classList.remove('is-stuck'); }
    }

    // 滚动进度条
    if (progress) {
      const doc = document.documentElement;
      const max = doc.scrollHeight - window.innerHeight;
      const pct = max > 0 ? (y / max) * 100 : 0;
      progress.style.width = Math.min(100, Math.max(0, pct)) + '%';
    }

    // 返回顶部按钮
    if (toTop) {
      if (y > window.innerHeight * 0.8) { toTop.classList.add('is-visible'); }
      else { toTop.classList.remove('is-visible'); }
    }

    // 首屏视差：内容上浮淡出，背景轻微下沉（幅度受限，避免露边）
    if (hasHeroFx && !reduceMotion && y <= window.innerHeight) {
      const vh = window.innerHeight;
      const bgShift = Math.min(y * 0.18, vh * 0.035);
      heroImg.style.transform = 'translate3d(0,' + bgShift.toFixed(1) + 'px,0) scale(1.08)';
      heroInner.style.transform = 'translate3d(0,' + (y * 0.3).toFixed(1) + 'px,0)';
      heroInner.style.opacity = String(Math.max(0, 1 - y / (vh * 0.72)));
    }

    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(onScrollFrame);
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScrollFrame();

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* =======================================================
     2. 移动端抽屉菜单
     ======================================================= */
  const burger = $('#burger');
  const drawer = $('#drawer');

  if (burger && drawer) {
    let lastFocus = null;

    const openDrawer = function () {
      lastFocus = document.activeElement;
      drawer.hidden = false;
      // 强制回流，保证 transform 过渡生效
      void drawer.offsetWidth;
      drawer.classList.add('is-open');
      burger.setAttribute('aria-expanded', 'true');
      burger.setAttribute('aria-label', 'Close menu');
      document.body.classList.add('is-locked');

      const first = $('.drawer__link', drawer);
      if (first) { first.focus(); }
    };

    const closeDrawer = function () {
      drawer.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Open menu');
      document.body.classList.remove('is-locked');

      window.setTimeout(function () {
        if (!drawer.classList.contains('is-open')) { drawer.hidden = true; }
      }, 450); // 与 CSS transition 时长保持一致

      if (lastFocus && typeof lastFocus.focus === 'function') { lastFocus.focus(); }
    };

    burger.addEventListener('click', function () {
      if (drawer.classList.contains('is-open')) { closeDrawer(); }
      else { openDrawer(); }
    });

    // 点击抽屉内链接后关闭
    $$('.drawer__link, .drawer .btn', drawer).forEach(function (link) {
      link.addEventListener('click', closeDrawer);
    });

    // Esc 关闭
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) { closeDrawer(); }
    });

    // 视口放大到桌面时自动复位
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 900 && drawer.classList.contains('is-open')) {
        drawer.classList.remove('is-open');
        drawer.hidden = true;
        burger.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('is-locked');
      }
    });
  }

  /* =======================================================
     3. 滚动揭示（双向 / 可回收）
        - 向下滚动进入观察带 → 淡入上移（0.8s，容器内错峰）
        - 退出观察带（还剩视口边缘窄条可见时）→ 平滑复位（0.6s，无延迟）
        - 复位带 120ms 去抖 + 页底兜底显示，防边界闪烁与内容永久隐藏
        - 只用 opacity/transform，rAF 节流，尊重系统减动效偏好
     ======================================================= */
  const revealEls = $$('.reveal');

  if (revealEls.length > 0) {
    if ('IntersectionObserver' in window && !reduceMotion) {
      // 观察带：视口上 / 下各收 18%，只把中间 64% 当"有效可视区"。
      // 元素必须完全退出这条带才复位——复位那一刻它还处在视口边缘的
      // 可见窄条里，所以回收动画肉眼能看到，而不是等它完全滚出屏幕。

      // 同一容器内的元素按顺序错峰（相邻 80ms，封顶 5 档 = 400ms）
      const groups = new Map();
      revealEls.forEach(function (el) {
        const parent = el.parentElement;
        const n = groups.get(parent) || 0;
        groups.set(parent, n + 1);
        el.dataset.revealDelay = String(Math.min(n, 5) * 80);
      });

      // 防闪烁去抖：离开观察带 120ms 后才真正回收；
      // 元素在带边界来回抖动时，重新 show() 会取消未执行的复位
      const hideTimers = new Map();

      function show(el) {
        const t = hideTimers.get(el);
        if (t) { window.clearTimeout(t); hideTimers.delete(el); }
        el.style.transitionDelay = (el.dataset.revealDelay || '0') + 'ms';
        el.classList.add('is-visible');
      }

      function hide(el) {
        if (hideTimers.has(el)) { return; }
        hideTimers.set(el, window.setTimeout(function () {
          hideTimers.delete(el);
          // 页面已滚到底：底部元素退不出观察带（下方没有滚动余量），
          // 此时保持显示，避免底部内容被复位到看不见
          if (atPageBottom() && inRealViewport(el)) { return; }
          el.style.transitionDelay = '0ms';
          el.classList.remove('is-visible');
        }, 120));
      }

      function inRealViewport(el) {
        const r = el.getBoundingClientRect();
        return r.top < window.innerHeight && r.bottom > 0;
      }

      function atPageBottom() {
        const doc = document.documentElement;
        return window.scrollY + window.innerHeight >= (doc.scrollHeight || 0) - 4;
      }

      const io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            show(entry.target);
          } else {
            hide(entry.target);
          }
        });
      }, { threshold: [0], rootMargin: '-18% 0px -18% 0px' });

      revealEls.forEach(function (el) { io.observe(el); });

      // 兜底：页面滚到底时，底部的短元素可能从未进入观察带
      // （下方没有滚动余量，IO 不再发事件）。这里强制显示它们，
      // 保证内容不会永远藏着。
      window.addEventListener('scroll', function () {
        if (!atPageBottom()) { return; }
        revealEls.forEach(function (el) {
          if (el.classList.contains('is-visible')) { return; }
          if (inRealViewport(el)) { show(el); }
        });
      }, { passive: true });
    } else {
      // 不支持 IO 或用户偏好减少动效 → 直接显示，不做动画
      revealEls.forEach(function (el) { el.classList.add('is-visible'); });
    }
  }

  /* =======================================================
     3b. 数字滚动计数（首屏数据条）
         进入视口从 0 计到目标值；离开后复位，回滚可重放
     ======================================================= */
  const counters = $$('[data-count]');

  if (counters.length > 0 && 'IntersectionObserver' in window && !reduceMotion) {
    const COUNT_DUR = 1300;

    const runCount = function (el) {
      if (el._counting) { return; }
      el._counting = true;
      const target = parseInt(el.getAttribute('data-count'), 10) || 0;
      const start = performance.now();
      const tick = function (now) {
        const t = Math.min(1, (now - start) / COUNT_DUR);
        const eased = 1 - Math.pow(1 - t, 3);   // ease-out-cubic
        el.textContent = String(Math.round(target * eased));
        if (t < 1) { requestAnimationFrame(tick); }
        else { el._counting = false; }
      };
      requestAnimationFrame(tick);
    };

    const resetCount = function (el) {
      el._counting = false;
      el.textContent = '0';
    };

    const cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.3) {
          runCount(entry.target);
        } else if (!entry.isIntersecting) {
          resetCount(entry.target);
        }
      });
    }, { threshold: [0, 0.3] });

    counters.forEach(function (el) { cio.observe(el); });
  }

  /* =======================================================
     4. FAQ 手风琴
     ======================================================= */
  const faqItems = $$('.faq__item');

  faqItems.forEach(function (item) {
    const btn  = $('.faq__q', item);
    const body = $('.faq__a', item);
    if (!btn || !body) { return; }

    btn.addEventListener('click', function () {
      const isOpen = item.getAttribute('data-open') === 'true';

      // 手风琴模式：先关闭其它项
      faqItems.forEach(function (other) {
        if (other === item) { return; }
        if (other.getAttribute('data-open') !== 'true') { return; }
        const oBody = $('.faq__a', other);
        const oBtn  = $('.faq__q', other);
        other.setAttribute('data-open', 'false');
        if (oBtn)  { oBtn.setAttribute('aria-expanded', 'false'); }
        if (oBody) { oBody.style.height = oBody.scrollHeight + 'px'; void oBody.offsetWidth; oBody.style.height = '0px'; }
      });

      if (isOpen) {
        body.style.height = body.scrollHeight + 'px';
        void body.offsetWidth;
        body.style.height = '0px';
        item.setAttribute('data-open', 'false');
        btn.setAttribute('aria-expanded', 'false');
      } else {
        body.style.height = body.scrollHeight + 'px';
        item.setAttribute('data-open', 'true');
        btn.setAttribute('aria-expanded', 'true');

        // 动画结束后改为 auto，避免窗口缩放时高度不跟随
        body.addEventListener('transitionend', function handler(e) {
          if (e.propertyName !== 'height') { return; }
          if (item.getAttribute('data-open') === 'true') { body.style.height = 'auto'; }
          body.removeEventListener('transitionend', handler);
        });
      }
    });
  });

  /* =======================================================
     5. 证言轮播
     ======================================================= */
  const tstRoot  = $('#testimonials');
  const tstTrack = $('#tstTrack');
  const tstNav   = $('#tstNav');

  if (tstRoot && tstTrack && tstNav) {
    const slides = $$('.tst-slide', tstTrack);
    let index = 0;
    let timer = null;

    // 生成指示点
    slides.forEach(function (_, i) {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'tst-dot';
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', 'Testimonial ' + (i + 1));
      dot.setAttribute('aria-current', i === 0 ? 'true' : 'false');
      dot.addEventListener('click', function () { goTo(i); });
      tstNav.appendChild(dot);
    });

    const dots = $$('.tst-dot', tstNav);

    function goTo(i) {
      index = (i + slides.length) % slides.length;
      tstTrack.style.transform = 'translateX(-' + (index * 100) + '%)';
      dots.forEach(function (d, di) {
        d.setAttribute('aria-current', di === index ? 'true' : 'false');
      });
      restart();
    }

    function next() { goTo(index + 1); }
    function restart() {
      if (timer) { window.clearInterval(timer); }
      timer = window.setInterval(next, 6000);
    }

    // 悬停 / 聚焦时暂停
    tstRoot.addEventListener('mouseenter', function () { if (timer) { window.clearInterval(timer); } });
    tstRoot.addEventListener('mouseleave', restart);

    // 尊重减少动效偏好
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduce) { restart(); }
  }

  /* =======================================================
     6. 当前年份
     ======================================================= */
  const yearEl = $('#year');
  if (yearEl) { yearEl.textContent = String(new Date().getFullYear()); }

  /* =======================================================
     7. 导航高亮（当前可见区块）
     ======================================================= */
  const navLinks = $$('.nav__link');

  if (navLinks.length > 0 && 'IntersectionObserver' in window) {
    const map = {};
    navLinks.forEach(function (link) {
      const id = (link.getAttribute('href') || '').replace('#', '');
      if (id) { map[id] = link; }
    });

    const sections = Object.keys(map)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);

    if (sections.length > 0) {
      const navIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) { return; }
          navLinks.forEach(function (l) { l.removeAttribute('aria-current'); });
          const link = map[entry.target.id];
          if (link) { link.setAttribute('aria-current', 'page'); }
        });
      }, { rootMargin: '-45% 0px -50% 0px' });

      sections.forEach(function (s) { navIO.observe(s); });
    }
  }
})();
