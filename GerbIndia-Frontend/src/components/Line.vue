<template>
  <div class="h-96">
    <div class="flex justify-evenly mb-6">
      <p class="font-bold">Machine ID:<span class="text-blue-500">{{ props.dataFromParent.machineId }}</span></p>
    <p class="font-bold">Voltage(LOW):<span class="text-green-500">{{ props.dataFromParent.range_voltage_low }}</span></p>
    <p class="font-bold">Voltage(HIGH):<span class="text-green-500">{{ props.dataFromParent.range_voltage_high }}</span></p>
    <p class="font-bold">Current(LOW): <span class=" text-blue-500">{{ props.dataFromParent.range_current_low }}</span></p>
    <p class="font-bold">Current(HIGH): <span class=" text-blue-500">{{ props.dataFromParent.range_current_high }}</span></p>
    <div class="flex justify-around">
      <div class="flex flex-col ml-7 rounded-lg w-40-mt-2">
        <div class="flex items-center mt-1 ml-2">
          <div class="w-4 h-4 bg-blue-500 rounded-full mr-2"></div>
          <span class="text-blue-600 font-bold font-poppins">CURRENT</span>
        </div>
      <div class="flex items-center">
        <div class="w-4 h-4 bg-green-500 rounded-full mr-2 ml-2"></div>
        <span class="text-blue-600 font-bold font-poppins">VOLTAGE</span>
      </div></div>
      </div>
    </div>
   
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
// const low_cur = props.dataFromParent.low_std_curr;
// const high_cur = props.dataFromParent.high_std_curr;
// const low_vol = props.dataFromParent.low_std_vol;
// const high_vol = props.dataFromParent.high_std_vol;




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
        axisLabel: {
      formatter: '{value} A', // Format for the y-axis labels
    },
        
      },
      {
        type: 'value',
        name: 'Voltage (V)',
        scale: true,
        axisLabel: {
      formatter: '{value} v', // Format for the y-axis labels
    },
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
        name: 'Critical Current (${props.dataFromParent.range_current_high})',
        data: Array(20).fill(props.dataFromParent.range_current_high),
        symbol: 'none',
        lineStyle: {
          color: 'blue',
          width: 2,
          type: 'solid',
        },
        yAxisIndex: 0,
        zlevel: 10,
      },
      // {
      //   type: 'line',
      //   name: 'Critical Voltage (300V)',
      //   data: [],
      //   symbol: 'none',
      //   lineStyle: {
      //     color: 'red',
      //     width: 2,
      //     type: 'solid',
      //   },
      //   areaStyle: {
      //     color: 'rgba(255, 0, 0, 0.1)',
      //   },
      //   yAxisIndex: 1,
      //   zlevel: 10,
      // },
      {
        type: 'line',
        name: 'Critical Current (${props.dataFromParent.range_current_low})',
        data: Array(20).fill(props.dataFromParent.range_current_low),
        symbol: 'none',
        lineStyle: {
          color: 'blue',
          width: 2,
          type: 'solid',
        },
        yAxisIndex: 0,
        zlevel: 10,
      },
      {
        type: 'line',
        name: 'Critical voltage (${props.dataFromParent.range_voltage_high})',
        data: Array(20).fill(props.dataFromParent.range_voltage_high),
        symbol: 'none',
        lineStyle: {
          color: 'green',
          width: 2,
          type: 'solid',
        },
        yAxisIndex: 1,
        zlevel: 10,
      },
      {
        type: 'line',
        name: 'Critical voltage (${props.dataFromParent.range_voltage_low})',
        data: Array(20).fill(props.dataFromParent.range_voltage_low),
        symbol: 'none',
        lineStyle: {
          color: 'green',
          width: 2,
          type: 'solid',
        },
        yAxisIndex: 1,
        zlevel: 10,
      },
      // {
      //   type: 'line',
      //   name: 'Critical Current (300A)',
      //   data: Array(20).fill(300),
      //   symbol: 'none',
      //   lineStyle: {
      //     color: 'purple',
      //     width: 2,
      //     type: 'solid',
      //   },
      //   yAxisIndex: 0,
      //   zlevel: 10,
      // },
      // {
      //   type: 'line',
      //   name: 'Critical Current (50A)',
      //   data: Array(20).fill(50),
      //   symbol: 'none',
      //   lineStyle: {
      //     color: 'blue',
      //     width: 2,
      //     type: 'solid',
      //   },
      //   yAxisIndex: 0,
      //   zlevel: 10,
      // },
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
    console.log("^^$^& ^&^&$&%&&    $^&&&&&&&&&&&&&&")
    console.log(newData.current)
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
