<template>
    
</template>
<script>
import html2pdf from 'html2pdf.js';


const downloadTableDataAsExcel = async () => {
  try {
    // Make a request to the backend to fetch the data
    const response = await axios.get('http://192.168.0.105:6969/op_shift/');

    // Assuming the API response has a 'dataToDownload' key containing the specific data
    const dataToDownload = response.data.dataToDownload;
    console.log(response.data.dataToDownload);

    // Convert JSON data to Excel workbook
    const ws = XLSX.utils.json_to_sheet(dataToDownload);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, 'tableData.xlsx');
    // Create a Blob containing the Excel workbook
    const blob = XLSX.write(wb, { bookType: 'xlsx', mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

    // Create a link element to trigger the download
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'table_data.xlsx';

    // Trigger a click on the link to initiate the download
    link.click();

    // Clean up by revoking the object URL
    window.URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error('Error downloading table data:', error);
  }
};
</script>
<style >


</style>