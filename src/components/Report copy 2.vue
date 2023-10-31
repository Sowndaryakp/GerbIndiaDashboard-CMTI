<template>
  <div class="container mx-auto p-4">
    <div class="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
      <!-- Date selection -->
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">Start Date:</label>
        <input type="date" v-model="startDate" class="block w-full bg-gray-100 border rounded p-2">
      </div>
      <div class="mb-4">
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
  </div>
     
      <div>
      <button @click="generateExcel" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow">
        Download Report
      </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import html2pdf from 'html2pdf.js';
import { ref } from 'vue';
import axios from 'axios';
import * as XLSX from 'xlsx';

const startDate = null;
const endDate = null;
const selectedTime = null;
const selectedShift = null;
const selectedMachine = ref(''); // Initialize selectedMachine as a ref

const shifts = [
  { id: 1, name: 'SHIFT-1' },
  { id: 2, name: 'SHIFT-2' },
  { id: 3, name: 'SHIFT-3' },
  { id: 4, name: 'All-SHIFTS' }
];

const generateAndDownloadPDF = () => {
  const content = '<div class="bg-white rounded-lg p-6 shadow-lg">GerbIndia</div>';
  const opt = {
    margin: 10,
    filename: 'report.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
  };
  html2pdf().from(content).set(opt).save();
};

const generateExcel = async () => {
  try {
    // Construct the Axios URL with the selected machine
    const url = `http://172.18.100.240:9999/live_data/${selectedMachine.value}`;

    // Fetch data for the selected machine using Axios
    const response = await axios.get(url);

    // Check if the response contains data
    if (response.data) {
      const machineData = response.data;

      // Create a new workbook
      const workbook = XLSX.utils.book_new();

      // Create an Excel sheet with the data
      const worksheet = XLSX.utils.json_to_sheet(machineData);

      // Add the sheet to the workbook
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

      // Convert the workbook to an array buffer
      const excelArrayBuffer = XLSX.write(workbook, { bookType: 'arraybuffer', type: 'array' });

      // Create a Blob from the array buffer
      const blob = new Blob([excelArrayBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

      // Create a download link and trigger the download
      const downloadLink = document.createElement('a');
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = `data_${selectedMachine.value}.xlsx`; // Set a dynamic file name
      downloadLink.click();
    }
  } catch (error) {
    console.error('Error generating Excel:', error);
  }
};





</script>



<style>
/* Add Tailwind CSS classes here or import a pre-built Tailwind CSS file */
</style>
