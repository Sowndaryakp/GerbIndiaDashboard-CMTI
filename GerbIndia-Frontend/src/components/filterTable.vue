<template>
  <div class="font-montserrat -mt-2">
    <h1 class="text-3xl font-bold mb-4 text-center mt-2">DOWNLOAD DATA</h1>
    <form @submit.prevent="submitForm" class="flex flex-wrap gap-4 mt-16">
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
      <button @click="showDownloadDaywisePopup" type="button" class="bg-purple-500 glassmorphic-button rounded-lg px-4 py-2 mt-3 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="20" height="20" src="https://img.icons8.com/ios-filled/50/FFFFFF/download.png" class="w-6 h-6 mr-2" alt="download"/>
        Download Day-wise
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
      <tr v-for="(value, index) in paginatedValues" :key="index" class="bg-gray-100">
    <td v-for="param in parameters" :key="param" class="py-2 px-4">
      {{ param === 'start_time' || param === 'end_time' ? formatDateTime(value[param]) : value[param] !== null ? value[param] : 'null' }}
    </td>
  </tr>
    </tbody>
  </table>
  <div class="flex justify-center items-center mt-4">
        <button @click="previousPage" :disabled="currentPage === 1" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg mr-2">Previous</button>
        <span class="text-gray-700 mx-2">Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Next</button>
      </div>
</div>

    <div v-else class="mt-4 p-4 bg-gray-100 rounded-md shadow-md">
      No data to display.
    </div>
  </div>
 <!-- Day-wise Download Popup -->
 <div v-if="showDaywisePopup" class="fixed inset-0 flex items-center justify-center z-50 bg-gray-800 bg-opacity-50">
      <div class="w-96 p-4 bg-white border border-gray-300 rounded-lg shadow-md">
        <h2 class="text-xl font-bold mb-4">Download Day-wise Data</h2>
        <div class="mb-4">
          <label for="machineName" class="block mb-2">Machine Name</label>
          <select id="machineName" v-model="selectedMachine" class="border p-2 rounded-md w-full">
            <option v-for="machine in machineIds" :key="machine" :value="machine">{{ machine }}</option>
          </select>
        </div>
        <div class="mb-4">
          <label for="selectedDate" class="block mb-2">Date &</label>
          <input type="datetime-local" id="selectedDate" v-model="selectedDate" class="border p-2 rounded-md w-full" />
        </div>

          <!-- <div class="mb-4">
          <label for="selectedDate" class="red-text" sclass="block mb-2">Start Date:</label>
          <input type="date" id="selectedDate" v-model="selectedDate" class="border border-gray-300 rounded-lg px-2 py-1">
        </div> -->

        <div class="flex justify-end">
          <button @click="downloadDaywiseData" class="bg-blue-500 text-white px-4 py-2 rounded-lg mr-2">Submit</button>
          <button @click="closeDaywisePopup" class="bg-gray-500 text-white px-4 py-2 rounded-lg">Cancel</button>
        </div>
      </div>
      </div>
  <div v-if="alertMessage" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="w-96 p-4 bg-gray-100 border text-center border-gray-300 rounded-lg shadow-md">
      <p class="text-center text-xl text-green-600">{{ alertMessage }}</p>
      <button @click="closeAlert" class="bg-blue-500 text-white px-2 py-1 rounded-lg mt-2">OK</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed  } from 'vue';
import axios from 'axios';
import * as XLSX from 'xlsx';

const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return null;

  const date = new Date(dateTimeString);
  const formattedDate = `${('0' + date.getDate()).slice(-2)}-${('0' + (date.getMonth() + 1)).slice(-2)}-${date.getFullYear()}`;
  const formattedTime = `${('0' + date.getHours()).slice(-2)}:${('0' + date.getMinutes()).slice(-2)}:${('0' + date.getSeconds()).slice(-2)}`;

  return `${formattedDate} ${formattedTime}`;
};


// Pagination variables
const currentPage = ref(1);
const itemsPerPage = 6; // Number of items per page
const paginatedValues = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  return filteredValues.value.slice(startIndex, startIndex + itemsPerPage);
});
const totalPages = computed(() => Math.ceil(filteredValues.value.length / itemsPerPage));

// Pagination methods
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

// New reactive variables for the popup
const showDaywisePopup = ref(false);
const machineIds = ref([]);
const selectedMachine = ref(null);
const selectedDate = ref(null);


// Method to show the popup
const showDownloadDaywisePopup = () => {
  showDaywisePopup.value = true;
  fetchMachineNames();
};

// Method to close the popup
const closeDaywisePopup = () => {
  showDaywisePopup.value = false;
  selectedMachine.value = null;
  selectedDate.value = null;
};

// Method to fetch machine names
const fetchMachineNames = async () => {
  const machinesUrl = 'http://172.18.100.54:6969/machines';
  try {
    const response = await axios.get(machinesUrl);
    machineIds.value = response.data.Data.map((machine) => machine.machine_id);
  } catch (error) {
    console.error('Error fetching machine names:', error);
  }
};

// Method to download day-wise data
// const downloadDaywiseData = async () => {
//   if (!selectedMachine.value || !selectedDate.value) {
//     showAlert('Please select both machine and date.');
//     return;
//   }

//   const url = `http://172.18.100.54:6969/production_data/live_data/?date=${selectedDate.value}&machine_id=${selectedMachine.value}`;
//   try {
//     const response = await axios.get(url);
//     if (response.data && Array.isArray(response.data) && response.data.length > 0) {
//       const ws = XLSX.utils.json_to_sheet(response.data);
//       const wb = XLSX.utils.book_new();
//       XLSX.utils.book_append_sheet(wb, ws, 'Day-wise Data');
//       XLSX.writeFile(wb, 'daywise_data.xlsx');
//       showAlert('Data downloaded successfully.');
//     } else {
//       showAlert('No data found for the selected machine and date.');
//     }
//   } catch (error) {
//     console.error('Error downloading day-wise data:', error);
//     showAlert('There was an issue retrieving the data. Please try again.');
//   } finally {
//     closeDaywisePopup();
//   }
// };
const convertToLocalEpochTime = (selectedDateTime) => {
  // Parse the selected date/time in local time
  const localDate = new Date(selectedDateTime);
  
  // Get the Epoch time in milliseconds
  const epochTime = localDate.getTime();
  
  // Get the timezone offset in minutes and convert to seconds
  const timezoneOffsetSeconds = localDate.getTimezoneOffset() * 60;
  
  // Convert to local Epoch time by subtracting the timezone offset
  const localEpochTime = Math.floor((epochTime / 1000) - timezoneOffsetSeconds);
  
  return localEpochTime;
};



const downloadDaywiseData = async () => {
  if (!selectedMachine.value || !selectedDate.value) {
    showAlert('Please select both machine and date.');
    return;
  }

  // Convert selectedDate to Epoch time in local timezone
  const epochLocalTime = convertToLocalEpochTime(selectedDate.value);

  // Construct URL with epochLocalTime and machine ID
  const url = `http://172.18.100.54:6969/production_data/live-data/?start_time=${epochLocalTime}&machine_id=${encodeURIComponent(selectedMachine.value)}&skip=0&limit=5000`;

  try {
    const response = await axios.get(url);
    if (response.data && Array.isArray(response.data) && response.data.length > 0) {
      const ws = XLSX.utils.json_to_sheet(response.data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Day-wise Data');
      XLSX.writeFile(wb, 'daywise_data.xlsx');
      showAlert('Data downloaded successfully.');
    } else {
      showAlert('No data found for the selected machine and date.');
    }
  } catch (error) {
    console.error('Error downloading day-wise data:', error);
    showAlert('There was an issue retrieving the data. Please try again.');
  } finally {
    closeDaywisePopup();
  }
};



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

//to removed range here 
const parameters = ["start_time", "end_time", "machine_id", "type",  "welder_name", "project", "I_no", "Fc_no", "plate_thickness", "plate_description","standard_current","standard_voltage","average_current","average_voltage","min_current","max_current","min_voltage","max_voltage"];
const parametersAll = ["start_time", "end_time", "machine_id", "type", "welder_name", "project", "I_no", "Fc_no", "plate_thickness", "plate_description"];
const filteredValues = ref([]);
const availableOptions = ref({});

const fetchDataForParameters = async () => {
  try {
    const endpoints = {
      plate_thickness: 'http://172.18.100.54:6969/elements',
      // range: 'http://172.18.100.54:6969/elements',
      machine_id: 'http://172.18.100.54:6969/machines',
      welder_name: 'http://172.18.100.54:6969/welder/',
      project: 'http://172.18.100.54:6969/op_shift/',
      I_no: 'http://172.18.100.54:6969/op_shift/',
      Fc_no: 'http://172.18.100.54:6969/op_shift/',
      type: 'http://172.18.100.54:6969/elements',
      standard_current: 'http://172.18.100.54:6969/elements',
      standard_voltage: 'http://172.18.100.54:6969/elements',
      plate_thickness: 'http://172.18.100.54:6969/plate/plate',
      plate_description: 'http://172.18.100.54:6969/plate/plate',
    };

    for (const param in endpoints) {
      const response = await axios.get(endpoints[param]);
      availableOptions.value[param] = extractOptions(response.data, param);
    }
    // availableOptions.value['range'] = Array.from(new Set(availableOptions.value['range']));
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
    const response = await axios.get('http://172.18.100.54:6969/excel/', { params: formData.value });

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
