<template>
  <nav class="flex items-center justify-between bg-gradient-to-r from-blue-500 to-purple-500 py-4 px-8  flex-wrap fixed w-full">
   <!-- Company Name -->
   <span class="text-white text-xl font-semibold">
     <!-- <img src="./gerbindia.svg" style='width:100px;margin-left: 2px;margin-top: -1px;'> -->
     <img src="https://www.gerb.com/wp-content/uploads/2021/03/GERB-Logo_black.png" style='width:100px;margin-left: 2px;margin-top: -1px;'>
   </span>

   <div class="flex flex-wrap"><router-link
 to="/weldertable"
 class="text-white text-lg font-poppins hover:text-blue-200 transition-colors"
 :class="{ selected: $route.path === '/weldertable' }">
 WELDER
</router-link>

<!-- Add Machine Scheduling link -->
<router-link 
 to="/machinescheduling"
 class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
 :class="{ selected: $route.path === '/machinescheduling' }">
 MACHINE-SCHEDULING
</router-link>

<router-link 
 to="/elementMasterTable"
 class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
 :class="{ selected: $route.path === '/elementMasterTable' }">
 Element-Master 
</router-link>
<router-link 
 to="/welderMasterTable"
 class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
 :class="{ selected: $route.path === '/welderMasterTable' }">
 Welder-Master 
</router-link>
<!-- <router-link 
 to="/projectMasterTable"
 class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
 :class="{ selected: $route.path === '/projectMasterTable' }">
 Project-Master 
</router-link> -->
<!-- <router-link 
 to="/masterTable"
 class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
 :class="{ selected: $route.path === '/masterTable' }">
 Master Table
</router-link> -->
<router-link 
 to="/reporttable"
 class="ml-4 text-white text-lg font-poppins hover:text-blue-200 transition-colors"
 :class="{ selected: $route.path === '/reporttable' }">
 Report 
</router-link>
</div>
   
<div class="text-white flex items-center space-x-9">
   <!-- Instruction Icon -->
   <button @click="showInstructionPopup" class="hover:text-gray-300 flex flex-wrap">
        <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/FFFFFF/info.png" alt="info"/>
      </button>

       <!-- User Button to Open Link -->
       <button @click="openUserLink" class="text-lghover:text-gray-300 p-1 border-white shadow flex flex-wrap">
  <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/FFFFFF/link.png" alt="link"/>
  <span class="ml-1">User Manual</span>
</button>
 <span class="text-white text-xl font-semibold">
     <!-- <img src="./cmti_logo.svg" class="white-image" style='width:85px;margin-left: 2px;margin-top: -1px; position: absolute; top: 15px; right:460px;'> -->
     <img src="https://static.wixstatic.com/media/c942f4_7e390963b5e14b6ea79bb91125959fbf~mv2.png/v1/fill/w_260,h_154,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/favicon.png" class="white-image" style='width:130px;margin-left: 2px;margin-top: -1px; position: absolute; top: 1px; right:350px;'>
     <!-- <img src="./cmti_logo.svg" class="white-image"> -->
   </span>
  
</div>

   <!-- Right Section: Date, Time, and User Icon -->
   <div class="text-white  items-center space-x-4 flex flex-wrap">
     <img width="24" height="24" src="https://img.icons8.com/material-outlined/24/FFFFFF/clock--v1.png" alt="clock--v1" class="flex flex-wrap -ml-1 mt-1 -mr-3"/><span>{{ currentDate }}</span>
     <!-- <img width="24" height="24" src="https://img.icons8.com/hieroglyphs/32/FFFFFF/experimental-calendar-hieroglyphs.png" alt="experimental-calendar-hieroglyphs" class="flex flex-wrap -ml-1 mt-1 -mr-3"/> -->
     <span>{{ currentTime }}</span>
   <!-- <p class="font-bold bg-blue-400   flex flex-col text-center w-20 shadow-lg hover:bg-lime-500    rounded  ">{{ currentShift }}</p> -->
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
    <div v-if="isUserPopupVisible" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-4 rounded-lg shadow-lg z-50  ">
  <!-- Content of the popup -->
  <div class="absolute inset-0 bg-gray-900 opacity-50 rounded-lg"></div>
  <div class="relative bg-white p-4 rounded-lg shadow-lg z-50">
  <div class="flex flex-col space-y-4 backdrop-blur-md">
    <!-- User information -->
    <!-- <p>Name: {{ userInfo.name }}</p>
    <p>Email: {{ userInfo.email }}</p>
    <p>Position: {{ userInfo.position }}</p> -->
    <!-- <p>Username: {{ enteredUsername }}</p> -->

    <!-- Buttons -->
    <div class="flex justify-end space-x-4 backdrop-blur-md">
      <!-- Logout button -->
      <button @click="logout" class="bg-red-500 text-white px-4 py-2 rounded-lg backdrop-blur-md">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAACXBIWXMAAAsTAAALEwEAmpwYAAABcElEQVR4nO3WPU8VURDG8W0RKbkgWIiQ4Hcx9AKfALESPwxaEErwDSKEHigIRhtNxBJqiFGEAtD8zAlDckNy4cCeXCl4mt3sPjv/3XNmZqeqbnXThHuYwhJ2cIgDbGEFk7hfEtiLWRy7XCd4hb660Af4EUETeB5P4noHOjGMUczhKLz7GKkL3sViOs/wP8TbgP/Fs6qdcpoLfwI+8j/gSb9SYrYb/i7gL3MfaOAzVmuCByPhTtCfA/0ab7pZBxzxXkesp7nQdGwUAI9HvOVWhm58CVPqRr11oRE33XnS91aGT66n9UvAXeHbLw1eqwvuPrfURWoPjyLmt5uVXC3gH6ty5TSRY27Enm/UhA5lN5CSwvv42ul2Ql8E9GepnpALPfstPr5OgDQI7GEBA5l7era8CTpZavR5g7GYNO7gbtTpeNw7blreq39ps9CDmaZ56iKl7J0uuqdOp83n+IDtGG9/p46UmkOq07aWzK2qTP0DEPoYdQrQa0kAAAAASUVORK5CYII=">
        Logout
      </button>
      
      <!-- Cancel button -->
      <button @click="hideUserPopup" class="bg-blue-500 text-white px-4 py-2 rounded-lg">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAACXBIWXMAAAsTAAALEwEAmpwYAAABpUlEQVR4nO2WXStEYRDHz61wSayXDVt8F7mRl7SfYO16C/kollJSIqwr+QBcKPYKWdeSWywJi5+mRg61e57nOYf2Yv91bs6Z+f+fmTPPzHheDdUGoANYAPaBa+AJeAQK+i4NtEcp2AmsAe8EowQsA7GwoqPAnZI+A+vAMBAH6oB6oBcYAzaBF7UtAgOuopPAhxJtS+QGPt3AjvpIhjK2okMqKs4TDoeeBd7U3yxyoE1TJZiyFf0lLrgHWk0cVtQh5yrq48op15KJ8SJwI9engs0BkAeaA7h6tOBKkknH8/8gPNZIzgzEt9R2PArhZhUNFAeSarcXWlgJm4BTJS2UKyC954LLSmSHuCNfhrNRvxerT/iPUt2nNhdWAgbFdf5vxQWcOFynVBQN5MiwgSSMGwjfLXPXCwnhUK6siXFMG7tgJoTonHLIPG8xdRrUsSjPtKPo11jst3XO+BYBGe5xA5+EL70imrY9tH8huPWtPhvACNClq0+D3tOkbimvvvTaRVpmu1zV1AVBqjdr/E8tNpN5aQTAla63D9KR9F0qkplbgxcxPgHl2I+IIKmA8QAAAABJRU5ErkJggg==">Cancel</button>
    </div>
  </div>
</div>
</div>


   <div v-if="isLoginPopupVisible" class="login-popup">
     <div class="login-content">
       <AdminLogin/>
       <button @click="hideLoginPopup" class="cancel-icon rounded-lg px-3 py-1 mt-1 mr-1  bg-white">
         <img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/>
       </button>
     </div>
   </div>
   
   <!-- Instruction Popup -->
   <div v-if="isInstructionPopupVisible" class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
  <div class="bg-white p-6 rounded-lg shadow-lg relative">
    <button @click="hideInstructionPopup" class="absolute top-2 right-2 text-gray-600 hover:text-gray-800">
      <img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign" />
    </button>
    <h2 class="text-xl font-semibold mb-4">Instructions</h2>
    <button @click="showAddInstruction"
        class="bg-blue-500 glassmorphic-button rounded-lg px-2 py-2 mt-2 mb-2 ml-3 text-white font-poppins flex flex-wrap">
        <img src="https://img.icons8.com/material-outlined/24/FFFFFF/add.png" alt="add" class="w-6 h-6 mr-2" />
        Add Instruction
      </button>
    <div v-for="instruction in instructions" :key="instruction.id" class="flex justify-between items-center mb-4">
      <!-- Editing View -->
      <div v-if="editingInstructionId === instruction.id" class="w-full">
        <textarea v-model="editingInstructionText" class="border border-gray-300 p-2 rounded-lg w-full"></textarea>
        <button @click="updateInstruction(instruction.id)" class="bg-green-500 text-white px-4 py-2 rounded-lg mt-2">Save</button>
        <button @click="cancelEdit" class="bg-gray-500 text-white px-4 py-2 rounded-lg mt-2 ml-2">Cancel</button>
      </div>
      <!-- Display View -->
      <div v-else class="flex justify-between w-full">
        <p class="text-gray-700">{{ instruction.instruction }}</p>
        <div class="flex space-x-2">
          <button @click="editInstruction(instruction)" class="bg-yellow-500 text-white px-1 py-2 rounded-lg">
            <img width="20" height="20" src="https://img.icons8.com/sf-black-filled/64/FFFFFF/edit.png" alt="edit"/>
          </button>
          <button @click="deleteInstruction(instruction.id)" class="bg-red-500 text-white px-1 py-2 rounded-lg">
            <img width="20" height="20" src="https://img.icons8.com/sf-black-filled/64/FFFFFF/delete-forever.png" alt="delete-forever"/>
          </button>
        </div>
      </div>
    </div>
    <div v-if="addingNewInstruction" class="w-full mb-4">
        <textarea v-model="newInstructionText" class="border border-gray-300 p-2 rounded-lg w-full"></textarea>
        <button @click="addInstruction" class="bg-green-500 text-white px-4 py-2 rounded-lg mt-2">Save</button>
        <button @click="cancelAdd" class="bg-gray-500 text-white px-4 py-2 rounded-lg mt-2 ml-2">Cancel</button>
      </div>
    </div>
    
</div>

   

    <div v-if="alertMessage" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="w-96 p-4 bg-gray-100 border text-center border-gray-300 rounded-lg shadow-md">
      <p class="text-center text-xl text-green-600">{{ alertMessage }}</p>
      <button @click="closeAlert" class="bg-blue-500 text-white px-2 py-1 rounded-lg mt-2">OK</button>
    </div>
  </div>
 </nav>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import Line from '@/components/Line.vue';
import AdminLogin from '@/components/AdminLogin.vue';
import { useRouter } from 'vue-router'
import { defineProps } from 'vue';
import axios from 'axios';

const router = useRouter()
const alertMessage = ref('');
const currentDate = ref('');
const currentTime = ref('');
const isUserPopupVisible = ref(false);
const isLoginPopupVisible = ref(false);
const isInstructionPopupVisible = ref(false);
const instruction = ref(null);
// const showInstructionPopup = ref(true);
const instructions = ref([]);
const editingInstructionId = ref(null);
const editingInstructionText = ref('');
const addingNewInstruction = ref(false);
const newInstructionText = ref('');

const showAlert = (message) => {
  alertMessage.value = message;
};

const closeAlert = () => {
  alertMessage.value = '';
};


const openUserLink = () => {
  window.open('https://app.tango.us/app/workflow/Managing-GerbIndia---IOT-Based-Machine-Monitoring-Dashboard----Powered-by---CMTI-445599c6dc614f309049a065bb2ab472', '_blank');
};

const  {props}  = defineProps(['enteredUsername']);
// console.log("enteredusersna 666666666666666666666")
// console.log({props})
const userInfo = {
 name: "Admin",
 email: "admin@example.com",
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

const showInstructionPopup = () => {
  isInstructionPopupVisible.value = true;
};

const hideInstructionPopup = () => {
  isInstructionPopupVisible.value = false;
  fetchInstructions();
};
// const hideUserPopup = () => {
//   try {
//     // Add the fetchData logic here
//     const storedToken = localStorage.getItem("authToken");
//     console.log(storedToken)

//     if (!storedToken) {
//       console.error("Token not found. User is not authenticated.");
//       alert("User Not Authenticated")
//       return;
//     }

//     this.$axios
//       .get("/login", {
//         headers: {
//           Authorization: `Bearer ${storedToken}`,
//         },
//       })
//       .then((response) => {
//         console.log("Fetched data:", response.data);

//         // Assuming you want to do something with the fetched data here

//         // Now proceed to logout
//         logout();
//       })
//       .catch((error) => {
//         console.error("Failed to fetch data:", error);

//         // If fetching data fails, still proceed to logout
//         logout();
//       });
//   } catch (error) {
//     console.error("An error occurred:", error);

//     // If an error occurs, still proceed to logout
//     logout();
//   }
// };

// Add the logout logic here
const logout = () => {
 // Clear the token from localStorage
 localStorage.removeItem("authToken");

 // Redirect to the login page
 // Assuming this.$router is available, you may need to adjust based on your setup
 isLoginPopupVisible.value = false;
//  console.log("logout");
 router.push("/log");
 hideUserPopup();


 // Optionally, you may want to perform additional cleanup or API calls on logout
};

onMounted(() => {
 setInterval(() => {
   const now = new Date();
   currentDate.value = now.toDateString();
   currentTime.value = now.toLocaleTimeString();
 }, 1000);
});
const fetchInstructions = () => {
  axios.get('http://192.168.0.105:6969/instruction/get_instructions/')
    .then(response => {
      instructions.value = response.data;
    })
    .catch(error => {
      console.error('Error fetching instructions:', error);
    });
};

// Inside the Navbar.vue component
onMounted(() => {
  fetchInstructions();
  // console.log("enteredUsername in Navbar:", props.enteredUsername);
});

// CRUD operations
const editInstruction = (instruction) => {
  editingInstructionId.value = instruction.id;
  editingInstructionText.value = instruction.instruction;
};

const cancelEdit = () => {
  editingInstructionId.value = null;
  editingInstructionText.value = '';
};

const updateInstruction = (instructionId) => {
  axios.put(`http://192.168.0.105:6969/instruction/put_instructions/instruction_id?instruction_id=${instructionId}`, {
    instruction: editingInstructionText.value
  })
    .then(response => {
      fetchInstructions(); // Refresh instructions after update
      // alert('Instruction updated successfully!');
      alertMessage.value = `Instruction updated successfully!`;
      cancelEdit();
    })
    .catch(error => {
      console.error('Error updating instruction:', error);
    });
};

const deleteInstruction = (instructionId) => {
  axios.delete(`http://192.168.0.105:6969/instruction/delete_instructions/instruction_id?instruction_id=${instructionId}`)
    .then(response => {
      fetchInstructions(); // Refresh instructions after deletion
      // alert('Instruction deleted successfully!');
      alertMessage.value = `Instruction deleted successfully!`;
    })
    .catch(error => {
      console.error('Error deleting instruction:', error);
    });
};

const showAddInstruction = () => {
  addingNewInstruction.value = true;
};

// const addInstruction = async () => {
//   const response = await fetch('http://192.168.0.105:6969/instruction/post_instructions/', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({ instruction: newInstructionText.value }),
//   });
//   const data = await response.json();
//   instructions.value.push(data);
//   addingNewInstruction.value = false;
//   newInstructionText.value = '';
// };


const addInstruction = () => {
  fetch('http://192.168.0.105:6969/instruction/post_instructions/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ instruction: newInstructionText.value }),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to add instruction');
    }
    return response.json();
  })
  .then(data => {
    instructions.value.push(data);
    addingNewInstruction.value = false;
    newInstructionText.value = '';
    alertMessage.value =  `Instruction added successfully!`;
    fetchInstructions(); // Fetch updated instructions after adding
  })
  .catch(error => {
    console.error('Error adding instruction:', error);
    // alert('Failed to add instruction. Please try again.');
  });
};


const cancelAdd = () => {
  addingNewInstruction.value = false;
  newInstructionText.value = '';
};
onMounted(() => {
  fetchInstructions();
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
 border-bottom: 2px solid white;
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
