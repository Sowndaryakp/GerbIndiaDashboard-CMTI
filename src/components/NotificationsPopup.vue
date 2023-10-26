<template>
    <div class="popup" v-if="showPopup">
      <div class="notification">
        <p>{{ message }}</p>
      </div>
      <button @click="closePopup">Close</button>
    </div>
  </template>
  
  <script setup>
import { ref, defineProps, defineEmits } from "vue";

const { message } = defineProps(["message"]);
const { closePopup } = defineEmits(["closePopup"]);

const showPopup = ref(true);

const closePopupHandler = () => {
  closePopup("closePopup");
};

</script>

<style scoped>
  /* Your styling for the pop-up component */
</style>
  