(function () {
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isMobile = window.matchMedia("(max-width: 767px)").matches;
  const animThreshold = isMobile ? 0.42 : 0.28;
  const animRootMargin = isMobile ? "0px 0px -12% 0px" : "0px 0px -8% 0px";

  /* Nav */
  const toggle = document.getElementById("navToggle");
  const nav = document.getElementById("nav");
  const backdrop = document.getElementById("navBackdrop");

  function setNavOpen(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("nav-open", open);
    if (backdrop) backdrop.hidden = !open;
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNavOpen(!nav.classList.contains("is-open"));
    });
    if (backdrop) {
      backdrop.addEventListener("click", function () { setNavOpen(false); });
    }
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setNavOpen(false); });
    });
  }

  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

  function countUp(el, target, duration, formatter) {
    const fallback = el.dataset.fallback;
    if (reduced) {
      el.textContent = fallback || formatter(target);
      return;
    }
    const start = performance.now();
    let lastText = "";
    function frame(now) {
      const p = Math.min((now - start) / duration, 1);
      const text = p >= 1
        ? (fallback || formatter(target))
        : formatter(target * easeOut(p));
      if (text !== lastText) {
        lastText = text;
        el.textContent = text;
      }
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function resetCounters(root) {
    root.querySelectorAll("[data-count]").forEach(function (el) {
      delete el.dataset.done;
      const raw = el.dataset.count;
      if (!raw || isNaN(Number(raw))) {
        if (el.dataset.fallback) el.textContent = el.dataset.fallback;
        return;
      }
      el.textContent = raw.includes(".") ? "0.0" : "0";
    });
  }

  function runCounters(root) {
    root.querySelectorAll("[data-count]").forEach(function (el, i) {
      if (el.dataset.done) return;
      const raw = el.dataset.count;
      if (!raw || isNaN(Number(raw))) {
        if (el.dataset.fallback) el.textContent = el.dataset.fallback;
        return;
      }
      el.dataset.done = "1";
      const target = parseFloat(raw);
      const isFloat = raw.includes(".");
      const fmt = isFloat
        ? function (v) { return v.toFixed(1); }
        : function (v) { return Math.round(v).toLocaleString(); };
      setTimeout(function () { countUp(el, target, 1400, fmt); }, i * 80);
    });
  }

  function resetBars(root) {
    root.querySelectorAll(".bar-chart__bar").forEach(function (bar) {
      delete bar.dataset.done;
      bar.style.height = "0";
    });
    root.querySelectorAll(".mini-bar__fill").forEach(function (fill) {
      delete fill.dataset.done;
      fill.style.width = "0";
    });
  }

  function animateBars(root) {
    root.querySelectorAll(".bar-chart__bar").forEach(function (bar, i) {
      if (bar.dataset.done) return;
      bar.dataset.done = "1";
      const h = parseFloat(bar.dataset.height) || 8;
      setTimeout(function () { bar.style.height = h + "%"; }, i * 70);
    });
    root.querySelectorAll(".mini-bar__fill").forEach(function (fill, i) {
      if (fill.dataset.done) return;
      fill.dataset.done = "1";
      const w = parseFloat(fill.dataset.width) || 0;
      setTimeout(function () { fill.style.width = w + "%"; }, 200 + i * 100);
    });
  }

  function animateDataSection(section) {
    if (!section || section.dataset.animated) return;
    section.dataset.animated = "1";
    resetCounters(section);
    resetBars(section);
    runCounters(section);
    animateBars(section);
  }

  const dataSectionObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting || e.intersectionRatio < animThreshold) return;
      animateDataSection(e.target);
      dataSectionObserver.unobserve(e.target);
    });
  }, { threshold: [0, animThreshold, 0.55], rootMargin: animRootMargin });

  ["numbers"].forEach(function (id) {
    const sec = document.getElementById(id);
    if (sec) dataSectionObserver.observe(sec);
  });

  /* Scroll reveal */
  const revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("is-visible");
      revealObserver.unobserve(e.target);
    });
  }, { threshold: isMobile ? 0.18 : 0.12, rootMargin: "0px 0px -8% 0px" });

  document.querySelectorAll(".reveal").forEach(function (el) {
    if (reduced) {
      el.classList.add("is-visible");
    } else {
      revealObserver.observe(el);
    }
  });

  /* Motion stages — staggered enter like FlareLane */
  function indexStageKids(stage) {
    const kids = stage.querySelectorAll(
      ":scope > .cap-tile, :scope > .process-col, :scope > .prog-demo, :scope > .scenario, :scope > .kakao-phone, :scope > article"
    );
    kids.forEach(function (el, i) {
      el.style.setProperty("--i", String(i));
    });
  }

  document.querySelectorAll(".motion-stage").forEach(indexStageKids);

  function activateStage(stage) {
    if (!stage || stage.classList.contains("is-on")) return;
    stage.classList.add("is-on");
    stage.querySelectorAll(".reveal").forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  function checkMotionStages() {
    document.querySelectorAll(".motion-stage:not(.is-on)").forEach(function (stage) {
      const rect = stage.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.9 && rect.bottom > 48) {
        activateStage(stage);
      }
    });
  }

  if (reduced) {
    document.querySelectorAll(".motion-stage").forEach(activateStage);
  } else {
    const stageObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        activateStage(e.target);
        stageObserver.unobserve(e.target);
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -4% 0px" });

    document.querySelectorAll(".motion-stage").forEach(function (stage) {
      stageObserver.observe(stage);
    });

    var stageScrollQueued = false;
    function onStageScroll() {
      if (stageScrollQueued) return;
      stageScrollQueued = true;
      requestAnimationFrame(function () {
        stageScrollQueued = false;
        checkMotionStages();
      });
    }
    window.addEventListener("scroll", onStageScroll, { passive: true });
    window.addEventListener("resize", onStageScroll, { passive: true });
    window.addEventListener("load", checkMotionStages);
    checkMotionStages();
  }

  if (reduced) {
    ["numbers"].forEach(function (id) {
      const sec = document.getElementById(id);
      if (sec) animateDataSection(sec);
    });
  }

  /* Hero: CSS grid + pointer spotlight only (no canvas / idle loop) */
  const hero = document.getElementById("intro");
  const heroInner = hero && hero.querySelector(".hero__inner");
  const canTrack =
    !reduced &&
    hero &&
    window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  if (canTrack) {
    let targetX = 0.5;
    let targetY = 0.42;
    let currentX = targetX;
    let currentY = targetY;
    let parallaxX = 0;
    let parallaxY = 0;
    let targetParallaxX = 0;
    let targetParallaxY = 0;
    let running = false;
    let heroVisible = true;
    let rafId = 0;

    function stopLoop() {
      running = false;
      if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = 0;
      }
    }

    function tick() {
      rafId = 0;
      if (!heroVisible || document.hidden) {
        running = false;
        return;
      }

      currentX += (targetX - currentX) * 0.16;
      currentY += (targetY - currentY) * 0.16;
      parallaxX += (targetParallaxX - parallaxX) * 0.14;
      parallaxY += (targetParallaxY - parallaxY) * 0.14;

      hero.style.setProperty("--mx", (currentX * 100).toFixed(1) + "%");
      hero.style.setProperty("--my", (currentY * 100).toFixed(1) + "%");
      if (heroInner) {
        heroInner.style.transform =
          "translate3d(" +
          parallaxX.toFixed(1) + "px, " +
          parallaxY.toFixed(1) + "px, 0)";
      }

      const moving =
        Math.abs(targetX - currentX) > 0.0015 ||
        Math.abs(targetY - currentY) > 0.0015 ||
        Math.abs(targetParallaxX - parallaxX) > 0.08 ||
        Math.abs(targetParallaxY - parallaxY) > 0.08;

      if (moving) {
        rafId = requestAnimationFrame(tick);
      } else {
        running = false;
        if (!hero.classList.contains("is-tracking") && heroInner) {
          heroInner.style.transform = "";
        }
      }
    }

    function startLoop() {
      if (running || !heroVisible || document.hidden) return;
      running = true;
      rafId = requestAnimationFrame(tick);
    }

    hero.addEventListener("pointerenter", function () {
      hero.classList.add("is-tracking");
      startLoop();
    });

    hero.addEventListener("pointerleave", function () {
      hero.classList.remove("is-tracking");
      targetX = 0.5;
      targetY = 0.42;
      targetParallaxX = 0;
      targetParallaxY = 0;
      startLoop();
    });

    hero.addEventListener("pointermove", function (e) {
      const rect = hero.getBoundingClientRect();
      const nx = (e.clientX - rect.left) / rect.width;
      const ny = (e.clientY - rect.top) / rect.height;
      targetX = Math.min(1, Math.max(0, nx));
      targetY = Math.min(1, Math.max(0, ny));
      targetParallaxX = (nx - 0.5) * 2.5;
      targetParallaxY = (ny - 0.5) * 1.8;
      startLoop();
    }, { passive: true });

    if ("IntersectionObserver" in window) {
      const heroIO = new IntersectionObserver(function (entries) {
        heroVisible = !!(entries[0] && entries[0].isIntersecting);
        if (!heroVisible) stopLoop();
      }, { threshold: 0.05 });
      heroIO.observe(hero);
    }

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stopLoop();
    });
  }
})();
