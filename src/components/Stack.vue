<template>
    <div id="app">
      <div id="stacked-bar-chart">
        <apexchart type="bar" height="350" :options="chartOptions" :series="chartData"></apexchart>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import VueApexCharts from 'vue3-apexcharts';
  
  export default {
    components: {
      apexchart: VueApexCharts,
    },
    setup() {
      const chartData = ref([
        {
          name: 'ON',
          data: [3, 2, 4, 3, 3, 6, 7, 5], // Example data for ON state (M1, M2, M3, M4)
        },
    
        {
          name: 'OFF',
          data: [1, 2, 1, 3, 2, 3, 2, 4], // Example data for OFF state (M1, M2, M3, M4)
        },
        {
          name: 'PRODUCTION',
          data: [2, 3, 2, 4, 2, 4, 3, 3,], // Example data for PRODUCTION state (M1, M2, M3, M4)
        },
        
      ]);
  
      const chartOptions = {
        chart: {
          height: 350,
          type: 'bar',
          stacked: true, // Enable stacked bar chart
          toolbar: {
            show: false,
          },
        },
        plotOptions: {
          bar: {
            horizontal: true, // Display as horizontal bar chart
          },
        },
        dataLabels: {
          enabled: false,
        },
        xaxis: {
          categories: ['7G','7H','7J','7K','7L','27C','27D','27E'], // Time intervals
          labels: {
            style: {
              colors: '#0000FF',
            },
          },
        },
        yaxis: {
          labels: {
            style: {
              colors: '#0000FF',
            },
          },
        },
        colors: ['#00C875', '#FF9900', '#0096FF'], // Colors for states (ON, OFF, PRODUCTION)
      };
  
      return {
        chartData,
        chartOptions,
      };
    },
  };
  </script>
  
  <style>
  /* Add any custom styles for the chart container if needed */
  #stacked-bar-chart {
    margin: 20px;
  }
  </style>
  