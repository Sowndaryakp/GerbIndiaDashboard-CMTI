<template>
  <div>
    <h2>Machine Data</h2>
    <div>
      <label for="date">Select Date:</label>
      <input type="date" v-model="selectedDate" id="date" />
    </div>
    <div>
      <label for="machine">Select Machine:</label>
      <select v-model="selectedMachine" id="machine">
        <option value="7D">7D</option>
        <option value="7F">7F</option>
        <option value="7E">7E</option>
      </select>
    </div>
    <button @click="downloadExcel">Download Excel</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedDate: "", // You can initialize with the current date if needed
      selectedMachine: "7D", // Default machine selection
    };
  },
  methods: {
    async downloadExcel() {
      const url = `http://192.168.0.105:9999/live_data/${this.selectedMachine}`;
      
      try {
        const response = await this.$axios.get(url, {
          params: {
            date: this.selectedDate,
          },
          responseType: "arraybuffer", // Specify response type as arraybuffer for binary data
        });

        // Create a Blob from the response data
        const blob = new Blob([response.data], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", // Excel MIME type
        });

        // Create a link to download the Blob
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "machine_data.xlsx"; // Change the filename as needed
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("Error downloading data:", error);
      }
    },
  },
};
</script>
