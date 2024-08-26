<template>
  <!-- <Navbar/> -->
  <div class="flex  flex-row justify-around   ">
    <h3 class="font-poppins text-purple-500 text-xl font-bold mt-3 mr-24">WELDER PAGE</h3>
    <div class="flex space-x-4 p-4 ml-24 ">
      <span class="text-lg font-montserrat font-bold text-blue-500">Machines States </span> 
    <div v-for="machine in machine1" :key="machine.id" :class="{ 'bg-green-500': machine.machine_state, 'bg-yellow-500': !machine.machine_state }" class="w-8 h-8 flex items-center justify-center text-white rounded-md ">
      {{ machine.machine_id }}
    </div>
  </div>
  </div>
  
   <div class="card p-8 bg-blue-50 shadow-lg rounded-lg "> 
       <div class="overflow-auto" >
         <table class="w-full">
           <thead>
             <tr class="bg-blue-500 text-white ">
               <th class="px-2 py-2 font-poppins">Item No</th>
               <th class="px-2 py-2 font-poppins">Welding Machine</th>
               <th class="px-4 py-2 font-poppins">Operator</th>
               <th class="px-4 py-2 font-poppins">Element</th>
               <th class="px-4 py-2 font-poppins">Plate</th>
               <th class="px-4 py-2 font-poppins">STANDARD</th>
               <th class="px-4 py-2 font-poppins ">ACTUAL</th>
               <th class="px-4 py-2 font-poppins">Live</th>
               <th class="px-4 py-2 font-poppins">Project</th>
               <th class="px-4 py-2 font-poppins">Remarks</th>
             </tr>
           </thead> 
           <!-- flex space-y-2 flex-col items-center -->
           <tbody>
             <tr v-for="row in dataRows" :key="row.id" class="border-t hover:bg-white transition-colors">
               <td class="flex space-y-2 flex-col items-center font-poppins font-bold text-blue-700 ">{{ row.itemno }}
               </td> 
               <td class="px-2 py-1 sm:px-2 sm:py-2 font-poppins font-bold text-blue-700" >
                 <div class="flex flex-col items-center ">
                   <img :src="row.machineimg" alt="Machine Image" width="150" class="mb-2">
                   <span class="text-center">{{ row.machine }}</span>
                 </div>
                 <div class="ml-16 ">
                  <button @click="nopenPopup(row.itemno)">
                    <div class="glassmorphic-button bg-blue-500 px-2 py-1 rounded-md w-8 h-8 mb-2  "><img width="24" height="24" src="https://img.icons8.com/material-rounded/24/FFFFFF/appointment-reminders.png" alt="appointment-reminders" /></div>
                    
                  </button>
                </div>
               </td>
               <td>
                 <div class=" flex space-y-2 flex-col items-center  sm:px-4 sm:py-16 font-poppins">
                   <!-- <select v-model="row.operator" @change="onOperatorSelected($event)"
                     class="border border-gray-300 px-2 py-1 rounded-md mb-4">
                     <option disabled value="">Operator Type</option>
                     <option v-for="operator in operators" :key="operator.value" :value="operator.value">{{ operator.label }} </option>
                   </select> -->
                   <td> <div class="text-lg font-bold text-center"> {{ row.operator }}</div><br>
                    
                    <div><span class="font-bold">Start Time: </span><br>{{ row.startTime }}</div><br>
                    <div><span class="font-bold">End Time: </span><br>{{ row.endTime }}</div>
                  
                  
                  </td>
                 </div>
               </td>
               <td class="flex flex-col items-center sm:px-4 sm:py-16 font-poppins">
    <div class="flex flex-col items-center font-poppins pt-16">
      <div v-if="!row.isEditing" type="text" class="border border-gray-300 rounded-md ml-4 h-8 w-24">
        <p class="text-lg text-blue-800 text-center font-bold">{{ row.plate }}</p>
      </div>
      <div v-else>
        <input v-model="row.plate" class="border border-gray-300 px-4 py-2 rounded-md ml-4 h-8 w-24 text-center" placeholder="plate">
      </div>
      <div v-if="!row.isEditing" type="text" class="border border-gray-300 rounded-md ml-4 h-8 mt-4 w-24">
        <p class="text-lg text-blue-800 text-center font-bold">{{ row.platediscription }}</p>
      </div>
      <div v-else>
        <input v-model="row.platediscription" class="border border-gray-300 px-4 py-2 rounded-md ml-4 h-8 w-24 text-center" placeholder="current range">
      </div>
    </div>
  </td>
                  <!-- <div class="flex space-x-2 px-2 py-1 rounded-md mb-4">
                   <input v-model="row.standard.plate" type="text" class="border border-gray-300 px-2 py-1 rounded-md w-40"
                     placeholder="Plate Thickness">
                 </div> -->
                 <!-- Add some spacing here -->
                 <!-- <div class="mt-2">
                   <textarea v-model="row.plateremarks" class="border border-gray-300 px-2 py-1 rounded-md"
                     placeholder="Plate Description"></textarea>
                 </div> -->
               <td>
                 <div class=" flex  flex-col items-center font-poppins ">
                  <div  v-if="!row.isEditing" class="text-center"><td class="border border-gray-300  px-2 py-1 rounded-md mb-4 w-24">{{ row.element }}</td></div>
                  <div v-else>
                   <select v-model="row.element" @change="onOptionSelected($event)"
                     class="border border-gray-300  px-2 py-1 rounded-md mb-4">
                     <option disabled value="">Element Type</option>
                     <option v-for="element in elements" :key="element.value" :value="element.value">{{ element.label }}
                     </option>
                   </select>
                  </div>
                   <!-- <div class="text-center"><td class="bg-blue-100 border-1    w-36 font-bold rounded-lg shadow-lg  ">{{ row.element }}</td></div> -->
                   
                 <div class="mt-2 mb-2"> 
                   <textarea v-model="row.element_description" class="border border-gray-300 px-1 py-1 rounded-md"
                     placeholder="Element Description"></textarea>
                 </div>
                 <div  v-if="!row.isEditing" type="text" class="border border-gray-300 rounded-md w-26 px-2 py-2 sm:px-4 sm:py-2 mb-2 w-40 text-center"><b> {{ row.range }}</b></div>
                 <div v-else><input v-model="row.range" class="border border-gray-300 px-4 py-2 rounded-md w-40 text-center" placeholder="range"></div>
               </div>
               <!-- <div class="flex space-x-2 mt-2 ml-24">
                   <button @click="toggleEdit(row)" v-if="!row.isEditing" class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md w-8 h-8 mb-2 flex flex-wrap"><img width="21" height="21" src="https://img.icons8.com/fluency-systems-filled/48/FFFFFF/edit.png" alt="edit" class="flex flex-warp mr-3 mt-1"/></button>
                   <button @click="saveEditedData(row)" v-else class="glassmorphic-button bg-green-500 text-white px-2 py-1 rounded-md w-10 h-8 mb-2 flex flex-wrap" ><img width="24" height="24" src="https://img.icons8.com/material-outlined/24/FFFFFF/save.png" alt="save" class="flex flex-warp"/></button>
                 </div> -->
               </td>
               <!-- <td>
                 <div
                   class="neumorphic w-60 px-4 mt-2 shadow-lg hover:shadow-xl transition-shadow rounded-lg bg-blue-100 h-36 ml-3">
                   <div class="flex mt-2 justify-center">
                     <div class="mt-14"><img width="50" height="50"
                         src="https://img.icons8.com/ios-glyphs/30/000000/lightning-bolt--v1.png" alt="lightning-bolt--v1"
                         class="h-6 w-7" /></div>
                     <div class="w-28 h-16 mt-9 rounded-lg bg-blue-300 mr-6 shadow-lg hover:shadow-xl transition-shadow">
                       <p class="text-sm text-white text-center font-bold">Current</p>
                       <p class="text-lg text-white text-center font-bold"> {{ getMachineCurrent(row.id) }} A</p>
                     </div>
   
                     <div class="mt-14 mr-1"><img width="50" height="50"
                         src="https://img.icons8.com/material-rounded/24/000000/speedometer.png" alt="speedometer"
                         class="h-6 w-7" /></div>
                     <div class="w-28 h-16 mt-9 rounded-lg bg-green-300 shadow-lg hover:shadow-xl transition-shadow">
                       <p class="text-sm text-white text-center font-bold">Voltage</p>
                       <p class="text-lg text-white text-center font-bold"> {{ getMachineVoltage(row.id) }} V</p>
                     </div>
                   </div>
                 </div>
               </td> -->
               <td>
                 <div class="flex space-y-2 flex-col items-center mb-3 mt-3 font-poppins">
                   <div class="border border-gray-300 px-4 py-6 rounded-md h-25 w-36">
                     <p class="text-lg text-black text-center font-bold -mb-2 ">Current</p>
                     <p class="text-sm text-black text-center font-bold mb-2 ">Range</p>
                     <div class="absolute  mr-4"><img width="24" height="24" src="https://img.icons8.com/material-rounded/24/lightning-bolt--v1.png" alt="lightning-bolt--v1 " class="-ml-1 mt-1"/></div>
                     <div v-if="!row.isEditing" type="text"  class="border border-gray-300 rounded-md ml-4 h-8 w-24">
                       <p class="text-lg text-blue-800 text-center font-bold "> {{ row.standard.standard_current }}A</p></div>
                     <div v-else><input v-model=" row.standard.standard_current" class="border border-gray-300 px-4 py-2 rounded-md ml-4 h-8 w-24 text-center" placeholder="current range"></div>
                   </div>
                   <div class="border border-gray-300 px-4 py-6 rounded-md h-25 w-36 ">
                     <p class="text-lg text-black text-center font-bold -mb-2 ">Voltage</p>
                     <p class="text-sm text-black text-center font-bold mb-2 ">Range</p>
                     <div class="absolute  mr-4"><img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/speedometer.png" alt="speedometer" class="-ml-1 mt-1"/></div>
                     <div v-if="!row.isEditing" type="text" class="border border-gray-300 rounded-md ml-4 h-8 w-24">
                       <p class="text-lg text-blue-800 text-center font-bold "> {{ row.standard.standard_voltage }}V</p></div>
                       <div v-else><input v-model="row.standard.standard_voltage" class="border border-gray-300 px-4 py-2 rounded-md ml-4 h-8 w-24 text-center" placeholder="voltage range"></div>
                     </div>
                 </div>
               </td>
               <td>
                <div class="mb-3 mt-3 font-poppins">
    <div class="flex space-y-2 flex-col items-center" v-if="dataLoaded">
      <div class="border border-gray-300 px-4 py-6 rounded-md h-25 w-36">
        <p class="text-lg text-black text-center font-bold -mb-2">Current</p>
        <p class="text-sm text-black text-center font-bold mb-2">Range</p>
        <div class="absolute mr-4">
          <img width="24" height="24" src="https://img.icons8.com/material-rounded/24/lightning-bolt--v1.png" alt="lightning-bolt--v1" class="-ml-1 mt-1" />
        </div>
        <div class="border border-gray-300 rounded-md ml-4 h-8 w-24">
          <p class="text-lg text-center font-bold text-lime-500">{{ getMachineLiveCurrent(row.id) }}A</p>
        </div>
      </div>
      <div class="border border-gray-300 px-4 py-6 rounded-md h-25 w-36">
        <p class="text-lg text-black text-center font-bold -mb-2">Voltage</p>
        <p class="text-sm text-black text-center font-bold mb-2">Range</p>
        <div class="absolute mr-4">
          <img width="24" height="24" src="https://img.icons8.com/ios-glyphs/30/speedometer.png" alt="speedometer" class="-ml-1 mt-1" />
        </div>
        <div class="border border-gray-300 rounded-md ml-4 h-8 w-24">
          <p class="text-lg text-lime-500 text-center font-bold">{{ getMachineLiveVoltage(row.id) }}V</p>
        </div>
      </div>
    </div>
    <div v-else>
      Loading data...
    </div>
  </div>
               </td>
               <td>
                 <div class="flex space-y-2 flex-col items-center font-poppins">
                   <button @click="showUserPopup(row.itemno)" class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md mr-4 w-16">
                     <img
                       src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWUlEQVR4nO2US0oDQRCGs5IIiaAkbjyAeolo5gjxAGrwsY6LoAg+F46HURfJzngBxcfSB7jSZGlMDvCHxm+gaXqGPARdpFbzVVX/NVM9VanU2P6VSZqTVBnhfMVoxAUnJd3px8pDiK9z1mikfQn7JLxLyg1RYEbSKxq7bnBaUpvgEr4VSYd9CB9IKvFcROPLaPo+7xqelfSNr5AgXiDH5ObxNfCt2YlXODfgU7gGT0g6l9SU9CkpND5iNXKP4S340i7wgnMefoKLsBF0LSQWwA/wAvxsF+jizMRw01OgRSwLd+AM3E0q0IGzsGmLax/EpqJ78HFcix7hIKFFZ06L7uFFX4uiS96ET+C6dckhX+Jecp3cI3gbvvD9pg04P+Bv2o6GU9INvtW4QVvGV4reKsnMMFqDFngHjeDeL6yKNzSqvoT0iMuuzNlb77Kz1vXOoOJ9reux/Zn1AHTH1NfLscaMAAAAAElFTkSuQmCC "
                       class="ml-3">
                     Live
                   </button><br>
                   <!-- <button @click="showUserLiveCurrentPopup(row.itemno)" class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md mr-4 w-16">
                     <img
                       src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWUlEQVR4nO2US0oDQRCGs5IIiaAkbjyAeolo5gjxAGrwsY6LoAg+F46HURfJzngBxcfSB7jSZGlMDvCHxm+gaXqGPARdpFbzVVX/NVM9VanU2P6VSZqTVBnhfMVoxAUnJd3px8pDiK9z1mikfQn7JLxLyg1RYEbSKxq7bnBaUpvgEr4VSYd9CB9IKvFcROPLaPo+7xqelfSNr5AgXiDH5ObxNfCt2YlXODfgU7gGT0g6l9SU9CkpND5iNXKP4S340i7wgnMefoKLsBF0LSQWwA/wAvxsF+jizMRw01OgRSwLd+AM3E0q0IGzsGmLax/EpqJ78HFcix7hIKFFZ06L7uFFX4uiS96ET+C6dckhX+Jecp3cI3gbvvD9pg04P+Bv2o6GU9INvtW4QVvGV4reKsnMMFqDFngHjeDeL6yKNzSqvoT0iMuuzNlb77Kz1vXOoOJ9reux/Zn1AHTH1NfLscaMAAAAAElFTkSuQmCC"
                       class="ml-3">
                     Live Current
                   </button><br> -->
                   <button @click="showStackPopup()"
                     class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md  mr-4 w-16">
                     <img
                       src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWUlEQVR4nO2US0oDQRCGs5IIiaAkbjyAeolo5gjxAGrwsY6LoAg+F46HURfJzngBxcfSB7jSZGlMDvCHxm+gaXqGPARdpFbzVVX/NVM9VanU2P6VSZqTVBnhfMVoxAUnJd3px8pDiK9z1mikfQn7JLxLyg1RYEbSKxq7bnBaUpvgEr4VSYd9CB9IKvFcROPLaPo+7xqelfSNr5AgXiDH5ObxNfCt2YlXODfgU7gGT0g6l9SU9CkpND5iNXKP4S340i7wgnMefoKLsBF0LSQWwA/wAvxsF+jizMRw01OgRSwLd+AM3E0q0IGzsGmLax/EpqJ78HFcix7hIKFFZ06L7uFFX4uiS96ET+C6dckhX+Jecp3cI3gbvvD9pg04P+Bv2o6GU9INvtW4QVvGV4reKsnMMFqDFngHjeDeL6yKNzSqvoT0iMuuzNlb77Kz1vXOoOJ9reux/Zn1AHTH1NfLscaMAAAAAElFTkSuQmCC "
                       class="ml-3">
                     All Stats
                   </button><br>
                   <button @click="showProductionPopup(row.itemno)"
                     class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md  mr-4 w-24">
                     <img
                       src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWUlEQVR4nO2US0oDQRCGs5IIiaAkbjyAeolo5gjxAGrwsY6LoAg+F46HURfJzngBxcfSB7jSZGlMDvCHxm+gaXqGPARdpFbzVVX/NVM9VanU2P6VSZqTVBnhfMVoxAUnJd3px8pDiK9z1mikfQn7JLxLyg1RYEbSKxq7bnBaUpvgEr4VSYd9CB9IKvFcROPLaPo+7xqelfSNr5AgXiDH5ObxNfCt2YlXODfgU7gGT0g6l9SU9CkpND5iNXKP4S340i7wgnMefoKLsBF0LSQWwA/wAvxsF+jizMRw01OgRSwLd+AM3E0q0IGzsGmLax/EpqJ78HFcix7hIKFFZ06L7uFFX4uiS96ET+C6dckhX+Jecp3cI3gbvvD9pg04P+Bv2o6GU9INvtW4QVvGV4reKsnMMFqDFngHjeDeL6yKNzSqvoT0iMuuzNlb77Kz1vXOoOJ9reux/Zn1AHTH1NfLscaMAAAAAElFTkSuQmCC "
                       class="ml-6">
                     Production
                   </button>
                   <!-- <button @click="showUserPopupGraph()" class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md  mr-4 w-16">
                     <img
                       src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWUlEQVR4nO2US0oDQRCGs5IIiaAkbjyAeolo5gjxAGrwsY6LoAg+F46HURfJzngBxcfSB7jSZGlMDvCHxm+gaXqGPARdpFbzVVX/NVM9VanU2P6VSZqTVBnhfMVoxAUnJd3px8pDiK9z1mikfQn7JLxLyg1RYEbSKxq7bnBaUpvgEr4VSYd9CB9IKvFcROPLaPo+7xqelfSNr5AgXiDH5ObxNfCt2YlXODfgU7gGT0g6l9SU9CkpND5iNXKP4S340i7wgnMefoKLsBF0LSQWwA/wAvxsF+jizMRw01OgRSwLd+AM3E0q0IGzsGmLax/EpqJ78HFcix7hIKFFZ06L7uFFX4uiS96ET+C6dckhX+Jecp3cI3gbvvD9pg04P+Bv2o6GU9INvtW4QVvGV4reKsnMMFqDFngHjeDeL6yKNzSqvoT0iMuuzNlb77Kz1vXOoOJ9reux/Zn1AHTH1NfLscaMAAAAAElFTkSuQmCC "
                       class="ml-3">
                       Graph</button> -->
                       <!-- <button @click="showUserPopupGraph()" class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md  mr-4 w-16"> -->
                         <!-- <img width="25" height="25" src="https://img.icons8.com/ios-filled/50/FFFFFF/appointment-reminders--v1.png" alt="appointment-reminders--v1" class="ml-3"/> -->
                         <!-- <img width="24" height="24" src="https://img.icons8.com/material-sharp/24/FFFFFF/alarm--v1.png" alt="alarm--v1" class="ml-3"/> -->
                       <!-- </button> -->
                       
                       <!-- <button @click="showNotificationPopup()" class=" bg-blue-500 text-white px-2 py-1 rounded-md mr-4 w-16">
                         <span width="24" height="24" v-if="notificationCount > 0" class="notification-counter">{{ notificationCount }}</span>
                         <img width="24" height="24" src="https://img.icons8.com/material-sharp/24/FFFFFF/alarm--v1.png" alt="alarm--v1" class="ml-3"/>
                       </button> -->
                       <!-- <Notification/>  
                       <button @click="openPopup(row)">Notification</button> -->
                 </div>
               </td>
               <td>
                 <!-- <div class=" flex space-y-2 flex-col items-center  sm:px-4 sm:py-16 font-poppins">
                   <div class="flex space-x-2"><input v-model="row.I_no" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center" placeholder="I_No"></div>
                   <div class="flex space-x-2 mt-2"><input v-model="row.Fc_no" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center" placeholder="Fc_No"></div>
                   <div class="flex space-x-2 mt-2"><input v-model="row.project" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center" placeholder="Project"></div>
                 </div> -->
                 <!-- <div class=" flex space-y-2 flex-col items-center  sm:px-4 sm:py-16 font-poppins">
                   
                   <div class="flex space-x-2">
                     <div v-if="!row.isEditing" type="text" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center"> {{ getoperatorIno(row.id) }}</div> -->
                     <!-- <div v-else><input v-model="row.I_no" class="border border-gray-300 px-4 py-2 rounded-md w-20  text-center"><div class="absolute -mt-9 ml-6 font-semibold text-xl ">{{ getoperatorIno(row.id) }}</div></div> -->
                     <!-- <div v-else><input v-model="row.I_no" class="border border-gray-300 px-4 py-2 rounded-md w-24  text-center" placeholder="I_No"></div>
                   </div> -->
                   
                   <!-- <div class="flex space-x-2 mt-2">
                     <div v-if="!row.isEditing" type="text" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center"> {{ getoperatorFcno(row.id) }}</div>
                     <div v-else><input v-model="row.Fc_no" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center" placeholder="Fc_No"></div>
                   </div>
                   <div class="flex space-x-2 mt-2">
                     <div v-if="!row.isEditing" type="text" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center"> {{ getoperatorProject(row.id) }}</div>
                     <div v-else><input v-model="row.project" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center" placeholder="Project"></div>
                   </div>
                   <div class="flex space-x-2 mt-2">
                   <button @click="toggleEdit(row)" v-if="!row.isEditing" class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md w-8 h-8 mb-2 flex flex-wrap"><img width="21" height="21" src="https://img.icons8.com/fluency-systems-filled/48/FFFFFF/edit.png" alt="edit" class="flex flex-warp mr-3 mt-1"/></button>
                   <button @click="saveEditedData(row)" v-else class="glassmorphic-button bg-green-500 text-white px-2 py-1 rounded-md w-10 h-8 mb-2 flex flex-wrap" ><img width="30" height="30" src="https://img.icons8.com/material-outlined/24/FFFFFF/save.png" alt="save" class="flex flex-warp"/></button> -->
                 <!-- </div> -->
 
                 <!-- <div class="mb-4">
                  <label class="block text-gray-700 text-sm font-bold mb-2" placeholder="select shift">Select Shift:</label><select v-model="row.selectedShift" class="block w-full bg-gray-100 border rounded p-2" >
                    <option disabled value="">Select Shift</option>
                    <option v-for="shift in shifts" :key="shift.id" :value="shift.id">{{ shift.name }}</option>
                     </select>
                 </div> -->
                 <!-- </div> -->

                 <div class=" flex space-y-2 flex-col items-center  sm:px-4 sm:py-16 font-poppins">
                   <!-- <div class=" space-x-2 border border-gray-300 px-4 py-6 rounded-md h-25 w-36">
                    <p class="text-lg text-black text-center font-bold -mb-2 ">I No</p>
                    <div  v-if="!row.isEditing" type="text" class="border border-gray-300 rounded-md w-26 px-2 py-2 sm:px-4 sm:py-2 mb-2 w-36 text-center"><b> {{ row.I_no }}</b></div>
                 <div v-else><input v-model="row.I_no" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center" placeholder="I_no"></div>
                 </div> -->

                 <div class="border border-gray-300 px-4 py-6 rounded-md h-20 w-36">
                     <p class="text-lg text-black text-center font-bold -mt-4 ">I No</p>
                     <div class="absolute  mr-4"></div>
                     <div v-if="!row.isEditing" type="text"  class="border border-gray-300 rounded-md ml-3 h-8 w-24 mb-6">
                       <p class="text-lg text-blue-800 text-center font-bold "> {{ row.I_no }}</p></div>
                     <div v-else><input v-model=" row.I_no" class="border border-gray-300 px-4 py-2 rounded-md ml-4 h-8 w-24 text-center" placeholder="I No"></div>
                   </div>

                   <div class="border border-gray-300 px-4 py-6 rounded-md h-20 w-36">
                     <p class="text-lg text-black text-center font-bold -mt-4 ">Fc No</p>
                     <div class="absolute  mr-4"></div>
                     <div v-if="!row.isEditing" type="text"  class="border border-gray-300 rounded-md ml-3 h-8 w-24 mb-6">
                       <p class="text-lg text-blue-800 text-center font-bold "> {{row.Fc_no}}</p></div>
                     <div v-else><input v-model="row.Fc_no" class="border border-gray-300 px-4 py-2 rounded-md ml-4 h-8 w-24 text-center" placeholder="Fc No"></div>
                   </div>

                   <div class="border border-gray-300 px-4 py-6 rounded-md h-20 w-36">
                     <p class="text-lg text-black text-center font-bold -mt-4 ">Project</p>
                     <div class="absolute  mr-4"></div>
                     <div v-if="!row.isEditing" type="text"  class="border border-gray-300 rounded-md  h-8 w-28 mb-6" placeholder="Project">
                       <p class="text-lg text-blue-800 text-center font-bold "> {{row.project}}</p></div>
                     <div v-else><input v-model="row.project" class="border border-gray-300 px-4 py-2 rounded-md h-8 w-28 text-center" placeholder="Project"></div>
                   </div>


                 <!-- <div class=" flex space-y-2 flex-col items-center  sm:px-4 sm:py-16 font-poppins">
                   <div class="flex space-x-2">
                  
                     <input v-model="row.I_no" class="border border-gray-300 px-4 py-2 rounded-md w-24  text-center" placeholder="I_No" >
                   </div>
                   <div class="flex space-x-2 mt-2"><input v-model="row.Fc_no" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center" placeholder="Fc_No">
                   </div>
                   <div class="flex space-x-2 mt-2"><input v-model="row.project" class="border border-gray-300 px-4 py-2 rounded-md w-24 text-center" placeholder="Project">
                   </div> -->
                   <!-- <div class="flex space-x-2 mt-2">
                   <button @click="toggleEdit(row)" v-if="!row.isEditing" class="glassmorphic-button bg-blue-500 text-white px-2 py-1 rounded-md w-8 h-8 mb-2 flex flex-wrap"><img width="21" height="21" src="https://img.icons8.com/fluency-systems-filled/48/FFFFFF/edit.png" alt="edit" class="flex flex-warp mr-3 mt-1"/></button>
                   <button @click="saveEditedData(row)" v-else class="glassmorphic-button bg-green-500 text-white px-2 py-1 rounded-md w-10 h-8 mb-2 flex flex-wrap" ><img width="30" height="30" src="https://img.icons8.com/material-outlined/24/FFFFFF/save.png" alt="save" class="flex flex-warp"/></button>
                 </div> -->
                 <!-- <div class="mb-4">
           <label class="block text-gray-700 text-sm font-bold mb-2" placeholder="select shift">Select Shift:</label>
           <select v-model="row.selectedShift" class="block w-full bg-gray-100 border rounded p-2" >
             <option disabled value="">Select Shift</option>
             <option v-for="shift in shifts" :key="shift.id" :value="shift.id">{{ shift.name }}</option>
           </select>
         </div> -->
                 </div>
               </td>
               <td class="font-poppins">
                 <div class="flex flex-col items-center">
                 <textarea v-model="row.remarks" class="border border-gray-300 px-2 py-1 rounded-md mb-2"
                   placeholder="Type here"></textarea>
                 <div class="flex space-x-2 mt-2">
                   <div class="flex flex-col items-center ">
                   <!-- <button @click="showloginPopup()"
                     class="glassmorphic-button bg-green-500 text-white px-2 py-1 rounded-md w-24 h-8 mb-2"><i class="fa-regular fa-floppy-disk"></i> Save</button> -->
                     <button @click="toggleEdit(row)" v-if="!row.isEditing" class="glassmorphic-button bg-yellow-500 text-white px-2 py-1 rounded-md w-24 h-8 mb-2 flex flex-wrap"><img width="18" height="18" src="https://img.icons8.com/fluency-systems-filled/48/FFFFFF/edit.png" alt="edit" class="flex flex-warp mr-3 mt-1"/> Edit</button>
                     <button @click="saveEditedData(row)" v-else class="glassmorphic-button bg-green-500 text-white px-2 py-1 rounded-md w-24 h-8 mb-2 flex flex-wrap" ><img width="24" height="24" src="https://img.icons8.com/material-outlined/24/FFFFFF/save.png" alt="save" class="flex flex-warp"/>Save</button>
                     
                   <button @click="generateReport(row.itemno)"
                     class="glassmorphic-button bg-purple-500 text-white px-2 py-1 rounded-md w-24 h-8 mb-2 flex flex-wrap ">
                     <img width="24" height="24" src="https://img.icons8.com/sf-black/64/FFFFFF/download.png" alt="download" class="flex flex-wrap"/>Report</button>
                     <!-- <button @click="generateReport()"
                     class="glassmorphic-button bg-green-500 text-white px-2 py-1 rounded-md w-28 h-8"><i class="fa-solid fa-chart-simple"></i>
                     Analytics</button> -->
                     
                 </div>
                 <button
       @click="scrollToTop"
       class="fixed bottom-14 right-4 bg-blue-500 text-white p-2 rounded-full shadow-md hover:bg-yellow-600 focus:outline-none"
     ><img width="24" height="24" src="https://img.icons8.com/glyph-neue/64/FFFFFF/up-squared.png" alt="up-squared" placeholder="Top"/>
       <!-- Scroll to Top -->
     </button>
               </div>
               </div>
               </td>
             </tr>
           
             <!-- //PopUp Chart -->
             <div v-if="isUserPopupVisible" class="fixed inset-0 flex items-center justify-center z-50">
               <div class="bg-white p-8 rounded-lg shadow-lg w-1/2 h-1/2 relative">
                 <!-- <Line  :dataFromParent="graphData"/> -->
                 <Line class="h-full w-full" :dataFromParent="graphData"/>
                 <!-- <Report/> -->
                 <button @click="hideUserPopup" class=" bg-white px-1 py-0 rounded-lg absolute top-2 right-0 -mt-1 mr-3">
                   <img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/>
                 </button>
               </div>
             </div>
             <div v-if="isUserLiveCurrentPopupVisible" class="fixed inset-0 flex items-center justify-center z-50">
               <div class="bg-white p-8 rounded-lg shadow-lg w-1/2 h-1/2 relative">
                <LineGraph :dataFromParent="graphData"/>
                <!-- <LiveCurrent/> -->
                 <!-- <Report/> -->
                 <button @click="hideUserLiveCurrentPopup" class=" bg-white px-1 py-0 rounded-lg absolute top-2 right-0 -mt-1 mr-3">
                   <img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/>
                 </button>
               </div>
             </div>
             <div v-if="isUserPopupVisibleGraph" class="fixed inset-0 flex items-center justify-center z-50">
                 <div class="bg-white p-8 rounded-lg shadow-lg w-1/2 h-1/2 relative">
                   <LineGraph />
                   <button @click="hideUserPopupGraph" class=" bg-white px-1 py-0 rounded-lg absolute top-2 right-0 -mt-1 mr-3"><img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/></button>
                 </div>
               </div>
             <div v-if="isStackVisible" class="fixed inset-0 flex items-center justify-center z-50">
               <div class="bg-white p-8 rounded-lg shadow-lg w-1/2 h-1/2 relative">
                <div class="m-2 ">
      <Stack class="h-96" :chartData="stateChartData" />
    </div>
                 <!-- <Report/> -->
                 <button @click="hideStackPopup" class=" bg-white px-1 py-0 rounded-lg absolute top-2 right-0 -mt-1 mr-3"><img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/>
                 </button>
               </div>
             </div>
             <div v-if="isProductionVisible" class="fixed inset-0 flex items-center justify-center z-50">
               <div class="bg-white p-8 rounded-lg shadow-lg w-1/2 h-1/2 relative">
                <div class="m-2 ">
      <Production :dataFromParentProduction="ParentProductionData" class="h-96"  />
    </div>
                 <!-- <Report/> -->
                 <button @click="hideProductionPopup" class=" bg-white px-1 py-0 rounded-lg absolute top-2 right-0 -mt-1 mr-3"><img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/>
                 </button>
               </div>
             </div>
             <div v-if="isNotificationVisible" class="fixed inset-0 flex items-center justify-center z-50">
               <div class="bg-white p-8 rounded-lg shadow-lg w-1/2 h-1/2 relative">
                 <Notification />
                 <!-- <Report/> -->
                 <button @click="hideNotificationPopup" class=" bg-white px-1 py-0 rounded-lg absolute top-2 right-0 -mt-1 mr-3"><img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/>
                 </button>
               </div>
             </div>
             <div v-if="isloginVisible" class="fixed inset-0 flex items-center justify-center z-50">
               <div class="bg-white p-8 rounded-lg shadow-lg w-1/2 h-1/2 relative">
   
                 <!-- <Report/> -->
                 <button @click="hideloginPopup" class=" bg-white px-1 py-0 rounded-lg absolute top-0 right-0 -mt-1 mr-4">
                   <img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/>
                 </button>
               </div>
             </div>
             <!-- //PopUp Chart -->
             <div v-if="isReport" class="fixed inset-0 flex items-center justify-center z-50">
               <div class="bg-white p-8 rounded-lg shadow-lg w-1\/2 h-1\/2 relative">
                 <Report :machine_id="selectedMachine"/>
                 <!-- <Report/> -->
                 <button @click="hideReportPopup" class=" bg-white px-1 py-0 rounded-lg absolute top-2 right-0 -mt-1 mr-1">
                   <img width="20" height="20" src="https://img.icons8.com/ios-glyphs/30/delete-sign.png" alt="delete-sign"/>
                   </button>
               </div>
             </div>
             
           </tbody>
         </table>
         <div>
    <div v-if="nisPopupOpen" class="npopup">
      <div class="npopup-content">
        <h1 class="font-montserrat font-bold">Machine ID: <p class="text-blue-600">{{ npopupData.machineId }}</p></h1>
        <h1 class="font-montserrat font-bold">Current : <p class="text-red-600">{{ npopupData.current }}</p> </h1>
        <h1 class="font-montserrat font-bold">Voltage : <p class="text-red-600">{{ npopupData.voltage }}</p> </h1>
        <h1 class="font-montserrat font-bold">Created at : <p class="text-blue-600"> {{ npopupData.createdat }}</p></h1>
        <h1 class="font-montserrat font-bold mt-2">Download Logs</h1>

        <div class="flex flex-col"><label class="font-montserrat font-bold">Start Date:</label>
        <flat-pickr v-model="startDate" :config="datePickerConfig" />

        <label class="font-montserrat font-bold">End Date:</label>
        <flat-pickr v-model="endDate" :config="datePickerConfig" />

        

       
      </div>
       <!-- Submit button -->
       <div class="flex flex-col items-center">
        <button @click="handleSubmit(npopupData.machineId)" class="bg-green-500 text-white rounded-md mt-2 mb-4 w-16">Submit</button>
      
<button @click="nclosePopup" class="bg-red-500 text-white rounded-md w-16 ml-1">Close</button>
       </div>
       </div>

<!-- Date selection using vue-flatpickr-component -->

    </div>
  </div>
       </div>
       <Line v-for="machine in machines" :key="machine.id" :machineData="machine" />
     </div>
   </template>
   
   <script setup>
   import Line from '@/components/Line.vue'
     import {computed, watch } from 'vue';
     import LineGraph from '@/components/LineGraph.vue'
     import Stack from '@/components/Stack.vue'
     import Production from '@/components/Production.vue'
     import Report from '@/components/Report.vue'
     import Notification from '@/components/Notification.vue'
     import { ref, onMounted,toRef} from 'vue'
     import axios from 'axios';
     import * as XLSX from 'xlsx';
    //  import Navbar from '@/components/Navbar.vue'
   
     const isReport = ref(false);
     const isUserPopupVisible = ref(false);
     const isUserLiveCurrentPopupVisible = ref(false);
     const isUserPopupVisibleGraph=ref(false);
     const isStackVisible = ref(false);
     const isProductionVisible = ref(false);
     const isNotificationVisible=ref(false);
     const isloginVisible = ref(false);
     const currentDate = ref('');
   const currentTime = ref('');
   const selectedShift = ref(null);
const stateChartData= ref([]);


import FlatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';

// Data
const startDate = ref(null);
const endDate = ref(null);
const datePickerConfig = {
  dateFormat: 'Y-m-d',
};

const handleSubmit = async (machineId) => {
  try {
    // Fetch data from the specified URL
    const url = `http://192.168.0.105:6969/all_logs/${machineId}/${startDate.value}/${endDate.value}`;
    const response = await axios.get(url);

    // Check if the response has a "detail" property and it's an array
    if (response.data && Array.isArray(response.data.detail)) {
      const logs = response.data.detail;

      // Convert logs to Excel
      const worksheet = XLSX.utils.json_to_sheet(logs);
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Logs');

      // Download the Excel file
      XLSX.writeFile(workbook, `Logs ${startDate.value}.xlsx`);
    } else {
      throw new Error('Invalid response format. Expected an array.');
    }
  } catch (error) {
    console.error('Error fetching or processing data:', error.message);
  }
};

// Helper function to format date as 'YYYY-MM-DD'

//notification new updated one
const fetchStateData = async () => {
  try {
    const response = await axios.get('http://192.168.0.105:6969/graph/get_graph_data');
    const responseData = response.data;
    //'http://192.168.0.105:6565/machines'
    //192.168.0.105:6969/graph/get_graph_data

    // Process the response data as needed
    stateChartData.value = responseData;
    // console.log("Fetched state data from the backend");
    // console.log(stateChartData.value);
  } catch (error) {
    console.error('Error fetching state data:', error);
  }
};
onMounted(() => {
fetchStateData();

// Fetch data every 2 seconds
// setInterval(fetchStateData, 000);
});


// const productChartData = ref([]);
// const fetchProductData = async () => {
//   try {
//     const response = await axios.get('http://192.168.0.105:6969/graph/get_graph_data');
//     const responseData = response.data;
//     //'http://192.168.0.105:6565/machines'
//     //192.168.0.105:6969/graph/get_graph_data

//     // Process the response data as needed
//     productChartData.value = responseData;
//     // console.log("Fetched state data from the backend");
//     // console.log(stateChartData.value);
//   } catch (error) {
//     console.error('Error fetching state data:', error);
//   }
// };
// onMounted(() => {
//   fetchProductData();

// // Fetch data every 2 seconds
// // setInterval(fetchStateData, 000);
// });

const nisPopupOpen = ref(false);
const npopupData = ref({
  machineId: '',
  current : '',
  voltage : '',
  createdat : ''
});

// const nopenPopup  = async(machineId) => {
//   nisPopupOpen.value = true;
//   npopupData.value.machineId = machineId;
//   console.log(npopupData.value.machineId)
//   try {
//     console.log(npopupData.value.machineId);
//     const popresponse = await axios.get(`http://192.168.0.105:6969/logs/${npopupData.value.machineId}`);
//     console.log("api called")
//     npopupData.value.current = popresponse.data.detail.current;
//     npopupData.value.voltage = popresponse.data.detail.voltage;
//     npopupData.value.createdat = popresponse.data.detail.createdat;
     
//   } catch (error) {
//     console.error('Error fetching data:', error);
//   }
  
  
// };

async function nopenPopup(machineId){
  nisPopupOpen.value = true;
  npopupData.value.machineId = machineId;
  // console.log(npopupData.value.machineId)
  try {
    // console.log(npopupData.value.machineId);
    const popresponse = await axios.get(`http://192.168.0.105:6969/logs/${npopupData.value.machineId}`);
    console.log(popresponse)
    // console.log("api called")
    npopupData.value.current = popresponse.data.detail.current;
    npopupData.value.voltage = popresponse.data.detail.voltage;
    npopupData.value.createdat = popresponse.data.detail.created_at;
     
  } catch (error) {
    console.error('Error fetching data:', error);
  }
  
  

}

// onMounted(async () => {
//   try {
//     const popresponse = await axios.get(`http://192.168.0.105:6969/logs/${npopupData.value.machineId}`);
//     console.log("api called")
//     data.value = popresponse.data;
//     npopupData.value.machineId = data.value
//   } catch (error) {
//     console.error('Error fetching data:', error);
//   }
// });

const nclosePopup = () => {
  nisPopupOpen.value = false;
};



 
 // Initialize the notification counter
 const notificationCount = ref(0);
 
 // Control the popup window
 const isPopupOpen = ref(false);
 
 // Random notification messages
 const messages = [
   "Hello, world!",
   "This is a random notification message.",
   "Vue.js is awesome!",
   "You've got a new message!",
   "Don't forget to stay hydrated.",
 ];
 // Generate a random message
 const randomMessage = ref('');
 
 const generateRandomMessage = () => {
   const randomIndex = Math.floor(Math.random() * messages.length);
   randomMessage.value = messages[randomIndex];
 };
 
 // Function to open the popup
 const openPopup = () => {
   generateRandomMessage();
   isPopupOpen.value = true;
 };
 
 // Function to close the popup
 const closePopup = () => {
   isPopupOpen.value = false;
 };
 // Increment the counter automatically every 2 seconds
 onMounted(() => {
   setInterval(() => {
     notificationCount.value++;
   }, 2000);
 });
 
   const userInfo = {
     name: "Admin",
     email: "admin@example.com",
     position: "Supervisor",
   };
   
   const shifts = [
     { id: 1, name: 'SHIFT-1' },
     { id: 2, name: 'SHIFT-2' },
     { id: 3, name: 'SHIFT-3' },
     { id: 4, name: 'All-SHIFTS' }
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
   
   onMounted(() => {
     setInterval(() => {
       const now = new Date();
       currentDate.value = now.toDateString();
       currentTime.value = now.toLocaleTimeString();
     }, 1000);
   });
   const dataRows = ref([
    //  {
    //    id: 1,
    //    itemno: '7D',
    //    machine: "AK-400-2-7D",
    //    machine_name: '7D',
    //    operator: "",
    //    element: "",
    //    element_description: "",
    //    plate: "",
    //    standard: { standard_current: "", standard_voltage: "" },
    //    actual: { current: "", voltage: "" },
    //    remarks: "",
    //    machineimg: "./src/assets/ak400.png",
    //  },
     // {
     //   id: 2,
     //   itemno: '7F',
     //   machine: "AK-400-7F",
     //   machine_name: '7F',
     //   operator: "",
     //   element: "",
     //   element_description: "",
     //   plate: "",
     //   standard: { standard_current: "", standard_voltage: "" },
     //   actual: { current: "", voltage: "" },
     //   remarks: "",
     //   machineimg: "./src/assets/ak400.png",
     // },
     {
       id: 3,
       itemno: '7G',
       machine: "AK-600-7G",
       machine_name: '7G',
       operator: "",
       element: "",
       element_description: "",
       plate: "",
       standard: { standard_current: "", standard_voltage: "" },
       actual: { current: "", voltage: "" },
       remarks: "",
       machineimg: "./src/assets/ak600.png",
     },
     {
       id: 4,
       itemno: '7H',
       machine: "AK-600-7H",
       machine_name: '7H',
       operator: "",
       element: "",
       element_description: "",
       plate: "",
       standard: { standard_current: "", standard_voltage: "" },
       actual: { current: "", voltage: "" },
       remarks: "",
       machineimg: "./src/assets/ak600.png",
     },
     // {
     //   id: 5,
     //   itemno: '7I',
     //   machine: "MIG-500-I-7I",
     //   machine_name: '7I',
     //   operator: "",
     //   element: "",
     //   element_description: "",
     //   plate: "",
     //   standard: { standard_current: "", standard_voltage: "" },
     //   actual: { current: "", voltage: "" },
     //   remarks: "",
     //   machineimg: "./src/assets/I500.png",
     // },
     {
       id: 6,
       itemno: '7J',
       machine: "MIG-500-I-7J",
       machine_name: '7J',
       operator: "",
       element: "",
       element_description: "",
       plate: "",
       standard: { standard_current: "", standard_voltage: "" },
       actual: { current: "", voltage: "" },
       remarks: "",
       machineimg: "./src/assets/I500.png",
     },
     {
       id: 7,
       itemno: '7K',
       machine: "MIG-500-I-7K",
       machine_name: '7K',
       operator: "",
       element: "",
       element_description: "",
       plate: "",
       standard: { standard_current: "", standard_voltage: "" },
       actual: { current: "", voltage: "" },
       remarks: "",
       machineimg: "./src/assets/I500.png",
     },
     {
       id: 8,
       itemno: '7L',
       machine: "MIG-500-I-7L",
       machine_name: '7L',
       operator: "",
       element: "",
       element_description: "",
       plate: "",
       standard: { standard_current: "", standard_voltage: "" },
       actual: { current: "", voltage: "" },
       remarks: "",
       machineimg: "./src/assets/I500.png",
     },
     // {
     //   id: 9,
     //   itemno: '27B',
     //   machine: "Panasonic KR-400-27A",
     //   machine_name: '27B',
     //   operator: "",
     //   element: "",
     //   element_description: "",
     //   plate: "",
     //   standard: { standard_current: "", standard_voltage: "" },
     //   actual: { current: "", voltage: "" },
     //   remarks: "",
     //   machineimg: "./src/assets/kr400.png",
     // },
     {
       id: 10,
       itemno: '27C',
       machine: "Panasonic AK-400-27C",
       machine_name: '27C',
       operator: "",
       element: "",
       element_description: "",
       plate: "",
       standard: { standard_current: "", standard_voltage: "" },
       actual: { current: "", voltage: "" },
       remarks: "",
       machineimg: "./src/assets/kr400.png",
     },
     {
       id: 11,
       itemno: '27D',
       machine: "Panasonic YD500RXI",
       machine_name: '27D',
       operator: "",
       element: "",
       element_description: "",
       plate: "",
       standard: { standard_current: "", standard_voltage: "" },
       actual: { current: "", voltage: "" },
       remarks: "",
       machineimg: "./src/assets/yd.webp",
     },
     {
       id: 12,
       itemno: '27E',
       machine: "Panasonic YD500RXI",
       machine_name: '27E',
       operator: "",
       element: "",
       element_description: "",
       plate: "",
       standard: { standard_current: "", standard_voltage: "" },
       actual: { current: "", voltage: "" },
       remarks: "",
       machineimg: "./src/assets/yd.webp",
     },
   ]);
   
   
   const elements = [
     { value: "type-1", label: "Type 1" },
     { value: "type-2", label: "Type 2" },
     { value: "type-3", label: "Type 3" },
     { value: "type-4", label: "Type 4" },
     { value: "type-5", label: "Type 5" },
     { value: "type-6", label: "Type 6" },
     { value: "type-7", label: "Type 7" },
     { value: "type-8", label: "Type 8" },
     { value: "type-9", label: "Type 9" },
     { value: "type-10", label: "Type 10" },
     { value: "type-11", label: "Type 11" },
   ];
   
   const operators = [
     { value: "Bhimappa", label: "Bhimappa" },
     { value: "Somappa", label: "Somappa" },
     { value: "Rajappa", label: "Rajappa" },
   ];
   
   const thicknesses = ["Thickness 1", "Thickness 2", "Thickness 3"];
   
   let selectedMachine = ref("7D");
 



//olasnkf



// const fetchopData = async () => {
//   try {
//     const rows = ['7H','7D'];
//     for (const row of rows) {
//       const response = await fetch(`http://192.168.0.105:6969/op_shift/${row}`);
//       const data = await response.json();
//       console.log(`Data for row ${row}:`, data);
//       if (operatorData) {
//       row.operator = operatorData.operator_name;
//       // Update other properties as needed
//     }
//     }
//   } catch (error) {
//     console.error('Error fetching data:', error);
//   }
// };

// onMounted(() => {
//   fetchopData();
// });

//WORKING CODE for the weleder display
// onMounted(async () => {
//   // Fetch operator data for each row
//   for (const row of dataRows.value) {
//     const response = await fetch(`http://192.168.0.105:6969/op_shift/${row.itemno}`);
//     const operatorData = await response.json();
//     console.log("++--==--")
//     console.log(operatorData)
    
    
//     // Assuming the response contains only one item
//     const operatorInfo = operatorData[0];
    


//     // Update the operator field for the current row
//     if (operatorInfo) {
//       row.operator = operatorInfo.operator_name;
      
      

//     }
//   }
// });

//Working Current and voltage

// onMounted(async () => {
//   // Fetch operator data for each row
//   for (const row of dataRows.value) {
//     try {
//       // Fetch element types based on row.itemno
//       const typesResponse = await fetch(`http://192.168.0.105:6969/op_shift/${row.itemno}`);
//       const typesData = await typesResponse.json();

//       // Assuming typesData is an array of types, for simplicity
//       const elementTypes = typesData.map(item => item.element_type);

//       // Fetch element data for each type
//       for (const elementType of elementTypes) {
//         const elementResponse = await fetch(`http://192.168.0.105:6969/elements/${elementType}`);
//         const elementData = await elementResponse.json();

//         console.log("Element Type:", elementType);
//         console.log("Element Data:", elementData);

//         const { current, voltage } = elementData;

//         console.log("Current:", current);
//         console.log("Voltage:", voltage);

//         // Assuming the response contains only one item
//         const operatorInfo = elementData;

//         // Update the operator field for the current row
//         if (operatorInfo) {
//           row.operator = operatorInfo.operator_name;
//         }
//       }
//     } catch (error) {
//       console.error('Error fetching data:', error);
//     }
//   }
// });

//old one
onMounted(async () => {
  // Fetch operator data for each row
  for (const row of dataRows.value) {
    try {
      // Fetch element types based on row.itemno
      const typesResponse = await fetch(`http://192.168.0.105:6969/op_shift/${row.itemno}`);
      const typesData = await typesResponse.json();
      console.log(typesData)

      // Ensure typesData is an array
      if (!Array.isArray(typesData)) {
        console.error('Invalid response format. Expected an array.');
        continue; // Skip to the next iteration
      }

      // Filter typesData based on the current time
      const currentDate = new Date();
      const filteredTypesData = typesData.filter(item => {
        const startTime = new Date(item.start_time);
        const endTime = new Date(item.end_time);
        return startTime <= currentDate && currentDate <= endTime;
      });

      // Sort filteredTypesData by start_time in descending order
      filteredTypesData.sort((a, b) => new Date(b.start_time) - new Date(a.start_time));

      // console.log(filteredTypesData)

      // Take the first element from the sorted array (most recent)
      const mostRecentElement = filteredTypesData[filteredTypesData.length - 1];
      console.log("MOST RECENT")
      console.log(mostRecentElement)

      // Assuming mostRecentElement is an object with element_type property
      const mostRecentElementType = mostRecentElement ? mostRecentElement.element_type : null;

      // Fetch welder data for the most recent operator
      const mostRecentOperatorName = mostRecentElement ? mostRecentElement.operator_name : null;
      const welderResponse = await fetch(`http://192.168.0.105:6969/welder/${mostRecentOperatorName}`);
      const welderData = await welderResponse.json();

      // Update row with welder data
      row.I_no = mostRecentElement.I_no;
      row.Fc_no = mostRecentElement.Fc_no;
      row.project = mostRecentElement.project;
      row.startTime = mostRecentElement.start_time;
      row.endTime = mostRecentElement.end_time;
      console.log("))))))))))))))))))))))))))")
      console.log(row.startTime)
      // console.log("plateeee")
      // console.log(mostRecentElement.plate)
      row.plate = mostRecentElement.plate_thickness
       row.platediscription = mostRecentElement.plate_description
       row.remarks = mostRecentElement.remarks

;

      // Fetch element data for the most recent type
      const elementResponse = await fetch(`http://192.168.0.105:6969/elements/${mostRecentElementType}`);
      const elementData = await elementResponse.json();

      // Assuming the response contains only one item
      const { standard_current, standard_voltage, range } = elementData;

      // Update the standard current and voltage for the current row
      row.standard.standard_current = standard_current;
      row.standard.standard_voltage = standard_voltage;
      row.range = range;

      // Display the standard current and voltage
      // console.log("Standard Current:", row.standard.standard_current);
      // console.log("Standard Voltage:", row.standard.standard_voltage);

      // Update the operator field for the current row
      row.operator = mostRecentOperatorName;
      row.element = mostRecentElementType;

    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }
});



// onMounted(async () => {
//   // Fetch operator data for each row
//   for (const row of dataRows.value) {
//     try {
//       // Fetch element types based on row.itemno
//       const typesResponse = await fetch(`http://192.168.0.105:6969/op_shift/${row.itemno}`);
//       const typesData = await typesResponse.json();

//       // Assuming typesData is an array of types, for simplicity
//       const elementTypes = typesData.map(item => item.element_type);
//       const welderDetails = typesData.map(item => item.operator_name);

//       //operator

//       for (const welderDetail of welderDetails) {
//         const welderResponse = await fetch(`http://192.168.0.105:6969/welder/${welderDetail}`);
//         const welderdata = await welderResponse.json();
//         console.log("_____________________________________________")
//         console.log(welderdata)
//         row.I_no=welderdata.I_no
//         row.Fc_no=welderdata.Fc_no
//         row.project=welderdata.project

//       }


//       // Fetch element data for each type
//       for (const elementType of elementTypes) {
//         const elementResponse = await fetch(`http://192.168.0.105:6969/elements/${elementType}`);
//         const elementData = await elementResponse.json();

//         console.log("Element Type:", elementType);
//         console.log("Element Data:", elementData);

//         // Assuming the response contains only one item
//         const { current, voltage,range } = elementData;
//         const operatorInfo = typesData[0];

//         // Update the standard current and voltage for the current row
//         row.standard.current = current;
//         row.standard.voltage = voltage;
//         row.range = range;
//         // row.standard.voltage = element_description;

//         // Display the standard current and voltage
//         console.log("Standard Current:", row.standard.current);
//         console.log("Standard Voltage:", row.standard.voltage);

//         // Update the operator field for the current row
//         if (operatorInfo) {
//           row.operator = operatorInfo.operator_name;
//           row.element = operatorInfo.element_type;
//           console.log(row.operator)
//         }
//       }
//     } catch (error) {
//       console.error('Error fetching data:', error);
//     }
//   }
// });

//http://192.168.0.105:6969/welder/

// console.log("************************************")
      // console.log(operatorInfo.element_type);
      // row.element = operatorInfo.element_type;
      // // row.element = operatorInfo.element_type;
      // // row.element = operatorInfo.element_type;
      // row.current = operatorInfo.current;
      // const responseelem = await fetch(`//192.168.0.105:6969/elements/${operatorInfo.element_type}`);
      // console.log("+++++++++++++++++++++++")
      // console.log(responseelem)




   //element select data getting
   const machineData = ref({});



  //  async function onOptionSelected(event) {
  //   //  const selectedValue = event.target.value;
  //   //  console.log('Selected item:', selectedValue);
   
  //    try {
  //     for (const row of dataRows.value){
  //      const response = await axios.get(`http://192.168.0.105:6969/elements/${row.element}`);
  //      console.log('API Response:', response.data);
  //      dataRows.value.forEach((row) => {
  //        if (row.element) {
  //          updateMachineData(row.id, response.data.current, response.data.voltage, response.data.range, response.data.element_descrption);
  //        }
  //      });
  //    }} catch (error) {
  //      console.error('Error fetching data:', error);
  //    }
  //  }
   
  //  async function onOptionSelected(event) {
  //    const selectedValue = event.target.value;
  //    console.log('Selected item:', selectedValue);
   
  //    try {
  //      const response = await axios.get(`http://192.168.0.105:6969/elements/${selectedValue}`);
  //      console.log('API Response:', response.data);
  //      dataRows.value.forEach((row) => {
  //        if (row.element === selectedValue) {
  //          updateMachineData(row.id, response.data.current, response.data.voltage, response.data.range, response.data.element_descrption);
  //        }
  //      });
  //    } catch (error) {
  //      console.error('Error fetching data:', error);
  //    }
  //  }
   
   function updateMachineData(machineId, current, voltage, range,element_description) {
     machineData.value[machineId] = { current, voltage, range,element_description};
   }
   
   // Get the current value for a specific machine
   function getMachineCurrent(machineId) {
     return machineData.value[machineId]?.current || "n/a";
   }
   
   // Get the voltage value for a specific machine
   function getMachineVoltage(machineId) {
     return machineData.value[machineId]?.voltage || "n/a";
   }
   
   function getMachineElementRange(machineId) {
     return machineData.value[machineId]?.range || "n/a";
   }
 
    //operator select data getting
   const operatorData = ref({});
 
   async function onOeratorSelected(event) {
     const selectedValue = event.target.value;
    //  console.log('Selected item:', selectedValue);
   
     try {
       const response = await axios.get(`http://192.168.0.105:6969/welder/${selectedValue}`);
      //  console.log('API Response:', response.data);
       dataRows.value.forEach((row) => {
         if (row.operator === selectedValue) {
           updateoperatorData(row.id, response.data.I_no, response.data.Fc_no, response.data.project);
         }
       });
     } catch (error) {
       console.error('Error fetching data:', error);
     }
   }

  //  async function onOeratorSelected(event) {
  //    const selectedValue = event.target.value;
  //    console.log('Selected item:', selectedValue);
   
  //    try {
  //      const response = await axios.get(`http://192.168.0.105:6969/welder/${selectedValue}`);
  //      console.log('API Response:', response.data);
  //      dataRows.value.forEach((row) => {
  //        if (row.operator === selectedValue) {
  //          updateoperatorData(row.id, response.data.I_no, response.data.Fc_no, response.data.project);
  //        }
  //      });
  //    } catch (error) {
  //      console.error('Error fetching data:', error);
  //    }
  //  }
   function updateoperatorData(machineId, I_no, Fc_no, project) {
     operatorData.value[machineId] = { I_no, Fc_no, project };
   }
   
   // Get the current value for a specific machine
   function getoperatorIno(machineId) {
     return operatorData.value[machineId]?.I_no || "n/a";
   }
   
   // Get the voltage value for a specific machine
   function getoperatorFcno(machineId) {
     return operatorData.value[machineId]?.Fc_no || "n/a";
   }
   
   function getoperatorProject(machineId) {
     return operatorData.value[machineId]?.project || "n/a";
   }
 

   //------------------------------------------



   const machineLiveData = ref({});
const dataLoaded = ref(false);


const connectToWebSocket = () => {
  const socket = new WebSocket('ws://192.168.0.105:6969/live_recent_ws');

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    data.forEach(({ machine_id, current, voltage }) => {
      const rowNumber = getRowNumberForMachine(machine_id);
      if (rowNumber !== null) {
        updateMachineLiveData(rowNumber, current, voltage);
      }
    });
  };

  socket.onclose = (event) => {
    console.error('WebSocket closed:', event);
    // You may want to handle reconnection logic here
  };
  
  socket.onopen = () => {
    console.log('WebSocket opened');
    dataLoaded.value = true; // Set dataLoaded to true once WebSocket is opened
  };

  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
    dataLoaded.value = false; // Set dataLoaded to false if there's an error
  };
};

const fetchDataFromWebSocket = () => {
  // No need for this function anymore as data is received through WebSocket
};

function updateMachineLiveData(rowNumber, current, voltage) {
  machineLiveData.value[rowNumber] = { current, voltage };
}

function getMachineLiveCurrent(rowNumber) {
  return machineLiveData.value[rowNumber]?.current || "0.0";
}

function getMachineLiveVoltage(rowNumber) {
  return machineLiveData.value[rowNumber]?.voltage || "0.0";
}

// Function to get the row number for each machine
function getRowNumberForMachine(machineId) {
  switch (machineId) {
   
    case '7G': return 3;
    case '7H': return 4;
    case '7J': return 6;
    case '7K': return 7;
    case '7L': return 8;
    case '27C': return 10;
    case '27D': return 11;
    case '27E': return 12;
    default: return null; // Return null for unknown machines
  }
}

onMounted(() => {
  connectToWebSocket(); // Use WebSocket connection instead of fetchDataFromBackend
});

// const fetchDataFromBackend = async () => {
//   try {
//     for (const row of dataRows.value) {
//       const response = await axios.get(`http://192.168.0.105:6969/live_data/${row.machine_name}`);
//       // console.log("Insde the");
//       const current = response.data[0]["current"];
//       const voltage = response.data[0]["voltage"];
      
      
//       // console.log(current);
//       // console.log(voltage);
//       updateMachineLiveData(row.id, current, voltage);
//     }
    

//     dataLoaded.value = true;
//   } catch (error) {
//     console.error('Error fetching data:', error);
//     dataLoaded.value = false;
//   }
// };

// function updateMachineLiveData(machine_id, current, voltage) {
//   machineLiveData.value[machine_id] = { current, voltage };
// }

// function getMachineLiveCurrent(machineId) {
//   return machineLiveData.value[machineId]?.current || "0.0";
// }

// function getMachineLiveVoltage(machineId) {
//   return machineLiveData.value[machineId]?.voltage || "0.0";
// }

// onMounted(() => {
//   connectToWebSocket();
//   // setInterval(fetchDataFromBackend, 1000);
// });

// Define the convertToEpochTime function
function convertToEpochTime(dateTimeString) {
  // Attempt to parse the date/time string
  const parsedDate = Date.parse(dateTimeString);

  // Check if the parsing was successful
  if (!isNaN(parsedDate)) {
    // If successful, return the epoch time
    return parsedDate / 1000; // Convert milliseconds to seconds
  } else {
    // If parsing fails, log an error and return null or handle accordingly
    console.error(`Error parsing date/time string: ${dateTimeString}`);
    return null;
  }
}


async function saveEditedData(row) {
  try {
    const response = await axios.put(`http://192.168.0.105:6969/edit/${row.element}/${row.operator}?machine_id=${row.itemno}`, {
      // standard_current: row.standard.standard_current,
      // standard_voltage: row.standard.standard_voltage,
      element_description: row.element_description,
      range: row.range,
      I_no: row.I_no,
      Fc_no: row.Fc_no,
      project: row.project,
      remarks: row.remarks,
      plate_thickness: row.plate,
      plate_description : row.platediscription
      
    });

    // Handle successful response, if needed
    // console.log('Data updated:', response.data);
    // console.log(row.element);
    


    updateoperatorData(row.id, row.I_no, row.Fc_no, row.project, row.current, row.voltage, row.element_description, row.range);
    // console.log("TTTTTTTTTTTTTTTTTTTTTTTTTTTTT");
    // console.log(updateoperatorData);
    graphData.value.range_current = 'row.range';

    // Toggle editing status
    toggleEdit(row);

    // Fetch recent data from the fast API endpoint
    const machineId = row.machine_name; // Implement a function to get machineId
    const recentDataResponse = await axios.get(`http://192.168.0.105:6969/op_shift/${machineId}`);
    const recentData = recentDataResponse.data; // Assuming the data is an array

    // Filter data for the specific operator
    const operatorRecentData = recentData.filter(item => item.operator_name === row.operator);

    if (operatorRecentData.length > 0) {
      // Find the most recent data based on the timestamp
      const mostRecentData = operatorRecentData.reduce((max, item) => (item.timestamp > max.timestamp ? item : max));

      // Get the start time and end time from the most recent data and convert to epoch-time
      const startTime = mostRecentData.start_time !== undefined ? convertToEpochTime(mostRecentData.start_time) : null;
      const endTime = mostRecentData.end_time !== undefined ? convertToEpochTime(mostRecentData.end_time) : null;

      // Continue with the rest of the code
      // console.log(row.operator);
      // console.log(row.element);
      // console.log(machineId);
      // console.log(mostRecentData.start_time);

      const createEntryResponse = await axios.post("http://192.168.0.105:6969/op_shift/", {
        operator_name: row.operator,
        element_type: row.element, // Change this to the appropriate type
        machine_name: machineId,
        start_time: row.startTime,
        end_time: row.endTime,
        I_no: row.I_no,
      Fc_no: row.Fc_no,
      project: row.project,
      remarks: row.remarks,
      plate_thickness: row.plate,
      plate_description : row.platediscription
      });
      console.log("(((((((((((((((((((((((((object)))))))))))))))))))))))))")
console.log(row.startTime)
      console.log("New entry created:", createEntryResponse.data);
    } else {
      console.log(`No recent data found for operator: ${row.operator}`);
    }
  } catch (error) {
    console.error('Error updating data:', error);
    // Handle error, if needed
  }
}

   
// //all element type and operator edit/save
// async function saveEditedData(row) {
//      try {
//        const response = await axios.put(`http://192.168.0.105:6969/edit/${row.element}/${row.operator}
//        `, {
//         standard_current: row.standard.standard_current, 
//         standard_voltage: row.standard.standard_voltage, 
//          element_description: row.element_description,
//          range: row.range,
//          I_no: row.I_no,
//          Fc_no: row.Fc_no,
//          project: row.project,
         
//        });
      
//        // Handle successful response, if needed
//       //  console.log('Data updated:', response.data);
   
//        updateoperatorData(row.id, row.I_no, row.Fc_no, row.project, row.current,row.voltage, row.element_description,row.range);
//        console.log("TTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
//        console.log(updateoperatorData)
   
//        // Toggle editing status
//        toggleEdit(row);
//      } catch (error) {
//        console.error('Error updating data:', error);
//        // Handle error, if needed
//      }
//    }
 
   //only element type saveEditedDataType http://172.18.7.66:6060/edit/type-1/Bhimappa
   // async function saveEditedDataElement(row) {
   //   try {
   //     const response = await axios.put(`http://172.18.7.66:6060/edit/${row.element}/${row.operator}`, {
   //       current: row.current, // Use the actual current value from the row
   //       voltage: row.voltage, // Use the actual voltage value from the row
   //       element_description: row.element_description,
   //       range: row.range,
   //     });
   
   //     // Handle successful response, if needed
   //     console.log('Data updated:', response.data);
   
   //     updateoperatorData(row.id, row.current,row.voltage, row.element_description);
   
   //     // Toggle editing status
   //     toggleEditElement(row);
   //   } catch (error) {
   //     console.error('Error updating data:', error);
   //     // Handle error, if needed
   //   }
   // }
 
   //http://172.18.7.66:6060/welder/Bhimappa
   function showGraph(rowId) {
     // Logic to show the graph for the selected row
   }
   
   function saveRemarks(rowId) {
     // Logic to save remarks for the selected row
   }
   
   function editRemarks(rowId) {
     // Logic to edit remarks for the selected row
   }
   
   function generateReport(newSelectedMachine) {
     isReport.value = true;
     selectedMachine.value = newSelectedMachine;
   }
   
   function hideReportPopup() {
     isReport.value = false;
   }

   let ParentData = ref(null);
   
   const graphData = ref({
  machineId: '',
  range_current_low :'',
  range_current_high :'',
  range_voltage_low : '',
  range_voltage_high : ''
});

function showUserPopup(machineId) {
  isUserPopupVisible.value = true;
  graphData.value.machineId = machineId;

  axios.get(`http://192.168.0.105:6969/live_data/live_type/${machineId}`)
    .then(response => {
      // Check if there is data in the response
      if (response.data && response.data.length > 0) {
        const lowStdVtgValue = response.data[0].low_std_vol;
        const highStdVtgValue = response.data[0].high_std_vol;
        const lowStdcurValue = response.data[0].low_std_curr;
        const highStdcurValue = response.data[0].high_std_curr;

        graphData.value.range_voltage_low = lowStdVtgValue
      graphData.value.range_voltage_high = highStdVtgValue
      graphData.value.range_current_low = lowStdcurValue
      graphData.value.range_current_high = highStdcurValue
        // console.log('Low Standard Voltage:', lowStdVtgValue);
      } else {
        console.error('No data or empty array in the response');
      }
      // Assuming sendata is defined somewhere in your component
      // Call the sendata function to update range values
      // sendata(machineId);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
}
function showUserLiveCurrentPopup(machineId) {
  isUserLiveCurrentPopupVisible.value = true;
  graphData.value.machineId = machineId;

  axios.get(`http://192.168.0.105:6969/live_data/live_type/${machineId}`)
    .then(response => {
      // Check if there is data in the response
      if (response.data && response.data.length > 0) {
        const lowStdVtgValue = response.data[0].low_std_vol;
        const highStdVtgValue = response.data[0].high_std_vol;
        const lowStdcurValue = response.data[0].low_std_curr;
        const highStdcurValue = response.data[0].high_std_curr;

        graphData.value.range_voltage_low = lowStdVtgValue
      graphData.value.range_voltage_high = highStdVtgValue
      graphData.value.range_current_low = lowStdcurValue
      graphData.value.range_current_high = highStdcurValue
        console.log('Low Standard Voltage:', lowStdVtgValue);
      } else {
        console.error('No data or empty array in the response');
      }
      // Assuming sendata is defined somewhere in your component
      // Call the sendata function to update range values
      // sendata(machineId);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
}
// async function sendata(machineId) {
//   try {
//     console.log(machineId)
//     const response = await axios.put(`http://192.168.0.105:6969/edit/${machineId.element}/${machineId.operator}`);
//     const recentData = response.data;
//     console.log("77777777777777777");

//     // Assuming `recentData.range` contains the new range value
//     graphData.value.range_current = recentData.range;
//     graphData.value.range_voltage = recentData.range;

//     // Log the updated graphData
//     console.log(graphData.value);
//   } catch (error) {
//     console.error('Error updating data:', error);
//   }
// }


///working line data connection
// function showUserPopup(machineId) {
//      isUserPopupVisible.value = true;
//      graphData.value.machineId=machineId;
//     //  console.log("%%%%%%%%%%")
//      //console.log(graphData.value.machineId);

//      ParentData.value  = graphData.value.machineId;
    

//     //  console.log("inside")
//     //  for (const row of dataRows.value) {
//     //   const response = row.machine_name;
//     //   console.log(response)}
//    }

const machine1 = ref([]);

const fetchDatastate = async () => {
  try {
    const response = await axios.get('http://192.168.0.105:6969/machine_color/');
    machine1.value = response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};
onMounted(fetchDatastate);

// Periodically update data (adjust the interval as needed)
setInterval(fetchDatastate, 5000);

watch(machine1, (newData) => {
  // You can add logic here to update colors based on newData
  console.log('Data updated:', newData);
});

   function showUserPopupGraph() {
       isUserPopupVisibleGraph.value = true;
     }
     
     function hideUserPopupGraph() {
       isUserPopupVisibleGraph.value = false;
     }
   function hideUserPopup() {
     isUserPopupVisible.value = false;
   }
   function hideUserLiveCurrentPopup(){
    isUserLiveCurrentPopupVisible.value=false;
   }
   
   function showStackPopup() {
     isStackVisible.value = true;
   }
   
   function hideStackPopup() {
     isStackVisible.value = false;
   }
   let ParentProductionData = ref();
   
 const productionData = ref({
  machineId:'',
 })
   function showProductionPopup(machineId) {
     isProductionVisible.value = true;
     productionData.value.machineId=machineId;
    //  console.log("%%%%%%%%%%")
     //console.log(graphData.value.machineId);

     ParentProductionData.value  = productionData.value.machineId;
    //  console.log("^^^^^^^^^^^^^^^^^^^^^^^^^^")
    //  console.log( ParentProductionData.value )
   }
   function hideProductionPopup() {
     isProductionVisible.value = false;
   }
   function showNotificationPopup() {
     // isNotificationVisible.value = true;
     isNotificationVisible.value =!isNotificationVisible.value;
     notificationCount.value = 0;
   };
   
   function hideNotificationPopup() {
     isNotificationVisible.value = false;
   }
   
   function showloginPopup() {
     isloginVisible.value = true;
   }
   
   function hideloginPopup() {
     isloginVisible.value = false;
   }
   function toggleEdit(row) {
     row.isEditing = !row.isEditing;
   }
   function toggleEditElement(row) {
     row.isEditing = !row.isEditing;
   }
 
   const scrollToTop = () => {
   window.scrollTo({
     top: 0,
     behavior: 'smooth' // Smooth scrolling
   });
 };
   </script>
   
   
   <style>
   /* Styling for the DataTable component can go here */
   thead tr {
     background-color: #3d5a80;
     color: white;
   }
   
   button,
   input,
   textarea {
     box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
   }
   
   /* Hover effect for buttons and text boxes */
   button:hover,
   input:hover,
   textarea:hover {
     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
   }
   
   /* Glassomorphic effect for buttons */
   .glassmorphic-button {
     border: none;
     background: rgba(255, 255, 255, 0.1);
     box-shadow: 8px 8px 16px rgba(0, 0, 0, 0.1), -8px -8px 16px rgba(255, 255, 255, 0.5);
     padding: 8px 16px;
     border-radius: 8px;
     transition: transform 0.2s, background-color 0.2s;
   }
   
   /* Hover effect for buttons */
   .glassmorphic-button:hover {
     background-color: rgba(0, 0, 0, 0.2);
     transform: scale(1.1);
   }
   
   /* Glassomorphic effect for text inputs and textareas */
   input[type="text"],
   textarea,
   select {
     background: rgba(81, 123, 170, 0.068);
     border: none;
     border-radius: 8px;
     box-shadow: 8px 8px 16px rgba(0, 0, 0, 0.1), -8px -8px 16px rgba(245, 252, 255, 0.5);
     padding: 8px;
   }
   
   /* Hover effect for text inputs and textareas */
   input[type="text"]:hover,
   textarea:hover {
     background-color: rgba(255, 255, 255, 0.2);
   }
   
   .card {
     opacity: 100;
     /* Set opacity to 1 for full opacity */
     background-color: transparent;
     /* Remove background color */
   }

   .npopup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.npopup-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
  max-width: 80%;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
}
 
   .notification-counter {
   position: absolute;
   /* top: -10px; */
   right: 438px;
   background-color: red;
   color: white;
   border-radius: 50%;
   padding: 4px 8px;
   font-size: 12px;
 }
   </style>
   