<template>
  <div>
    <button @click="showElementMasterTable">Element Master Table</button>
    <button @click="showWelderMasterTable">Welder Master Table</button>
  </div>
</template>

  
<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const showElementMasterTable = () => {
  // Navigate to the ElementMasterTable component
  router.push('/elementMasterTable');
};

const showWelderMasterTable = () => {
  // Navigate to the WelderMasterTable component
  router.push('/welderMasterTable');
};
</script>

  
  <style>
  
  </style>