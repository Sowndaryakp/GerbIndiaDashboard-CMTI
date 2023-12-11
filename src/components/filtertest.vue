<template>
  <div class="font-montserrat">
  <h1 class="text-3xl font-bold mb-4 text-center mt-2 ">FILTER DATA</h1>
  <form @submit.prevent="submitForm" class="flex flex-wrap gap-4">
    <div v-for="param in parameters" :key="param" class="flex flex-col font-poppins">
      <label :for="param" class="mb-1">{{ param }}</label>
      <select v-if="param !== 'start_time' && param !== 'end_time'" :id="param" v-model="formData[param]" class="border p-2 rounded-md">
        <option v-for="option in availableOptions[param]" :key="option" :value="option">{{ option }}</option>
      </select>
      <input v-else-if="param === 'start_time'" type="datetime-local" :id="param" v-model="formData[param]" class="border p-2 rounded-md" />
      <input v-else-if="param === 'end_time'" type="datetime-local" :id="param" v-model="formData[param]" class="border p-2 rounded-md" />
      <input v-else :id="param" v-model="formData[param]" class="border p-2 rounded-md" />
    </div>
    <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-md">Submit</button>
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
import { ref,onMounted } from 'vue';
import axios from 'axios';
import * as XLSX from 'xlsx';

const formData = ref({});
const parameters = [
"start_time", "end_time", "machine_id",
"type", "range", "standard_current", "standard_voltage",
"welder_name", "project", "shift", "I_no", "Fc_no"
];
const filteredValues = ref([]);
const availableOptions = ref({});

const fetchDataForParameters = async () => {
try {
  const endpoints = {
    plate_thickness: 'http://172.18.100.240:6969/elements',
    machine_id: 'http://172.18.100.240:6969/machines',
    welder_name: 'http://172.18.100.240:6969/welder/',
    project: 'http://172.18.100.240:6969/welder/',
    shift: 'http://172.18.100.240:6969/welder/',
    I_no: 'http://172.18.100.240:6969/welder/',
    Fc_no: 'http://172.18.100.240:6969/welder/',
    type: 'http://172.18.100.240:6969/elements',
    standard_current: 'http://172.18.100.240:6969/elements',
    standard_voltage: 'http://172.18.100.240:6969/elements',
  };

  for (const param in endpoints) {
    const response = await axios.get(endpoints[param]);
    availableOptions.value[param] = extractOptions(response.data, param);
  }
} catch (error) {
  console.error('Error fetching available options:', error);
}
};

const extractOptions = (data, param) => {
if (data.Data) {
  // Handle the case where data is wrapped in a "Data" property
  return data.Data.map(item => item[param]);
} else {
  // Handle the case where data is directly an array
  return data.map(item => item[param]);
}
};

const submitForm = async () => {
try {
  // Convert start_time and end_time to epoch format
  if (formData.value.start_time) {
    formData.value.start_time = new Date(formData.value.start_time).getTime() / 1000;
  }
  if (formData.value.end_time) {
    formData.value.end_time = new Date(formData.value.end_time).getTime() / 1000;
  }

  const response = await axios.get('http://172.18.100.240:6969/excel/', { params: formData.value });
  filteredValues.value = response.data;
  console.log(response)
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

onMounted(() => {
fetchDataForParameters();
});
</script>
