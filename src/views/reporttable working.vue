<script setup>
import {  ref, onMounted, } from "vue";

import html2pdf from 'html2pdf.js';

import axios from 'axios';


import Stack from "@/components/Stack.vue";

//Importing Store Statements
const reportContainer = ref(null);
const selectedDate = ref(getCurrentDate());
const showReportPopup = ref(false);

function getCurrentDate() {
  const currentDate = new Date();
  const year = currentDate.getFullYear();
  const month = String(currentDate.getMonth() + 1).padStart(2, '0');
  const day = String(currentDate.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

const downloadPDF = () => {
  const element = reportContainer.value;
  const pdfOptions = {
    margin: 10,
    filename: `report_${selectedDate}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
  };

  html2pdf(element, pdfOptions);
};


const downloadReport = () => {
  // Perform the download logic here using selectedDate.value
  // For example, you can reuse the downloadPDF logic from your main component
  // and pass selectedDate.value as a parameter.
  // Then close the popup.
  downloadPDF();
  closeReportPopup();
};


// Reactive reference for chart data
const stateChartData = ref([]);

// Function to fetch state data from the endpoint
const fetchStateData = async () => {
try {
  const response = await axios.get('http://172.18.7.76:6565/machines');
  const responseData = response.data;

  // Process the response data as needed
  stateChartData.value = responseData;
  console.log("Fetched state data from the backend");
  console.log(stateChartData);
} catch (error) {
  console.error('Error fetching state data:', error);
}
};

const openReportPopup = () => {
  showReportPopup.value = true;
};

const closeReportPopup = () => {
  showReportPopup.value = false;
};






// Fetch state data when the component is mounted
onMounted(() => {
fetchStateData();

// Fetch data every 2 seconds
setInterval(fetchStateData, 2000);
});




</script>

<!-- Template -->

<template>
  <div>
    <div class="flex flex-row justify-center" >
      <div class="mb-10 ">
      <!-- <input type="date" v-model="selectedDate" class="bg-white rounded p-2" /> -->
      <button @click="openReportPopup" class="bg-blue-500 text-white p-2 rounded-lg mt-4">
        <div class="flex">
          <img width="24" height="24" src="https://img.icons8.com/material-rounded/24/FFFFFF/calendar--v1.png" alt="calendar--v1"/>
        <h1 class="ml-2">Select Date</h1>
        </div>
        
        
      </button>
    </div>
    <div></div>
    </div>
    



<div class="bg-slate-100  rounded-md m-2 font-lexend    " ref="reportContainer">

  <div class="flex flex-col gap-4 p-4 rounded-md border bg-opacity-50 font-montserrat "  id="pdf-content">
  <div class="flex justify-between ">
    
    <img height="104" width="110" src="/src/components/gerb.png" alt="gerb_logo" class="rounded-lg">
    <span class="text-3xl font-bold font-poppins ">REPORT</span>
    <div class="text-right bg-white rounded-lg shadow-lg w-40">
      <p class="text-black font-bold text-xl mr-4 mt-1 h-8">{{ selectedDate }}</p>
        <!-- <p class="text-sm text-black font-semibold mr-12 mt-2 mb-2">{{ selectedDate.toLocaleTimeString() }}</p> -->
      </div>
  </div>

  <div class="flex justify-between ">
    <div class="bg-white rounded-lg shadow-lg w-56 ">
<h2 class="text-2xl text-black   font-bold text-center">MAIN WORKSHOP</h2>
<h3 class="font-poppins text-center ">GERB Main Workshop</h3>
<h3 class="font-poppins text-center ">Peenya 2nd Stage</h3>
    </div>
    <div class="flex-col   bg-white rounded-lg shadow-lg w-60 ">
      <div class="flex mt-2">
        <p class="text-sm text-black ml-2 font-semibold mt-2">Previous Day curent :
      </p>
      <p class="text-sm text-blue-500 ml-2 font-semibold mt-2">
        64.65A
      </p>
      </div>
      <div class="flex mt-1">
        <p class="text-sm text-black ml-2 font-semibold mt-2">Current Month :
      </p>
      <p class="text-sm text-blue-500 ml-2 font-semibold mt-2">
        3710.74A
      </p>
      </div>
      
    
    </div>
    
  </div>


  <div class="flex justify-between">
    <div class="flex justify-center bg-white rounded-lg shadow-lg w-44 ">
      <div>
        <p class="text-sm text-black ml-2 font-semibold mt-1  ">Powered by 
      </p>
      </div>
      

      <img height="104" width="104" src="/src/components/cmti.png" alt="cmti_logo" class="rounded-lg ml-3">
    
      
    </div>
    <!-- <p class="text-sm text-black-bold">Current Month : 3710.74A</p> -->
    <div class="flex justify-between">
      
      
      </div>
    <!-- <p class="text-sm text-black">Current Data from: 06:00 am, 27-06-2022 to 06:00 am, 28-06-2022</p> -->
  </div>

  
  <div class="flex flex-col gap-2 border-2 bg-blue-100 border-blue-500 rounded-lg ">
    <div class="flex justify-end -mt-4 mr-5">
      <div class="flex justify-between bg-blue-500   rounded-lg w-96 h-8 shadow-lg ">
      <div class=" flex ml-2 mt-1">
        <div><img width="24" height="24" src="/src/components/date.png" alt="calendar"/></div>
        <p class="text-sm text-white font-semibold"> 06:00 AM, 27-06-2022 -</p>
      </div>
      <div class=" flex mr-1 mt-1">
        <div><img width="24" height="24" src="/src/components/date.png" alt="calendar"/></div>
        <p class="text-sm text-white font-semibold">   06:00 AM, 28-06-2022</p>
      </div>
    </div>
    
      
      </div  >
    <div class="drop-shadow-xl m-4  flex">
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
<div class="bg-blue-100 m-4 mt-44 h-auto w-auto rounded-lg border-2  border-blue-500 ">
<div class="flex justify-end -mt-4 mr-5">
      <div class="flex justify-between bg-blue-500   rounded-lg w-96 h-8 shadow-lg ">
      <div class=" flex ml-2 mt-1">
        <div><img width="24" height="24" src="/src/components/date.png" alt="calendar"/></div>
        <p class="text-sm text-white font-semibold"> 06:00 AM, 27-06-2022 -</p>
      </div>
      <div class=" flex mr-1 mt-1">
        <div><img width="24" height="24" src="/src/components/date.png" alt="calendar"/></div>
        <p class="text-sm text-white font-semibold">   06:00 AM, 28-06-2022</p>
      </div>
    </div>
    
      
      </div  >
  <hr class="border-dashed ">
  <div></div>

  <div class="bg-white rounded-lg m-3  mb-2">
    <div class="m-2 ">
      <Stack class="h-96" :chartData="stateChartData" />
    </div>

    <div class="flex justify-around  ">
      <div class="flex flex-col ml-7 bg-slate-200 rounded-lg h-24 w-40  mt-2">
        <span class="text-black text-center font-bold font-poppins">STATES</span>
        <div class="flex items-center mt-1 ml-2">
          
  <div class="w-4 h-4 bg-red-400 rounded-full mr-2"></div>
  
  <span class="text-blue-600 font-bold font-poppins">IDLE</span>
</div>

<!-- Production Legend Item -->
<div class="flex items-center">
  <div class="w-4 h-4 bg-green-500 rounded-full mr-2 ml-2"></div>
  <span class="text-blue-600 font-bold font-poppins">PRODUCTION</span>
</div></div>
<!-- Idle Legend Item -->
<div class="flex flex-col h-auto w-48 mb-3 items-center bg-slate-200 font-poppins rounded-lg ">
  <div class="flex">
    <h1 class="font-bold">MACHINES</h1>
  </div>
  <div class="flex mt-2 rounded-lg ">
    <h1>M2 - 7F (Panasonic)</h1>
  </div>
  <div class="flex">
    <h1>M2 - 7F (Panasonic)</h1>
  </div>
  <div class="flex">
    <h1>M2 - 7F (Panasonic)</h1>
  </div><div class="flex">
    <h1>M2 - 7F (Panasonic)</h1>
  </div><div class="flex">
    <h1>M2 - 7F (Panasonic)</h1>
  </div><div class="flex">
    <h1>M2 - 7F (Panasonic)</h1>
  </div><div class="flex mb-2">
    <h1>M2 - 7F (Panasonic)</h1>
  </div>
</div>

</div>

    <!-- <div class="flex flex-col ">
      <div>
        <h3>IDLE</h3>
      </div>
      <div>
        <h3>PRODUCTION</h3>
      </div>
    </div> -->
        
    </div>
  </div>
  
</div>
<div v-if="showReportPopup" class="popup-overlay">
      <div class="popup-container">
        <label for="reportDate">Select Date:</label>
        <input type="date" v-model="selectedDate" id="reportDate" class="bg-white rounded p-2" />
        <button @click="downloadReport" class="bg-blue-500 text-white p-2 rounded-lg mt-4">
          Download Report
        </button>
        <button @click="closeReportPopup" class="bg-red-500 text-white p-2 rounded-lg mt-2">
          Close
        </button>
      </div>
    </div>
</div>

    
    
</template>

<style>
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
  }

  .popup-container {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }</style>





