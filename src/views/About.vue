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
    const dummyData = [
      { name: 'John Doe', age: 30, email: 'john@example.com' },
      { name: 'Jane Smith', age: 28, email: 'jane@example.com' },
      { name: 'Bob Johnson', age: 35, email: 'bob@example.com' }
    ];

    const workbook = XLSX.utils.book_new();
    const worksheet = XLSX.utils.json_to_sheet(dummyData);
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
      
    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(blob);
    downloadLink.download = 'data.xlsx';
    downloadLink.click();
  } catch (error) {
    console.error('Error generating Excel:', error);
  }
};
</script>
