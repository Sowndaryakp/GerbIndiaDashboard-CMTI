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
import { ref, provide, watch } from 'vue';
import axios from 'axios';
import Datepicker from 'vue3-datepicker';

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

let option;

let startTime = +new Date();
let categories = ['7G', '7H', '7J','7K', '7L', '27C','27D', '27E'];

const props = defineProps({
  chartData: {
    type: Object,
    default: () => ({ minimumTimestamp: 0, dataPoints: [] }),
  }
});

const startDate = ref('');
const endDate = ref('');

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

option = ref({
  tooltip: {
    formatter: function (params) {
      return params.marker + params.name + ', ' + 'Start Time: ' + epochToDateTimeString(params.value[1]) +
        ', End Time: ' + epochToDateTimeString(params.value[2]) + ', Duration: ' + params.value[3] + ' ms';
    }
  },
  title: {
    text: '',
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
    min: props.chartData.minimumTimestamp,
    scale: true,
    axisLabel: {
      formatter: function (val) {
        return epochToDateTimeString(val);
      }
    }
  },
  yAxis: {
    data: categories
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
      data: props.chartData.dataPoints
    }
  ]
});

const fetchData = async (startEpoch, endEpoch) => {
  try {
    const response = await axios.get(`http://192.168.0.105:6969/graph/get_graph_data_new?start_time=${startEpoch}&end_time=${endEpoch}`);
    const newData = response.data;
    option.value.series[0].data = newData.dataPoints;
    option.value.xAxis.min = newData.minimumTimestamp;
    option.value = { ...option.value };  // Trigger Vue reactivity
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

const submitDate = () => {
  if (startDate.value && endDate.value) {
    const startEpoch = Math.floor(new Date(startDate.value).getTime() / 1000);
    const endEpoch = Math.floor(new Date(endDate.value).getTime() / 1000);
    fetchData(startEpoch, endEpoch);
  } else {
    console.error('Please select both start date and end date.');
  }
};
</script>


<template>
  <div>
    <div class="flex justify-center mb-4">
      <span class="text-blue-600 font-montserrat font-bold">All Machines Production Stats</span>
    </div>
    <div class="flex justify-center mb-4 items-center">
      <div class="mr-4 ml-12">
        <label for="start-date" class="mr-2 text-sm font-medium text-gray-700">
          Start Date:
          <input type="date" v-model="startDate" id="start-date" class="border border-gray-300 rounded-lg px-2 py-1" />
        </label>
      </div>
      <div class="mr-4">
        <label for="end-date" class="mr-2 text-sm font-medium text-gray-700">
          End Date:
          <input type="date" v-model="endDate" id="end-date" class="border border-gray-300 rounded-lg px-2 py-1" />
        </label>
      </div>
      <button @click="submitDate" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 ml-2 px-4 rounded shadow mb-1">Submit</button>
    </div>
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>




