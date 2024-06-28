<template>
  <div>
    <div class="flex">
      <div class="flex mb-2 mt-16">
        <button @click="showElementForm"
          class="bg-blue-500 glassmorphic-button rounded-lg px-4 py-2 mt-10 mb-2 ml-3 text-white font-poppins flex flex-wrap">
          <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
          Add Element Type
        </button>
      </div>
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
          <tr v-for="(data, index) in paginatedData" :key="index">
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
            <td class="border px-4 py-2 flex">
              <button v-if="!data.isEditing" @click="toggleEdit(index)" class="bg-blue-500 glassmorphic-button text-white px-2 py-1 rounded-lg mr-2">Edit</button>
              <button v-else @click="saveEditedElement(index)" class="bg-green-500 glassmorphic-button text-white px-2 py-1 rounded-lg mr-2">Save</button>
              <button @click="deleteElement(data)" class="bg-red-500 glassmorphic-button text-white font-bold py-2 px-4 rounded">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="flex justify-center items-center mt-4">
        <button @click="prevPage" :disabled="currentPage === 1" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg mr-2">Previous</button>
        <span class="text-gray-700 mx-2">Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Next</button>
      </div>
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
              <div v-if="elementCurrent && currentError" class="text-red-600">{{ currentError }}</div>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Voltage:</label>
              <input v-model="elementVoltage" type="text" id="elementVoltage" @input="validateStandardVoltage" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter voltage"/>
              <div v-if="elementVoltage && voltageError" class="text-red-600">{{ voltageError }}</div>
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
  <div v-if="alertMessage" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="w-96 p-4 bg-gray-100 border text-center border-gray-300 rounded-lg shadow-md">
      <p class="text-center text-xl text-green-600">{{ alertMessage }}</p>
      <button @click="closeAlert" class="bg-blue-500 text-white px-2 py-1 rounded-lg mt-2">OK</button>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const isComponentMounted = ref(false);
const tableHeaders = ["Type", "Range", "Standard Current", "Standard Voltage", "Element Description"];
const tableData = ref([]);
const isElementForm = ref(false);
const elementType = ref('');
const elementRange = ref('');
const elementCurrent = ref('');
const elementVoltage = ref('');
const elementDescription = ref('');
const alertMessage = ref('');
const itemsPerPage = ref(9);
const currentPage = ref(1);
const currentError = ref('');
const voltageError = ref('');

const showAlert = (message) => {
  alertMessage.value = message;
};

const closeAlert = () => {
  alertMessage.value = '';
};

const validateStandardCurrent = () => {
  const currentPattern = /^\d{3}-\d{3}$|^\d{2}-\d{3}$/;
  if (!currentPattern.test(elementCurrent.value)) {
    currentError.value = 'You have to enter the format as 123-345 or 12-345';
  } else {
    currentError.value = ''; // Reset the error message if the input is correct
  }
};

const validateStandardVoltage = () => {
  const voltagePattern = /^\d{2}-\d{2}$/;
  if (!voltagePattern.test(elementVoltage.value)) {
    voltageError.value = 'You have to enter the format as 12-34';
  } else {
    voltageError.value = ''; // Reset the error message if the input is correct
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
};

const submitElementForm = async () => {
  try {
    validateStandardCurrent();
    validateStandardVoltage();

    if (currentError.value || voltageError.value) {
      return; // Do not proceed with form submission if there are validation errors
    }

    const formData = {
      type: elementType.value,
      range: elementRange.value,
      standard_current: elementCurrent.value,
      standard_voltage: elementVoltage.value,
      element_description: "N/A",
    };

    const response = await axios.post('http://172.18.100.33:6969/elements/', formData);
    alertMessage.value = `Element ${elementType.value} created successfully`;

    resetFormFields();
    isElementForm.value = false;
    fetchData();
  } catch (error) {
    handleErrorResponse(error);
  }
};

const fetchData = async () => {
  try {
    const response = await fetch("http://172.18.100.33:6969/elements");
    const result = await response.json();
    tableData.value = result.Data.map(data => ({ ...data, isEditing: false }));
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

onMounted(() => {
  if (!isComponentMounted.value) {
    fetchData();
    isComponentMounted.value = true;
  }
});

const toggleEdit = (index) => {
  const globalIndex = (currentPage.value - 1) * itemsPerPage.value + index;
  tableData.value[globalIndex].isEditing = !tableData.value[globalIndex].isEditing;
};

// const saveEditedElement = async (index) => {
//   const globalIndex = (currentPage.value - 1) * itemsPerPage.value + index;
//   const editedElement = tableData.value[globalIndex];

//   const postData = {
//     range: editedElement.range || 'N/A',
//     standard_current: editedElement.standard_current || 'N/A',
//     standard_voltage: editedElement.standard_voltage || 'N/A',
//     element_description: editedElement.element_description || 'N/A',
//   };

//   try {
//     const url = `http://172.18.100.33:6969/elements/${editedElement.type}`;
//     await axios.put(url, postData);
//     tableData.value[globalIndex].isEditing = false;
//     alertMessage.value = `Element ${editedElement.type} edited successfully`;
//   } catch (error) {
//     console.error('Error updating the element data:', error);
//   }
// };



const saveEditedElement = async (index) => {
  const globalIndex = (currentPage.value - 1) * itemsPerPage.value + index;
  const editedElement = tableData.value[globalIndex];

  const postData = {
    range: editedElement.range || 'N/A',
    standard_current: editedElement.standard_current || 'N/A',
    standard_voltage: editedElement.standard_voltage || 'N/A',
    element_description: editedElement.element_description || 'N/A',
  };

  try {
    let convertedstring = editedElement.type
    const encodedString = encodeURIComponent(convertedstring);
    const url = `http://172.18.100.33:6969/elements/type?string=${encodedString}&encoding=utf-8&errors=replace`;

    // const url = `http://172.18.100.33:6969/elements/${encodedString}`;
    await axios.put(url, postData);
    tableData.value[globalIndex].isEditing = false;
    alertMessage.value = `Element ${editedElement.type} edited successfully`;
  } catch (error) {
    console.error('Error updating the element data:', error);
  }
};


// const deleteElement = async (element) => {
//   try {
//     const url = `http://172.18.100.33:6969/elements/${element.type}`;
//     await axios.delete(url);
//     tableData.value = tableData.value.filter(data => data.type !== element.type);
//     alertMessage.value = `Element ${element.type} deleted successfully`;
//   } catch (error) {
//     console.error('Error deleting the element:', error);
//   }
// };

const deleteElement = async (element) => {
  try {
    // Encode the type parameter
    const encodedType = encodeURIComponent(element.type);
    // Construct the URL with the encoded type in the query string
    const url = `http://172.18.100.33:6969/elements/type?string=${encodedType}&encoding=utf-8&errors=replace`;
    await axios.delete(url);
    // Update the table data by removing the deleted element
    tableData.value = tableData.value.filter(data => data.type !== element.type);
    alertMessage.value = `Element ${element.type} deleted successfully`;
  } catch (error) {
    console.error('Error deleting the element:', error);
  }
};



const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return tableData.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(tableData.value.length / itemsPerPage.value);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const handleErrorResponse = (error) => {
  if (error.response) {
    const { status, data } = error.response;
    if (status === 400) {
      alertMessage.value = data.detail;
    } else if (status === 422) {
      alertMessage.value = data.detail.includes("Element with type") ? data.detail : `Validation Error: ${data.detail}`;
    } else {
      alertMessage.value = error.message;
    }
  } else {
    alertMessage.value = error.message;
  }
};
</script>

<style scoped>
/* Add your scoped styles here */
</style>
