/**
 * BookWise Atelier — Core Application Script
 * Theme toggle, modal controls, and global utilities.
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initModals();
  initImageFallbacks();
  initAutoDismissAlerts();
});

// Theme Management
function initTheme() {
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const storedTheme = localStorage.getItem('bookwise-theme') || 'light';
  
  // Set initial theme
  document.documentElement.setAttribute('data-theme', storedTheme);
  updateThemeIcon(storedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const target = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', target);
      localStorage.setItem('bookwise-theme', target);
      updateThemeIcon(target);
    });
  }
}

function updateThemeIcon(theme) {
  const icon = document.getElementById('theme-icon');
  if (icon) {
    if (theme === 'dark') {
      icon.innerHTML = '☀️';
      icon.setAttribute('title', 'Switch to Ivory Light mode');
    } else {
      icon.innerHTML = '🌙';
      icon.setAttribute('title', 'Switch to Midnight Dark mode');
    }
  }
}

// Modal Helpers
function initModals() {
  // Close modals on clicking backdrop or close button
  document.querySelectorAll('.atelier-modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) {
        backdrop.classList.remove('active');
      }
    });
  });

  document.querySelectorAll('[data-modal-close]').forEach(btn => {
    btn.addEventListener('click', () => {
      const modal = btn.closest('.atelier-modal-backdrop');
      if (modal) modal.classList.remove('active');
    });
  });
}

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
  }
}

// Broken Image / Remote Cover Fallbacks
function initImageFallbacks() {
  document.querySelectorAll('img.book-cover-img').forEach(img => {
    img.addEventListener('error', function() {
      const fallback = this.getAttribute('data-fallback');
      if (fallback && this.src !== fallback) {
        this.src = fallback;
      }
    });
  });
}

// Auto-dismiss Flash Alerts
function initAutoDismissAlerts() {
  document.querySelectorAll('.alert-atelier').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 400ms ease, transform 400ms ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-6px)';
      setTimeout(() => alert.remove(), 400);
    }, 4500);
  });
}
