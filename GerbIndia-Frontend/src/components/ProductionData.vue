<template>
    <!-- <Navbar/> -->
  
    <div class="container mx-auto p-4">
      <div class="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
        <!-- Date selection -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">Start Date:</label>
          <input type="date" v-model="startDate" class="block w-full bg-gray-100 border rounded p-2">
        </div>
        <!-- <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">Select Machine:</label>
          <select v-model="selectedMachine">
            <option value="7D">7D</option>
            <option value="7F">7F</option>
            <option value="7G">7G</option>
            <option value="7H">7H</option>
            <option value="7I">7I</option>
            <option value="7J">7J</option>
            <option value="7K">7K</option>
            <option value="7L">7L</option>
          </select>
        </div> -->
  
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">Select Operator:</label>
          <select v-model="selectedName">
            <option value="Bhimappa">Bhimappa</option>
            <option value="Somappa">Somappa</option>
            <option value="Rajappa">Rajappa</option>
          </select>
        </div>
       
        <!-- <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">Select Type:</label>
          <select v-model="selectedType">
            <option value="type-1">type-1</option>
            <option value="type-2">type-2</option>
            <option value="type-3">type-3</option>
            <option value="type-1">type-1</option>
            <option value="type-1">type-1</option>
            <option value="type-1">type-1</option>
            <option value="type-1">type-1</option>
            <option value="type-1">type-1</option>
          </select>
        </div> -->
  
        <div>
          <button @click="generateExcel" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow">
            Download Report
          </button>
        </div>
        
        <!-- Display data from the API -->
        <!-- <div v-if="data">
          <h2 class="text-lg font-semibold mt-4">Data from API:</h2>
          <pre>{{ data }}</pre>
        </div> -->
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, computed, defineProps } from 'vue';
  import axios from 'axios';
  import * as XLSX from 'xlsx';
  import Navbar from '@/components/Navbar.vue'
  
  // Define reactive variables
  const startDate = ref('');
  const selectedMachine = ref('7D'); // Default value
  const selectedName = ref('Bhimappa'); // Default value for the new dropdown
  const data = ref(null);
  const predeterminedType = 'type-1'; // Change this to your actual predetermined type
  
  const sampleProperties = defineProps({
    machine_id: String,
  });
  
  console.log("=============================");
  console.log(sampleProperties.machine_id);
  
  // Computed property for the Axios URL for machine data
  const axiosMachineUrl = computed(() => {
    return `http://192.168.0.105:6969/live_data/${sampleProperties.machine_id}`;
  });
  
  // Computed property for the Axios URL for operator data
  const axiosOperatorUrl = computed(() => {
    return `http://192.168.0.105:6969/welder/${selectedName.value}`;
  });
  
  // Computed property for the Axios URL for the predetermined type
  const axiosTypeUrl = computed(() => {
    return `http://192.168.0.105:6969/elements/${predeterminedType}`;
  });
  
  
  // Function to fetch data from the API for both machine and operator
  const generateExcel = async () => {
    try {
      const machineResponse = await axios.get(axiosMachineUrl.value);
      const operatorResponse = await axios.get(axiosOperatorUrl.value);
      const typeResponse = await axios.get(axiosTypeUrl.value);
  
      console.log('Machine Response Data:', machineResponse.data);
      console.log('Operator Response Data:', operatorResponse.data);
      console.log('Type Response Data:', typeResponse.data);
  
      // Convert response data to arrays (if necessary)
      const machineData = Array.isArray(machineResponse.data) ? machineResponse.data : [machineResponse.data];
      const operatorData = Array.isArray(operatorResponse.data) ? operatorResponse.data : [operatorResponse.data];
      const typeData = Array.isArray(typeResponse.data) ? typeResponse.data : [typeResponse.data];
  
      // Combine the data from all responses into a single array
      const combinedData = [...machineData, ...operatorData, ...typeData];
  
      data.value = combinedData;
  
      // Generate and download Excel file
      const ws = XLSX.utils.json_to_sheet(combinedData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'DataSheet');
      XLSX.writeFile(wb, 'report.xlsx');
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
  
  
  
  // Watch for changes in selectedName and trigger data fetching
  watch(selectedName, () => {
    generateExcel();
  });
  </script>
  
  
  