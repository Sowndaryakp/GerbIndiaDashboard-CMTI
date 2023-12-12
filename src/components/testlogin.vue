<template>
  <div class="min-h-screen flex items-center justify-center bg-cover " style="background-image: url('/src/components/welder.jpg');">
    <div><img src="/src/components/login.png" alt="" class="h-72  "></div>
    <div class="bg-white bg-opacity-30 p-8 rounded-md shadow-md backdrop-blur-md">
      <h2 class="text-2xl font-semibold mb-4  text-white">
        <div>
          <img src="/src/components/gerbindia.svg" alt="" class="h-20 w-25">
          
      

        </div>
        
      </h2>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="text-white font-poppins">Username :</label>
          <input v-model="username" class="w-full p-2 rounded-md bg-gray-100 text-gray-800" />
        </div>
        <div class="mb-4">
          <label class="text-white font-poppins">Password :</label>
          <input type="password" v-model="password" class="w-full p-2 rounded-md bg-gray-100 text-gray-800" />
        </div>
        <button type="submit" class="w-full bg-blue-500 text-white font-novasquare  p-2 rounded-md hover:bg-blue-600 focus:outline-none">Login</button>
        
      </form>
      <div class="flex ml-8 mt-6">
            <p class="text-base mt-1 text-white font-novasquare ">Powered By    </p>
            <!-- <img width="30" height="30" src="https://img.icons8.com/ios-glyphs/30/FFFFFF/lightning-bolt--v1.png" alt="lightning-bolt--v1"/>  -->
          <img src="/src/components/cmti_logo.svg" alt="" class="h-8 w-25 ml-3" style="filter: brightness(0) invert(1) grayscale(1) contrast(100);"/>


          </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        // Create a FormData object to send the payload as multipart/form-data
        const formData = new FormData();
        formData.append("username", this.username);
        formData.append("password", this.password);

        // Use Axios to send login request to the FastAPI backend
        const response = await this.$axios.post("http://192.168.0.105:6969/login", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        // Store the token securely in localStorage
        const token = response.data.access_token;
        localStorage.setItem("authToken", token);

        // Redirect to the home page
        this.$router.push("/weldertable");
      } catch (error) {
        console.error("Login failed:", error);
      }
    },
  },
};
</script>
