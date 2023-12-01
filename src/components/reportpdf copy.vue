  <template>
    <div>
      <div class="flex flex-col gap-4 p-4 rounded-md border bg-opacity-50">
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
        <div class="drop-shadow-xl  ">
          <table class="w-full table-auto bg-white bg-opacity-80 rounded-lg overflow-hidden shadow-lg">
          <thead>
            <tr>
              <th class="text-center border border-gray-300 p-2">MACHINES</th>
              <th class="text-center border border-gray-300 p-2">FIRST SHIFT </th>
              <th class="text-center border border-gray-300 p-2">SECOND SHIFT </th>
              <th class="text-center border border-gray-300 p-2">THIRD SHIFT </th>
              <th class="text-center border border-gray-300 p-2">ALL SHIFTS </th>
              <th class="text-center border border-gray-300 p-2">TOTAL COST </th>
            </tr>
          </thead>
          <tbody class="text-center border border-gray-300 p-2">
            <tr>
              <td class="border border-gray-300 p-2">7G</td>
              <td class="border border-gray-300 p-2">13.96</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">14.16</td>
              <td class="border border-gray-300 p-2">141.6</td>
            </tr>
            <tr>
              <td class="border border-gray-300 p-2">7H</td>
              <td class="border border-gray-300 p-2">9.65</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">9.85</td>
              <td class="border border-gray-300 p-2">98.5</td>
            </tr>
            <tr>
              <td class="border border-gray-300 p-2">7J</td>
              <td class="border border-gray-300 p-2">4.7</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">4.9</td>
              <td class="border border-gray-300 p-2">49</td>
            </tr>
            <tr>
              <td class="border border-gray-300 p-2">7K</td>
              <td class="border border-gray-300 p-2">3</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">3.2</td>
              <td class="border border-gray-300 p-2">32</td>
            </tr>
            <tr>
              <td class="border border-gray-300 p-2">7L</td>
              <td class="border border-gray-300 p-2">1.17</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">1.37</td>
              <td class="border border-gray-300 p-2">13.7</td>
            </tr>
            <tr>
              <td class="border border-gray-300 p-2">27C</td>
              <td class="border border-gray-300 p-2">5.72</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">5.92</td>
              <td class="border border-gray-300 p-2">59.2</td>
            </tr>
            <tr>
              <td class="border border-gray-300 p-2">27D</td>
              <td class="border border-gray-300 p-2">0.2</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">0.1</td>
              <td class="border border-gray-300 p-2">18.3</td>
              <td class="border border-gray-300 p-2">183</td>
            </tr>
            <tr>
              <td class="border border-gray-300 p-2">27E</td>
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
        
        <div > 
        <div class="flex flex-col items-center">
      <h1 class="text-3xl font-bold">Workshop Production - 27-06-2022</h1>

      <div class="mt-4 flex flex-row justify-space-around">
        <div class="flex flex-col items-center">
          <h2 class="text-2xl font-bold">First Shift</h2>

          <ul class="mt-4">
            <li v-for="machine in machines" :key="machine.name">
              <div class="flex flex-row justify-between items-center">
                <span class="text-lg font-semibold">{{ machine.name }}</span>
                <div
                  class="w-16 h-8 rounded-full"
                  :class="getBarClass(machine)"
                ></div>
                <span class="text-lg font-semibold">{{ machine.firstShift }}</span>
              </div>

            </li>
          </ul>
        </div>

        <div class="flex flex-col items-center">
          <h2 class="text-2xl font-bold">Second Shift</h2>

          <ul class="mt-4">
            <li v-for="machine in machines" :key="machine.name">
              <div class="flex flex-row justify-between items-center">
                <span class="text-lg font-semibold">{{ machine.name }}</span>
                <div
                  class="w-16 h-8 rounded-full"
                  :class="getBarClass(machine)"
                ></div>
                <span class="text-lg font-semibold">{{ machine.secondShift }}</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>   
</div>
</div>
<div></div>
<div class="bg-slate-500 mt-16">
      <hr class="border-dashed ">
      </div>
    <div class=" h-96">
      <Stack/>
    </div> 
  </div>
    
  </template>

  <script setup>
  import { defineComponent } from 'vue';
  import Stack from '@/components/Stack.vue';


  defineComponent({
    name: 'gerb',
    components: {
      Stack,
    }
  });

  </script>

  <style>

  </style>