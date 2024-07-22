<template>
  <div class="font-montserrat">
    <h1 class="text-3xl font-bold mb-4 text-center mt-2">DOWNLOAD DATA</h1>
    <form @submit.prevent="submitForm" class="flex flex-wrap gap-4">
      <div v-for="param in parametersAll" :key="param" class="flex flex-col font-poppins">
        <label :for="param" class="mb-1">{{ param }}</label>
        <select v-if="param !== 'start_time' && param !== 'end_time'" :id="param" v-model="formData[param]" class="border p-2 rounded-md">
          <option v-for="option in availableOptions[param]" :key="option" :value="option">{{ option }}</option>
        </select>
        <input v-else-if="param === 'start_time'" type="date" :id="param" v-model="formData[param]" class="border p-2 rounded-md" />
        <input v-else-if="param === 'end_time'" type="date" :id="param" v-model="formData[param]" class="border p-2 rounded-md" />
        <input v-else :id="param" v-model="formData[param]" class="border p-2 rounded-md" />
      </div>

      <button type="submit" class="bg-blue-500 glassmorphic-button rounded-lg px-4 py-2 mt-3 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/FFFFFF/submit-for-approval.png" class="w-6 h-6 mr-2" alt="submit-for-approval"/>
        Submit
      </button>
      <button @click="downloadExcel" class="bg-green-500 glassmorphic-button rounded-lg px-4 py-2 mt-3 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="24" height="24" src="https://img.icons8.com/sf-black/64/FFFFFF/download.png" alt="download" class="flex flex-wrap"/>
        Download Excel
      </button>
      <button @click="resetForm" class="bg-gray-500 glassmorphic-button rounded-lg px-4 py-2 mt-3 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/FFFFFF/refresh.png" alt="refresh" class="w-6 h-6 mr-2" />
        Reset
      </button>
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
            <td v-for="param in parameters" :key="param" class="py-2 px-4"> {{ value[param] !== null ? value[param] : 'null' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="mt-4 p-4 bg-gray-100 rounded-md shadow-md">
      No data to display.
    </div>
  </div>

  <div v-if="alertMessage" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="w-96 p-4 bg-gray-100 border text-center border-gray-300 rounded-lg shadow-md">
      <p class="text-center text-red-600">{{ alertMessage }}</p>
      <button @click="closeAlert" class="bg-blue-500 text-white px-2 py-1 rounded-lg mt-2">OK</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import * as XLSX from 'xlsx';

const alertMessage = ref('');
const showAlert = (message) => {
  alertMessage.value = message;
};

const closeAlert = () => {
  alertMessage.value = null;
};

const resetForm = () => {
  // Reload the page
  window.location.reload();
};


const formData = ref({
  start_time: null,
  end_time: null,
  machine_id: null,
  type: null,
  range: null,
  welder_name: null,
  project: null,
  I_no: null,
  Fc_no: null,
  plate_thickness: null,
  plate_description: null,
});

const parameters = ["start_time", "end_time", "machine_id", "type", "range", "welder_name", "project", "I_no", "Fc_no", "plate_thickness", "plate_description","standard_current","standard_voltage","average_current","average_voltage","min_current","max_current","min_voltage","max_voltage"];
const parametersAll = ["start_time", "end_time", "machine_id", "type", "range", "welder_name", "project", "I_no", "Fc_no", "plate_thickness", "plate_description"];
const filteredValues = ref([]);
const availableOptions = ref({});

const fetchDataForParameters = async () => {
  try {
    const endpoints = {
      plate_thickness: 'http://192.168.0.105:6969/elements',
      range: 'http://192.168.0.105:6969/elements',
      machine_id: 'http://192.168.0.105:6969/machines',
      welder_name: 'http://192.168.0.105:6969/welder/',
      project: 'http://192.168.0.105:6969/op_shift/',
      I_no: 'http://192.168.0.105:6969/op_shift/',
      Fc_no: 'http://192.168.0.105:6969/op_shift/',
      type: 'http://192.168.0.105:6969/elements',
      standard_current: 'http://192.168.0.105:6969/elements',
      standard_voltage: 'http://192.168.0.105:6969/elements',
      plate_thickness: 'http://192.168.0.105:6969/plate/plate',
      plate_description: 'http://192.168.0.105:6969/plate/plate',
    };

    for (const param in endpoints) {
      const response = await axios.get(endpoints[param]);
      availableOptions.value[param] = extractOptions(response.data, param);
    }
    availableOptions.value['range'] = Array.from(new Set(availableOptions.value['range']));
    availableOptions.value['project'] = Array.from(new Set(availableOptions.value['project']));
    availableOptions.value['I_no'] = Array.from(new Set(availableOptions.value['I_no']));
    availableOptions.value['Fc_no'] = Array.from(new Set(availableOptions.value['Fc_no']));
    availableOptions.value['plate_thickness'] = Array.from(new Set(availableOptions.value['plate_thickness']));
    availableOptions.value['plate_description'] = Array.from(new Set(availableOptions.value['plate_description']));
    
  } catch (error) {
    console.error('Error fetching available options:', error);
  }
};

const extractOptions = (data, param) => {
  if (data.Data) {
    return data.Data.map(item => item[param]);
  } else {
    return data.map(item => item[param]);
  }
};

const submitForm = async () => {
  try {
    const response = await axios.get('http://192.168.0.105:6969/excel/', { params: formData.value });

    if (response.data && Array.isArray(response.data) && response.data.length > 0) {
      filteredValues.value = response.data;
      showAlert("Data retrieved successfully.");
    } else {
      showAlert("No data found for the selected parameters.");
    }
  } catch (error) {
    console.error('Error fetching filtered values:', error);
    showAlert("There was an issue retrieving the data. Please check your selected parameters and try again.");
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
