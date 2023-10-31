<template>
  <div>
    <button @click="generateExcel">Generate Excel</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import * as XLSX from 'xlsx';

const generateExcel = async () => {
  try {
    const response = await axios.get('your_backend_api_endpoint');
    const data = response.data;

    if (data && Array.isArray(data)) {
      const workbook = XLSX.utils.book_new();
      const worksheet = XLSX.utils.json_to_sheet(data);
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
      
      const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
      const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      
      const downloadLink = document.createElement('a');
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = 'data.xlsx';
      downloadLink.click();
    }
  } catch (error) {
    console.error('Error generating Excel:', error);
  }
};
</script>
