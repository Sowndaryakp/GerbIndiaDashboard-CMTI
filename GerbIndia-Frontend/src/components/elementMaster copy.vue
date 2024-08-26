<template>
  <div>
    <div class="flex">
<!--add element type-->
<button @click="showElementForm"
        class="bg-blue-500 glassmorphic-button rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
        Add Element Type
      </button>
      </div>
    <div class="container mx-auto" ref="reportContainerTable">
      <h1 class="text-2xl font-semibold my-4">Element Data</h1>
      <table class="table-auto border-collapse w-full">
        <thead>
          <tr>
            <th v-for="(header, index) in tableHeaders" :key="index" class="px-4 py-2">{{ header }}</th>
            <th class="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in tableData" :key="index">
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.type }}</span>
              <input v-else v-model="data.type" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" disabled/>
            </td>
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.range }}</span>
              <input v-else v-model="data.range" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" />
            </td>
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.standard_current }}</span>
              <input v-else v-model="data.standard_current" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" />
            </td>
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.standard_voltage }}</span>
              <input v-else v-model="data.standard_voltage" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" />
            </td>
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.element_description }}</span>
              <input v-else v-model="data.element_description" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" />
            </td>
            <!-- <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.plate_thickness }}</span>
              <input v-else v-model="data.plate_thickness" class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
            </td>
            <td class="border px-4 py-2">
              <span v-if="!data.isEditing">{{ data.plate_description }}</span>
              <input v-else v-model="data.plate_description" class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
            </td> -->
            <td class="border px-4 py-2 flex">
              <button v-if="!data.isEditing" @click="toggleEdit(index)" class="bg-blue-500 glassmorphic-button text-white px-2 py-1 rounded-lg mr-2">Edit</button>
              <button v-else @click="saveEditedElement(index)" class="bg-green-500 glassmorphic-button text-white px-2 py-1 rounded-lg mr-2">Save</button>
              <button @click="deleteElement(data)" class="bg-red-500 glassmorphic-button text-white font-bold py-2 px-4 rounded">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="isElementForm" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
        <form @submit.prevent="submitElementForm">
          <div class="mb-2">
            <label class="block text-gray-800">Type:</label>
            <input v-model="elementType" type="text" id="elementType" class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="Enter element type" />
            <!-- Validation Message for Type -->
            <div v-if="showTypeValidation" class="text-red-500">{{ typeValidationMessage }}</div>
          </div>

          <div class="mb-2">
            <label class="block text-gray-800">Range:</label>
            <input v-model="elementRange" type="text" id="elementRange" class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="Enter element range"/>
            <!-- Validation Message for Range -->
            <div v-if="showRangeValidation" class="text-red-500">{{ rangeValidationMessage }}</div>
          </div>

          <div class="mb-2">
            <label class="block text-gray-800">Current:</label>
            <input v-model="elementCurrent" type="text" id="elementCurrent" class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="Enter current" />
            <!-- Validation Message for Current -->
            <div v-if="showCurrentValidation" class="text-red-500">{{ currentValidationMessage }}</div>
          </div>

          <div class="mb-2">
            <label class="block text-gray-800">Voltage:</label>
            <input v-model="elementVoltage" type="text" id="elementVoltage" class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="Enter voltage" />
            <!-- Validation Message for Voltage -->
            <div v-if="showVoltageValidation" class="text-red-500">{{ voltageValidationMessage }}</div>
          </div>

          <div class="mt-2 flex justify-end">
            <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Create</button>
            <button @click="cancelElementForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
          </div>
        </form>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const isElementForm = ref(false);
const elementType = ref('');
const elementRange = ref('');
const elementCurrent = ref('');
const elementVoltage = ref('');
const elementDescription = ref('');
const elementPlateThickness = ref('');
const elementPlateDescription = ref('');


const showTypeValidation = ref(false);
const showRangeValidation = ref(false);
const showCurrentValidation = ref(false);
const showVoltageValidation = ref(false);

const typeValidationMessage = ref('');
const rangeValidationMessage = ref('');
const currentValidationMessage = ref('');
const voltageValidationMessage = ref('');

const validateForm = () => {
  // Clear previous validation messages
  clearValidationMessages();

  // Validate Type
  if (!/^[A-Za-z]+-\w+$/.test(elementType)) {
    showTypeValidation.value = true;
    typeValidationMessage.value = "Type should be in the format 'Type-xx'.";
    return false;
  }

  // Validate Range
  if (!/^[A-Za-z]+$/.test(elementRange)) {
    showRangeValidation.value = true;
    rangeValidationMessage.value = "Range should be in string format.";
    return false;
  }

  // Validate Current
  if (!/^\d{3}-\d{3}$/.test(elementCurrent)) {
    showCurrentValidation.value = true;
    currentValidationMessage.value = "Current should be in the format '123-234'.";
    return false;
  }

  // Validate Voltage
  if (!/^\d{2}-\d{2}$/.test(elementVoltage)) {
    showVoltageValidation.value = true;
    voltageValidationMessage.value = "Voltage should be in the format '12-34'.";
    return false;
  }

  // If all validations pass, return true
  return true;
};

const clearValidationMessages = () => {
  showTypeValidation.value = false;
  showRangeValidation.value = false;
  showCurrentValidation.value = false;
  showVoltageValidation.value = false;

  typeValidationMessage.value = '';
  rangeValidationMessage.value = '';
  currentValidationMessage.value = '';
  voltageValidationMessage.value = '';
};

const showElementForm = () => {
  isElementForm.value = true;
};
const cancelElementForm = () => {
  isElementForm.value = false;
  resetFormFields();
};
const resetFormFields = () => {
  elementType.value = '';
  elementRange.value = '';
  elementCurrent.value = '';
  elementVoltage.value = '';
  elementDescription.value = '';
  elementPlateThickness.value = '',
  elementPlateDescription.value = ''
};
const submitElementForm = async () => {
  if (validateForm()) {
  try {
    // Prepare the data to be sent to the backend
    const formData = {
      type: elementType.value,
      range: elementRange.value,
      standard_current: elementCurrent.value,
      standard_voltage: elementVoltage.value,
      element_description:  "N/A",
      plate_thickness:  "N/A",
      plate_description:  "N/A",
    };

    // Make the HTTP POST request to your FastAPI backend
    const response = await axios.post('http://192.168.0.105:6969/elements/', formData);

    // Handle the response as needed
    console.log('Element created successfully:', response.data);

    // Reset form fields and hide the form
    resetFormFields();
    isElementForm.value = false;
    fetchData();
  } catch (error) {
    console.error('Error creating element:', error);
  }
}
};
onMounted(() => {
  submitElementForm();
});



const tableHeaders = ["Type", "Range", "Standard Current", "Standard Voltage", "Element Description", ];

const tableData = ref([]);

const fetchData = async () => {
  try {
    const response = await fetch("http://192.168.0.105:6969/elements");
    const result = await response.json();
    tableData.value = result.Data.map(data => ({ ...data, isEditing: false }));
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

onMounted(() => {
  fetchData();
});

const toggleEdit = (index) => {
  tableData.value[index].isEditing = !tableData.value[index].isEditing;
};

const saveEditedElement = async (index) => {
  const editedElement = tableData.value[index];
  
  const postData = {
    range: editedElement.range || 'N/A',
    standard_current: editedElement.standard_current || 'N/A',
    standard_voltage: editedElement.standard_voltage || 'N/A',
    plate_thickness: editedElement.plate_thickness || 'N/A',
    plate_description: editedElement.plate_description || 'N/A',
    element_description: editedElement.element_description || 'N/A',
  };

  try {
    const url = `http://192.168.0.105:6969/elements/${editedElement.type}`;
    await axios.put(url, postData);

    tableData.value[index].isEditing = false;
  } catch (error) {
    console.error('Error updating the element data:', error);
  }
};

const deleteElement = async (element) => {
  try {
    const url = `http://192.168.0.105:6969/elements/${element.type}`;
    await axios.delete(url);

    tableData.value = tableData.value.filter(data => data.id !== element.id);
  } catch (error) {
    console.error('Error deleting the element:', error);
  }
};
</script>

<style scoped>
/* Add your scoped styles here */
</style>
