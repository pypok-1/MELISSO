(function () {
  "use strict";

  async function postJSON(url, payload) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return res.json();
  }

  function initAddToCart() {
    document.querySelectorAll(".add-to-cart").forEach(btn => {
      btn.addEventListener("click", async () => {
        const pid = btn.dataset.productId;
        if (!pid) return;

        try {
          const data = await postJSON("/api/cart/add", { product_id: pid, qty: 1 });
          if (!data.ok) {
            console.error("Add to cart error:", data);
            return;
          }

          const cartLink = document.querySelector('header a[href="/cart"]');
          if (cartLink) {
            let badge = cartLink.querySelector(".cart-badge");
            if (!badge) {
              badge = document.createElement("span");
              badge.className = "cart-badge absolute -top-1 -right-1 w-4 h-4 rounded-full bg-secondary text-on-secondary font-label-sm text-[9px] flex items-center justify-center leading-none";
              cartLink.appendChild(badge);
            }
            badge.textContent = data.cart_count;
          }

          const label = btn.querySelector(".btn-label");
          const icon  = btn.querySelector(".material-symbols-outlined");
          const original = label ? label.textContent : "ADD TO CART";

          if (label) label.textContent = "ADDED ✓";
          if (icon)  icon.textContent  = "check";
          btn.classList.add("bg-primary", "text-on-primary");
          btn.disabled = true;

          setTimeout(() => {
            if (label) label.textContent = original;
            if (icon)  icon.textContent  = "shopping_bag";
            btn.classList.remove("bg-primary", "text-on-primary");
            btn.disabled = false;
          }, 1400);

        } catch (err) {
          console.error("Network error:", err);
        }
      });
    });
  }

  function initTerroirReveal() {
    const terroirSection = document.getElementById("terroir");
    if (!terroirSection) return;

    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            terroirSection.classList.add("terroir-revealed");
            obs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.2 });
      observer.observe(terroirSection);
    } else {
      terroirSection.classList.add("terroir-revealed");
    }
  }

  const QUIZ_DATA = {
    morning: {
      icon: "local_cafe",
      tag: "Morning Ritual & Coffee",
      title: "White Thistle & Orange Blossom (Fleur d'Oranger)",
      desc: "Silky cream texture. Melts effortlessly into specialty filter coffee, matcha latte, or drizzled over fresh brioche."
    },
    cheese: {
      icon: "dinner_dining",
      tag: "Cheese Board & Wine",
      title: "Wild Thyme & Pine (Cretan Thyme & Pine)",
      desc: "Resinous, full-bodied with notes of rosemary and malotira. An impeccable pairing for aged Graviera, Manchego, and dry orange wine."
    },
    gift: {
      icon: "featured_seasonal_and_gifts",
      tag: "Gift for a Connoisseur",
      title: "Artisan Honeycomb Duo Box",
      desc: "Architectural raw honeycombs in a luxury artisanal wooden box from Cretan timber. The ultimate prestigious gourmet gesture."
    },
    wellness: {
      icon: "health_and_safety",
      tag: "Immunity & Clean Bio-Boost",
      title: "Wild Thyme Raw Reserve (98% Thyme Pollen)",
      desc: "Peak diastase rating (34.2 DN) with high antioxidant density from the wild mountain herbs of Samaria. Take 1 spoonful every morning."
    }
  };

  function initQuiz() {
    const quizButtons = document.querySelectorAll(".quiz-btn");
    const resultIcon  = document.getElementById("result-icon");
    const resultTag   = document.getElementById("result-tag");
    const resultTitle = document.getElementById("result-title");
    const resultDesc  = document.getElementById("result-desc");

    if (!quizButtons.length || !resultIcon) return;

    quizButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        quizButtons.forEach(b => {
          b.classList.remove("bg-inverse-surface", "text-inverse-on-surface");
          b.classList.add("bg-surface-container", "text-on-surface-variant");
        });
        btn.classList.remove("bg-surface-container", "text-on-surface-variant");
        btn.classList.add("bg-inverse-surface", "text-inverse-on-surface");

        const data = QUIZ_DATA[btn.getAttribute("data-match")];
        if (data) {
          resultIcon.textContent  = data.icon;
          resultTag.textContent   = data.tag;
          resultTitle.textContent = data.title;
          resultDesc.textContent  = data.desc;
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initAddToCart();
    initTerroirReveal();
    initQuiz();
  });
})();