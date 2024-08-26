<template>
  <div>
    <div class="flex">
      <button @click="showProjectForm" class="bg-blue-500 glassmorphic-button rounded-lg px-4 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
        Add Project Details
      </button>
    </div>
    <div class="container mx-auto" ref="reportContainerTable">
      <h1 class="text-2xl font-semibold my-4">Project Data</h1>
      <table class="table-auto border-collapse w-full">
        <thead>
          <tr>
            <th v-for="(header, index) in tableHeaders" :key="index" class="px-4 py-2">{{ header }}</th>
            <th class="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in tableData" :key="index">
            <td class="border px-4 py-2 text-center">
              <span v-if="!data.isEditing">{{ data.project }}</span>
              <input v-else v-model="data.project" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" disabled/>
            </td>
            <td class="border px-4 py-2 text-center">
              <span v-if="!data.isEditing">{{ data.I_no }}</span>
              <input v-else v-model="data.I_no" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" />
            </td>
            <td class="border px-4 py-2 text-center">
              <span v-if="!data.isEditing">{{ data.Fc_no }}</span>
              <input v-else v-model="data.Fc_no" class="border border-gray-300 rounded-lg px-2 py-1 w-full text-center" />
            </td>
            <td class="border px-4 py-2 flex justify-center">
              <button v-if="!data.isEditing" @click="toggleEdit(index)" class="bg-blue-500 glassmorphic-button text-white px-2 py-1 rounded-lg mr-2">Edit</button>
              <button v-else @click="saveEditedProject(index)" class="bg-green-500 glassmorphic-button text-white px-2 py-1 rounded-lg mr-2">Save</button>
              <button @click="deleteProject(data)" class="bg-red-500 glassmorphic-button text-white font-bold py-2 px-4 rounded">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="isProjectForm" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="w-96 p-4 bg-gray-100 border border-gray-300 rounded-lg shadow-md">
          <form @submit.prevent="submitProjectForm">
            <div class="mb-2">
              <label class="block text-gray-800">I No:</label>
              <input v-model="I_noValue" type="text" id="elementType" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter I no" />
            </div>

            <div class="mb-2">
              <label class="block text-gray-800">Fc No:</label>
              <input v-model="Fc_noValue" type="text" id="elementRange" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter Fc no"/>
            </div>
            <div class="mb-2">
              <label class="block text-gray-800">Project:</label>
              <input v-model="projectValue" type="text" id="elementCurrent" required class="border border-gray-300 rounded-lg px-2 py-1 w-full" placeholder="enter project name"/>
            </div>
            <div class="mt-2 flex justify-end">
              <button type="submit" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Create</button>
              <button @click="cancelProjectForm" class="bg-gray-300 text-gray-700 px-2 py-1 rounded-lg">Cancel</button>
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

const isComponentMounted = ref(false);

const isProjectForm = ref('');
const I_noValue = ref('');
const Fc_noValue = ref('');
const projectValue = ref('');

const showProjectForm = () => {
  isProjectForm.value = true;
};

const cancelProjectForm = () => {
  isProjectForm.value = false;
  resetProjectFormFields();
};

const resetProjectFormFields = () => {
  I_noValue.value = '';
  Fc_noValue.value = '';
  projectValue.value = '';
};

const submitProjectForm = async () => {
  try {
    const formData = {
      I_no: I_noValue.value,
      Fc_no: Fc_noValue.value,
      project: projectValue.value,
    };

    const response = await axios.post('http://192.168.0.105:6969/project/', formData);

    console.log('Project created successfully:', response.data);

    resetProjectFormFields();
    isProjectForm.value = false;
    fetchData();
  } catch (error) {
    console.error('Error creating project:', error);
  }
};

onMounted(() => {
  if (!isComponentMounted.value) {
    fetchData();
    isComponentMounted.value = true;
  }
});

const tableHeaders = [ "Project","I_no", "Fc_no"];

const tableData = ref([]);

const fetchData = async () => {
  try {
    const response = await fetch("http://192.168.0.105:6969/project/");
    const result = await response.json();

    const projectData = result.Data || [];

    tableData.value = projectData.map(data => ({ ...data, isEditing: false }));
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

const saveEditedProject = async (index) => {
  const editedProject = tableData.value[index];
  
  const postData = {
    I_no: editedProject.I_no || 'N/A',
    Fc_no: editedProject.Fc_no || 'N/A',
    project: editedProject.project || 'N/A',
  };

  try {
    const url = `http://192.168.0.105:6969/project/${editedProject.project}`;

    await axios.put(url, postData);

    tableData.value[index].isEditing = false;
  } catch (error) {
    console.error('Error updating the project data:', error);
  }
};

const deleteProject = async (project, I_no, Fc_no) => {
  try {
    const url = `http://192.168.0.105:6969/project/${project.project}?project=${project.project}&I_no=${project.I_no}&Fc_no=${project.Fc_no}`;
    await axios.delete(url);

    // Update the local tableData by filtering out the deleted project
    tableData.value = tableData.value.filter(data => data.id !== project.id);
  } catch (error) {
    console.error('Error deleting the project:', error);
  }
};




</script>

<style scoped>
/* Add your scoped styles here */
</style>
