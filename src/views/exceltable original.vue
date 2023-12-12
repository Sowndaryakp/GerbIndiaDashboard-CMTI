<template>
  <div >
    <div class="flex">
    <button @click="showFilterForm" class="bg-gray-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white   font-poppins flex flex-wrap">
  Filter Table
  </button>
        <button @click="downloadTableDataExcel" class="bg-green-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
  <img width="24" height="24" src="https://img.icons8.com/sf-black/64/FFFFFF/download.png" alt="download" class="flex flex-wrap"/>
  Download Table Excel
  </button>
    </div>
  
    <div class="container mx-auto" ref="reportContainerTable">
      <h1 class="text-2xl font-semibold my-4">Machine Data</h1>
      <table class="table-auto border-collapse w-full">
        <thead>
            <tr>
    <!-- <th v-for="(header, index) in tableHeaders" :key="index" class="px-4 py-2">{{ header }}</th> -->
              <th class="py-2 px-4 border-b">Machine Name</th>
            <th class="py-2 px-4 border-b">Element Type</th>
            <th class="py-2 px-4 border-b">Operator Name</th>
            <th class="py-2 px-4 border-b">Start time</th>
            <th class="py-2 px-4 border-b">End time</th>6666
    <th class="px-4 py-2">Actions</th>
  </tr>
        </thead>
        <tbody>
  
            <td class="py-2 px-4 border-b">
              <div class="mb-2">
              <select v-model="formData.machineName" required class="border border-gray-300 rounded-lg px-2 py-1 w-full"
                @click="fetchMachineNames">
                <option value="">Select Machine Name</option>
                <option v-for="machineId in machineIds" :key="machineId">{{ machineId }}</option>
              </select>
            </div>
            </td>
            <td class="py-2 px-4 border-b">
            <div class="mb-2">
              <select v-model="formData.element_type" required class="border border-gray-300 rounded-lg px-2 py-1 w-full"
                @click="fetchElementTypes">
                <option value="" >Select Element Type</option>
                <option v-for="elementType in elementTypes" :key="elementType">{{ elementType }}</option>
              </select>
            </div>
            </td>
            <td class="py-2 px-4 border-b">
            <div class="mb-2">
    <select v-model="formData.operator_name" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" @click="fetchOperators">
      <option value="">Select Operator Type</option>
      <option v-for="operator in operators" :key="operator" >{{ operator }} </option>
    </select>
  </div>
  </td>
  <td class="py-2 px-4 border-b">
  <div class="mb-2">
              <label class="block text-gray-800">start_time:</label>
              <input v-model="startDateTime" type="datetime-local" required
                class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
            </div>
            </td>
            <td class="py-2 px-4 border-b">
              <div class="mb-2">
              <label class="block text-gray-800">end_time:</label>
              <input v-model="endDateTime" type="datetime-local" required
                class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
            </div>
              </td>
            
            
            <td class="border px-4 py-2">
              <button @click="editMachine(index)" class="bg-blue-400 text-white px-2 py-1 rounded-lg mr-2 w-20 "><img width="20" height="20" src="https://img.icons8.com/ios-filled/50/FFFFFF/search--v1.png" alt="search--v1"/>Search</button>
            </td>
        </tbody>
      </table>
   </div>
   </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue';
  import axios from 'axios';
  import { computed } from 'vue';
  import moment from 'moment';
  import * as XLSX from 'xlsx';
  // import reporttable from '../views/reporttable.vue';
  import html2pdf from 'html2pdf.js';
  const isReport = ref(false);
  
  //Importing Store Statements
  const reportContainerTable = ref(null);
  const downloadTablePDF = () => {
  const element = reportContainerTable.value; // Reference to the container you want to download
  const pdfOptions = {
  margin: 10,
  filename: 'reportTable.pdf',
  image: { type: 'jpeg', quality: 0.98 },
  html2canvas: { scale: 2 },
  jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
  };
  
  html2pdf(element, pdfOptions);
  }
  
  function downloadTableDataAsExcel(){
  isReport.value = true;
  }
  const downloadTableDataExcel = async () => {
  try {
    // Make a request to the backend to fetch the data
    const response = await axios.get('http://localhost:6969/op_shift/');
  
    // Assuming the API response has a 'Download' key containing the specific data
    const dataToDownload = response.data.Download;
  console.log(dataToDownload)
    // Convert JSON data to Excel workbook
    const ws = XLSX.utils.json_to_sheet(dataToDownload);
  
    // Add your previous code for combining data and generating Excel here
    const header = ["machine_name", "element_type", "operator_name", "start_time","end_time","shift"];
    XLSX.utils.sheet_add_aoa(ws, [header], { origin: -1 });
  
    // Add data rows
    const dataRows = dataToDownload.map(item => [
      item.machine_name, // Replace with the actual property names from your machine data
      item.element_type,
      item.operator_name,
      item.start_time,
      item.end_time,
      item.shift,
    ]);
  
    XLSX.utils.sheet_add_aoa(ws, dataRows, { origin: -1 });
  
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, 'tableData.xlsx');
  } catch (error) {
    console.error('Error downloading table data as Excel:', error);
  }
  };
  
  const machineNames = [ '7G', '7H', '7J', '7K', '7L', '27C', '27D', '27E'];
  // const elementTypes = ['type-1', 'type-2', 'type-3'];
  const isFormVisible = ref(false);
  const isEditFormVisible = ref(false);
  const isEditMode = ref(false);
  const isSaveMode =ref(false);
  const formData = reactive({
  machineName: '',
  element_type: '',
  operator_name: '',
  // operator_id: '',
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
      return moment.unix(formData.start_time).local().format('YYYY-MM-DDTHH:mm');
    }
    return '';
  },
  set: (newValue) => {
    formData.start_time = moment(newValue).unix();
    console.log(formData.start_time );
  }
  });
  
  const endDateTime = computed({
  get: () => {
    if (formData.end_time) {
      return moment.unix(formData.end_time).local().format('YYYY-MM-DDTHH:mm');
    }
    return '';
  },
  set: (newValue) => {
    formData.end_time = moment(newValue).unix();
  }
  });
  
  const downloadReport = () => {
  const reporttable = ref(null);
  
  // Access the child component's methods using the ref
  reporttable.value.downloadReport();
  };
  
  const downloadTableData = async () => {
  try {
    // Make a request to the backend to fetch the data
    const response = await axios.get('http://192.168.0.105:6969/op_shift/');
  
    // Assuming the API response has a 'dataToDownload' key containing the specific data
    const dataToDownload = response.data.dataToDownload;
  
    // Convert JSON data to Excel workbook
    const ws = XLSX.utils.json_to_sheet(dataToDownload);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, 'tableData.xlsx');
    // Create a Blob containing the Excel workbook
    const blob = XLSX.write(wb, { bookType: 'xlsx', mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  
    // Create a link element to trigger the download
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'table_data.xlsx';
  
    // Trigger a click on the link to initiate the download
    link.click();
  
    // Clean up by revoking the object URL
    window.URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error('Error downloading table data:', error);
  }
  };
  
  const machineIds = ref([]); // Store machine IDs
  
  const fetchMachineNames = async () => {
  const machinesUrl = 'http://192.168.0.105:6969/machines'; // Replace with the actual endpoint
  try {
    const response = await axios.get(machinesUrl);
    machineIds.value = response.data.Data.map((machine) => machine.machine_id);
    console.log(machineIds.value);
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
  const machinesUrl = 'http://192.168.0.105:6969/elements'; // Replace with the actual endpoint
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
  const machinesUrl = 'http://192.168.0.105:6969/welder'; // Replace with the actual endpoint
  
  try {
    const response = await axios.get(machinesUrl);
    console.log("++++++++++++++")
    console.log(response.data)
    operators.value = response.data.Data.map((machine) => machine.welder_name);
    console.log("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    console.log(machine.welder_name)
      // Extract "machine_id" property
  } catch (error) {
    console.error('Error fetching machine names:', error);
  }
  };
  
  // const operatorIds = ref([]); // Store machine IDs
  
  // const fetchOperatorIds = async () => {
  //   const machinesUrl = 'http://192.168.0.105:6969/welder'; // Replace with the actual endpoint
  //   try {
  //     const response = await axios.get(machinesUrl);
  //     operatorIds.value = response.data.Data.map((machine) => machine.id);
  //     // Extract "machine_id" property
  //   } catch (error) {
  //     console.error('Error fetching machine names:', error);
  //   }
  // };
  
  const shiftTypes = ref([]); // Store machine IDs
  
  const fetchShiftTypes = async () => {
  const machinesUrl = 'http://192.168.0.105:6969/shift'; // Replace with the actual endpoint
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
  isSaveMode.value = false;
  resetFormData();
  };
  
  // Store the original table data and initialize it
  const originalTableData = ref([]);
  
  
  // Function to fetch and display the data for all machines
  const fetchAndDisplayDataForAllMachines = () => {
  machineNames.forEach((machineId) => {
    console.log(machineId);
    const url = `http://192.168.0.105:6969/op_shift/${machineId}`;
    
    axios
      .get(url)
      .then((response) => {
        if (tableHeaders.value.length === 0) {
          // Set the headers based on the first machine's response
          tableHeaders.value = Object.keys(response.data[0]);
        }
        // Append the data to the existing tableData
        tableData.value = [...tableData.value, ...response.data];
        // TO EXTRA LINE
        originalTableData.value = [...originalTableData.value, ...response.data]; // Store original data
      })
      .catch((error) => {
        console.error(`Error fetching data for machine ${machineId}:`, error);
      });
  });
  };
  
  
  const deleteData = (machineName, startTime, endTime) => {
  // Convert local date and time to epoch timestamps
  const startTimeEpoch = moment(startTime, 'YYYY-MM-DDTHH:mm').unix();
  const endTimeEpoch = moment(endTime, 'YYYY-MM-DDTHH:mm').unix();
  
  // Make the delete request to the backend
  const url = `http://192.168.0.105:6969/op_shift/?machine_name=${machineName}&start_time=${startTimeEpoch}&end_time=${endTimeEpoch}`;
  
  axios
    .delete(url)
    .then(() => {
      console.log(`Data for machine ${machineName} deleted successfully.`);
      // After successful deletion, remove the deleted row from tableData
      tableData.value = tableData.value.filter((data) => {
        return !(data.machine_name === machineName && data.start_time === startTimeEpoch && data.end_time === endTimeEpoch);
      });
      setTimeout(() => {
        location.reload();
      }, 500);
    })
    .catch((error) => {
      console.error(`Error deleting data for machine ${machineName}:`, error);
    });
  
  };
  
  // const saveMachine = async () => {
  //   if (isEditMode.value) {
  //     // Implement your update logic here
  //   } else {
  //     // Create a new machine object
  //     const newMachine = {
  //       machine_name: formData.machineName,
  //       element_type: formData.element_type,
  //       operator_name: formData.operator_name,
  //       start_time: formData.start_time,
  //       end_time: formData.end_time,
  //       shift: formData.shift,
  //       // operator_id: formData.operator_id,
  //     };
  
  //     const newMachineString = {
  //       machine_name: formData.machineName,
  //       element_type: formData.element_type,
  //       operator_name: formData.operator_name,
  //       start_time: moment.unix(formData.start_time).format('YYYY-MM-DD HH:mm'), // Convert to date-time string
  //       end_time: moment.unix(formData.end_time).format('YYYY-MM-DD HH:mm'), // Convert to date-time string
  //       shift: formData.shift,
  //       // operator_id: formData.operator_id,
  //     };
  
  //     try {
  //       // Make a POST request to save the new machine data to the backend
  //       await axios.post('http://192.168.0.105:6969/op_shift/', newMachine); // Updated URL
  //       // Add the new machine to the table data
  //       console.log(newMachine);
  //       tableData.value.push(newMachineString);
  //     } catch (error) {
  //       console.error('Error saving the new machine:', error);
  //       // Handle the error as needed (e.g., show an error message)
  //     }
  //     resetFormData();
  //     isFormVisible.value = false;
  //     isEditFormVisible.value = false;
  //   }
  // };
  
  const saveMachine = async () => {
  if (isSaveMode.value) {
    // Update the existing machine data
    const updatedMachine = {
      machine_name: formData.machineName,
      element_type: formData.element_type,
      operator_name: formData.operator_name,
      start_time: formData.start_time,
      end_time: formData.end_time,
      shift: formData.shift,
    };
  
    try {
      // Make a PUT request to update the machine data
      const url = `http://192.168.0.105:6969/op_shift/shiftops/update?machine_id=${formData.machineName}&operator_name=${formData.operator_name}`;
      const response = await axios.put(url, updatedMachine);
  
      // Check the response for any error messages
      if (response.status === 404) {
        console.error('ShiftOp record not found:', response.data);
        // Handle the error as needed (e.g., show an error message)
      } else {
        // Update the data in the table by finding and replacing the matching record
        const recordIndex = tableData.value.findIndex((data) => {
          return (
            data.machine_name === formData.machineName &&
            data.start_time === formData.start_time
          );
        });
        if (recordIndex !== -1) {
          // Merge the updated data with the existing data in the same row
          const existingMachine = tableData.value[recordIndex];
  for (const key in updatedMachine) {
    existingMachine[key] = updatedMachine[key];
          }
        }
      }
      console.log("(((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))");
      console.log(tableData);
      // tableData.value.,map(updatedMachine);
      tableData.value = tableData.value.map((data) => {
  if (data.machine_id === machineNames && data.operator_name === operator_name) {
    // Update the data with the edited values
    return { ...data, ...editData };
  } else {
    return data;
  }
  });
  setTimeout(() => {
        location.reload();
      }, 50);
        // Reset the form and visibility
    resetFormData();
    isEditFormVisible.value = false;
        isFormVisible.value = false;
        // isEditMode.value = false;
        isSaveMode.value = false;
        
    } catch (error) {
      console.error('Error updating the machine data:', error);
      // Handle the error as needed (e.g., show an error message)
    }
  
    
    
  } else {
    // Create a new machine object
    const newMachine = {
      machine_name: formData.machineName,
      element_type: formData.element_type,
      operator_name: formData.operator_name,
      start_time: formData.start_time,
      end_time: formData.end_time,
      shift: formData.shift,
    };
    const newMachineString = {
      machine_name: formData.machineName,
      element_type: formData.element_type,
      operator_name: formData.operator_name,
      start_time: moment.unix(formData.start_time).format('YYYY-MM-DD HH:mm'), // Convert to date-time string
      end_time: moment.unix(formData.end_time).format('YYYY-MM-DD HH:mm'), // Convert to date-time string
      shift: formData.shift,
      // operator_id: formData.operator_id,
    };
  
    try {
      // Make a POST request to save the new machine data to the backend
      const url = 'http://192.168.0.105:6969/op_shift/';
      await axios.post(url, newMachine);
  
      // Add the new machine to the table data
      tableData.value.push(newMachineString);
  
        // Reset the form and visibility
    resetFormData();
        isFormVisible.value = false;
      
    } catch (error) {
      console.error('Error saving the new machine:', error);
      // Handle the error as needed (e.g., show an error message)
    }
  }
  };
  
  
  
  const cancelForm = () => {
  resetFormData();
  isFormVisible.value = false;
  isEditFormVisible.value = false;
  };
  
  const resetFormData = () => {
  formData.machineName = '';
  formData.element_type = '';
  formData.operator_name = '';
  // formData.operator_id = '';
  formData.start_time = '';
  formData.end_time = '';
  formData.shift = '';
  };
  
  
  
  // Other code for fetching machine names and other data remains the same
  
  const editMachine = async (index) => {
  // Fetch the list of operators if it hasn't been fetched already
  if (operators.value.length === 0) {
    await fetchOperators();
  }
  
  const selectedRow = tableData.value[index];
  formData.machineName = selectedRow.machine_name;
  formData.element_type = selectedRow.element_type;
  
  // Set the operator_name to the selected operator name
  formData.operator_name = selectedRow.operator_name;
  
  formData.start_time = moment.unix(selectedRow.start_time).format('YYYY-MM-DDTHH:mm');
  formData.end_time = moment.unix(selectedRow.end_time).format('YYYY-MM-DDTHH:mm');
  formData.shift = selectedRow.shift;
  isEditMode.value = true;
  isSaveMode.value = true;
  isEditFormVisible.value = true;
  };
  
  const filterData = reactive({
  operatorName: '',
  machineId: '',
  startDate: '',
  });
  
  const isFilterFormVisible = ref(false);
  
  const showFilterForm = () => {
  isFilterFormVisible.value = true;
  };
  
  const applyFilters = () => {
  // Filter the tableData based on the filterData values (operatorName, machineId, startDate)
  const filteredData = tableData.value.filter((data) => {
    const operatorNameMatch = !filterData.operatorName || data.operator_name === filterData.operatorName;
    const machineIdMatch = !filterData.machineId || data.machine_name === filterData.machineId;
  
    // Extract the date part from the timestamp and compare it with the filter date
    const startDateMatch = !filterData.startDate || moment(data.start_time).format('YYYY-MM-DD') === filterData.startDate;
  
    return operatorNameMatch && machineIdMatch && startDateMatch;
  });
  
  // Update the tableData with the filtered results
  tableData.value = filteredData;
  
  // Hide the filter form
  isFilterFormVisible.value = false;
  };
  
  // Add this variable to store the original data
  
  onMounted(() => {
  fetchAndDisplayDataForAllMachines();
  originalTableData.value = [...tableData.value]; // Store the original data
  });
  
  const resetFilters = () => {
  // Reset the filterData values
  filterData.operatorName = '';
  filterData.machineId = '';
  filterData.startDate = '';
  
  // Reset tableData to the original unfiltered data
  tableData.value = [...originalTableData.value];
  
  // Hide the filter form
  isFilterFormVisible.value = false;
  };
  
  </script>
  
  <style scoped>
  /* Add your Tailwind CSS classes or styles here if needed */
  </style>
  