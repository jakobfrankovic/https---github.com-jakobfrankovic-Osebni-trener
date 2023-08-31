// Get the canvas element from the HTML
const ctx = document.getElementById('myChart').getContext('2d');

// Define the initial chart data
const data = {
  labels: ['Zajtrk', 'Kosilo', 'Večerja', 'Drugo'],
  datasets: [
    {
      label: 'Količina hrane',
      data: [200, 400, 600, 100],
      backgroundColor: [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
      ],
      borderWidth: 1,
    },
  ],
};

// Define the chart options
const options = {
  scales: {
    yAxes: [
      {
        ticks: {
          beginAtZero: true,
        },
      },
    ],
  },
};

// Create the chart object
const myChart = new Chart(ctx, {
  type: 'bar',
  data: data,
  options: options,
});

