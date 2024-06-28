<template>
  <div class="overflow-y-auto h-64">
    <table class="min-w-full divide-y divide-gray-200">
      <thead tclass="sticky top-0 bg-whie">
        <tr>
          <th v-for="header in headers" :key="header" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {{ header }}
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="(row, index) in rows" :key="index" class="bg-white">
          <td v-for="(cell, cellIndex) in row" :key="cellIndex" class="px-6 py-4 whitespace-no-wrap text-sm font-medium text-gray-900">
            {{ cell }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const headers = ['Column 1', 'Column 2'];
const rows = Array.from({ length: 20 }, (_, index) => [index + 1, 'Data ' + (index + 1)]);
</script>
