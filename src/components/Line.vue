<template>
  <div class="h-96">
    <!-- <p>{{ props.dataFromParent }}</p> -->
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup >
import { defineProps, watch } from 'vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { CustomChart, LineChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
} from 'echarts/components';
import * as echarts from 'echarts/core';

// Import VChart from vue-echarts
import VChart from 'vue-echarts';

// Register components
use([
  CanvasRenderer,
  CustomChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  LineChart
]);

const props = defineProps(['dataFromParent']);
console.log("*********************");
console.log(props.dataFromParent);
console.log()
// const machineName = 'dataFromParent';
// console.log(props)

const option = ref({
  title: {
    text: `Current and Voltage Chart (${props.dataFromParent})`,
    left: 'center',
  },
  tooltip: {
    trigger: 'axis',
    formatter: function (params) {
      return (
        params[0].axisValueLabel +
        '<br/>' +
        params[0].marker +
        'Current: ' +
        params[0].value +
        ' A<br/>' +
        params[1].marker +
        'Voltage: ' +
        params[1].value +
        ' V'
      );
    },
  },
  dataZoom: [
    {
      type: 'slider',
      filterMode: 'weakFilter',
      showDataShadow: false,
      bottom: 20,
      start: 0,
      end: 100,
    },
    {
      type: 'inside',
      filterMode: 'weakFilter',
      start: 0,
      end: 100,
    },
  ],
  grid: {
    height: 300,
    bottom: 80,
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: [],
  },
  yAxis: [
    {
      type: 'value',
      name: 'Current (A)',
      scale: true,
    },
    {
      type: 'value',
      name: 'Voltage (V)',
      scale: true,
    },
  ],
  series: [
    {
      name: `Current (${props.dataFromParent})`,
      type: 'line',
      yAxisIndex: 0,
      data: [],
    },
    {
      name: `Voltage (${props.dataFromParent})`,
      type: 'line',
      yAxisIndex: 1,
      data: [],
    },
  ],
});

const fetchData = async () => {
  try {
    const url = `http://192.168.0.105:6969/live_data/${props.dataFromParent}`;
    const response = await axios.get(url);
    const newData = response.data[0]; // Assuming only one data point is returned

    const time = new Date(newData.created_at).toLocaleTimeString();

    option.value.xAxis.data.push(time);
    option.value.series[0].data.push(newData.current);
    option.value.series[1].data.push(newData.voltage);

    // Keep only the last 20 data points for better visualization
    if (option.value.xAxis.data.length > 20) {
      option.value.xAxis.data.shift();
      option.value.series[0].data.shift();
      option.value.series[1].data.shift();
    }

    option.value = { ...option.value }; // Trigger Vue reactivity
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

onMounted(() => {
  // Fetch data initially
  fetchData();

  // Fetch data every 2 seconds
  setInterval(fetchData, 5000);
});


watch(() => props.dataFromParent, (newVal, oldVal) => {
  console.log("+*+*+*+*+*+*+*+*+*");
  console.log("from watch");
  console.log('props.dataFromParent changed:', newVal, oldVal);
  // You can perform additional actions based on the changes if needed
});

</script>
