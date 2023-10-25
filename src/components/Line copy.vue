<template>
    <div id="app">
      <div id="chart">
        <apexchart type="area" height="350" :options="chartOptions" :series="series"></apexchart>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, onUnmounted } from 'vue';
  import VueApexCharts from 'vue3-apexcharts';
  
  export default {
    components: {
      apexchart: VueApexCharts,
    },
    setup() {
      const series = ref([
        {
          name: 'Voltage',
          data: [], // Initialize with empty data array
        },
        {
          name: 'Current',
          data: [], // Initialize with empty data array
        },
      ]);
  
      const chartOptions = {
        chart: {
          height: 350,
          type: 'area',
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: 'smooth',
        },
        xaxis: {
          type: 'datetime',
          labels: {
            datetimeFormatter: {
              year: 'yyyy',
              month: "MMM 'yy",
              day: 'dd MMM',
              hour: 'HH:mm',
            },
            style: {
              colors: '#00008B', // Set the x-axis label text color to white
            },
          },
        },
        yaxis: {
          labels: {
            style: {
              colors: '#00008B', // Set the y-axis label text color to white
            },
          },
        },
        tooltip: {
          x: {
            format: 'dd/MM/yy HH:mm',
          },
        },
        theme: {
          mode: 'light', // Use dark theme for the chart
        },
      };
  
      // Update data every 5 seconds
      const intervalId = setInterval(updateChartData, 1000);
  
      // Clear interval on component unmount
      onUnmounted(() => clearInterval(intervalId));
  
      // Function to update the chart data
      function updateChartData() {
        // Generate random values for current and voltage
        const current = getRandomValue(18, 35);
        const voltage = getRandomValue(180, 350);
  
        // Get the current timestamp in UTC format and convert to IST (UTC+5:30)
        const utcTimestamp = new Date().toISOString();
        const istTimestamp = new Date(utcTimestamp);
        istTimestamp.setHours(istTimestamp.getHours() + 5);
        istTimestamp.setMinutes(istTimestamp.getMinutes() + 30);
  
        // Add the new data point to the series array
        series.value[0].data.push({ x: istTimestamp.getTime(), y: voltage });
        series.value[1].data.push({ x: istTimestamp.getTime(), y: current });
  
        // Remove the oldest data point to maintain 7 data points on the chart
        if (series.value[0].data.length > 7) {
          series.value[0].data.shift();
          series.value[1].data.shift();
        }
      }
  
      // Function to generate random value within a range
      function getRandomValue(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
      }
  
      // Initial update
      updateChartData();
  
      return {
        series,
        chartOptions,
      };
    },
  };
  </script>
  
  <style>
  /* Add any custom styles for the chart container if needed */
  #chart {
    margin: 20px;
  }
  </style>
  