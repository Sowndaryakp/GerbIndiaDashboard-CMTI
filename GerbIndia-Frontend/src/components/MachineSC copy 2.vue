<template>
  <!-- <Navbar/> -->
  <div >
    <div class="flex">
      <!-- Add a button to open the "Create" form -->
      <button @click="showCreateForm"
        class="bg-blue-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
        Add Schedule
      </button>
     
<!--add element type-->
<button @click="showElementForm"
        class="bg-blue-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
        Add Element Type
      </button>
      <button @click="showWelderForm"
        class="bg-blue-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
        Add Welder
      </button>

<!-- Add a filter button -->
<button @click="showFilterForm" class="bg-gray-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
  Filter Table
</button>

<!--Download table data-->
<!-- <button @click="downloadTableData"
        class="bg-blue-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="24" height="24" src="https://img.icons8.com/sf-black/64/FFFFFF/download.png" alt="download" class="flex flex-wrap"/>
        Download Table Data
      </button> -->
      <!-- <button @click="downloadTablePDF" class="bg-blue-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="24" height="24" src="https://img.icons8.com/sf-black/64/FFFFFF/download.png" alt="download" class="flex flex-wrap"/>
          Download Table Report
        </button> -->

        <button @click="downloadTableDataExcel" class="bg-green-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="24" height="24" src="https://img.icons8.com/sf-black/64/FFFFFF/download.png" alt="download" class="flex flex-wrap"/>
         Download Table Excel
        </button>
        <div class="flex">
      <button @click="showProductionForm" class="bg-purple-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
        Download Production Data
      </button>
    </div>
        <!-- <button @click="downloadTablePDF" class="bg-blue-500 rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img width="24" height="24" src="https://img.icons8.com/sf-black/64/FFFFFF/download.png" alt="download" class="flex flex-wrap"/>
          Download Table Exel
        </button> -->
    </div>
    <!-- <div>
      <button @click="downloadReport">Download Report</button>
      <reporttable ref="reporttableRef" />
    </div> -->

    <div class="container mx-auto" ref="reportContainerTable">
      <h1 class="text-2xl font-semibold my-4">Machine Data</h1>
      <table class="table-auto border-collapse w-full">
        <thead>
           <tr>
    <th v-for="(header, index) in tableHeaders" :key="index" class="px-4 py-2">{{ header }}</th>
    <th class="px-4 py-2">Actions</th>
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
              <button @click="deleteData(data.machine_name, data.start_time, data.end_time, data.element_type, data.operator_name)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
               Delete
              </button>

            </td>
          </tr>
        </tbody>
      </table>
      <!-- create form -->
      <div v-if="isFormVisible" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
          <h2 class="text-lg font-semibold text-gray-800">{{ isSaveMode ? 'Edit Machine' : 'Create Machine' }}</h2>
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
                <option value="" >Select Element Type</option>
                <option v-for="elementType in elementTypes" :key="elementType">{{ elementType }}</option>
              </select>
            </div>

            <div class="mb-2">
    <label class="block text-gray-800">operator_name:</label>
    <select v-model="formData.operator_name" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" @click="fetchOperators">
      <option value="">Select Operator Type</option>
      <option v-for="operator in operators" :key="operator" >{{ operator }} </option>
    </select>
  </div>

            <!-- <div class="mb-2">
              <label class="block text-gray-800">Operator ID:</label>
              <select v-model="formData.operator_id" required class="border border-gray-300 rounded-lg px-2 py-1 w-full"
                @click="fetchOperatorIds">
                <option value="">Select Operator ID</option>
                <option v-for="operatorId in operatorIds" :key="operatorId">{{ operatorId }} </option>
              </select>
            </div> -->

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
              <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">{{ isSaveMode ? 'Update' :
                'Create' }}</button>
              <button @click="cancelForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
            </div>
          </form>
        </div>
      </div>
      <!-- Production data excel -->
      <div v-if="isProductionFormVisible" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
          <form>
            <div class="mb-2">
              <label class="block text-gray-800">Machine Name:</label>
              <select v-model="machine_id" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" @click="fetchMachineNames">
                <option value="">Select Machine Name</option>
                <option v-for="machineId in machineIds" :key="machineId">{{ machineId }}</option>
              </select>
            </div>

            <div class="mb-2">
              <label class="block text-gray-800">start_time:</label>
              <input v-model="startDateProd" type="date" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
            </div>

            <div class="mb-2">
              <label class="block text-gray-800">end_time:</label>
              <input v-model="endDateProdProd" type="date" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
            </div>

            <div class="mt-2 flex justify-end">
              <button @click="generateProductionExcel($event)" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow">
                 Download
              </button>
              <button @click="cancelForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
            </div>
          </form>
        </div>
      </div>
      <!--old add  element type-->
      <!-- <div v-if="isElementForm" class="modal fixed top-0 left-0 flex items-center justify-center w-full h-full bg-black bg-opacity-50">
      <div class="modal-content bg-white p-6 rounded-lg shadow-lg">
        <span @click="cancelElementForm" class="close absolute top-2 right-2 text-gray-600 cursor-pointer text-2xl">&times;</span>
        <form @submit.prevent="submitElementForm">
        <div class="mb-4">
          <label for="elementType">Type:</label>
          <input v-model="elementType" type="text" id="elementType" required />
        </div>
        <div class="mb-4">
          <label for="elementRange">Range:</label>
          <input v-model="elementRange" type="text" id="elementRange" required />
        </div>
        <div class="mb-4">
          <label for="elementCurrent">Current:</label>
          <input v-model="elementCurrent" type="text" id="elementCurrent" required />
        </div>
        <div class="mb-4">
          <label for="elementVoltage">Voltage:</label>
          <input v-model="elementVoltage" type="text" id="elementVoltage" required />
        </div>
        <div class="mb-4">
          <label for="elementDescription">Element Description:</label>
          <textarea v-model="elementDescription" id="elementDescription" required></textarea>
        </div>
        <div class="flex justify-end">
            <button type="submit" class="bg-green-500 text-white px-4 py-2 mr-2 rounded">Create</button>
            <button @click="cancelElementForm" type="button" class="bg-red-500 text-white px-4 py-2 rounded">Cancel</button>
          </div>
      </form>
    </div>
    </div> -->
    <div v-if="isElementForm" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
          <form @submit.prevent="submitElementForm">
            <div class="mb-2">
              <label class="block text-gray-800">Type:</label>
              <input v-model="elementType" type="text" id="elementType" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter element type" />
            </div>

            <div class="mb-2">
              <label class="block text-gray-800">Range:</label>
              <input v-model="elementRange" type="text" id="elementRange" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter element range"/>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Current:</label>
              <input v-model="elementCurrent" type="text" id="elementCurrent" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter current"/>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Voltage:</label>
              <input v-model="elementVoltage" type="text" id="elementVoltage" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter voltage"/>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Element Description:</label>
              <textarea v-model="elementDescription" id="elementDescription" required class="border border-gray-300 px-1 py-1 rounded-md w-80" placeholder="enter Element Description"></textarea>
            </div>
            <div class="mt-2 flex justify-end">
              <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Create</button>
              <button @click="cancelElementForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <!--old add welder-->
    <!-- <div v-if="isWelderForm" class="modal fixed top-0 left-0 flex items-center justify-center w-full h-full bg-black bg-opacity-50">
      <div class="modal-content bg-white p-6 rounded-lg shadow-lg">
        <span @click="cancelWelderForm" class="close absolute top-2 right-2 text-gray-600 cursor-pointer text-2xl">&times;</span>
        <form @submit.prevent="submitWelderForm">
        <div class="mb-4">
          <label for="welderName">Welder Name:</label>
          <input v-model="welderName" type="text" id="welderName" required />
        </div>
        <div class="mb-4">
          <label for="welderNumber">Welder Number:</label>
          <input v-model="welderNumber" type="text" id="welderNumber" required />
        </div>
        <div class="mb-4">
          <label for="dateOfJoining">Date Of Joining:</label>
          <input v-model="dateOfJoining" type="date" id="dateOfJoining" required />
        </div>
        <div class="mb-4">
          <label for="welderQualification">Welder Qualification:</label>
          <input v-model="welderQualification" type="text" id="welderQualification" required />
        </div>
        <div class="mb-4">
          <label for="qualifiedThickness">Qualified Thickness:</label>
          <input v-model="qualifiedThickness" type="text" id="qualifiedThickness" required />
        </div>
        <div class="mb-4">
          <label for="iNo">I Number:</label>
          <input v-model="iNo" type="text" id="iNo" required />
        </div>
        <div class="mb-4">
          <label for="fcNo">Fc Number:</label>
          <input v-model="fcNo" type="text" id="fcNo" required />
        </div>
        <div class="mb-4">
          <label for="project">Project:</label>
          <input v-model="project" type="text" id="project" required />
        </div>
        <div class="flex justify-end">
            <button type="submit" class="bg-green-500 text-white px-4 py-2 mr-2 rounded">Create</button>
            <button @click="cancelWelderForm" type="button" class="bg-red-500 text-white px-4 py-2 rounded">Cancel</button>
          </div>
      </form>
    </div>
    </div> -->
    <div v-if="isWelderForm" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
          <form @submit.prevent="submitWelderForm">
            <div class="mb-2">
              <label class="block text-gray-800">Welder Name:</label>
              <input v-model="welderName" type="text" id="welderName" required  class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter welder name" />
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Welder Number:</label>
              <input v-model="welderNumber" type="text" id="welderNumber" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter welder number"/>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Date Of Joining:</label>
              <input v-model="dateOfJoining" type="date" id="dateOfJoining" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter date of joining"/>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Welder Qualification:</label>
              <input v-model="welderQualification" type="text" id="welderQualification" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter welder qualification"/>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Qualified Thickness:</label>
              <input v-model="qualifiedThickness" type="text" id="qualifiedThickness" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter qualified thickness"/>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">I Number:</label>
              <input v-model="iNo" type="text" id="iNo" required  class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter I number " />
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Fc Number:</label>
              <input v-model="fcNo" type="text" id="fcNo" required  class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter Fc number" />
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Project:</label>
              <input v-model="project" type="text" id="project" required  class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter project" />
            </div>
            <div class="mt-2 flex justify-end">
              <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Create</button>
              <button @click="cancelWelderForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
            </div>
          </form>
        </div>
      </div>
      <!--edit table-->
      <div v-if="isEditFormVisible" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
          <h2 class="text-lg font-semibold text-gray-800">{{ isEditMode ? 'Edit Machine' : 'Create Machine' }}</h2>
          <form @submit.prevent="saveMachine">
            <div class="mb-2">
              <label class="block text-gray-800">Machine Name:</label>
              <input v-model="formData.machineName" type="text" class="border border-gray-300 rounded-lg px-2 py-1 w-full" readonly />
              <!-- <select v-model="formData.machineName" required class="border border-gray-300 rounded-lg px-2 py-1 w-full"
                @click="fetchMachineNames">
                <option value="">Select Machine Name</option>
                <option v-for="machineId in machineIds" :key="machineId">{{ machineId }}</option>
              </select> -->
            </div>
            <div class="mb-2">
  <label class="block text-gray-800">element_type:</label>
  <select v-model="formData.element_type" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" @click="fetchElementTypes">
    <option value="" >Select Element Type</option>
    <option v-for="elementType in elementTypes" :key="elementType" >{{ elementType }}</option>
  </select>
</div>


            <div class="mb-2">
    <label class="block text-gray-800">operator_name:</label>
    <input v-model="formData.operator_name" type="text" class="border border-gray-300 rounded-lg px-2 py-1 w-full" readonly />
    <!-- <select v-model="formData.operator_name" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" @click="fetchOperators">
      <option value="">Select Operator Type</option>
      <option v-for="operator in operators" :key="operator" >{{ operator }} </option>
    </select> -->
  </div>

            <!-- <div class="mb-2">
              <label class="block text-gray-800">Operator ID:</label>
              <select v-model="formData.operator_id" required class="border border-gray-300 rounded-lg px-2 py-1 w-full"
                @click="fetchOperatorIds">
                <option value="">Select Operator ID</option>
                <option v-for="operatorId in operatorIds" :key="operatorId">{{ operatorId }} </option>
              </select>
            </div> -->

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
    <div v-if="isFilterFormVisible" class="fixed inset-0 flex items-center justify-center z-50">
  <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
    <h2 class="text-lg font-semibold text-gray-800">Filter Table</h2>
    <form @submit.prevent="applyFilters">
      <div class="mb-2">
        <label class="block text-gray-800">Operator Name:</label>
        <select v-model="filterData.operatorName" class="border border-gray-300 rounded-lg px-2 py-1 w-full">
          <option value="">All</option>
          <option v-for="operator in operators" :key="operator">{{ operator }}</option>
        </select>
      </div>
      <div class="mb-2">
        <label class="block text-gray-800">Machine ID:</label>
        <select v-model="filterData.machineId" class="border border-gray-300 rounded-lg px-2 py-1 w-full">
          <option value="">All</option>
          <option v-for="machineId in machineIds" :key="machineId">{{ machineId }}</option>
        </select>
      </div>
      <div class="mb-2">
        <label class="block text-gray-800">Start Date:</label>
        <input v-model="filterData.startDate" type="date" class="border border-gray-300 rounded-lg px-2 py-1 w-full" />
      </div>
      <div class="mt-2 flex justify-end">
        <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Apply Filters</button>
        <button @click="resetFilters" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Reset Filters</button>
      </div>
      <div v-if="isReport" class="fixed inset-0 flex items-center justify-center z-50">
               <div class="bg-white p-8 rounded-lg shadow-lg w-1\/2 h-1\/2 relative">
                 <MachineSCTable />
                 <!-- <Report/> -->
                 <button @click="hideReportPopup" class=" bg-white px-1 py-0 rounded-lg absolute top-2 right-0 -mt-1 mr-1">
                   <img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/>
                   </button>
               </div>
             </div>
    </form>
  </div>
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
// import Navbar from '@/components/Navbar.vue'
const isProductionFormVisible = ref(false);
const isProductionDataFormVisible = ref(false);
const machine_id = ref('');
const startDateProd = ref('');
const endDateProdProd = ref('');
const machineIds = ref([]);

// Reactive variables for form fields
const isElementForm = ref(false);
const isWelderForm = ref(false);
const elementType = ref('');
const elementRange = ref('');
const elementCurrent = ref('');
const elementVoltage = ref('');
const elementDescription = ref('');
const elementPlateThickness = ref('');
const elementPlateDescription = ref('');

const welderName = ref('');
const welderNumber = ref('');
const dateOfJoining = ref('');
const welderQualification = ref('');
const qualifiedThickness = ref('');
const iNo = ref('');
const fcNo = ref('');
const project = ref('');

// Function to show the form
const showElementForm = () => {
  isElementForm.value = true;
};

const showWelderForm = () => {
  isWelderForm.value = true;
}
// Function to hide the form and reset fields
const cancelElementForm = () => {
  isElementForm.value = false;
  resetFormFields();
};

const cancelWelderForm = () => {
  isWelderForm.value = false;
  resetWelderFormFields();
};

// Function to reset form fields
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
    // Prepare the data to be sent to the backend
    const formData = {
      type: elementType.value,
      range: elementRange.value,
      standard_current: elementCurrent.value,
      standard_voltage: elementVoltage.value,
      element_description: elementDescription.value,
      plate_thickness: elementPlateThickness.value,
      plate_description: elementPlateDescription.value,
    };

    // Make the HTTP POST request to your FastAPI backend
    const response = await axios.post('http://192.168.0.105:6969/elements/', formData);

    // Handle the response as needed
    console.log('Element created successfully:', response.data);

    // Reset form fields and hide the form
    resetFormFields();
    isElementForm.value = false;
  } catch (error) {
    console.error('Error creating element:', error);
  }
};

// Function to reset form fields
const resetWelderFormFields = () => {
  welderName.value = '';
  welderNumber.value = '';
  dateOfJoining.value = '';
  welderQualification.value = '';
  qualifiedThickness.value = '';
  iNo.value = '',
  fcNo.value = '',
  project.value = ''
};
const submitWelderForm = async () => {
  try {
    // Prepare the data to be sent to the backend
    const formData = {
      welder_name: welderName.value,
      welder_number: welderNumber.value,
      // date_of_joining: moment.unix(dateOfJoining.value).format('YYYY-MM-DD HH:mm'), 
      date_of_joining: dateOfJoining.value,
      welder_qualification: welderQualification.value,
      qualified_thickness: qualifiedThickness.value,
      I_no: iNo.value,
      Fc_no: fcNo.value,
      project: project.value,
    };

    // Make the HTTP POST request to your FastAPI backend
    const response = await axios.post('http://192.168.0.105:6969/welder/', formData);

    // Handle the response as needed
    console.log('Welder created successfully:', response.data);

    // Reset form fields and hide the form
    resetWelderFormFields();
    isWelderForm.value = false;
  } catch (error) {
    console.error('Error creating welder:', error);
  }
};

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
const startDate = ref('');
const data = ref(null);

// Computed property for the Axios URL for op_shift data
const axiosOpShiftUrl = computed(() => {
  return `http://192.168.0.105:6969/op_shift/`;
});

// Function to fetch data from the API for op_shift
const downloadTableDataExcel = async () => {
  try {
    const opShiftResponse = await axios.get(axiosOpShiftUrl.value);

    console.log('Op Shift Response Data:', opShiftResponse.data);

    // Convert response data to arrays (if necessary)
    const opShiftData = Array.isArray(opShiftResponse.data) ? opShiftResponse.data : [opShiftResponse.data];

    data.value = opShiftData;

    // Generate and download Excel file
    const ws = XLSX.utils.json_to_sheet(opShiftData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'DataSheet');
    XLSX.writeFile(wb, 'tableExcel.xlsx');
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};


// const downloadTableDataAsExcel = async () => {
//   try {
//     // Make a request to the backend to fetch the data
//     const response = await axios.get('http://192.168.0.105:6969/op_shift/');

//     // Assuming the API response has a 'dataToDownload' key containing the specific data
//     const dataToDownload = response.data.dataToDownload;
//     console.log(response.data.dataToDownload);

//     // Convert JSON data to Excel workbook
//     const ws = XLSX.utils.json_to_sheet(dataToDownload);
//     const wb = XLSX.utils.book_new();
//     XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
//     XLSX.writeFile(wb, 'tableData.xlsx');
//     // Create a Blob containing the Excel workbook
//     const blob = XLSX.write(wb, { bookType: 'xlsx', mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

//     // Create a link element to trigger the download
//     const link = document.createElement('a');
//     link.href = window.URL.createObjectURL(blob);
//     link.download = 'table_data.xlsx';

//     // Trigger a click on the link to initiate the download
//     link.click();

//     // Clean up by revoking the object URL
//     window.URL.revokeObjectURL(link.href);
//   } catch (error) {
//     console.error('Error downloading table data:', error);
//   }
// };

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

// const dojDateTime = computed({
//   get: () => {
//     if (formData.dateOfJoining) {
//       return moment.unix(formData.dateOfJoining).local().format('YYYY-MM-DDTHH:mm');
//     }
//     return '';
//   },
//   set: (newValue) => {
//     formData.dateOfJoining = moment(newValue).unix();
//     console.log(formData.dateOfJoining );
//   }
// });

const startDateTime = computed({
  get: () => {
    if (formData.start_time) {
      return moment.unix(formData.start_time).local().format('YYYY-MM-DDTHH:mm');
    }
    return '';
  },
  set: (newValue) => {
    formData.start_time = moment(newValue).unix();
    // console.log(formData.start_time );
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

const fetchMachineNames = async () => {
  const machinesUrl = 'http://192.168.0.105:6969/machines'; // Replace with the actual endpoint
  try {
    const response = await axios.get(machinesUrl);
    machineIds.value = response.data.Data.map((machine) => machine.machine_id);
    // console.log(machineIds.value);
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
    // console.log("++++++++++++++")
    // console.log(response.data)
    operators.value = response.data.Data.map((machine) => machine.welder_name);
    // console.log("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    // console.log(machine.welder_name)
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
    // console.log(machineId);
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


const deleteData = (machineName, startTime, endTime, elementName, operatorName) => {
  // Convert local date and time to epoch timestamps
  const startTimeEpoch = moment(startTime, 'YYYY-MM-DDTHH:mm').unix();
  const endTimeEpoch = moment(endTime, 'YYYY-MM-DDTHH:mm').unix();

  // Make sure elementName and operatorName are properly encoded
  const encodedElementName = encodeURIComponent(elementName);
  const encodedOperatorName = encodeURIComponent(operatorName);

  // Make the delete request to the backend
  const url = `http://192.168.0.105:6969/op_shift/?machine_name=${machineName}&start_time=${startTimeEpoch}&end_time=${endTimeEpoch}&element_name=${encodedElementName}&operator_name=${encodedOperatorName}`;

  axios
    .delete(url)
    .then(() => {
      console.log(`Data for machine ${machineName} deleted successfully.`);
      // After successful deletion, remove the deleted row from tableData
      tableData.value = tableData.value.filter((data) => {
        return !(data.machine_name === machineName && data.start_time === startTimeEpoch && data.end_time === endTimeEpoch && data.element_name === elementName && data.operator_name === operatorName);
      });
      setTimeout(() => {
        location.reload();
      }, 300);
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

const fetchMachineData = async () => {
  // Use the appropriate API endpoint to fetch data based on machine and operator names
  const url = `http://192.168.0.105:6969/op_shift/machine-data?machineName=${formData.machineName}&operatorName=${formData.operator_name}`;
  const response = await axios.get(url);




//  console.log("Insde the");
//  const current = response.data[0]["current"];
      // const voltage = response.data[0]["voltage"];
      // console.log(current);
      // console.log(voltage);

      let element_type = response.formData.element_type;
  // console.log(element_type);

  // Populate form data with the fetched data
  formData.element_type = response.data.element_type;
//   console.log("######################################################")
// console.log( formData.element_type)
  formData.start_time = response.data.start_time;
  formData.end_time = response.data.end_time;
  formData.shift = response.data.shift;
};



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

// Call fetchMachineData when the form is visible and in edit mode
onMounted(() => {
  if (isEditFormVisible.value && isEditMode.value) {
    fetchMachineData();
  }
});

const cancelForm = () => {
  resetFormData();
  isFormVisible.value = false;
  isProductionFormVisible.value = false;
  isProductionDataFormVisible.value = false;
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
const showProductionForm = () => {
  isProductionFormVisible.value = true;
  resetFormData();
};

const generateProductionExcel = async (event) => {
  // Prevent the default form submission behavior
  event.preventDefault();

  if (!machine_id || !startDateProd || !endDateProdProd) {
    alert('Please fill in all fields');
    return;
  }

  const formattedstartDateProd = moment(startDateProd).format('YYYY-MM-DD');
  const formattedendDateProdProd = moment(endDateProdProd).format('YYYY-MM-DD');

  console.log('Formatted Start Date:', formattedstartDateProd);
  console.log('Formatted End Date:', formattedendDateProdProd);

  // Updated backend URL with query parameters
  const backendURL = `http://192.168.0.105:6969/graph/get_production_end_data?machine_id=${machine_id.value}&start_date=${formattedstartDateProd}&end_date=${formattedendDateProdProd}`;
// const backendURL = `http://192.168.0.105:6969/graph/get_production_end_data?machine_id=${machine_id.value}&start_date=${formattedstartDateProd}&end_date=${formattedendDateProdProd}`;
  console.log('Backend URL:', backendURL);

  try {
    console.log('Before HTTP request');
const response = await axios.get(backendURL);
console.log('After HTTP request');

  console.log('Response Data:', response.data);

  if (response.data) {
    const processedData = response.data;
    console.log('Processed Data:', processedData);

    const ws = XLSX.utils.json_to_sheet(processedData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

    // Use await to ensure the file is generated before proceeding
    console.log('Before file download');
await XLSX.writeFileAsync(wb, 'production_data.xlsx');
console.log('After file download');
  } else {
    alert('No data found for the selected parameters');
  }
} catch (error) {
  console.error('Error fetching or processing production data:', error);
}

}
</script>

<style scoped>
/* Add your Tailwind CSS classes or styles here if needed */
/* .modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 10% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer; */
/* } */
</style>
