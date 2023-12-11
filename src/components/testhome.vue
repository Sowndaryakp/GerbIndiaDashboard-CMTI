<template>
    <!-- <Navbar/> -->
      <div>
  
        <h2>Home</h2>
        <button @click="fetchData">Fetch Data</button>
        <button @click="logout">Logout</button>
        <filtertest/>
        
      </div>
    </template>
    
    <script>
    // import Navbar from '@/components/Navbar.vue';
    import filtertest from './filtertest.vue';
    export default {
      components: {
      // Navbar,
      filtertest,
    },
      methods: {
        fetchData() {
          try {
            // Retrieve the stored token from localStorage
            const storedToken = localStorage.getItem("authToken");
    
            if (!storedToken) {
              console.error("Token not found. User is not authenticated.");
              return;
            }
    
            // Use Axios to send authenticated request to fetch data
            this.$axios
              .get("/protected-data", {
                headers: {
                  Authorization: `Bearer ${storedToken}`,
                },
              })
              .then((response) => {
                console.log("Fetched data:", response.data);
              })
              .catch((error) => {
                console.error("Failed to fetch data:", error);
              });
          } catch (error) {
            console.error("An error occurred:", error);
          }
        },
        logout() {
        // Clear the token from localStorage
        localStorage.removeItem("authToken");
  
        // Redirect to the login page
        this.$router.push("/log");
  
        // Optionally, you may want to perform additional cleanup or API calls on logout
      },
  
  
      },
    };
    </script>
    