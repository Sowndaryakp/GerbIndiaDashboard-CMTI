<template>
  <div>
    <button @click="calculateRanges" class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md mr-4 w-16">
      <div class="notification-icon relative">
        <i width="24" height="24" class="fas fa-bell cursor-pointer" @click="showPopup = true"></i>
        <span v-if="notificationCount > 0" class="notification-count">{{ notificationCount }}</span>
        <div v-if="showPopup" class="popup top-0">
          <div class="popup-content">
            <h2>Alert Messages</h2>
            <ul>
              
                <!-- {{ message }} -->
                 <!-- Display data in a table -->
    <table class="table-auto" v-if="responseData">
      <thead>
        <tr>
          <th>Time</th>
          <th>Current</th>
          <th>Voltage</th>
          <th>Machine ID</th>
        </tr>
      </thead>
      <li v-for="(message, index) in alertMessages" :key="index" class="text-red-500">
      <tbody>
        <tr v-for="(item, index) in responseData.Data" :key="index">
          <td>{{ item.time }}</td>
          <td>{{ item.current }}</td>
          <td>{{ item.voltage }}</td>
          <td>{{ item.machine_id }}</td>
        </tr>
      </tbody>
    </li>
    </table>
             
            </ul>
            <button @click="closePopup">Close</button>
          </div>
        </div>
      </div>
    </button>

   
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; // Import Vue Router

const notificationCount = ref(0);
const showPopup = ref(false);
const alertMessages = ref([]);
const responseData = ref(null); // New variable to hold API response data

const router = useRouter(); // Initialize Vue Router

const calculateRanges = async () => {
  try {
    // Make an Axios request to fetch data from the specified URL
    const response = await axios.get(`http://172.18.100.240:6969/logs/${'7H'}`);
    responseData.value = response.data; // Store the entire response

    // Extract and process data, similar to your previous code
    const data = response.data.Data;
    data.forEach((item) => {
      const { machine_id, voltage, current, time } = item;
      alertMessages.value.push(`Machine id ${machine_id} has crossed voltage ${voltage}/current ${current} at the time ${time}`);
      notificationCount.value++;
    });
    showPopup.value = true;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

const closePopup = () => {
  showPopup.value = false;
  alertMessages.value = [];
  router.go(0); // Navigate back to the current page using Vue Router
};
</script>

<style>
.table-container {
  max-width: 100%;
  overflow-x: auto;
}
.notification-icon {
  position: relative;
  display: inline-block;
}

.notification-count {
  position: absolute;
  top: -15px;
  right: -48px;
  background-color: red;
  color: white;
  border-radius: 50%;
  padding: 5px 10px;
}

.popup {
  @apply absolute p-4 bg-white border shadow-lg rounded-md;
  top: 0;
  max-height: 80vh;
  overflow-y: auto;
  width: 320px;
}

.popup-content {
  @apply space-y-4;
}

.popup-content h2 {
  @apply text-lg font-bold;
}

.popup button {
  @apply bg-red-500 text-white py-2 px-4 rounded;
}

/* Responsive styles for smaller screens */
/* @media (max-width: 800px) {
  .popup {
    width: 100%;
  }
} */
</style>
