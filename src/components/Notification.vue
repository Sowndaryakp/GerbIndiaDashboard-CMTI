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
              <li v-for="(message, index) in alertMessages" :key="index" class="text-red-500">
                {{ message }}
              </li>
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

const router = useRouter(); // Initialize Vue Router

const calculateRanges = async () => {
  try {
    // Make an Axios request to fetch data from the specified URL
    const response = await axios.get("http://172.18.100.240:6969/logs/");
    const data = response.data.Data; // Access the "Data" property

    // Assuming the response is an array of JSON objects
    data.forEach((item) => {
      const { machine_id, voltage, current, time } = item;
      // Create the alert message using the data
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
  router.go(-1); // Navigate back to the previous page using Vue Router
};
</script>

<style>
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
@media (max-width: 640px) {
  .popup {
    width: 90%;
  }
}
</style>
