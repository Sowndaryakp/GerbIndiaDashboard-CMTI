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
              <input v-model="elementType" type="text" id="elementType"  class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter element type" />
            </div>

            <div class="mb-2">
              <label class="block text-gray-800">Range:</label>
              <input v-model="elementRange" type="text" id="elementRange"  class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter element range"/>
            </div>
            <div class="mb-2">
          <label class="block text-gray-800">Current:</label>
          <input v-model="elementCurrent" type="text" id="elementCurrent" @input="validateStandardCurrent" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter current"/>
          <div v-if="currentError" class="text-red-600">{{ currentError }}</div>
        </div>
            <div class="mb-2">
              <label class="block text-gray-800">Voltage:</label>
              <input v-model="elementVoltage" type="text" id="elementVoltage" @input="validateStandardVoltage" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter voltage"/>
              <div v-if="voltageError" class="text-red-600">{{ voltageError }}</div>
            </div>
            <!-- <div class="mb-2">
              <label class="block text-gray-800">Element Description:</label>
              <textarea v-model="elementDescription" id="elementDescription" required class="border border-gray-300 px-1 py-1 rounded-md w-80" placeholder="enter Element Description"></textarea>
            </div> -->
            <div class="mt-2 flex justify-end">
              <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Create</button>
              <button @click="cancelElementForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div v-if="alertMessage" class="fixed inset-0 flex items-center justify-center z-50 ">
    <div class="w-96 p-4 bg-gray-100 border text-center border-gray-300 rounded-lg shadow-md">
      <p class="text-center text-red-600">{{ alertMessage }}</p>
      <button @click="closeAlert" class="bg-blue-500 text-white px-2 py-1 rounded-lg mt-2 ">OK</button>
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

const alertMessage = ref('');

const showAlert = (message) => {
  alertMessage.value = message;
};

const closeAlert = () => {
  alertMessage.value = '';
};

const currentError = ref('');

const validateStandardCurrent = () => {
  const currentPattern = /^\d{3}-\d{3}$|^\d{2}-\d{3}$/; // Regex pattern for the format 123-345

  if (!currentPattern.test(elementCurrent.value)) {
    currentError.value = 'You have to enter the format as 123-345 or 12-345';
  } else {
    currentError.value = '';
  }
};

const voltageError = ref('');

const validateStandardVoltage = () => {
  const voltagePattern = /^\d{2}-\d{2}$|^\d{2}-\d{3}$/; // Regex pattern for the format 123-345

  if (!voltagePattern.test(elementVoltage.value)) {
    voltageError.value = 'You have to enter the format as 12-34 or 12-345  ';
  } else {
    voltageError.value = '';
  }
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
  try {
    validateStandardCurrent(); // Validate current format
    validateStandardVoltage(); // Validate voltage format

    if (currentError.value || voltageError.value) {
      // If there are validation errors, do not proceed with form submission
      return;
    }
    // Prepare the data to be sent to the backend
    const formData = {
      type: elementType.value,
      range: elementRange.value,
      standard_current: elementCurrent.value,
      standard_voltage: elementVoltage.value,
      element_description: "N/A",
      plate_thickness: "N/A",
      plate_description: "N/A",
    };

    // Make the HTTP POST request to your FastAPI backend
    const response = await axios.post('http://192.168.0.105:6969/elements/', formData);

    // Handle the response as needed
    console.log('Element created successfully:', response.data);
    alertMessage.value = `Element ${elementType.value} created successfully`;

    // Reset form fields and hide the form
    resetFormFields();
    isElementForm.value = false;

    // Fetch data to update the table
    fetchData();
  }catch (error) {
    if (error.response && error.response.status === 400) {
      // If the server responds with a 400 Bad Request status code,
      // extract and display the error message from the response body
      const errorMessage = error.response.data.detail;
      alertMessage.value = `Error creating element: ${errorMessage}`;
    } else if (error.response && error.response.status === 422) {
      // If the server responds with a 422 Unprocessable Entity status code,
      // extract and display the error message from the response body
      const errorMessage = error.response.data.detail;

      // Check if the error message indicates that the element already exists
      if (errorMessage.includes("Element with type")) {
        alertMessage.value = errorMessage;
      } else {
        // Handle other validation errors
        alertMessage.value = ` ${errorMessage}`;
      }
    } else {
      // Handle other errors
      alertMessage.value =  error.message;
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
    alertMessage.value = `Element ${editedElement.type} Edited successfully`;
    await axios.put(url, postData);
   
    tableData.value[index].isEditing = false;
  } catch (error) {
    console.error('Error updating the element data:', error);
  }
};

const deleteElement = async (element) => {
  try {
    const url = `http://192.168.0.105:6969/elements/${element.type}`;
    alertMessage.value = `Element ${element} Deleted successfully`;
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
