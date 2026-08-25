/* Nature Nudge — progressive enhancement only.
   Everything here is decorative; the page is fully usable without it. */

(function () {
    "use strict";

    // Hairline under the sticky header once the page has scrolled.
    var header = document.getElementById("siteHeader");
    if (header) {
        var setStuck = function () {
            header.classList.toggle("is-stuck", window.scrollY > 8);
        };
        setStuck();
        window.addEventListener("scroll", setStuck, { passive: true });
    }

    // Reveal-on-scroll. Skipped entirely when the visitor prefers reduced motion
    // or when IntersectionObserver is unavailable.
    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var items = document.querySelectorAll(".reveal");

    if (reduced || !("IntersectionObserver" in window)) {
        items.forEach(function (el) { el.classList.add("is-visible"); });
        return;
    }

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
        });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });

    items.forEach(function (el) { observer.observe(el); });
}());
