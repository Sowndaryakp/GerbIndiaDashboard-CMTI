<template>
  <div class="h-96">
    <p>{{ props.dataFromParent.machineId }}</p>
    <p>{{ props.dataFromParent.range_voltage_low }}</p>
    <p>{{ props.dataFromParent.range_voltage_high }}</p>
    <p>{{ props.dataFromParent.range_current_low }}</p>
    <p>{{ props.dataFromParent.range_current_high }}</p>
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup>
import { defineProps, ref, onMounted, watch } from 'vue';
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

console.log("Machine ID:", props.dataFromParent.machineId);

const option = ref(null);

const createOption = () => {
  return {
    title: {
      text: `Current and Voltage Chart (${props.dataFromParent.machineId})`,
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
        name: `Current (${props.dataFromParent.machineId})`,
        type: 'line',
        yAxisIndex: 0,
        data: [],
      },
      {
        name: `Voltage (${props.dataFromParent.machineId})`,
        type: 'line',
        yAxisIndex: 1,
        data: [],
      },
      {
        type: 'line',
        name: 'Critical Voltage (300V)',
        data: [],
        symbol: 'none',
        lineStyle: {
          color: 'red',
          width: 2,
          type: 'solid',
        },
        areaStyle: {
          color: 'rgba(255, 0, 0, 0.1)',
        },
        yAxisIndex: 1,
        zlevel: 10,
      },
    ],
  };
};

onMounted(() => {
  option.value = createOption();

  // Fetch data initially
  fetchData();

  // Fetch data every 2 seconds
  setInterval(fetchData, 1000);
});

const fetchData = async () => {
  try {
    const url = `http://192.168.0.105:6969/live_data/${props.dataFromParent.machineId}`;

    const response = await axios.get(url);
    console.log(response);
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

    // Update critical voltage line data
    const criticalVoltageData = Array(option.value.xAxis.data.length).fill(240);
    option.value.series[2].data = criticalVoltageData;

    option.value = { ...option.value }; // Trigger Vue reactivity
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

watch(() => props.dataFromParent.machineId, (newVal, oldVal) => {
  console.log("+*+*+*+*+*+*+*+*+*");
  console.log("from watch");
  console.log('props.dataFromParent.machineId changed:', newVal, oldVal);
  // You can perform additional actions based on the changes if needed
});
</script>
