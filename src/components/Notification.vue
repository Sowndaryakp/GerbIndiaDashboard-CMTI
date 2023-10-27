<template>
  <div class="container mx-auto p-4">
    <button @click="togglePopup" class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md mr-4 w-16 relative">
      <img width="24" height="24" src="https://img.icons8.com/material-sharp/24/FFFFFF/alarm--v1.png" alt="alarm--v1" class="ml-3"/>
      <span v-if="notificationCount > 0" class="notification-counter absolute top-0 right-0 -mt-2 -mr-2 bg-red-500 text-white rounded-full w-6 h-6 text-center">
        {{ notificationCount }}
      </span>
    </button>

    <!-- Popup -->
    <!-- <div v-if="isPopupOpen" class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50"> -->
      <div class="bg-white p-4 rounded-md shadow-md w-48">
        <!-- Close button -->
        <!-- <button @click="closePopup" class="absolute top-0 right-0 p-1 m-1 h-6 w-6 text-gray-500 hover:text-red-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button> -->

        <!-- Random notification content -->
        <div>
          <h2 class="text-xl font-semibold mb-2">Notification</h2>
          <p>{{ randomMessage }}</p>
        </div>
      </div>
    </div>
  <!-- </div> -->
</template>

<script setup>
import { ref, onMounted } from 'vue';

const notificationCount = ref(5); // Initial notification count
const isPopupOpen = ref(false);
const randomMessage = ref('');

const messages = [
  "Hello, world!",
  "This is a random message.",
  "Vue.js is awesome!",
  "You've got a new message!",
  "Don't forget to stay hydrated.",
];

const togglePopup = () => {
  isPopupOpen.value = !isPopupOpen.value;
  notificationCount.value = 0;
};

const closePopup = () => {
  isPopupOpen.value = false;
};

const generateRandomMessage = () => {
  const randomIndex = Math.floor(Math.random() * messages.length);
  randomMessage.value = messages[randomIndex];
};

onMounted(() => {
  generateRandomMessage();
});
</script>

<style>
.notification-counter {
  line-height: 1.25rem;
}
</style>
