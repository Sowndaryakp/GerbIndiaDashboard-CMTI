<template>
  <div>
    <button @click="openPopup">Open Alert</button>
    <div v-if="showPopup" class="popup">
      {{ alertMessage }}
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';

let showPopup = false;
let alertMessage = "";

const openPopup = async () => {
  try {
    // Make an Axios request to fetch data from the specified URL
    const response = await axios.get("http://172.18.100.240:6969/logs/");
    const data = response.data.Data; // Access the "Data" property

    // Assuming the response is an array of JSON objects
    data.forEach((item) => {
      const { machine_id, voltage, current, time } = item;
      // Create the alert message using the data
      alertMessage = `Machine id ${machine_id} has crossed voltage ${voltage}/current ${current} at the time ${time}`;
      showPopup = true;
    });
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};
</script>

<style>
.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  padding: 10px;
  border: 1px solid #000;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  z-index: 999;
}
</style>
