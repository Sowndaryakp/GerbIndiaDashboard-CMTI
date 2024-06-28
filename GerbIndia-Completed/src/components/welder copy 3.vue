<template>
  <div class="card p-8 bg-blue-50 shadow-lg rounded-lg">
    <div class="overflow-y-auto h-64">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="sticky top-0 bg-white">
          <tr class="bg-blue-500 text-white">
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-300">
          <tr v-for="row in dataRows" :key="row.id" class="border-t hover:bg-white transition-colors">
            </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const dataRows = ref([
  // Your row data here
]);
</script>
