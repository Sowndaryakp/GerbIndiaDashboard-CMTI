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

const notificationCount = ref(0);
const showPopup = ref(false);
const alertMessages = ref([]);

const calculateRanges = () => {
  for (let i = 1; i <= 40; i++) {
    if (i > 30) {
      // Use setTimeout to add a delay of 5 seconds (5000 milliseconds)
      setTimeout(() => {
        alertMessages.value.push(`Alert ${notificationCount.value + 1}: Range ${i} is greater than 30`);
        notificationCount.value++;
      }, 6000 * (i - 30)); // Delay each notification by 5 seconds
    }
  }
};
const closePopup = () => {
  showPopup.value = false;
  alertMessages.value = [];
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
