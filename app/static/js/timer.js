/**
 * BookWise Atelier — Reading Timer & Stopwatch Module
 */

let timerInterval = null;
let secondsElapsed = 0;
let isRunning = false;
let sessionToken = null;

function generateUUID() {
  return 'sess-' + Math.random().toString(36).substring(2, 9) + '-' + Date.now();
}

function updateDisplay() {
  const display = document.getElementById('timer-time');
  if (!display) return;

  const hrs = Math.floor(secondsElapsed / 3600);
  const mins = Math.floor((secondsElapsed % 3600) / 60);
  const secs = secondsElapsed % 60;

  if (hrs > 0) {
    display.textContent = `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  } else {
    display.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }

  // Update hidden form input
  const durationInput = document.getElementById('duration-seconds-input');
  if (durationInput) durationInput.value = secondsElapsed;
}

function startTimer() {
  if (isRunning) return;
  isRunning = true;

  if (!sessionToken) {
    sessionToken = generateUUID();
    const tokenInput = document.getElementById('idempotency-token-input');
    if (tokenInput) tokenInput.value = sessionToken;
  }

  const startBtn = document.getElementById('start-btn');
  const pauseBtn = document.getElementById('pause-btn');
  if (startBtn) startBtn.style.display = 'none';
  if (pauseBtn) pauseBtn.style.display = 'inline-flex';

  timerInterval = setInterval(() => {
    secondsElapsed++;
    updateDisplay();
  }, 1000);
}

function pauseTimer() {
  if (!isRunning) return;
  isRunning = false;
  clearInterval(timerInterval);

  const startBtn = document.getElementById('start-btn');
  const pauseBtn = document.getElementById('pause-btn');
  if (startBtn) {
    startBtn.style.display = 'inline-flex';
    startBtn.innerHTML = '▶ Resume';
  }
  if (pauseBtn) pauseBtn.style.display = 'none';
}

function resetTimer() {
  pauseTimer();
  secondsElapsed = 0;
  sessionToken = generateUUID();
  const tokenInput = document.getElementById('idempotency-token-input');
  if (tokenInput) tokenInput.value = sessionToken;
  updateDisplay();

  const startBtn = document.getElementById('start-btn');
  if (startBtn) startBtn.innerHTML = '▶ Start Reading';
}

document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('start-btn');
  const pauseBtn = document.getElementById('pause-btn');
  const resetBtn = document.getElementById('reset-btn');
  const finishBtn = document.getElementById('finish-btn');

  if (startBtn) startBtn.addEventListener('click', startTimer);
  if (pauseBtn) pauseBtn.addEventListener('click', pauseTimer);
  if (resetBtn) resetBtn.addEventListener('click', resetTimer);

  if (finishBtn) {
    finishBtn.addEventListener('click', () => {
      pauseTimer();
      if (secondsElapsed < 10) {
        alert('Please read for at least 10 seconds before recording a session.');
        return;
      }
      openModal('log-session-modal');
    });
  }

  updateDisplay();
});
