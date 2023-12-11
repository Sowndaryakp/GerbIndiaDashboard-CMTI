<template>
    <div class="font-montserrat">
      <h1 class="text-3xl font-bold mb-4">Filter Values</h1>
      <form @submit.prevent="submitForm" class="flex flex-wrap gap-4">
        <div v-for="param in parameters" :key="param" class="flex flex-col">
          <label :for="param" class="mb-1">{{ param }}</label>
          <input :id="param" v-model="formData[param]" class="border p-2 rounded-md" />
        </div>
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-md ">Submit</button>
        <button @click="downloadExcel" class="mt-4 bg-green-500 text-white px-4 py-2 rounded-md">Download Excel</button>
      </form>
  
      <div v-if="filteredValues.length > 0" class="mt-4 p-4 bg-gray-100 rounded-md shadow-md overflow-x-auto">
        <table class="min-w-full rounded-md overflow-hidden shadow-lg">
          <thead class="bg-blue-500 text-white">
            <tr>
              <th v-for="param in parameters" :key="param" class="py-2 px-4">{{ param }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, index) in filteredValues" :key="index" class="bg-gray-100">
              <td v-for="param in parameters" :key="param" class="py-2 px-4">{{ value[param] }}</td>
            </tr>
          </tbody>
        </table>
        
      </div>
      <div v-else class="mt-4 p-4 bg-gray-100 rounded-md shadow-md">
        No data to display.
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import * as XLSX from 'xlsx';
  
  const formData = ref({});
  const parameters = [
    "starttime", "endtime", "live_voltage", "live_current", "machine_name",
    "element_type", "element_range", "standard_current", "standard_voltage",
    "operator", "operator_info", "project"
  ];
  const filteredValues = ref([]);
  
  const submitForm = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/filter_values', formData.value);
      filteredValues.value = response.data;
    } catch (error) {
      console.error('Error fetching filtered values:', error);
    }
  };
  
  const downloadExcel = () => {
    const ws = XLSX.utils.json_to_sheet(filteredValues.value);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Filtered Data');
    XLSX.writeFile(wb, 'filtered_data.xlsx');
  };
  </script>
  