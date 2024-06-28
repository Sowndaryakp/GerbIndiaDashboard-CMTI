<template>
  <div>
    <div class="flex">
      <div class="flex mb-2 mt-24">
        <button @click="showWelderForm" class="bg-blue-500 glassmorphic-button rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
          <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
          Add Welder
        </button>
      </div>
    </div>
    <div class="container mx-auto" ref="reportContainerTable">
      <h1 class="text-2xl font-semibold my-4">Welder Data</h1>
      <table class="table-auto border-collapse w-full">
        <thead>
          <tr>
            <th v-for="(header, index) in tableHeaders" :key="index" class="px-4 py-2">{{ header }}</th>
            <th class="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in paginatedData" :key="index">
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.welder_name }}</span>
              <input v-else v-model="data.welder_name" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" disabled />
            </td>
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.welder_number }}</span>
              <input v-else v-model="data.welder_number" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" disabled />
            </td>
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.date_of_joining }}</span>
              <input v-else v-model="data.date_of_joining" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" />
            </td>
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.welder_qualification }}</span>
              <input v-else v-model="data.welder_qualification" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" />
            </td>
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.qualified_thickness }}</span>
              <input v-else v-model="data.qualified_thickness" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" />
            </td>
            <td class="border px-4 py-2 flex">
              <button v-if="!data.isEditing" @click="toggleEdit(index)" class="bg-blue-500 glassmorphic-button text-white px-2 py-1 rounded-lg mr-2">Edit</button>
              <button v-else @click="saveEditedWelder(index)" class="bg-green-500 glassmorphic-button text-white px-2 py-1 rounded-lg mr-2">Save</button>
              <button @click="deleteWelder(data)" class="bg-red-500 glassmorphic-button text-white font-bold py-2 px-4 rounded">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="flex justify-center items-center mt-4">
        <button @click="prevPage" :disabled="currentPage === 1" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg mr-2">Previous</button>
        <span class="text-gray-700 mx-2">Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Next</button>
      </div>
      <div v-if="isWelderForm" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
          <form @submit.prevent="submitWelderForm">
            <div class="mb-2">
              <label class="block text-gray-800">Welder Name:</label>
              <input v-model="welderName" type="text" id="welderName" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter welder name" />
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Welder Number:</label>
              <input v-model="welderNumber" type="text" id="welderNumber" @input="validateWelderNumber" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter welder number" />
              <div v-if="welderNumberError" class="text-red-600">{{ welderNumberError }}</div>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Date Of Joining:</label>
              <input v-model="dateOfJoining" type="date" id="dateOfJoining" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter date of joining" />
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Welder Qualification:</label>
              <input v-model="welderQualification" type="text" id="welderQualification" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter welder qualification" />
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Qualified Thickness:</label>
              <input v-model="qualifiedThickness" type="text" id="qualifiedThickness" @input="validateQualifiedThickness" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter qualified thickness" />
              <div v-if="qualifiedThicknessError" class="text-red-600">{{ qualifiedThicknessError }}</div>
            </div>
            <div class="mt-2 flex justify-end">
              <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Create</button>
              <button @click="cancelWelderForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div v-if="alertMessage" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="w-96 p-4 bg-gray-100 border text-center border-gray-300 rounded-lg shadow-md">
      <p class="text-center text-green-600">{{ alertMessage }}</p>
      <button @click="closeAlert" class="bg-blue-500 text-white px-2 py-1 rounded-lg mt-2">OK</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// Define reactive references for component state
const isComponentMounted = ref(false);
const tableHeaders = ["Welder Name", "Welder Number", "Date of Joining", "Welder Qualification", "Qualified Thickness"];
const tableData = ref([]);
const isWelderForm = ref(false);
const welderName = ref('');
const welderNumber = ref('');
const dateOfJoining = ref('');
const welderQualification = ref('');
const qualifiedThickness = ref('');
const welderNumberError = ref('');
const qualifiedThicknessError = ref('');
const alertMessage = ref('');
const itemsPerPage = ref(9); // Number of items to display per page
const currentPage = ref(1);

const validateWelderNumber = () => {
  const welderNumberPattern = /^\d+$/; // Regex pattern for digits only
  if (!welderNumberPattern.test(welderNumber.value)) {
    welderNumberError.value = 'Welder number must contain only digits';
  } else {
    welderNumberError.value = '';
  }
};

const validateQualifiedThickness = () => {
  const thicknessPattern = /^\d+(\.\d+)?$/; // Regex pattern for digits (with optional decimal part)
  if (!thicknessPattern.test(qualifiedThickness.value)) {
    qualifiedThicknessError.value = 'Qualified thickness must be a valid number';
  } else {
    qualifiedThicknessError.value = '';
  }
};

const showAlert = (message) => {
  alertMessage.value = message;
};

const closeAlert = () => {
  alertMessage.value = '';
};

const showWelderForm = () => {
  isWelderForm.value = true;
};

const cancelWelderForm = () => {
  isWelderForm.value = false;
  resetWelderFormFields();
};

const resetWelderFormFields = () => {
  welderName.value = '';
  welderNumber.value = '';
  dateOfJoining.value = '';
  welderQualification.value = '';
  qualifiedThickness.value = '';
};

const paginatedData = computed(() => {
  const sortedData = tableData.value.sort((a, b) => a.welder_name.localeCompare(b.welder_name));
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return sortedData.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(tableData.value.length / itemsPerPage.value);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value += 1;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value -= 1;
  }
};

const submitWelderForm = async () => {
  try {
    const welderNumberValue = Number(welderNumber.value);
    const qualifiedThicknessValue = Number(qualifiedThickness.value);

    if (isNaN(welderNumberValue) || isNaN(qualifiedThicknessValue)) {
      showAlert("Welder Number and Qualified Thickness must be valid numbers.");
      return;
    }

    const formData = {
      welder_name: welderName.value,
      welder_number: welderNumber.value,
      date_of_joining: dateOfJoining.value,
      welder_qualification: welderQualification.value,
      qualified_thickness: qualifiedThickness.value,
    };

    const response = await axios.post('http://172.18.100.33:6969/welder/', formData);

    alertMessage.value = `Welder ${welderName.value} created successfully`;
    resetWelderFormFields();
    isWelderForm.value = false;
    fetchData();
  } catch (error) {
    if (error.response && error.response.status === 400) {
      alertMessage.value = error.response.data.detail;
    } else if (error.response && error.response.status === 422) {
      alertMessage.value = error.response.data.detail;
    } else {
      alertMessage.value = error.message;
    }
  }
};

onMounted(() => {
  if (!isComponentMounted.value) {
    fetchData();
    isComponentMounted.value = true;
  }
});

const fetchData = async () => {
  try {
    const response = await fetch("http://172.18.100.33:6969/welder/", {
      redirect: 'follow',
    });
    const result = await response.json();
    tableData.value = result.map(data => ({ ...data, isEditing: false }));
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

const toggleEdit = (index) => {
  const globalIndex = (currentPage.value - 1) * itemsPerPage.value + index;
  tableData.value[globalIndex].isEditing = !tableData.value[globalIndex].isEditing;
};

const saveEditedWelder = async (index) => {
  const globalIndex = (currentPage.value - 1) * itemsPerPage.value + index;
  const editedWelder = tableData.value[globalIndex];

  const postData = {
    welder_name: editedWelder.welder_name || 'N/A',
    welder_number: editedWelder.welder_number || 'N/A',
    date_of_joining: editedWelder.date_of_joining || 'N/A',
    welder_qualification: editedWelder.welder_qualification || 'N/A',
    qualified_thickness: editedWelder.qualified_thickness || 'N/A',
  };

  try {
    const url = `http://172.18.100.33:6969/welder/${editedWelder.welder_name}?welder_number=${editedWelder.welder_number}`;
    alertMessage.value = `Welder "${editedWelder.welder_name}" edited successfully`;
    await axios.put(url, postData);
    tableData.value[globalIndex].isEditing = false;
    // fetchData();
  } catch (error) {
    console.error('Error updating the welder data:', error);
  }
};

const deleteWelder = async (welder) => {
  try {
    const url = `http://172.18.100.33:6969/welder/${welder.welder_name}?welder_number=${welder.welder_number}`;
    alertMessage.value = `Welder "${welder.welder_name}" deleted successfully`;
    await axios.delete(url);
    fetchData();
  } catch (error) {
    console.error('Error deleting the welder:', error);
  }
};
</script>

<style scoped>
/* Add your scoped styles here */
</style>
