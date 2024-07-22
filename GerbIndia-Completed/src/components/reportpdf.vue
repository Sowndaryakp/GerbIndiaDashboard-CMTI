<template>
  <div>
    <div class="flex flex-col gap-4 p-4 rounded-md border bg-opacity-50 font-montserrat">
    <div class="flex justify-between">
      <img height="104" width="104" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqWfvnFX0fIpNbtVdvYVLPLMy_bwzP7aXZhxp6Szk62A&s" alt="cmti_logo">
      <div class="text-right bg-slate-200 rounded-lg shadow-lg w-40">
        <p class=" text-black font-bold text-xl mr-4 mt-1
         ">June 28, 2022</p>
        <p class="text-sm text-black font-semibold mr-12 mt-2">14:18:11</p>
      </div>
    </div>

    <div class="flex justify-between ">
      <div class="bg-slate-200 rounded-lg shadow-lg w-56 ">
  <h2 class="text-2xl text-black  ml-3 font-bold ">Main Workshop</h2>
      </div>
      <div class="flex justify-center bg-slate-200 rounded-lg shadow-lg w-60 ">
        <p class="text-sm text-black ml-2 font-semibold mt-2">Previous Day curent :
        </p>
        <p class="text-sm text-blue-500 ml-2 font-semibold mt-2">
          64.65A
        </p>
      </div>
     
    </div>


    <div class="flex justify-between">
        
      <div class="flex justify-center bg-slate-200 rounded-lg shadow-lg w-60 ml-96 ">
        <p class="text-sm text-black ml-2 font-semibold mt-1">Current Month :
        </p>
        <p class="text-sm text-blue-500 ml-2 font-semibold mt-1">
          3710.74A
        </p>
      </div>
    
      <!-- <p class="text-sm text-black">Current Data from: 06:00 am, 27-06-2022 to 06:00 am, 28-06-2022</p> -->
    </div>

    <div class="flex justify-between">
      <div class="flex justify-center bg-slate-200 rounded-lg shadow-lg w-60 ">
        <p class="text-sm text-black ml-2 font-semibold mt-1">Current Month :
        </p>
        <p class="text-sm text-blue-500 ml-2 font-semibold mt-1">
          3710.74A
        </p>
      </div>
      <!-- <p class="text-sm text-black-bold">Current Month : 3710.74A</p> -->
      <div class="flex justify-between bg-slate-200 rounded-lg w-96 shadow-lg ">
        <div class=" flex ml-2">
          <div><img width="24" height="24" src="https://img.icons8.com/material-outlined/24/calendar--v1.png" alt="calendar--v1"/></div>
          <p class="text-sm text-black font-semibold"> 06:00 AM, 27-06-2022 -</p>
        </div>
        <div class=" flex mr-1">
          <div><img width="24" height="24" src="https://img.icons8.com/material-outlined/24/calendar--v1.png" alt="calendar--v1"/></div>
          <p class="text-sm text-black font-semibold">   06:00 AM, 28-06-2022</p>
        </div>
        
       </div>
      <!-- <p class="text-sm text-black">Current Data from: 06:00 am, 27-06-2022 to 06:00 am, 28-06-2022</p> -->
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
  <div class=" h-96" :chartData="stateChartData">
    <Stack/>
  </div> 
</div>
  
</template>

<script setup>
import { defineComponent, ref, onMounted } from 'vue';
import Stack from '@/components/Stack.vue';

import axios from 'axios';


//Importing Store Statements


defineComponent({
  name: 'gerb',
  components: {
    Stack,
  }
});




// Reactive reference for chart data
const stateChartData = ref([]);

// Function to fetch state data from the endpoint
const fetchStateData = async () => {
  try {
    const response = await axios.get('http://192.168.0.105:6565/machines');
    const responseData = response.data;

    // Process the response data as needed
    stateChartData.value = responseData;
    console.log("Fetched state data from the backend");
    console.log(stateChartData);
  } catch (error) {
    console.error('Error fetching state data:', error);
  }
};

// Fetch state data when the component is mounted
onMounted(() => {
  fetchStateData();

  // Fetch data every 2 seconds
  setInterval(fetchStateData, 2000);
});




</script>

<style>

</style>






<!-- 
<script setup>
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas'; // Optional, if you want to use html2canvas as well

const myComponent = ref(null); // Holds a reference to the element you'll convert

function generatePDF() {
  const doc = new jsPDF();

  // Option 1: Directly from HTML content
  doc.html(myComponent.value, {
    callback: (doc) => {
      doc.save('my_report.pdf');
    },
    x: 10,
    y: 10
  });

  // Option 2: Using html2canvas (for better handling of some complex elements)
  html2canvas(myComponent.value).then((canvas) => {
    const imgData = canvas.toDataURL('image/jpeg'); 
    doc.addImage(imgData, 'JPEG', 15, 15, 180, 150); // Adjust position/size
    doc.save('my_report.pdf');
  });
}
</script>

<template>
  <div ref="myComponent">
    <h1>My Report</h1>
    <p>This content will be in the PDF.</p>
  </div>
  <button @click="generatePDF">Generate PDF</button>
</template> -->



<!-- <template>
  <div>
    
    <table id="tableId" >
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
      </tbody>
    </table>

    <!-- Button to download HTML as PDF -->
    <button @click="downloadPDF">Download as PDF</button>
  </div>
</template>

<script>
import jsPDF from 'jspdf';

export default {
  data() {
    return {
      showTable: false
    };
  },
  methods: {
    downloadPDF() {
      // Show the table before generating PDF
      this.showTable = true;

      // Get the table element
      const table = document.getElementById('tableId');

      // Create a new jsPDF instance
      const pdf = new jsPDF();

      // Convert the table element to a PDF
      pdf.html(table, {
        callback: function (pdf) {
          // Save the PDF
          pdf.save('table.pdf');

          // Hide the table after PDF is generated
          this.showTable = false;
        }.bind(this) // Ensure the correct 'this' context inside the callback function
      });
    }
  }
}
</script>

<style scoped> -->
/* Add scoped CSS styles here if needed *