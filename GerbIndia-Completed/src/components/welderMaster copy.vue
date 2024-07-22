<template>
  <div>
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
          <tr v-for="(data, index) in tableData" :key="index">
            <td class="border px-4 py-2">{{ data.welder_name }}</td>
            <td class="border px-4 py-2">{{ data.welder_number }}</td>
            <td class="border px-4 py-2">{{ data.date_of_joining }}</td>
            <td class="border px-4 py-2">{{ data.welder_qualification }}</td>
            <td class="border px-4 py-2">{{ data.qualified_thickness }}</td>
            <td class="border px-4 py-2">
              <button @click="editWelder(index)" class="bg-blue-500 text-white px-2 py-1 rounded-lg mr-2">Edit</button>
              <button @click="deleteWelder(data.id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const tableHeaders = ["Welder Name","Welder Number",  "Date of Joining", "Welder Qualification", "Qualified Thgickness"];
const tableData = ref([]);

const fetchData = async () => {
  try {
    const response = await fetch("http://192.168.0.105:6969/welder/");
    const result = await response.json();
    tableData.value = result.Data;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

onMounted(() => {
  fetchData();
});

const editElement = (index) => {
  // Add your edit logic here
  console.log("Edit element at index:", index);
};

const deleteElement = (elementId) => {
  // Add your delete logic here
  console.log("Delete element with ID:", elementId);
};
</script>

<style scoped>
/* Add your scoped styles here */
</style>
