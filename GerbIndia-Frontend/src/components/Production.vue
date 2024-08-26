<script setup>
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { CustomChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
} from 'echarts/components';
import * as echarts from 'echarts/core';

import VChart, { THEME_KEY } from 'vue-echarts';
import { ref, provide, onMounted, watch } from 'vue';
import axios from 'axios';

use([
  CanvasRenderer,
  CustomChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
]);

provide(THEME_KEY, 'light');
const totalIdleDuration = ref(0);
const totalProductionDuration = ref(0);

let option;

let startTime = +new Date();
const selectedDate = ref('');
const props = defineProps({
    dataFromParentProduction: {
    type: String,
    required: true
  }
});

function renderItem(params, api) {
  let categoryIndex = api.value(0);
  let start = api.coord([api.value(1), categoryIndex]);
  let end = api.coord([api.value(2), categoryIndex]);
  let height = api.size([0, 1])[1] * 0.3;
  let rectShape = echarts.graphic.clipRectByRect(
    {
      x: start[0],
      y: start[1] - height / 2,
      width: end[0] - start[0],
      height: height
    },
    {
      x: params.coordSys.x,
      y: params.coordSys.y,
      width: params.coordSys.width,
      height: params.coordSys.height
    }
  );
  return (
    rectShape && {
      type: 'rect',
      transition: ['shape'],
      shape: rectShape,
      style: api.style()
    }
  );
}

function epochToDateTimeString(epochTimestamp) {
  const date = new Date(epochTimestamp);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

const fetchData = async () => {
  try {
    const response = await axios.get(`http://192.168.0.105:6969/graph/get_production_data?machine_id=${props.dataFromParentProduction}&date=${selectedDate.value}`);
    const newData = response.data;

    // Calculate total duration for IDLE and PRODUCTION states
    totalIdleDuration.value = calculateTotalDuration(newData.dataPoints, 'IDLE');
    totalProductionDuration.value = calculateTotalDuration(newData.dataPoints, 'PRODUCTION');

    // Update other properties as needed
    option.value.series[0].data = newData.dataPoints;
    option.value.xAxis.min = newData.minimumTimestamp;
    option.value.yAxis.data = [props.dataFromParentProduction];
    option.value = { ...option.value };
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};


watch(() => props.dataFromParentProduction, (newMachineName, oldMachineName) => {
  fetchData();
});

const calculateTotalDuration = (dataPoints, state) => {
  return dataPoints
    .filter(point => point.name === state)
    .reduce((totalDuration, point) => totalDuration + point.value[3], 0);
};
// Helper function to format duration in hours
const formatDuration = (durationInMilliseconds) => {
  const seconds = Math.floor(durationInMilliseconds / 1000);
  const minutes = Math.floor((seconds % 3600) / 60);
  const hours = Math.floor(seconds / 3600);

  return `${hours}h ${minutes}m ${seconds % 60}s`;
};
onMounted(() => {
  fetchData();
});

option = ref({
  tooltip: {
    formatter: function (params) {
      return params.marker + params.name + ', ' + 'Start Time: ' +  epochToDateTimeString(params.value[1]) +
       ', End Time: ' + epochToDateTimeString(params.value[2]) + ', Duration: ' + params.value[3] + ' ms' ;
    }
  },
  title: {
    text: 'Stats Chart',
    left: 'center'
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
    }
  ],
  grid: {
    height: 300,
    bottom: 80
  },
  xAxis: {
    min: 0,
    scale: true,
    axisLabel: {
      formatter: function (val) {
        return epochToDateTimeString(val);
      }
    }
  },
  yAxis: {
    data: [props.dataFromParentProduction] // Initialize y-axis data with the current machine
  },
  series: [
    {
      type: 'custom',
      renderItem: renderItem,
      itemstyle: {
        opacity: 1
      },
      encode: {
        x: [1, 2],
        y: 0
      },
      data: []
    }
  ]
});
const submitDate = () => {
  fetchData();
};

</script>

<template>
 <div>
  <div class="flex  justify-around">
    <div> <label for="dateInput" class="text-xl">Select Date:</label>
    <input type="date" id="dateInput" v-model="selectedDate" class="border border-gray-300 rounded-lg px-2 py-1 " />
    <button @click="submitDate" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 ml-2 px-4 rounded shadow mb-1">Submit</button></div>
    <div>
    <!-- Your Vue template code here -->
    <p class="text-lg text-blue-500 font-bold font-poppins">{{props.dataFromParentProduction}}</p>
    <p class="text-lg  font-montserrat text-slate-600  ">Total <span class="text-yellow-400">IDLE</span> Duration: <span class="font-montserrat text-blue-600 font-bold ">{{ formatDuration(totalIdleDuration) }}</span></p>
    <p class="text-lg  font-montserrat text-slate-600  ">Total <span class="text-green-600">PRODUCTION</span> Duration: <span class="font-montserrat text-blue-600 font-bold ">{{ formatDuration(totalProductionDuration) }}</span></p>
    <!-- <p>Total PRODUCTION Duration: {{ formatDuration(totalProductionDuration) }}</p> -->
  </div>
  </div>
  
   

    
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>
