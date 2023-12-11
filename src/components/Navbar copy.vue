
<template>
   <nav class="flex items-center justify-between bg-gradient-to-r from-blue-500 to-purple-500 py-4 px-8  flex-wrap">
    <!-- Company Name -->
    <span class="text-white text-xl font-semibold">
      <!-- <img src="./gerbindia.svg" style='width:100px;margin-left: 2px;margin-top: -1px;'> -->
      <img src="https://www.gerb.com/wp-content/uploads/2021/03/GERB-Logo_black.png" style='width:100px;margin-left: 2px;margin-top: -1px;'>
    </span>

    <div class="flex flex-wrap"><router-link
  to="/weldertable"
  class="text-white text-lg font-poppins hover:text-blue-200 transition-colors"
  :class="{ selected: $route.path === '/weldertable' }"
  
>

  WELDER
</router-link>

<!-- Add Machine Scheduling link -->
<router-link 
  to="/machinescheduling"
  class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
  :class="{ selected: $route.path === '/machinescheduling' }"

>
  MACHINE-SCHEDULING
  
</router-link>

<router-link 
  to="/reporttable"
  class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
  :class="{ selected: $route.path === '/reporttable' }"

>
  Report 
  
</router-link>
</div>
    
<div class="text-white flex items-center space-x-9">
  <span class="text-white text-xl font-semibold">
      <!-- <img src="./cmti_logo.svg" class="white-image" style='width:85px;margin-left: 2px;margin-top: -1px; position: absolute; top: 15px; right:460px;'> -->
      <img src="https://static.wixstatic.com/media/c942f4_7e390963b5e14b6ea79bb91125959fbf~mv2.png/v1/fill/w_260,h_154,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/favicon.png" class="white-image" style='width:85px;margin-left: 2px;margin-top: -1px; position: absolute; top: 15px; right:460px;'>
      <!-- <img src="./cmti_logo.svg" class="white-image"> -->
    </span>
</div>


    <!-- Right Section: Date, Time, and User Icon -->
    <div class="text-white  items-center space-x-4 flex flex-wrap">
      
      <img width="24" height="24" src="https://img.icons8.com/material-outlined/24/FFFFFF/clock--v1.png" alt="clock--v1" class="flex flex-wrap -ml-1 mt-1 -mr-3"/><span>{{ currentDate }}</span>
      <img width="24" height="24" src="https://img.icons8.com/hieroglyphs/32/FFFFFF/experimental-calendar-hieroglyphs.png" alt="experimental-calendar-hieroglyphs" class="flex flex-wrap -ml-1 mt-1 -mr-3"/><span>{{ currentTime }}</span>

      
    <p class="font-bold bg-blue-400   flex flex-col text-center w-20 shadow-lg hover:bg-lime-500    rounded  ">{{ currentShift }}</p>
      <button @click="showUserPopup()" class="hover:text-gray-300 flex flex-wrap">
        <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/FFFFFF/user--v1.png" alt="user--v1" class="flex flex-wrap "/>

      </button>

    </div>

    <!-- <div>
    -->
    <!-- <h2>Upcoming Shifts:</h2>
    <ul>
      <li v-for="shift in upcomingShifts" :key="shift.id">{{ shift.name }}</li>
    </ul> -->
  <!-- </div> -->

    <!-- User Info Popup -->
    <div v-if="isUserPopupVisible" class="absolute top-16 right-8 bg-white p-4 rounded-lg shadow-lg">
      <p>Name: {{ userInfo.name }}</p>
      <p>Email: {{ userInfo.email }}</p>
      <p>Position: {{ userInfo.position }}</p>
      <div class="flex space-x-4 mt-2"> 
        <button @click="showLoginPopup" class="bg-blue-500 text-white px-4 py-2 mt-4 rounded-lg"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAACXBIWXMAAAsTAAALEwEAmpwYAAABpUlEQVR4nO2WXStEYRDHz61wSayXDVt8F7mRl7SfYO16C/kollJSIqwr+QBcKPYKWdeSWywJi5+mRg61e57nOYf2Yv91bs6Z+f+fmTPPzHheDdUGoANYAPaBa+AJeAQK+i4NtEcp2AmsAe8EowQsA7GwoqPAnZI+A+vAMBAH6oB6oBcYAzaBF7UtAgOuopPAhxJtS+QGPt3AjvpIhjK2okMqKs4TDoeeBd7U3yxyoE1TJZiyFf0lLrgHWk0cVtQh5yrq48op15KJ8SJwI9engs0BkAeaA7h6tOBKkknH8/8gPNZIzgzEt9R2PArhZhUNFAeSarcXWlgJm4BTJS2UKyC954LLSmSHuCNfhrNRvxerT/iPUt2nNhdWAgbFdf5vxQWcOFynVBQN5MiwgSSMGwjfLXPXCwnhUK6siXFMG7tgJoTonHLIPG8xdRrUsSjPtKPo11jst3XO+BYBGe5xA5+EL70imrY9tH8huPWtPhvACNClq0+D3tOkbimvvvTaRVpmu1zV1AVBqjdr/E8tNpN5aQTAla63D9KR9F0qkplbgxcxPgHl2I+IIKmA8QAAAABJRU5ErkJggg==">Log in</button>
      <button @click="hideUserPopup" class="bg-red-500 text-white px-4 py- mt-4 rounded-lg"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAACXBIWXMAAAsTAAALEwEAmpwYAAABcElEQVR4nO3WPU8VURDG8W0RKbkgWIiQ4Hcx9AKfALESPwxaEErwDSKEHigIRhtNxBJqiFGEAtD8zAlDckNy4cCeXCl4mt3sPjv/3XNmZqeqbnXThHuYwhJ2cIgDbGEFk7hfEtiLWRy7XCd4hb660Af4EUETeB5P4noHOjGMUczhKLz7GKkL3sViOs/wP8TbgP/Fs6qdcpoLfwI+8j/gSb9SYrYb/i7gL3MfaOAzVmuCByPhTtCfA/0ab7pZBxzxXkesp7nQdGwUAI9HvOVWhm58CVPqRr11oRE31XnS91aGT66n9UvAXeHbLw1eqwvuPrfURWoPjyLmt5uVXC3gH6ty5TSRY27Enm/UhA5lN5CSwvv42ul2Ql8E9GepnpALPfstPr5OgDQI7GEBA5l7era8CTpZavR5g7GYNO7gbtTpeNw7blreq39ps9CDmaZ56iKl7J0uuqdOp83n+IDtGG9/p46UmkOq07aWzK2qTP0DEPoYdQrQa0kAAAAASUVORK5CYII=">Logout</button>

    </div>
    </div>

    <div v-if="isLoginPopupVisible" class="login-popup">
  <div class="login-content">
    <AdminLogin/>
    <!-- Add content for login popup here -->
    <!-- For example, you can add a cancel icon and other login-related elements -->
    <button @click="hideLoginPopup" class="cancel-icon rounded-lg px-3 py-1 mt-1 mr-1  bg-white"><img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/></button>
    <!-- Add other login form elements here -->
  </div>
</div>
    
  </nav>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import Line from '@/components/Line.vue';
import AdminLogin from '@/components/AdminLogin.vue';

const currentDate = ref('');
const currentTime = ref('');
const isUserPopupVisible = ref(false);
const isLoginPopupVisible = ref(false);
const userInfo = {
  name: "Admin",
  email: "admin@gmail.com",
  position: "Supervisor",
};
const shifts = [
  { id: 1, name: 'SHIFT-1', startTime: '09:00', endTime: '12:00' },
  { id: 2, name: 'SHIFT-2', startTime: '12:00', endTime: '14:00' },
  { id: 3, name: 'SHIFT-3', startTime: '14:00', endTime: '16:00' },
  { id: 4, name: 'SHIFT-4', startTime: '16:00', endTime: '18:00' }
];

const isTimeInRange = (time, startTime, endTime) => {
  return time >= startTime && time < endTime;
};

const currentShift = computed(() => {
  const currentTimeValue = new Date().toLocaleTimeString('en-US', {
    hour12: false,
    hour: 'numeric',
    minute: 'numeric'
  });

  for (const shift of shifts) {
    if (isTimeInRange(currentTimeValue, shift.startTime, shift.endTime)) {
      return shift.name;
    }
  }
  return 'No shift currently';
});

const upcomingShifts = computed(() => {
  const currentTimeValue = new Date().toLocaleTimeString('en-US', {
    hour12: false,
    hour: 'numeric',
    minute: 'numeric'
  });

  return shifts.filter(shift => {
    return !isTimeInRange(currentTimeValue, shift.endTime);
  });
});

const showLoginPopup = () => {
  isLoginPopupVisible.value = true;
  isUserPopupVisible.value = false;
};

const hideLoginPopup = () => {
  isLoginPopupVisible.value = false;
};

const showUserPopup = () => {
  isUserPopupVisible.value = true;
};

const hideUserPopup = () => {
  isUserPopupVisible.value = false;
};

onMounted(() => {
  setInterval(() => {
    const now = new Date();
    currentDate.value = now.toDateString();
    currentTime.value = now.toLocaleTimeString();
  }, 1000);
});
</script>

<style>
/* Styling for the Navbar component can go here */
.popup {
  width: 320px; /* Adjust the width as needed */
  height: 240px; /* Adjust the height as needed */
  padding: 20px; /* Add padding to create spacing between content and buttons */
}

/* Styling for the buttons inside the popup */
.popup button {
  margin-top: 8px; /* Add margin between the buttons */
}
/* Styling for the Login Popup Window */
.login-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.5); /* Add a semi-transparent background to blur the content behind the popup */
  z-index: 9999; /* Set a high z-index to ensure the popup appears above other elements */
}

.login-content {
  background-color: #b4dcf3; /* Set the background color of the popup content */
  padding: 5px;
  border-radius: 8px;
  position: relative;
}
/* Styling for the selected link in the Navbar */
.selected {
  background-color: #386d98; /* Add the background color you prefer */
  color: #333; /* Add the text color you prefer */
  border-radius: 8px; /* Add rounded corners */
  padding: 4px 12px; /* Add padding to create spacing */
}


.cancel-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  border: none;
  cursor: pointer;
}
.white-image {
    filter: brightness(0) invert(1) brightness(100%);
    width: 100px;
    margin-left: 2px;
    margin-top: -1px;
  }
/* .cursor{
  cursor:pointer;
}
.cursor{
  cursor : url("./https://www.gerb.com/about-gerb/"),auto;
} */
</style>
