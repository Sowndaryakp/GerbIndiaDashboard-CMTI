<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
      <div class="text-center">
        <img src="./error.png" alt="404 Image" class="w-32 mx-auto mb-4" />
  
        <h1 class="text-4xl font-bold text-gray-800">404 - Not Found</h1>
        
        <p class="text-gray-600 mb-4">Access Restricted. Please login to continue.</p>
        
        <router-link to="/log" class="text-blue-500 underline">Login</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    // Component logic goes here if needed
  };
  </script>
  
  <style scoped>
  /* Add any additional styling specific to this component */
  </style>
  