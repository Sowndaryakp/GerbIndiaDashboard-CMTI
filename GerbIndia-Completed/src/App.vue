<template>
  <div>
  <Navbar/>
    <!-- The Navbar component is included here -->
    <!-- <Navbar /> -->

    <!-- The content for the current route will be rendered here -->
    <router-view />

    <!-- The DataTable component should be included here -->
    <!-- <DataTable /> -->
    <!-- <DataTableCopy /> -->
    <!-- <welder/> -->
    <Footer />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';
// import DataTable from './components/DataTable.vue';
import Footer from './components/Footer.vue';
// import DataTableCopy from './components/DataTableCopy.vue';
// import DataTab from './components/DataTab.vue';
import welder from './components/welder.vue';


export default {
  components: {
    Navbar,
    // DataTable,
    // DataTableCopy,
    // DataTab,
    welder,
    Footer,
    name: 'MyComponent',
  },
};
</script>

<style>
/* Global styling for the App component can go here */
.popins-font {
  font-family: 'Poppins', sans-serif;
  
}
</style>
