/**
 * BookWise Atelier — Chart.js Visualizations for Reading Velocity & Genre Distribution
 */

function initStatisticsCharts(monthlyData, genreData) {
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  const textColor = currentTheme === 'dark' ? '#f4ede2' : '#23211e';
  const gridColor = currentTheme === 'dark' ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';

  // 1. Monthly Velocity Bar Chart
  const velocityCanvas = document.getElementById('monthlyVelocityChart');
  if (velocityCanvas && monthlyData && monthlyData.length) {
    const labels = monthlyData.map(d => d.month);
    const books = monthlyData.map(d => d.books);
    const minutes = monthlyData.map(d => d.minutes);

    new Chart(velocityCanvas, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Books Completed',
            data: books,
            backgroundColor: '#1a3c2e',
            borderColor: '#1a3c2e',
            borderRadius: 6,
            yAxisID: 'y'
          },
          {
            label: 'Minutes Read',
            data: minutes,
            type: 'line',
            borderColor: '#c5a059',
            backgroundColor: 'rgba(197, 160, 89, 0.2)',
            tension: 0.3,
            fill: true,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: textColor }
          },
          y: {
            type: 'linear',
            position: 'left',
            grid: { color: gridColor },
            ticks: { color: textColor, precision: 0 },
            title: { display: true, text: 'Books', color: textColor }
          },
          y1: {
            type: 'linear',
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: { color: textColor },
            title: { display: true, text: 'Minutes', color: textColor }
          }
        },
        plugins: {
          legend: {
            labels: { color: textColor }
          }
        }
      }
    });
  }

  // 2. Genre Distribution Doughnut Chart
  const genreCanvas = document.getElementById('genreDistributionChart');
  if (genreCanvas && genreData && Object.keys(genreData).length) {
    const labels = Object.keys(genreData);
    const data = Object.values(genreData);

    const palette = [
      '#1a3c2e', '#c5a059', '#0f172a', '#285441',
      '#dfbe7d', '#334155', '#475569', '#64748b'
    ];

    new Chart(genreCanvas, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: palette.slice(0, labels.length),
          borderWidth: 2,
          borderColor: currentTheme === 'dark' ? '#182232' : '#ffffff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: textColor }
          }
        }
      }
    });
  }
}
