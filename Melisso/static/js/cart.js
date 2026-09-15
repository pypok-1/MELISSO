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

  function updateSummary(data) {
    const subEl  = document.getElementById("summary-subtotal");
    const shipEl = document.getElementById("summary-shipping");
    const totEl  = document.getElementById("summary-total");

    if (subEl)  subEl.textContent  = "€" + data.subtotal.toFixed(2);
    if (shipEl) shipEl.textContent = data.shipping === 0 ? "Free" : "€" + data.shipping.toFixed(2);
    if (totEl)  totEl.textContent  = "€" + data.total.toFixed(2);

    const badge = document.querySelector("header .bg-secondary");
    if (badge) {
      if (data.cart_count > 0) badge.textContent = data.cart_count;
      else badge.remove();
    }
  }

  function initCartItems() {
    document.querySelectorAll(".cart-item").forEach(itemEl => {
      const pid   = itemEl.dataset.productId;
      const qtyEl = itemEl.querySelector(".qty-value");
      if (!pid || !qtyEl) return;

      itemEl.querySelectorAll("[data-action]").forEach(btn => {
        btn.addEventListener("click", async () => {
          const action = btn.dataset.action;
          let qty = parseInt(qtyEl.textContent, 10);

          if (action === "increase") qty += 1;
          if (action === "decrease") qty = Math.max(0, qty - 1);
          if (action === "remove")   qty = 0;

          const data = await postJSON("/api/cart/update", { product_id: pid, qty });
          if (!data.ok) return;

          if (qty === 0) {
            itemEl.style.transition = "opacity .2s";
            itemEl.style.opacity = "0";
            setTimeout(() => itemEl.remove(), 200);
          } else {
            qtyEl.textContent = qty;
          }
          updateSummary(data);
        });
      });
    });
  }

  function initAddToCart() {
    document.querySelectorAll(".add-to-cart").forEach(btn => {
      btn.addEventListener("click", async () => {
        const pid = btn.dataset.productId;
        if (!pid) return;

        const data = await postJSON("/api/cart/add", { product_id: pid, qty: 1 });
        if (!data.ok) return;

        btn.textContent = "✓ Added";
        setTimeout(() => { btn.textContent = "+ Add"; }, 1200);

        const badge = document.querySelector("header .bg-secondary");
        if (badge) badge.textContent = data.cart_count;
        else location.reload();
      });
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initCartItems();
    initAddToCart();
  });
})();