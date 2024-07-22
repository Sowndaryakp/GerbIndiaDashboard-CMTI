<template>
  <div class="flex justify-evenly mb-6">
    <p class="font-bold">Machine ID:<span class="text-blue-500">{{ props.dataFromParent.machineId }}</span></p>
    <p class="font-bold">Voltage(LOW):<span class="text-green-500">{{ props.dataFromParent.range_voltage_low }}</span></p>
    <p class="font-bold">Voltage(HIGH):<span class="text-green-500">{{ props.dataFromParent.range_voltage_high }}</span></p>
    <p class="font-bold">Current(LOW): <span class="text-blue-500">{{ props.dataFromParent.range_current_low }}</span></p>
    <p class="font-bold">Current(HIGH): <span class="text-blue-500">{{ props.dataFromParent.range_current_high }}</span></p>
    <div class="flex justify-around">
      <div class="flex flex-col ml-7 rounded-lg w-40 mt-2">
        <div class="flex items-center mt-1 ml-2">
          <div class="w-4 h-4 bg-blue-500 rounded-full mr-2"></div>
          <span class="text-blue-600 font-bold font-poppins">CURRENT</span>
        </div>
        <div class="flex items-center">
          <div class="w-4 h-4 bg-green-500 rounded-full mr-2 ml-2"></div>
          <span class="text-blue-600 font-bold font-poppins">VOLTAGE</span>
        </div>
      </div>
    </div>
  </div>
  <CanvasJSChart class="chart" :options="options" :style="styleOptions" @chart-ref="chartInstance" />
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import { defineProps } from 'vue';
import axios from 'axios';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { CustomChart, LineChart } from 'echarts/charts';

import VChart from 'vue-echarts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
} from 'echarts/components';
use([
  CanvasRenderer,
  CustomChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  LineChart,
]);
const props = defineProps(['dataFromParent']);
// console.log("commingggggggggggg")
// console.log("Machine ID:", props.dataFromParent.machineId);
// console.log("Data ID:", props.dataFromParent);

const updateInterval = 1000;
const initialNumberOfDataPoints = 50;
let dataPoints1 = [];
let dataPoints2 = [];
let yValue1 = 0; // Initialize yValue1 to 0 initially
let yValue2 = 0; // Initialize yValue2 to 0 initially
let xValue = new Date().getTime() - updateInterval * initialNumberOfDataPoints;

const chart = ref(null);
let timeout = null;

const toggleDataSeries = (e) => {
  if (typeof e.dataSeries.visible === 'undefined' || e.dataSeries.visible) {
    e.dataSeries.visible = false;
  } else {
    e.dataSeries.visible = true;
  }

  if (e.dataSeriesIndex === 0) {
    options.axisY.valueFormatString = '##V';
  } else if (e.dataSeriesIndex === 1) {
    options.axisY.valueFormatString = '##A';
  }

  e.chart.render();
};

const options = {
  zoomEnabled: true,
  exportEnabled: true,
  theme: 'light2',
  title: {
    text: 'Live Current and Voltage',
  },
  axisX: {
    valueFormatString: 'H:mm:ss TT',
  },
  axisY: {
    valueFormatString: '##A',
  },
  tooltip: {
    shared: true,
  },
  legend: {
    cursor: 'pointer',
    fontColor: 'dimGrey',
    itemclick: toggleDataSeries,
  },
  data: [
    {
      type: 'spline',
      name: 'Current in Amps',
      color: 'blue',
      xValueType: 'dateTime',
      yValueFormatString: '#,### amps',
      xValueFormatString: 'hh:mm:ss TT',
      showInLegend: true,
      legendText: "{name} " + yValue1 + " Amps",
      dataPoints: dataPoints1,
    },
    {
      type: 'spline',
      name: 'Voltage in Volts',
      color: 'green',
      xValueType: 'dateTime',
      yValueFormatString: '#,### volts',
      showInLegend: true,
      legendText: "{name} " + yValue2 + " Volts",
      dataPoints: dataPoints2,
    },
  ],
  markLine: {
  data: [
    {
      name: 'Voltage Low',
      yAxis: props.dataFromParent.range_voltage_low,
      lineStyle: {
        type: 'solid',
        color: 'green',
      },
    },
    {
      name: 'Voltage High',
      yAxis: props.dataFromParent.range_voltage_high,
      lineStyle: {
        type: 'solid',
        color: 'red',
      },
    },
    {
      name: 'Current Low',
      yAxis: props.dataFromParent.range_current_low,
      lineStyle: {
        type: 'solid',
        color: 'blue',
      },
    },
    {
      name: 'Current High',
      yAxis: props.dataFromParent.range_current_high,
      lineStyle: {
        type: 'solid',
        color: 'orange',
      },
    },
  ],
  animation: false, // Disable animation for better visibility
},
};

const styleOptions = {
  width: '100%',
  height: '360px',
};

const chartInstance = (chart) => {
  chart.value = chart;
  timeout = setTimeout(() => updateChart(chart), updateInterval);
};

const updateChart = async (chart) => {
  try {
    const url = `http://192.168.0.105:6969/live_data/${props.dataFromParent.machineId}`;
    const response = await axios.get(url);
    const newData = response.data[0];

    xValue += updateInterval;
    yValue1 = newData.current; // Use current data from the backend
    yValue2 = newData.voltage; // Use voltage data from the backend

    dataPoints1.push({
      x: xValue,
      y: yValue1,
    });

    dataPoints2.push({
      x: xValue,
      y: yValue2,
    });

    options.data[0].legendText = "Current in amps - " + yValue1 + " amps";
    options.data[1].legendText = "Voltage in volts - " + yValue2 + " volts";

    if (chart) {
      chart.render();
    }

    timeout = setTimeout(() => updateChart(chart), updateInterval);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

// Call updateChart to fetch and render initial live data
updateChart(chart.value);

onUnmounted(() => {
  clearTimeout(timeout);
});
</script>
