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

  /* Step tabs */
  const capSection = document.getElementById("capabilities");
  const tabBtns = document.querySelectorAll(".step-nav__btn");
  const panels = document.querySelectorAll(".cap-panel");
  let capIndex = 0;
  let capAutoTimer = null;
  let capPaused = false;
  let capSectionVisible = false;

  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

  function countUp(el, target, duration, formatter) {
    const fallback = el.dataset.fallback;
    if (reduced) {
      el.textContent = fallback || formatter(target);
      return;
    }
    const start = performance.now();
    function frame(now) {
      const p = Math.min((now - start) / duration, 1);
      if (p >= 1) {
        el.textContent = fallback || formatter(target);
        return;
      }
      el.textContent = formatter(target * easeOut(p));
      requestAnimationFrame(frame);
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

  function resetCapVisual(panel) {
    if (!panel) return;
    panel.querySelectorAll(".rank-chart__bar").forEach(function (bar) {
      bar.style.height = "0";
    });
    panel.querySelectorAll(".sentiment-fill").forEach(function (fill) {
      fill.style.width = "0";
    });
    const ring = panel.querySelector(".donut-gauge__ring");
    if (ring) {
      ring.style.background = "conic-gradient(var(--gray-200) 0deg, var(--gray-200) 360deg)";
    }
    const spark = panel.querySelector(".spark-line__path");
    if (spark) spark.style.strokeDashoffset = "300";
  }

  function animateCapVisual(panel) {
    if (!panel) return;

    panel.querySelectorAll(".rank-chart__bar").forEach(function (bar, i) {
      const h = bar.dataset.h || "50";
      bar.style.height = "0";
      setTimeout(function () { bar.style.height = h + "%"; }, reduced ? 0 : 80 + i * 90);
    });

    const ring = panel.querySelector(".donut-gauge__ring");
    if (ring) {
      const val = parseFloat(ring.dataset.value) || 90;
      const deg = (val / 100) * 360;
      if (reduced) {
        ring.style.background = "conic-gradient(var(--orange) " + deg + "deg, var(--gray-200) " + deg + "deg)";
      } else {
        ring.style.background = "conic-gradient(var(--gray-200) 0deg, var(--gray-200) 360deg)";
        setTimeout(function () {
          ring.style.background = "conic-gradient(var(--orange) " + deg + "deg, var(--gray-200) " + deg + "deg)";
        }, 120);
      }
    }

    panel.querySelectorAll(".sentiment-fill").forEach(function (fill, i) {
      const w = fill.dataset.w || "0";
      fill.style.width = "0";
      setTimeout(function () { fill.style.width = w + "%"; }, reduced ? 0 : 100 + i * 100);
    });

    const spark = panel.querySelector(".spark-line__path");
    if (spark && !reduced) {
      spark.style.strokeDashoffset = "300";
      setTimeout(function () { spark.style.strokeDashoffset = "0"; }, 200);
    }
  }

  function playCapPanel(panel) {
    if (!panel) return;
    resetCounters(panel);
    resetCapVisual(panel);
    animateCapVisual(panel);
    runCounters(panel);
  }

  function activateCapTab(id) {
    tabBtns.forEach(function (b) {
      const active = b.dataset.tab === id;
      b.classList.toggle("is-active", active);
      b.setAttribute("aria-selected", active ? "true" : "false");
      if (active) {
        b.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      }
    });
    panels.forEach(function (p) {
      const active = p.id === "panel-" + id;
      p.classList.toggle("is-active", active);
      if (active && capSectionVisible) playCapPanel(p);
    });
    capIndex = Array.from(tabBtns).findIndex(function (b) { return b.dataset.tab === id; });
    if (capIndex < 0) capIndex = 0;
  }

  function stopCapAutoRotate() {
    if (capAutoTimer) {
      clearInterval(capAutoTimer);
      capAutoTimer = null;
    }
  }

  function startCapAutoRotate() {
    if (reduced || capPaused || !capSectionVisible || tabBtns.length <= 1) return;
    stopCapAutoRotate();
    capAutoTimer = setInterval(function () {
      if (capPaused || !capSectionVisible) return;
      capIndex = (capIndex + 1) % tabBtns.length;
      activateCapTab(tabBtns[capIndex].dataset.tab);
    }, 3500);
  }

  tabBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      activateCapTab(btn.dataset.tab);
      stopCapAutoRotate();
      startCapAutoRotate();
    });
  });

  if (capSection) {
    capSection.addEventListener("mouseenter", function () { capPaused = true; });
    capSection.addEventListener("mouseleave", function () {
      capPaused = false;
      startCapAutoRotate();
    });
    capSection.addEventListener("focusin", function () { capPaused = true; });
    capSection.addEventListener("focusout", function (e) {
      if (!capSection.contains(e.relatedTarget)) {
        capPaused = false;
        startCapAutoRotate();
      }
    });

    const capObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        const visible = e.isIntersecting && e.intersectionRatio >= animThreshold;
        if (visible) {
          if (!capSectionVisible) {
            capSectionVisible = true;
            if (!capSection.dataset.animated) {
              capSection.dataset.animated = "1";
              playCapPanel(document.querySelector(".cap-panel.is-active"));
            }
            startCapAutoRotate();
          }
        } else if (capSectionVisible) {
          capSectionVisible = false;
          stopCapAutoRotate();
        }
      });
    }, { threshold: [0, 0.15, animThreshold, 0.5], rootMargin: animRootMargin });
    capObs.observe(capSection);
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

  ["numbers", "cases", "kmong"].forEach(function (id) {
    const sec = document.getElementById(id);
    if (sec) dataSectionObserver.observe(sec);
  });

  /* Scroll reveal — opacity only, no counter trigger */
  const revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("is-visible");
      revealObserver.unobserve(e.target);
    });
  }, { threshold: isMobile ? 0.2 : 0.12, rootMargin: "0px 0px -5% 0px" });

  document.querySelectorAll(".reveal").forEach(function (el) {
    if (reduced) {
      el.classList.add("is-visible");
    } else {
      revealObserver.observe(el);
    }
  });

  if (reduced) {
    ["numbers", "cases", "kmong"].forEach(function (id) {
      const sec = document.getElementById(id);
      if (sec) animateDataSection(sec);
    });
    if (capSection) {
      capSectionVisible = true;
      playCapPanel(document.querySelector(".cap-panel.is-active"));
    }
  }
})();
