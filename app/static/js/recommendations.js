/**
 * BookWise Atelier — Explainable Recommendations Interactive Breakdowns
 */

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.toggle-breakdown-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const targetId = this.getAttribute('data-target');
      const breakdownEl = document.getElementById(targetId);
      if (breakdownEl) {
        const isHidden = breakdownEl.style.display === 'none' || !breakdownEl.style.display;
        breakdownEl.style.display = isHidden ? 'block' : 'none';
        this.textContent = isHidden ? 'Hide Detailed Scoring ▲' : 'Why this book? (Score Breakdown) ▼';
      }
    });
  });
});
