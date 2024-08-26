<template>
    <div>
      <label for="selectedDate">Select Date:</label>
      <input type="date" v-model="selectedDate" id="selectedDate" class="bg-white rounded p-2" />
      <button @click="downloadReport" class="bg-blue-500 text-white p-2 rounded-lg mt-4">
        Download Report
      </button>
    </div>
  </template>
  
  <script setup>
  import { ref, defineProps, defineEmits } from 'vue';
  
  const props = defineProps();
  const emits = defineEmits();
  
  const selectedDate = ref('');
  
  const downloadReport = () => {
    // Emit an event to notify the parent component with the selected date
    emits('download-report', selectedDate.value);
  };
  </script>
  