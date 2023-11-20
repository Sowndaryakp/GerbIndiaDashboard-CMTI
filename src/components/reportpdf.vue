<template>
        <div class="flex flex-col gap-4 p-4 rounded-md border border-blue-700 bg-opacity-50">
    <div class="flex justify-between">
      <img height="104" width="104" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqWfvnFX0fIpNbtVdvYVLPLMy_bwzP7aXZhxp6Szk62A&s" alt="cmti_logo">
      <div class="text-right">
        <p class="text-xl text-black">June 28, 2022</p>
        <p class="text-sm text-black">14:18:11</p>
      </div>
    </div>

    <div class="flex justify-between">
      <h2 class="text-xl text-black">Main Workshop</h2>
      <p class="text-sm text-black">Previous Day curent: 64.65A</p>
    </div>

    <div class="flex justify-between">
      <p class="text-sm text-black-bold">Current Month : 3710.74A</p>
      <p class="text-sm text-black">Current Data from: 06:00 am, 27-06-2022 to 06:00 am, 28-06-2022</p>
    </div>

    <div class="flex flex-col gap-2">
      <table class="w-full table-auto bg-white bg-opacity-80 rounded-lg overflow-hidden shadow-lg">
        <thead>
          <tr>
            <th class="text-left border border-gray-300 p-2">MACHINES</th>
            <th class="text-left border border-gray-300 p-2">FIRST SHIFT </th>
            <th class="text-left border border-gray-300 p-2">SECOND SHIFT </th>
            <th class="text-left border border-gray-300 p-2">THIRD SHIFT </th>
            <th class="text-left border border-gray-300 p-2">ALL SHIFTS </th>
            <th class="text-left border border-gray-300 p-2">TOTAL COST </th>
          </tr>
        </thead>
        <tbody class="border border-gray-300 p-2">
          <tr>
            <td class="border border-gray-300 p-2">Excel CNC</td>
            <td class="border border-gray-300 p-2">13.96</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">14.16</td>
            <td class="border border-gray-300 p-2">141.6</td>
          </tr>
          <tr>
            <td class="border border-gray-300 p-2">LMW LL20T L10</td>
            <td class="border border-gray-300 p-2">9.65</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">9.85</td>
            <td class="border border-gray-300 p-2">98.5</td>
          </tr>
          <tr>
            <td class="border border-gray-300 p-2">JYOTHI VMC</td>
            <td class="border border-gray-300 p-2">4.7</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">4.9</td>
            <td class="border border-gray-300 p-2">49</td>
          </tr>
          <tr>
            <td class="border border-gray-300 p-2">Hyundai Wia VMC</td>
            <td class="border border-gray-300 p-2">3</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">3.2</td>
            <td class="border border-gray-300 p-2">32</td>
          </tr>
          <tr>
            <td class="border border-gray-300 p-2">HMT C32 CNC</td>
            <td class="border border-gray-300 p-2">1.17</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">1.37</td>
            <td class="border border-gray-300 p-2">13.7</td>
          </tr>
          <tr>
            <td class="border border-gray-300 p-2">LMW LL20T L7</td>
            <td class="border border-gray-300 p-2">5.72</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">5.92</td>
            <td class="border border-gray-300 p-2">59.2</td>
          </tr>
          <tr>
            <td>CL25 CNC</td>
            <td class="border border-gray-300 p-2">18.1</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">18.3</td>
            <td class="border border-gray-300 p-2">183</td>
          </tr>
          <tr>
            <td class="border border-gray-300 p-2">Leadwell CNC</td>
            <td class="border border-gray-300 p-2">6.75</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">0.1</td>
            <td class="border border-gray-300 p-2">6.95</td>
            <td class="border border-gray-300 p-2">69.5</td>
          </tr>
          <tr>
            <td class="border border-gray-300 p-2 font-bold">Total</td>
            <td class=" border border-gray-300 p-2 font-bold">64.65</td>
            <td class=" border border-gray-300 p-2 font-bold">0.6</td>
            <td class="border border-gray-300 p-2 font-bold">0.6</td>
            <td class="border border-gray-300 p-2 font-bold">65.85</td>
            <td class="border border-gray-300 p-2 font-bold">646.5</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="graph">
    <canvas id="myChart"></canvas>
  </div>
  </div>
  
</template>

<script setup>
import { defineComponent } from 'vue';


defineComponent({
  name: 'gerb',
});
</script>

<style>

</style>