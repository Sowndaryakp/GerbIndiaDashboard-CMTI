<template>
  <div>
    <!-- Add a button to open the "Create" form -->
    <div class="flex">
      <!-- Add a button to open the "Create" form -->
      <button @click="showCreateForm" class="bg-blue-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap ">
        <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
        Add Machine
      </button>

      <!-- Add a "New Machine" button -->
      <button @click="showNewMachineForm" class="bg-green-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="25" height="50" src="https://img.icons8.com/ios-filled/50/FFFFFF/gears.png" alt="gears" class="mr-2"/>
        New Machine
      </button>

      <!-- Filter button to open filter popup -->
      <button @click="toggleFilter" class="bg-yellow-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="25" height="50" src="https://img.icons8.com/ios-filled/50/FFFFFF/filter--v1.png" alt="filter--v1" class="mr-2"/>
        Filter
      </button>

      <!-- Button to download filtered table as Excel -->
      <button @click="downloadFilteredTable" class="bg-purple-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex ">
        <img width="24" height="24" src="https://img.icons8.com/material-outlined/24/FFFFFF/ms-excel--v1.png" alt="ms-excel--v1" class="mr-2"/>
        Download (Excel)
      </button>
    </div>
     <!-- Filter popup -->
     <div v-if="isFilterVisible" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md ">
        <h2 class="text-lg font-semibold text-gray-800">Filter Machines</h2>
        <form @submit.prevent="applyFilter">
          <div class="mb-2   ">
            <label class="block text-gray-800 ">Machine ID:</label>
            <select v-model="filterCriteria.machineId" class="border border-gray-300 rounded-lg px-2 py-1 w-full">
              <option value="">All</option>
              <option value="id1">id1</option>
              <option value="id2">id2</option>
              <option value="id3">id3</option>
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-800">Project ID:</label>
            <select v-model="filterCriteria.projectId" class="border border-gray-300 rounded-lg px-2 py-1 w-full">
              <option value="">All</option>
              <option value="pp1">pp1</option>
              <option value="pp2">pp2</option>
              <option value="pp3">pp3</option>
              <!-- Add more options as needed -->
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-800">Operator:</label>
            <select v-model="filterCriteria.operator" class="border border-gray-300 rounded-lg px-2 py-1 w-full">
              <option value="">All</option>
              <option value="op1">op1</option>
              <option value="op2">op2</option>
              <option value="op3">op3</option>
              <!-- Add more options as needed -->
            </select>
          </div>

          <div class="mb-2">
          <label class="block text-gray-800">Date:</label>
          <input v-model="filterCriteria.date" type="date" class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
        </div>
          
          <div class="mt-2 flex justify-end">
            <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg">Apply</button>
            <button @click="resetFilter" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg ml-2">Reset</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Table to display machine data -->
    <table class="table-auto w-full mt-4">
      <thead>
    <tr>
      <!-- Machine Name Column -->
<th @click="sortBy('machineName')" class="px-4 py-2 cursor-pointer flex ">
  Machine Name
  <img v-if="sortColumn === 'machineName'" :src="sortDirection === 'asc' ? 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-up.png' : 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-down.png'" alt="sort-icon" class="h-5 w-5 ml-2 " />
</th>

<!-- Machine ID Column -->
<th @click="sortBy('machineId')" class="px-4 py-2 cursor-pointer flex-end">
  Machine ID
  <img v-if="sortColumn === 'machineId'" :src="sortDirection === 'asc' ? 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-up.png' : 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-down.png'" alt="sort-icon" class="h-5 w-5 ml-2 " />
</th>

<!-- Operator Column -->
<th @click="sortBy('operator')" class="px-4 py-2 cursor-pointer flex flex-wrap ">
  Operator
  <img v-if="sortColumn === 'operator'" :src="sortDirection === 'asc' ? 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-up.png' : 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-down.png'" alt="sort-icon" class="h-5 w-5 ml-2 " />
</th>

<!-- Part No Column -->
<th @click="sortBy('partNo')" class="px-4 py-2 cursor-pointer">
  Part No
  <img v-if="sortColumn === 'partNo'" :src="sortDirection === 'asc' ? 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-up.png' : 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-down.png'" alt="sort-icon" class="h-5 w-5 ml-2 " />
</th>

<!-- Project ID Column -->
<th @click="sortBy('projectId')" class="px-4 py-2 cursor-pointer">
  Project ID
  <img v-if="sortColumn === 'projectId'" :src="sortDirection === 'asc' ? 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-up.png' : 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-down.png'" alt="sort-icon" class="h-5 w-5 ml-2 " />
</th>

<!-- Shift Column -->
<th @click="sortBy('shift')" class="px-4 py-2 cursor-pointer">
  Shift
  <img v-if="sortColumn === 'shift'" :src="sortDirection === 'asc' ? 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-up.png' : 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-down.png'" alt="sort-icon"  class="h-5 w-5 ml-2 "/>
</th>

<!-- Date Column -->
<th @click="sortBy('date')" class="px-4 py-2 cursor-pointer">
  Date
  <img v-if="sortColumn === 'date'" :src="sortDirection === 'asc' ? 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-up.png' : 'https://img.icons8.com/ios-glyphs/30/FFFFFF/sort-down.png'" alt="sort-icon" class="h-5 w-5 ml-2 "/>
</th>
 <th class="px-4 py-2">Actions</th>
    </tr>
  </thead>
      <tbody>
        <!-- Iterate through the machine data and display it in rows -->
        <tr v-for="(machine, index) in filteredMachines" :key="index">
  <td class="border px-4 py-2">{{ machine.machineName }}</td>
  <td class="border px-4 py-2">{{ machine.machineId }}</td>
  <td class="border px-4 py-2">{{ machine.operator }}</td>
  <td class="border px-4 py-2">{{ machine.partNo }}</td>
  <td class="border px-4 py-2">{{ machine.projectId }}</td>
  <td class="border px-4 py-2">{{ machine.shift }}</td>
  <td class="border px-4 py-2">{{ machine.date }}</td>
  <td class="border px-4 py-2">
    <!-- Buttons for CRUD operations -->
    <button @click="editMachine(index)" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Edit</button>
    <button @click="deleteMachine(index)" class="bg-red-500 text-white px-2 py-1 rounded-lg">Delete</button>
  </td>
</tr>
      </tbody>
    </table>

     

    <!-- Popup for creating and editing machines -->
    <div v-if="isFormVisible" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
        <h2 class="text-lg font-semibold text-gray-800">{{ isEditMode ? 'Edit Machine' : 'Create Machine' }}</h2>
        <form @submit.prevent="saveMachine">
          <div class="mb-2">
            <label class="block text-gray-800">Machine Name:</label>
            <select v-model="formData.machineName" required class="border border-gray-300 rounded-lg px-2 py-1 w-full">
              <option value="">Select Machine Name</option>
              <option value="name1">AK-400-2-7D</option>
              <option value="name2">AK-400-7F</option>
              <option value="name3">AK-600-7G</option>
              <option value="name3">AK-600-7H</option>
              <option value="name3">MIG-500-I-7I</option>
              <option value="name3">MIG-500-I-7J</option>
              <option value="name3">MIG-500-I-7K</option>
              <option value="name3">MIG-500-I-7L</option>
              <option value="name3">Panasonic KR-400-27A</option>
              <option value="name3">Panasonic AK-400-27C</option>
              <option value="name3">Panasonic YD500RXI</option>
              <option value="name3">Panasonic YD500RXI</option>
              <!-- Add more options as needed -->
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-800">Machine ID:</label>
            <select v-model="formData.machineId" required class="border border-gray-300 rounded-lg px-2 py-1 w-full">
              <option value="">Select Machine ID</option>
              <option value="id1">id1</option>
              <option value="id2">id2</option>
              <option value="id3">id3</option>
              <!-- Add more options as needed -->
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-800">Operator:</label>
            <select v-model="formData.operator" required class="border border-gray-300 rounded-lg px-2 py-1 w-full">
              <option value="">Select Operator</option>
              <option value="op1">op1</option>
              <option value="op2">op2</option>
              <option value="op3">op3</option>
              <!-- Add more options as needed -->
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-800">Part No:</label>
            <select v-model="formData.partNo" required class="border border-gray-300 rounded-lg px-2 py-1 w-full">
              <option value="">Select Part No</option>
              <option value="p1">p1</option>
              <option value="p2">p2</option>
              <option value="p3">p3</option>
              <!-- Add more options as needed -->
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-800">Project ID:</label>
            <select v-model="formData.projectId" required class="border border-gray-300 rounded-lg px-2 py-1 w-full">
              <option value="">Select Project ID</option>
              <option value="pp1">pp1</option>
              <option value="pp2">pp2</option>
              <option value="pp3">pp3</option>
              <!-- Add more options as needed -->
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-800">Shift:</label>
            <select v-model="formData.shift" required class="border border-gray-300 rounded-lg px-2 py-1 w-full">
              <option value="">Select Shift</option>
              <option value="s1">s1</option>
              <option value="s2">s2</option>
              <option value="s3">s3</option>
              <!-- Add more options as needed -->
            </select>
          </div>
          <div class="mb-2">
            <label class="block text-gray-800">Date:</label>
            <input v-model="formData.date" type="date" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
          </div>
          <div class="mt-2 flex justify-end">
            <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">{{ isEditMode ? 'Update' : 'Create' }}</button>
            <button @click="cancelForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Popup for adding a new machine -->
    <div v-if="isNewMachineFormVisible" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
        <h2 class="text-lg font-semibold text-gray-800">New Machine</h2>
        <form @submit.prevent="addNewMachine">
          <div class="mb-2">
            <label class="block text-gray-800">Machine Name:</label>
            <input v-model="newMachineName" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
          </div>
          <div class="mt-2 flex justify-end">
            <button type="submit" class="bg-green-500 text-white px-2 py-1 rounded-lg mr-2">Add</button>
            <button @click="cancelNewMachineForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import Papa from 'papaparse';


export default {
  data() {
    return {
      sortColumn: '', // Track the currently sorted column
      sortDirection: 'asc', // Track the sorting direction ('asc' or 'desc')
    
      machines: [], // Array to store machine data
      isFormVisible: false,
      isEditMode: false,
      formData: {
        machineName: '',
        machineId: '',
        operator: '',
        partNo: '',
        projectId: '',
        shift: '',
        date: '',
      },
      editedMachineIndex: -1,
      isNewMachineFormVisible: false,
      newMachineName: '',
      isFilterVisible: false, // Control filter popup visibility
      filterCriteria: {
        machineId: '',
        projectId: '',
        operator: '',
        date:'',
      },
    };
  },
  created() {
    // Define available options
    const machineNames = ["name1", "name2", "name3"];
    const machineIds = ["id1", "id2", "id3"];
    const operators = ["op1", "op2", "op3"];
    const partNos = ["p1", "p2", "p3"];
    const projectIds = ["pp1", "pp2", "pp3"];
    const shifts = ["s1", "s2", "s3"];

    const getRandomDate = () => {
      const now = new Date();
      const pastYear = now.getFullYear() - 1;
      
      const randomMonth = Math.floor(Math.random() * 12);
      const randomDay = Math.floor(Math.random() * 28 + 1); // Assume 28 days in a month

      return `${2023}-${String(8 + 1).padStart(2, '0')}-${String(randomDay).padStart(2, '0')}`;
    };

   // Generate dummy machine data using random selections
   const dummyMachines = Array.from({ length: 20 }, () => ({
      machineName: machineNames[Math.floor(Math.random() * machineNames.length)],
      machineId: machineIds[Math.floor(Math.random() * machineIds.length)],
      operator: operators[Math.floor(Math.random() * operators.length)],
      partNo: partNos[Math.floor(Math.random() * partNos.length)],
      projectId: projectIds[Math.floor(Math.random() * projectIds.length)],
      shift: shifts[Math.floor(Math.random() * shifts.length)],
      date: getRandomDate(), // Ensure the date format is "YYYY-MM-DD"
    }));


    // Set the machines data
    this.machines = dummyMachines;
  },
  computed: {
    // Filter machines based on filter criteria
    filteredMachines() {
      return this.machines.filter((machine) => {
        const filterMachineId = this.filterCriteria.machineId;
        const filterProjectId = this.filterCriteria.projectId;
        const filterOperator = this.filterCriteria.operator;
        const filterDate = this.filterCriteria.date;

        return (
          (filterMachineId === '' || machine.machineId === filterMachineId) &&
          (filterProjectId === '' || machine.projectId === filterProjectId) &&
          (filterOperator === '' || machine.operator === filterOperator) &&
          (filterDate === '' || machine.date === filterDate)
        );
      });
    },
  },
  methods: {
    sortBy(column) {
  // If clicking on the same column, reverse the sorting direction
  if (this.sortColumn === column) {
    this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
  } else {
    // If clicking on a different column, set it as the new sorting column and start with ascending order
    this.sortColumn = column;
    this.sortDirection = 'asc';
  }

  // Sort the machines array based on the selected column and direction
  this.machines.sort((a, b) => {
    const valueA = a[column];
    const valueB = b[column];

    if (this.sortDirection === 'asc') {
      return valueA.localeCompare(valueB);
    } else {
      return valueB.localeCompare(valueA);
    }
  });
},

    downloadFilteredTable() {
      // Filtered data to export
      const filteredData = this.filteredMachines.map((machine) => ({
        'Machine Name': machine.machineName,
        'Machine ID': machine.machineId,
        'Operator': machine.operator,
        'Part No': machine.partNo,
        'Project ID': machine.projectId,
        'Shift': machine.shift,
        'Date': machine.date,
      }));

      // Convert filteredData to CSV format
      const csv = Papa.unparse(filteredData, {
        header: true, // Include headers in the CSV
      });

      // Create a Blob with the CSV data
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });

      // Create a download link
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'filtered_machines.csv';
      link.style.display = 'none';

      // Trigger a click event to initiate the download
      document.body.appendChild(link);
      link.click();

      // Clean up
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);
    },
  


    
    showCreateForm() {
      this.isFormVisible = true;
      this.isEditMode = false;
      this.resetFormData();
    },
    editMachine(index) {
      this.isFormVisible = true;
      this.isEditMode = true;
      this.formData = { ...this.machines[index] };
      this.editedMachineIndex = index;
    },
    deleteMachine(index) {
      this.machines.splice(index, 1);
    },
    saveMachine() {
      if (this.isEditMode) {
        if (this.editedMachineIndex !== -1) {
          this.machines[this.editedMachineIndex] = { ...this.formData };
          this.editedMachineIndex = -1;
        }
      } else {
        this.machines.push({ ...this.formData });
      }
      this.resetFormData();
      this.isFormVisible = false;
    },
    cancelForm() {
      this.resetFormData();
      this.isFormVisible = false;
      this.editedMachineIndex = -1;
    },
    resetFormData() {
      this.formData = {
        machineName: '',
        machineId: '',
        operator: '',
        partNo: '',
        projectId: '',
        shift: '',
        date: '',
      };
    },
    showNewMachineForm() {
      this.isNewMachineFormVisible = true;
    },
    cancelNewMachineForm() {
      this.isNewMachineFormVisible = false;
      this.newMachineName = '';
    },
    addNewMachine() {
      if (this.newMachineName.trim() !== '') {
        this.formData.machineName = this.newMachineName;
        this.newMachineName = '';
        this.isNewMachineFormVisible = false;
      }
    },
    toggleFilter() {
      this.isFilterVisible = !this.isFilterVisible;
    },
    applyFilter() {
  // Filter the machines based on filter criteria
  this.isFilterVisible = false;

  // Filter the machines based on the selected filter criteria
  this.filteredMachines = this.machines.filter((machine) => {
    // Check if the machine matches the filter criteria
    const matchesMachineId = !this.filterCriteria.machineId || machine.machineId === this.filterCriteria.machineId;
    const matchesProjectId = !this.filterCriteria.projectId || machine.projectId === this.filterCriteria.projectId;
    const matchesOperator = !this.filterCriteria.operator || machine.operator === this.filterCriteria.operator;

    // Parse the dates and compare only the date part (excluding time)
    const filterDate = this.filterCriteria.date ? new Date(this.filterCriteria.date).toISOString().split('T')[0] : null;
    const machineDate = new Date(machine.date).toISOString().split('T')[0];

    // Log the values for debugging
    console.log('Filter Date:', filterDate);
    console.log('Machine Date:', machineDate);

    // If filterDate is not null, check if it matches the machine's date
    const matchesDate = !filterDate || (filterDate === machineDate);

    // Log the matchesDate value
    console.log('Matches Date:', matchesDate);

    // Return true if all criteria match
    return matchesMachineId && matchesProjectId && matchesOperator && matchesDate;
  });
},


    resetFilter() {
      // Reset filter criteria
      this.filterCriteria = {
        machineId: '',
        projectId: '',
        operator: '',
      };
      // Apply filter or reset data as needed
    },
  },
  
  
};
</script>



<style scoped>
/* Add custom styles for your component here */
</style>