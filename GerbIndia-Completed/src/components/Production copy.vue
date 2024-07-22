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

let option;

let startTime = +new Date();
let categories = ['7G', '7H', '7J','7K', '7L', '27C','27D', '27E'];
// let types = [
//   { name: 'OFF', color: '#7b9ce1' },
//   { name: 'IDLE', color: '#bd6d6c' },
//   { name: 'PRODUCTION', color: '#75d874' }
// ];

const props = defineProps({
  dataFromParentProduction: {
    type: Object,
    default: () => ({ minimumTimestamp: 0, dataPoints: [] }),
  }
});
console.log("&&&&&&&&&&&&&&&&&&&&&&&&&")
console.log(props.dataFromParentProduction);

// Generate mock data
// function generateChartData() {
//   categories.forEach(function (category, index) {
//     var baseTime = startTime;
//     for (var i = 0; i < dataCount; i++) {
//       var typeItem = types[Math.round(Math.random() * (types.length - 1))];
//       var duration = Math.round(Math.random() * 10000);
//       data.push({
//         name: typeItem.name,
//         value: [index, baseTime, (baseTime += duration), duration],
//         itemStyle: {
//           normal: {
//             color: typeItem.color
//           }
//         }
//       });
//       baseTime += Math.round(Math.random() * 2000);
//     }
//     console.log("okokok");
//     console.log(data);
//   });
// }

// generateChartData();

// console.log("Graph DATA: ");
// console.log(data);

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
  const date = new Date(epochTimestamp); // Convert seconds to milliseconds
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Month is zero-based
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  // Return the formatted date-time string
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

option = ref({
  tooltip: {
    formatter: function (params) {
      return params.marker + params.name + ', ' + 'Start Time: ' +  epochToDateTimeString(params.value[1]) +
       ', End Time: ' + epochToDateTimeString(params.value[2]) + ', Duration: ' + params.value[3] + ' ms' ;
    }
  },
  title: {
    text: 'Production Chart',
    left: 'center'
  },
  dataZoom: [
    {
      type: 'slider',
      filterMode: 'weakFilter',
      showDataShadow: false,
      bottom: 20, // Change to the desired position (e.g., bottom or top)
      start: 0, // Initial start value (e.g., 0%)
      end: 100, // Initial end value (e.g., 100%)
    },
    {
      type: 'inside',
      filterMode: 'weakFilter',
      start: 0, // Initial start value (e.g., 0%)
      end: 100, // Initial end value (e.g., 100%)
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

// const fetchData = async () => {
//   try {
//     const response = await axios.get('http://192.168.0.105:6565/machines');
//     console.log("OKOKOKOKOKOK");
//     const newData = response.data;
//     // Assuming the structure of newData is similar to props.chartData
//     option.value.series[0].data = newData;
//     option.value = { ...option.value };  // Trigger Vue reactivity
//   } catch (error) {
//     console.error('Error fetching data:', error);
//   }
// };
console.log("from script setup");
console.log(option.value);
watch(() => props.chartData, (newData, oldData) => {
  console.log("fsdfssssssssssssssssssssss");
  console.log('props.chartData changed:', newData);
  // You can update the series data here if needed
  option.value.series[0].data = newData.dataPoints;
  option.value.xAxis.min = newData.minimumTimestamp;

  option.value = { ...option.value }; // Trigger Vue reactivity
  console.log(option.value);
});

// onMounted(() => {
//   setInterval(() => {
//     generateChartData();
//     option.value.series[0].data = data;
//     option.value = { ...option.value };  // Trigger Vue reactivity
//   }, 2000);
// });

// onMounted(() => {
//   // Fetch data initially
//   fetchData();

//   // Fetch data every 2 seconds
//   setInterval(fetchData, 2000);
// });


const productChartData = ref([]);
const fetchProductData = async () => {
  try {
    const response = await axios.get('http://192.168.0.105:6969/graph/${props.dataFromParentProduction}');
    const responseData = response.data;
    console.log("%%%%%%%%%%%%%%%%%%%%%%%%%")
    //'http://192.168.0.105:6565/machines'
    //192.168.0.105:6969/graph/get_graph_data

    // Process the response data as needed
    productChartData.value = responseData;
    // console.log("Fetched state data from the backend");
    // console.log(stateChartData.value);
  } catch (error) {
    console.error('Error fetching state data:', error);
    console.log("$$$$$$$$$$$$$$$")
  }
};
onMounted(() => {
  fetchProductData();

// Fetch data every 2 seconds
// setInterval(fetchStateData, 000);
});
</script>

<template>
  <v-chart class="chart" :option="option" autoresize />
</template>