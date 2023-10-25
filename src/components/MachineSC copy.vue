<template>
  <div>
    <div class="flex">
      <!-- Add a button to open the "Create" form -->
      <button @click="showCreateForm"
        class="bg-blue-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
        Add Machine
      </button>
    </div>

    <div class="container mx-auto">
      <h1 class="text-2xl font-semibold my-4">Machine Data</h1>
      <table class="table-auto border-collapse w-full">
        <thead>
          <tr>
            <th v-for="(header, index) in tableHeaders" :key="index" class="px-4 py-2">{{ header }}</th>
            <th class="px-4 py-2">Actions</th> <!-- Added Actions column -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in tableData" :key="index">
            <td class="border px-4 py-2">{{ data.machine_name }}</td>
            <td class="border px-4 py-2">{{ data.element_type }}</td>
            <td class="border px-4 py-2">{{ data.operator_name }}</td>
            <td class="border px-4 py-2">{{ data.start_time }}</td>
            <td class="border px-4 py-2">{{ data.end_time }}</td>
            <td class="border px-4 py-2">{{ data.shift }}</td>
            <td class="border px-4 py-2">
              <button @click="editMachine(index)" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Edit</button>
              <button @click="deleteData(data.machine_name, data.start_time, data.end_time)"
                class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="isFormVisible" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
          <h2 class="text-lg font-semibold text-gray-800">{{ isEditMode ? 'Edit Machine' : 'Create Machine' }}</h2>
          <form @submit.prevent="saveMachine">
            <div class="mb-2">
              <label class="block text-gray-800">Machine Name:</label>
              <select v-model="formData.machineName" required class="border border-gray-300 rounded-lg px-2 py-1 w-full"
                @click="fetchMachineNames">
                <option value="">Select Machine Name</option>
                <option v-for="machineId in machineIds" :key="machineId">{{ machineId }}</option>
              </select>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">element_type:</label>
              <select v-model="formData.element_type" required class="border border-gray-300 rounded-lg px-2 py-1 w-full"
                @click="fetchElementTypes">
                <option value="">Select Element Type</option>
                <option v-for="elementType in elementTypes" :key="elementType">{{ elementType }}</option>
              </select>
            </div>

            <!-- <div class="mb-2">
    <label class="block text-gray-800">operator_name:</label>
    <select v-model="formData.operator_name" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" @click="fetchOperators">
      <option value="">Select Operator Type</option>
      <option v-for="operator in operators" :key="operator" >{{ operator }} </option>
    </select>
  </div> -->

            <div class="mb-2">
              <label class="block text-gray-800">Operator ID:</label>
              <select v-model="formData.operator_id" required class="border border-gray-300 rounded-lg px-2 py-1 w-full"
                @click="fetchOperatorIds">
                <option value="">Select Operator ID</option>
                <option v-for="operatorId in operatorIds" :key="operatorId">{{ operatorId }} </option>
              </select>
            </div>

            <div class="mb-2">
              <label class="block text-gray-800">start_time:</label>
              <input v-model="startDateTime" type="datetime-local" required
                class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
            </div>

            <div class="mb-2">
              <label class="block text-gray-800">end_time:</label>
              <input v-model="endDateTime" type="datetime-local" required
                class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
            </div>

            <div class="mb-2">
              <label class="block text-gray-800">Shift:</label>
              <select v-model="formData.shift" required class="border border-gray-300 rounded-lg px-2 py-1 w-full"
                @click="fetchShiftTypes">
                <option value="">Select Shift</option>
                <option v-for="shiftType in shiftTypes" :key="shiftType">{{ shiftType }}</option>
              </select>
            </div>

            <div class="mt-2 flex justify-end">
              <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">{{ isEditMode ? 'Update' :
                'Create' }}</button>
              <button @click="cancelForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { computed } from 'vue';
import moment from 'moment';

const machineNames = ['7D', '7F', '7G', '7H', '7I', '7J', '7K', '7L', '27B', '27C', '28D', '28E'];
// const elementTypes = ['type-1', 'type-2', 'type-3'];
const isFormVisible = ref(false);
const isEditMode = ref(false);
const formData = reactive({
  machineName: '',
  element_type: '',
  operator_name: '',
  operator_id: '',
  start_time: '',
  end_time: '',
  shift: '',
});
const tableHeaders = ref([]);
const tableData = ref([]);

const convertToEpoch = (field) => {
  const selectedDateTime = moment(formData[field]).format('YYYY-MM-DD HH:mm');
  const epochTimestamp = moment(selectedDateTime, 'YYYY-MM-DD HH:mm').unix();
  formData[field] = epochTimestamp;
};

const startDateTime = computed({
  get: () => {
    if (formData.start_time) {
      return moment.unix(formData.start_time).format('YYYY-MM-DDTHH:mm');
    }
    return '';
  },
  set: (newValue) => {
    formData.start_time = moment(newValue).unix();
  }
});

const endDateTime = computed({
  get: () => {
    if (formData.end_time) {
      return moment.unix(formData.end_time).format('YYYY-MM-DDTHH:mm');
    }
    return '';
  },
  set: (newValue) => {
    formData.end_time = moment(newValue).unix();
  }
});

const machineIds = ref([]); // Store machine IDs

const fetchMachineNames = async () => {
  const machinesUrl = 'http://172.18.100.240:6969/machines'; // Replace with the actual endpoint
  try {
    const response = await axios.get(machinesUrl);
    machineIds.value = response.data.Data.map((machine) => machine.machine_id);
    // Extract "machine_id" property
  } catch (error) {
    console.error('Error fetching machine names:', error);
  }
};
onMounted(() => {
  fetchMachineNames(); // Fetch machine IDs when the component is mounted
});

const elementTypes = ref([]); // Store machine IDs

const fetchElementTypes = async () => {
  const machinesUrl = 'http://172.18.100.240:6969/elements'; // Replace with the actual endpoint
  try {
    const response = await axios.get(machinesUrl);
    elementTypes.value = response.data.Data.map((machine) => machine.type);
    // Extract "machine_id" property
  } catch (error) {
    console.error('Error fetching machine names:', error);
  }
};

const operators = ref([]); // Store machine IDs

const fetchOperators = async () => {
  const machinesUrl = 'http://172.18.100.240:6969/welder'; // Replace with the actual endpoint
  try {
    const response = await axios.get(machinesUrl);
    operators.value = response.data.Data.map((machine) => machine.welder_name);
     // Extract "machine_id" property
  } catch (error) {
    console.error('Error fetching machine names:', error);
  }
};

const operatorIds = ref([]); // Store machine IDs

const fetchOperatorIds = async () => {
  const machinesUrl = 'http://172.18.100.240:6969/welder'; // Replace with the actual endpoint
  try {
    const response = await axios.get(machinesUrl);
    operatorIds.value = response.data.Data.map((machine) => machine.id);
    // Extract "machine_id" property
  } catch (error) {
    console.error('Error fetching machine names:', error);
  }
};

const shiftTypes = ref([]); // Store machine IDs

const fetchShiftTypes = async () => {
  const machinesUrl = 'http://172.18.100.240:6969/shift'; // Replace with the actual endpoint
  try {
    const response = await axios.get(machinesUrl);
    shiftTypes.value = response.data.Data.map((machine) => machine.shift);
    // Extract "machine_id" property
  } catch (error) {
    console.error('Error fetching machine names:', error);
  }
};

const showCreateForm = () => {
  isFormVisible.value = true;
  isEditMode.value = false;
  resetFormData();
};

const fetchAndDisplayDataForAllMachines = () => {
  machineNames.forEach((machineId) => {
    const url = `http://172.18.100.240:6969/op_shift/${machineId}`;
    axios
      .get(url)
      .then((response) => {
        if (tableHeaders.value.length === 0) {
          // Set the headers based on the first machine's response
          tableHeaders.value = Object.keys(response.data[0]);
        }
        // Append the data to the existing tableData
        tableData.value = [...tableData.value, ...response.data];
      })
      .catch((error) => {
        console.error(`Error fetching data for machine ${machineId}:`, error);
      });
  });
};

const deleteData = (machineName, startTime, endTime) => {
  const url = `http://172.18.100.240:6969/op_shift/${machineName}/${startTime}/${endTime}`;
  axios
    .delete(url)
    .then(() => {
      // Remove the deleted row from tableData
      tableData.value = tableData.value.filter((data) => {
        return !(data.machine_name === machineName && data.start_time === startTime && data.end_time === endTime);
      });
    })
    .catch((error) => {
      console.error(`Error deleting data for machine ${machineName}:`, error);
    });
};


const saveMachine = async () => {
  if (isEditMode.value) {
    // Implement your update logic here
  } else {
    // Create a new machine object
    const newMachine = {
      machine_name: formData.machineName,
      element_type: formData.element_type,
      operator_name: formData.operator_name,
      start_time: formData.start_time,
      end_time: formData.end_time,
      shift: formData.shift,
      operator_id: formData.operator_id,
    };

    try {
      // Make a POST request to save the new machine data to the backend
      await axios.post('http://172.18.100.240:6969/op_shift/', newMachine); // Updated URL
      // Add the new machine to the table data
      tableData.value.push(newMachine);
    } catch (error) {
      console.error('Error saving the new machine:', error);
      // Handle the error as needed (e.g., show an error message)
    }
    resetFormData();
    isFormVisible.value = false;
  }
};



const cancelForm = () => {
  resetFormData();
  isFormVisible.value = false;
};

const resetFormData = () => {
  formData.machineName = '';
  formData.element_type = '';
  formData.operator_name = '';
  formData.operator_id = '';
  formData.start_time = '';
  formData.end_time = '';
  formData.shift = '';
};

onMounted(() => {
  fetchAndDisplayDataForAllMachines();
});
</script>

<style scoped>
/* Add your Tailwind CSS classes or styles here if needed */
</style>
