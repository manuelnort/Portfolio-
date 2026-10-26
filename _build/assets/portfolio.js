/* Portfolio additions that run after the theme's scripts (GSAP and ScrollTrigger come from the theme). */
(function () {
  "use strict";

  // "I build websites…" section: the UI design image starts small and grows to fill the frame as you scroll.
  // The section stays pinned while it grows; the theme's own text-fill animation runs on top of it.
  function revealImage() {
    var section = document.querySelector(".dn-reveal-section");
    var frame = section && section.querySelector(".dn-reveal__frame");
    var shade = section && section.querySelector(".dn-reveal__shade");
    if (!frame || !window.gsap || !window.ScrollTrigger) return;

    // Reduce Motion: show the image at full size, with no pinning or scaling
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      gsap.set(frame, { scale: 1 });
      gsap.set(shade, { opacity: 1 });
      return;
    }

    gsap.registerPlugin(ScrollTrigger);
    gsap.timeline({
      scrollTrigger: {
        trigger: section,
        start: "top top",
        end: "+=110%",
        scrub: 1,
        pin: true,
        anticipatePin: 1,
        refreshPriority: -1,   // measured after the theme's pinned panels above it
      },
    })
      .fromTo(frame, { scale: 0.24, borderRadius: "120px" }, { scale: 1, borderRadius: "40px", ease: "power2.inOut" }, 0)
      .fromTo(shade, { opacity: 0.6 }, { opacity: 1, ease: "none" }, 0);
  }

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Hero globe: land dots on a sphere that sways around Accra, a lit link to London, and a ring in orbit.
  // Draws one still frame under Reduce Motion, and pauses while the hero is off screen.
  function heroGlobe() {
    var wrap = document.querySelector(".dn-hero__globe");
    var canvas = wrap && wrap.querySelector("canvas");
    if (!canvas || !window.DN_GLOBE_LAND) return;
    var ctx = canvas.getContext("2d");
    var rad = Math.PI / 180;
    var land = window.DN_GLOBE_LAND.split(" ").map(function (p) {
      var ll = p.split(",");
      return toVec(ll[0] / 10, ll[1] / 10, 1);
    });
    var ACCRA = [-0.19, 5.6], LONDON = [-0.13, 51.5];
    var accra = toVec(ACCRA[0], ACCRA[1], 1), london = toVec(LONDON[0], LONDON[1], 1);
    var arc = [];
    for (var i = 0; i <= 60; i++) arc.push(slerp(accra, london, i / 60, 1 + 0.22 * Math.sin(Math.PI * i / 60)));
    var size = 0, dpr = 1, running = false, visible = true, start = performance.now(), pointerX = 0, pointerY = 0;

    function toVec(lon, lat, r) {
      return [r * Math.cos(lat * rad) * Math.sin(lon * rad), r * Math.sin(lat * rad), r * Math.cos(lat * rad) * Math.cos(lon * rad)];
    }
    function slerp(a, b, t, r) {
      var d = Math.acos(a[0] * b[0] + a[1] * b[1] + a[2] * b[2]), s = Math.sin(d);
      var wa = Math.sin((1 - t) * d) / s, wb = Math.sin(t * d) / s;
      return [r * (wa * a[0] + wb * b[0]), r * (wa * a[1] + wb * b[1]), r * (wa * a[2] + wb * b[2])];
    }
    // Rotate about the vertical axis (spin), then tip the north pole towards the viewer (tilt)
    function view(v, spin, tilt) {
      var cs = Math.cos(spin), ss = Math.sin(spin), ct = Math.cos(tilt), st = Math.sin(tilt);
      var x = v[0] * cs - v[2] * ss, z = v[0] * ss + v[2] * cs;
      return [x, v[1] * ct - z * st, v[1] * st + z * ct];
    }
    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      size = wrap.clientWidth;
      canvas.width = canvas.height = Math.round(size * dpr);
    }

    function frame(now) {
      // the first animation frame's timestamp can be a little earlier than start
      var t = Math.max(0, (now - start) / 1000);
      var spin =(reduceMotion ? 8 : 8 + 32 * Math.sin(t * 0.12) + pointerX * 10) * rad;
      var tilt = (18 + (reduceMotion ? 0 : pointerY * 6)) * rad;
      var c = size * dpr / 2, R = c * 0.7;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Atmosphere and the dark sphere
      var glow = ctx.createRadialGradient(c, c, R * 0.9, c, c, R * 1.35);
      glow.addColorStop(0, "rgba(248,112,96,0.22)");
      glow.addColorStop(1, "rgba(248,112,96,0)");
      ctx.fillStyle = glow;
      ctx.beginPath(); ctx.arc(c, c, R * 1.35, 0, Math.PI * 2); ctx.fill();
      var body = ctx.createRadialGradient(c - R * 0.35, c - R * 0.4, R * 0.1, c, c, R);
      body.addColorStop(0, "#1b1d24");
      body.addColorStop(1, "#08090c");
      ctx.fillStyle = body;
      ctx.beginPath(); ctx.arc(c, c, R, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = "rgba(255,255,255,0.12)";
      ctx.lineWidth = dpr;
      ctx.stroke();

      // Orbit ring, behind half first
      drawOrbit(t, spin, c, R, false);

      // Land dots: bright on the near side, a faint trace of the far side
      for (var i = 0; i < land.length; i++) {
        var p = view(land[i], spin, tilt);
        var x = c + p[0] * R, y = c - p[1] * R;
        if (p[2] > 0) {
          ctx.fillStyle = "rgba(255,255,255," + (0.25 + 0.65 * p[2]).toFixed(3) + ")";
          var s = (0.9 + 0.8 * p[2]) * dpr;
          ctx.fillRect(x - s / 2, y - s / 2, s, s);
        } else if (p[2] > -0.6) {
          ctx.fillStyle = "rgba(255,255,255,0.05)";
          ctx.fillRect(x - 0.5 * dpr, y - 0.5 * dpr, dpr, dpr);
        }
      }

      // Accra to London: the arc, then a light travelling along it
      ctx.lineWidth = 1.5 * dpr;
      ctx.strokeStyle = "rgba(248,112,96,0.75)";
      ctx.beginPath();
      var drawn = false;
      for (var k = 0; k < arc.length; k++) {
        var q = view(arc[k], spin, tilt);
        if (q[2] < 0 && Math.hypot(q[0], q[1]) < 1) { drawn = false; continue; }
        if (drawn) ctx.lineTo(c + q[0] * R, c - q[1] * R); else ctx.moveTo(c + q[0] * R, c - q[1] * R);
        drawn = true;
      }
      ctx.stroke();
      if (!reduceMotion) {
        var head = arc[Math.floor(((t * 0.45) % 1) * (arc.length - 1))];
        var h = view(head, spin, tilt);
        if (h[2] > 0 || Math.hypot(h[0], h[1]) >= 1) dot(c + h[0] * R, c - h[1] * R, 3.2 * dpr, "#fff", 14 * dpr);
      }

      // Places
      place(accra, "Accra", true, t, spin, tilt, c, R);
      place(london, "London", false, t, spin, tilt, c, R);

      drawOrbit(t, spin, c, R, true);
    }

    function dot(x, y, r, color, blur) {
      ctx.save();
      ctx.shadowColor = color; ctx.shadowBlur = blur;
      ctx.fillStyle = color;
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    }
    function place(v, label, home, t, spin, tilt, c, R) {
      var p = view(v, spin, tilt);
      if (p[2] <= 0) return;
      var x = c + p[0] * R, y = c - p[1] * R;
      if (home && !reduceMotion) {   // pulse ring
        var k = (t * 0.6) % 1;
        ctx.strokeStyle = "rgba(248,112,96," + (1 - k).toFixed(3) + ")";
        ctx.lineWidth = 1.5 * dpr;
        ctx.beginPath(); ctx.arc(x, y, (4 + 22 * k) * dpr, 0, Math.PI * 2); ctx.stroke();
      }
      dot(x, y, (home ? 4.5 : 3) * dpr, home ? "#f87060" : "#fff", (home ? 18 : 8) * dpr);
      ctx.font = "500 " + 11 * dpr + "px 'Roboto Flex', sans-serif";
      ctx.fillStyle = "rgba(255,255,255,0.9)";
      ctx.fillText(label.toUpperCase(), x + 10 * dpr, y - 8 * dpr);
    }
    // A tilted ring around the globe with a small satellite; the half behind the globe is drawn first
    function drawOrbit(t, spin, c, R, front) {
      var ringTilt = 72 * rad, ringTurn = -24 * rad, r = 1.22, steps = 120;
      ctx.lineWidth = dpr;
      ctx.strokeStyle = "rgba(255,255,255," + (front ? 0.22 : 0.08) + ")";
      ctx.setLineDash([2 * dpr, 6 * dpr]);
      ctx.beginPath();
      var pen = false;
      for (var i = 0; i <= steps; i++) {
        var a = i / steps * Math.PI * 2;
        var o = orbitPoint(a, r, ringTilt, ringTurn);
        if ((o[2] > 0) !== front) { pen = false; continue; }
        if (pen) ctx.lineTo(c + o[0] * R, c - o[1] * R); else ctx.moveTo(c + o[0] * R, c - o[1] * R);
        pen = true;
      }
      ctx.stroke();
      ctx.setLineDash([]);
      var sat = orbitPoint(reduceMotion ? 0.6 : t * 0.35, r, ringTilt, ringTurn);
      if ((sat[2] > 0) === front) dot(c + sat[0] * R, c - sat[1] * R, 2.6 * dpr, front ? "#00c5fe" : "rgba(0,197,254,0.35)", 10 * dpr);
    }
    function orbitPoint(a, r, ringTilt, ringTurn) {
      var x = r * Math.cos(a), z = r * Math.sin(a);
      var y = z * Math.cos(ringTilt), zz = z * Math.sin(ringTilt);
      return [x * Math.cos(ringTurn) - y * Math.sin(ringTurn), x * Math.sin(ringTurn) + y * Math.cos(ringTurn), zz];
    }

    function loop(now) {
      if (!running) return;
      frame(now);
      requestAnimationFrame(loop);
    }
    function play() {
      if (running || reduceMotion || !visible || document.hidden) return;
      running = true;
      requestAnimationFrame(loop);
    }
    resize();
    frame(performance.now());
    window.addEventListener("resize", function () { resize(); frame(performance.now()); });
    if (reduceMotion) return;
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible) play(); else running = false;
    }).observe(wrap);
    document.addEventListener("visibilitychange", function () { if (document.hidden) running = false; else play(); });
    window.addEventListener("pointermove", function (e) {
      pointerX = e.clientX / window.innerWidth - 0.5;
      pointerY = e.clientY / window.innerHeight - 0.5;
    }, { passive: true });
    play();
  }

  // Hero tagline decodes from random glyphs into the words, one line after the other
  function decodeTagline() {
    var lines = document.querySelectorAll(".dn-hero [data-scramble]");
    if (reduceMotion) return;
    var glyphs = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789/<>{}#*+=";
    Array.prototype.forEach.call(lines, function (el, n) {
      var text = el.textContent, startAt = performance.now() + 250 + n * 420, length = 900;
      el.style.minWidth = el.offsetWidth + "px";
      function step(now) {
        var progress = Math.max(0, (now - startAt) / length), out = "";
        for (var i = 0; i < text.length; i++) {
          if (text[i] === " " || i < progress * text.length) out += text[i];
          else out += glyphs[Math.floor(Math.random() * glyphs.length)];
        }
        el.textContent = out;
        if (progress < 1) requestAnimationFrame(step); else el.textContent = text;
      }
      requestAnimationFrame(step);
    });
  }

  // Accra time in the hero readout and the footer
  function accraClock() {
    var clocks = document.querySelectorAll("[data-clock]");
    if (!clocks.length) return;
    var format = new Intl.DateTimeFormat("en-GB", { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false, timeZone: "Africa/Accra" });
    function tick() {
      var now = format.format(new Date());
      Array.prototype.forEach.call(clocks, function (el) { el.textContent = now; });
    }
    tick();
    setInterval(tick, 1000);
  }

  // Glides the page to an element (or the top). The browser's own smooth scroll stops early when the pinned
  // sections re-measure on the way, so this moves the page itself, rechecking the target every frame.
  // Scrolling by hand stops it.
  function glideTo(target) {
    var where = function () { return target ? target.getBoundingClientRect().top + window.pageYOffset : 0; };
    if (reduceMotion) { window.scrollTo(0, where()); return; }
    var from = window.pageYOffset, t0 = performance.now();
    var time = Math.min(1600, Math.max(600, Math.abs(where() - from) / 8));
    var stopped = false, stop = function () { stopped = true; };
    window.addEventListener("wheel", stop, { once: true, passive: true });
    window.addEventListener("touchstart", stop, { once: true, passive: true });
    (function step(now) {
      if (stopped) return;
      var k = Math.min(1, (now - t0) / time), eased = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
      window.scrollTo(0, from + (where() - from) * eased);
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }

  // Footer: back to the top of the page
  function backToTop() {
    var link = document.querySelector(".dn-foot__top-link");
    if (!link) return;
    link.addEventListener("click", function (e) {
      e.preventDefault();
      glideTo(null);
    });
  }

  // Testimonials: thumbnails switch the photo and quote; they also advance on their own every 7 seconds
  // until someone interacts (never under Reduce Motion)
  function testimonials() {
    var root = document.querySelector(".dn-testi");
    if (!root) return;
    var parts = root.querySelectorAll(".dn-testi__photo, .dn-testi__quote, .dn-testi__thumb");
    var count = root.querySelectorAll(".dn-testi__thumb").length, current = 0, timer = null;
    function show(index) {
      current = (index + count) % count;
      Array.prototype.forEach.call(parts, function (el) {
        var on = +el.getAttribute("data-index") === current;
        el.classList.toggle("is-active", on);
        if (el.tagName === "BUTTON") el.setAttribute("aria-pressed", on ? "true" : "false");
      });
    }
    function stop() { clearInterval(timer); timer = null; }
    root.addEventListener("click", function (e) {
      var thumb = e.target.closest(".dn-testi__thumb");
      if (!thumb) return;
      stop();
      show(+thumb.getAttribute("data-index"));
    });
    if (!reduceMotion && count > 1) {
      timer = setInterval(function () { show(current + 1); }, 7000);
      root.addEventListener("pointerenter", stop);
      root.addEventListener("focusin", stop);
    }
  }

  // Contact form: no server on this site, so it opens the visitor's email app with the message filled in
  function contactForm() {
    var form = document.querySelector(".dn-form");
    if (!form) return;
    var note = form.querySelector(".dn-form__note"), defaultNote = note.textContent;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      Array.prototype.forEach.call(form.querySelectorAll("input, select, textarea"), function (field) {
        var bad = !field.checkValidity();
        field.closest(".dn-field").classList.toggle("is-invalid", bad);
        if (bad && !firstBad) firstBad = field;
      });
      if (firstBad) {
        note.textContent = firstBad.type === "email" && firstBad.value ? "Check your email address." : "Fill in your name, email, service and message.";
        note.classList.add("is-error");
        firstBad.focus();
        return;
      }
      note.textContent = defaultNote;
      note.classList.remove("is-error");
      var v = function (name) { return form.elements[name].value.trim(); };
      var body = "Name: " + v("name") + "\nEmail: " + v("email") + "\nService: " + v("service") +
        "\nBudget: " + (v("budget") || "Not given") + "\n\n" + v("message");
      window.location.href = "mailto:" + form.getAttribute("data-email") +
        "?subject=" + encodeURIComponent("New project: " + v("service") + " for " + v("name")) +
        "&body=" + encodeURIComponent(body);
    });
    form.addEventListener("input", function (e) {
      var field = e.target.closest(".dn-field");
      if (field && e.target.checkValidity()) field.classList.remove("is-invalid");
    });
  }

  // Client wall: a field of dots rolling like a wave behind the cards (one still frame under Reduce Motion,
  // paused off screen), and cards drifting at their own speeds as the section scrolls past
  function clientWall() {
    var section = document.querySelector(".dn-voices");
    var canvas = section && section.querySelector(".dn-voices__wave");
    if (!canvas) return;
    var ctx = canvas.getContext("2d"), w = 0, h = 0, dpr = 1, running = false, start = performance.now();
    var COLS = 170, ROWS = 56;
    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = section.clientWidth; h = section.clientHeight;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    }
    function frame(now) {
      var t = (now - start) / 1000;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#fff";
      for (var r = 0; r < ROWS; r++) {
        var depth = r / (ROWS - 1);                   // 0 far, 1 near
        var scale = 0.35 + depth * 0.9;
        for (var c = 0; c < COLS; c++) {
          var u = c / (COLS - 1);
          // a ribbon rising from bottom left to top right, rolling over time
          var lift = Math.sin(u * 5.2 + t * 0.6 + depth * 2.4) * 0.09 + Math.cos(u * 2.1 - t * 0.35 + depth * 3.1) * 0.06;
          var x = (u - 0.5) * w * scale * 1.5 + w / 2;
          var y = h * (0.78 - u * 0.48) + (depth - 0.5) * h * 0.3 + lift * h;
          if (x < -10 || x > w + 10 || y < -10 || y > h + 10) continue;
          ctx.globalAlpha = (0.16 + 0.6 * depth) * (0.35 + 0.65 * Math.sin(u * Math.PI));
          var s = (0.6 + depth * 1.2) * dpr;
          ctx.fillRect(x * dpr, y * dpr, s, s);
        }
      }
      ctx.globalAlpha = 1;
    }
    function loop(now) { if (!running) return; frame(now); requestAnimationFrame(loop); }
    resize();
    frame(performance.now());
    window.addEventListener("resize", function () { resize(); frame(performance.now()); });
    if (reduceMotion) return;
    new IntersectionObserver(function (entries) {
      running = entries[0].isIntersecting && !document.hidden;
      if (running) { resize(); requestAnimationFrame(loop); }
    }).observe(section);

    if (!window.gsap || !window.ScrollTrigger || window.matchMedia("(max-width: 1100px)").matches) return;
    gsap.registerPlugin(ScrollTrigger);
    Array.prototype.forEach.call(section.querySelectorAll(".dn-voice"), function (card) {
      var speed = parseFloat(card.getAttribute("data-speed")) || 0;
      gsap.fromTo(card, { y: -120 * speed }, { y: 120 * speed, ease: "none",
        scrollTrigger: { trigger: section, start: "top bottom", end: "bottom top", scrub: true } });
    });
  }

  // Site grid: the fixed layer moves up with the page by the scroll offset within one box,
  // so the boxes look painted on the page while the layer itself never leaves the screen.
  // It's at full strength over the hero and fades to a trace as the hero scrolls away.
  function siteGrid() {
    var grid = document.querySelector(".dn-grid");
    var layer = grid && grid.querySelector("i");
    if (!layer) return;
    var hero = document.querySelector(".dn-hero");
    var BODY = 0.3, queued = false;
    // The backdrop's two lights wander as you read: the coral one starts behind the globe, crosses to the
    // left halfway down the page and ends on the right; the cyan one rises from the bottom left.
    var warm = document.querySelector(".dn-backdrop__glow--warm");
    var cool = document.querySelector(".dn-backdrop__glow--cool");
    function place() {
      queued = false;
      var y = window.pageYOffset, box = window.innerWidth < 768 ? 48 : 64;
      layer.style.setProperty("--dn-grid-y", -(y % box) + "px");
      var past = hero ? Math.min(1, Math.max(0, y / (hero.offsetHeight * 0.8))) : 1;
      grid.style.opacity = (1 - (1 - BODY) * past).toFixed(3);
      if (!warm || reduceMotion) return;
      var room = document.documentElement.scrollHeight - window.innerHeight;
      var p = room > 0 ? Math.min(1, y / room) : 0, arc = Math.sin(p * Math.PI);
      warm.style.transform = "translate3d(" + (72 - 54 * arc + 8 * p).toFixed(2) + "vw," + (45 + 15 * arc - 5 * p).toFixed(2) + "vh,0)";
      cool.style.transform = "translate3d(" + (10 + 70 * p).toFixed(2) + "vw," + (92 - 50 * arc).toFixed(2) + "vh,0)";
    }
    window.addEventListener("scroll", function () {
      if (!queued) { queued = true; requestAnimationFrame(place); }
    }, { passive: true });
    window.addEventListener("resize", place);
    place();
  }

  // Chapter 1 counts run up from zero the first time they come into view
  function countUp() {
    var nums = document.querySelectorAll(".dn-counts [data-count]");
    if (!nums.length || reduceMotion || !("IntersectionObserver" in window)) return;
    Array.prototype.forEach.call(nums, function (el) { el.textContent = "0"; });
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        seen.unobserve(entry.target);
        var el = entry.target, end = +el.getAttribute("data-count"), t0 = performance.now();
        (function step(now) {
          var k = Math.min(1, (now - t0) / 1400), eased = 1 - Math.pow(1 - k, 3);
          el.textContent = Math.round(end * eased);
          if (k < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, { threshold: 0.6 });
    Array.prototype.forEach.call(nums, function (el) { seen.observe(el); });
  }

  // Chapter 3 steps: each step's top line draws in as the step comes into view
  function stepsInView() {
    var steps = document.querySelectorAll(".dn-steps__step");
    if (!steps.length || !("IntersectionObserver" in window)) return;
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        seen.unobserve(entry.target);
        var i = Array.prototype.indexOf.call(steps, entry.target);
        setTimeout(function () { entry.target.classList.add("is-seen"); }, reduceMotion ? 0 : i * 180);
      });
    }, { threshold: 0.5 });
    Array.prototype.forEach.call(steps, function (el) { seen.observe(el); });
  }

  // Chapter guide: marks the chapter in view, and its links (and the hero's) glide to their chapter
  function chapterGuide() {
    var links = document.querySelectorAll(".dn-rail a");
    var jumpers = document.querySelectorAll('.dn-rail a, .dn-hero a[href^="#"]');
    Array.prototype.forEach.call(jumpers, function (a) {
      a.addEventListener("click", function (e) {
        var target = document.querySelector(a.getAttribute("href"));
        if (!target) return;
        e.preventDefault();
        glideTo(target);
      });
    });
    if (!links.length || !("IntersectionObserver" in window)) return;
    var byId = {};
    Array.prototype.forEach.call(links, function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var watch = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        Array.prototype.forEach.call(links, function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
        var a = byId[entry.target.id];
        if (a) { a.classList.add("is-active"); a.setAttribute("aria-current", "true"); }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(byId).forEach(function (id) {
      var section = document.getElementById(id);
      if (section) watch.observe(section);
    });
  }

  // Floating menu: hidden at the top of the page, shown once you've scrolled a little way down
  function floatingMenu() {
    var menu = document.querySelector(".dn-dock");
    if (!menu) return;
    var queued = false;
    function update() {
      queued = false;
      var shown = window.pageYOffset > 140;
      menu.classList.toggle("is-shown", shown);
      menu.toggleAttribute("inert", !shown);   // not reachable by keyboard while it's hidden
    }
    window.addEventListener("scroll", function () {
      if (!queued) { queued = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  siteGrid();
  floatingMenu();
  countUp();
  stepsInView();
  chapterGuide();
  decodeTagline();
  accraClock();
  backToTop();
  testimonials();
  contactForm();
  // Pinned sections measure where they sit when they're set up; fonts, images and the chapters above can still
  // move things after that, so measure again once everything has settled
  function settle() {
    if (!window.ScrollTrigger) return;
    var again = function () { ScrollTrigger.sort(); ScrollTrigger.refresh(); };
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(again);
    setTimeout(again, 600);
    // The theme sets up some pinned panels only when you first scroll near them, which makes the page taller
    // later on; whenever the page height changes, measure again
    if (!("ResizeObserver" in window)) return;
    var lastHeight = document.body.scrollHeight, timer = null;
    new ResizeObserver(function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        var height = document.body.scrollHeight;
        if (Math.abs(height - lastHeight) < 2) return;
        lastHeight = height;
        again();
        lastHeight = document.body.scrollHeight;
      }, 150);
    }).observe(document.body);
  }

  function start() { revealImage(); heroGlobe(); clientWall(); settle(); }
  if (document.readyState === "complete") start();
  else window.addEventListener("load", start);
})();
