<template>
  <div>
    <h1>Machine States Over Time</h1>
    <vue-apex-charts type="bar" :options="chartOptions" :series="chartSeries" />
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';

export default {
  components: {
    VueApexCharts,
  },
  data() {
    return {
      chartOptions: {
        chart: {
          stacked: true,
          toolbar: {
            show: false,
          },
        },
        xaxis: {
          categories: ['7d', '7f', '7g', '7h', '7k'],
          labels: {
            show: true,
          },
        },
        yaxis: {
          title: {
            text: 'Time',
          },
        },
      },
      chartSeries: [
        {
          name: 'Idle',
          data: this.generateRandomDurations(),
        },
        {
          name: 'Production',
          data: this.generateRandomDurations(),
        },
      ],
    };
  },
  methods: {
    generateRandomDurations() {
      // Generate random durations for demonstration purposes
      return [
        Math.floor(Math.random() * (60 - 10 + 1) + 10), // 7d
        Math.floor(Math.random() * (60 - 10 + 1) + 10), // 7f
        Math.floor(Math.random() * (60 - 10 + 1) + 10), // 7g
        Math.floor(Math.random() * (60 - 10 + 1) + 10), // 7h
        Math.floor(Math.random() * (60 - 10 + 1) + 10), // 7k
      ];
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
