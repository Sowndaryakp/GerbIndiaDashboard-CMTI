<template>
    <nav class="flex items-center justify-between bg-gradient-to-r from-blue-500 to-purple-500 py-4 px-8 flex-wrap fixed w-full">
      <!-- Company Name -->
      <span class="text-white text-xl font-semibold">
        <img src="https://www.gerb.com/wp-content/uploads/2021/03/GERB-Logo_black.png" style="width:100px;margin-left: 2px;margin-top: -1px;">
      </span>
  
      <!-- Navigation Links -->
      <div class="flex flex-wrap">
        <router-link to="/weldertable" class="text-white text-lg font-poppins hover:text-blue-200 transition-colors"
          :class="{ selected: $route.path === '/weldertable' }">WELDER</router-link>
        <router-link to="/machinescheduling"
          class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
          :class="{ selected: $route.path === '/machinescheduling' }">MACHINE-SCHEDULING</router-link>
        <router-link to="/elementMasterTable"
          class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
          :class="{ selected: $route.path === '/elementMasterTable' }">Element-Master</router-link>
        <router-link to="/welderMasterTable"
          class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
          :class="{ selected: $route.path === '/welderMasterTable' }">Welder-Master</router-link>
        <router-link to="/reporttable"
          class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
          :class="{ selected: $route.path === '/reporttable' }">Report</router-link>
      </div>
  
      <!-- Right Section: Icons and User Info -->
      <div class="text-white flex items-center space-x-9">
        <!-- Instruction Icon -->
        <button @click="showInstructionPopup" class="hover:text-gray-300 flex flex-wrap">
          <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/FFFFFF/info.png" alt="info">
        </button>
  
        <!-- User Manual Link -->
        <button @click="openUserLink" class="text-lg hover:text-gray-300 p-1 border-white shadow flex flex-wrap">
          <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/FFFFFF/link.png" alt="link">
          <span class="ml-1">User Manual</span>
        </button>
  
        <!-- CMTI Logo -->
        <span class="text-white text-xl font-semibold">
          <img src="https://static.wixstatic.com/media/c942f4_7e390963b5e14b6ea79bb91125959fbf~mv2.png/v1/fill/w_260,h_154,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/favicon.png"
            class="white-image" style="width:130px;margin-left: 2px;margin-top: -1px; position: absolute; top: 1px; right:350px;">
        </span>
  
        <!-- Clock and User Icon -->
        <div class="text-white items-center space-x-4 flex flex-wrap">
          <img width="24" height="24" src="https://img.icons8.com/material-outlined/24/FFFFFF/clock--v1.png"
            alt="clock--v1" class="flex flex-wrap -ml-1 mt-1 -mr-3">
          <span>{{ currentDate }}</span>
          <span>{{ currentTime }}</span>
          <button @click="showUserPopup()" class="hover:text-gray-300 flex flex-wrap">
            <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/FFFFFF/user--v1.png" alt="user--v1"
              class="flex flex-wrap">
          </button>
        </div>
      </div>
  
      <!-- User Info Popup -->
      <div v-if="isUserPopupVisible"
        class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-4 rounded-lg shadow-lg z-50">
        <div class="absolute inset-0 bg-gray-900 opacity-50 rounded-lg"></div>
        <div class="relative bg-white p-4 rounded-lg shadow-lg z-50">
          <div class="flex flex-col space-y-4 backdrop-blur-md">
            <!-- User information -->
            <p>Name: {{ userInfo.name }}</p>
            <p>Email: {{ userInfo.email }}</p>
            <p>Position: {{ userInfo.position }}</p>
  
            <!-- Buttons -->
            <div class="flex justify-end space-x-4 backdrop-blur-md">
              <!-- Logout button -->
              <button @click="logout" class="bg-red-500 text-white px-4 py-2 rounded-lg backdrop-blur-md">
                <img
                  src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAACXBIWXMAAAsTAAALEwEAmpwYAAABcElEQVR4nO3WPU8VURDG8W0RKbkgWIiQ4Hcx9AKfALESPwxaEErwDSKEHigIRhtNxBJqiFGEAtD8zAlDckNy4cCeXCl4mt3sPjv/3XNmZqeqbnXThHuYwhJ2cIgDbGEFk7hfEtiLWRy7XCd4hb660Af4EUETeB5P4noHOjGMUczhKLz7GKkL3sViOs/wP8TbgP/Fs6qdcpoLfwI+8j/gSb9SYrYb/i7gL3MfaOAzVmuCByPhTtCfA/0ab7pZBxzxXkesp7nQdGwUAI9HvOVWhm58CVPqRr11oRE33XnS91aGT66n9UvAXeHbLw1eqwvuPrfURWoPjyLmt5uVXC3gH6ty5TSRY27Enm/UhA5lN5CSwvv42ul2Ql8E9GepnpALPfstPr5OgDQI7GEBA5l7era8CTpZavR5g7GYNO7gbtTpeNw7blreq39ps9CDmaZ56iKl7J0uuqdOp83n+IDtGG9/p46UmkOq07aWzK2qTP0DEPoYdQrQa0kAAAAASUVORK5CYII="
                  alt="Logout">
                Logout
              </button>
              <!-- Cancel button -->
              <button @click="hideUserPopup" class="bg-blue-500 text-white px-4 py-2 rounded-lg">
                <img
                  src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAACXBIWXMAAAsTAAALEwEAmpwYAAABpUlEQVR4nO2WXStEYRDHz61wSayXDVt8F7mRl7SfYO16C/kollJSIqwr+QBcKPYKWdeSWywJi5+mRg61e57nOYf2Yv91bs6Z+f+fmTPPzHheDdUGoANYAPaBa+AJeAQK+i4NtEcp2AmsAe8EowQsA7GwoqPAnZI+A+vAMBAH6oB6oBcYAzaBF7UtAgOuopPAhxJtS+QGPt3AjvpIhjK2okMqKs4TDoeeBd7U3yxyoE1TJZiyFf0lLrgHWk0cVtQh5yrq48op15KJ8SJwI9engs0BkAeaA7h6tOBKkknH8/8gPNZIzgzEt9R2PArhZhUNFAeSarcXWlgJm4BTJS2UKyC954LLSmSHuCNfhrNRvxerT/iPUt2nNhdWAgbFdf5vxQWcOFynVBQN5MiwgSSMGwjfLXPXCwnhUK6siXFMG7tgJoTonHLIPG8xdRrUsSjFJ4IiNmEQLvooFh3nOoC8D9YBOI/xJUuIF6FqZsHPUwBziN7fKw3QA9BivHsO3XJ7nJfLgAAAABJRU5ErkJggg=="
                  alt="Cancel">
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Instruction Popup -->
      <div v-if="isInstructionPopupVisible"
        class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div class="bg-white p-6 rounded-lg shadow-lg relative">
          <button @click="hideInstructionPopup" class="absolute top-2 right-2 text-gray-600 hover:text-gray-800">
            <img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign" />
          </button>
          <h2 class="text-lg font-semibold mb-4">Instructions</h2>
          <p class="text-gray-700">The shift is scheduled from the specified start time to the designated end time.</p>
          <p class="text-gray-700">On the welder's page, the scheduled shift will be displayed for the allotted duration.</p>
          <p class="text-gray-700">Once the shift has concluded, it will no longer be visible on the welder's page.</p>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue';
  import axios from 'axios';
  
  // Reactive data
  const isUserPopupVisible = ref(false);
  const isInstructionPopupVisible = ref(false);
  const userInfo = reactive({
    name: 'John Doe',
    email: 'john.doe@example.com',
    position: 'Engineer'
  });
  const currentDate = ref('');
  const currentTime = ref('');
  
  // Methods
  const showUserPopup = () => {
    isUserPopupVisible.value = true;
  };
  
  const hideUserPopup = () => {
    isUserPopupVisible.value = false;
  };
  
  const showInstructionPopup = () => {
    isInstructionPopupVisible.value = true;
  };
  
  const hideInstructionPopup = () => {
    isInstructionPopupVisible.value = false;
  };
  
  const fetchDataFromBackend = () => {
    axios.get('YOUR_API_URL/data')
      .then(response => {
        console.log('Data from backend:', response.data);
        // Handle data received from backend
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        // Handle error
      });
  };
  
  const updateDataOnBackend = (dataToUpdate) => {
    axios.put('YOUR_API_URL/data', dataToUpdate)
      .then(response => {
        console.log('Data updated successfully:', response.data);
        // Handle success message or update local state
      })
      .catch(error => {
        console.error('Error updating data:', error);
        // Handle error
      });
  };
  
  const deleteDataOnBackend = (idToDelete) => {
    axios.delete(`YOUR_API_URL/data/${idToDelete}`)
      .then(response => {
        console.log('Data deleted successfully:', response.data);
        // Handle success message or update local state
      })
      .catch(error => {
        console.error('Error deleting data:', error);
        // Handle error
      });
  };
  
  // Lifecycle hook
  onMounted(() => {
    // Fetch initial data or perform other actions on component mount
    fetchDataFromBackend();
  
    // Example: Update current date and time every second
    setInterval(() => {
      const now = new Date();
      currentDate.value = now.toLocaleDateString();
      currentTime.value = now.toLocaleTimeString();
    }, 1000);
  });
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  </style>
  