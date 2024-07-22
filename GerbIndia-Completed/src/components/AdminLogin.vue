<template>
  <div class="container">
   
    <!-- Render the form only if not logged in -->
    <form v-if="!loggedIn" class="login-form" @submit.prevent="handleLogin">
      <h2 class="login-title">Log in</h2>
      <div>
        <label for="email">Email </label>
        <input
          v-model="email"
          id="email"
          type="email"
          placeholder="me@example.com"
          name="email"
          required
        />
      </div>

      <div>
        <label for="password">Password </label>
        <input
          v-model="password"
          id="password"
          type="password"
          placeholder="password"
          name="password"
          required
        />
      </div>

      <button class="btn btn--form" type="submit">Log in</button>
    </form>
   
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const email = ref('');
const password = ref('');
const router = useRouter();
const loggedIn = ref(false); // Add a reactive variable to track login state

const handleLogin = async () => {
  try {
    const response = await axios.get('http://192.168.0.105:6969/users/2');
    const user = response.data;
    if (email.value === user.email && password.value === user.password) {
      loggedIn.value = true; // Set login state to true
      router.push({ name: 'admintable' });
    } else {
      alert('Invalid credentials. Please try again.');
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
    alert('An error occurred while fetching user data. Please try again later.');
  }
};

// const handleLogin = async () => {
//   try {
//     const response = await axios.get('http://192.168.0.105:6969/users/2', {
//       headers: {
//         'Authorization': `Bearer ${token}`,
//       },
//     });
//     const user = response.data;
//     if (email.value === user.email && password.value === user.password) {
//       loggedIn.value = true;
//       router.push({ name: 'admintable' });
//     } else {
//       alert('Invalid credentials. Please try again.');
//     }
//   } catch (error) {
//     console.error('Error fetching user data:', error);
//     alert('An error occurred while fetching user data. Please try again later.');
//   }
// };

const handleLogout = async () => {
  // try {
  //   await axios.post('http://your-server-address/logout');
    // After successful logout, clear the client-side authentication state
    loggedIn.value = false;
    email.value = '';
    password.value = '';
    
//     // Redirect the user to the login page or perform any other actions
//   } catch (error) {
//     console.error('Error logging out:', error);
//     // Handle error as needed
//   }
};
</script>

<style>
.container {
  width: 400px;
  margin: auto;
  padding: 36px 48px 48px 48px;
  background-color: #f2efee;

  border-radius: 11px;
  box-shadow: 0 2.4rem 4.8rem rgba(0, 0, 0, 0.15);
}

.login-title {
  padding: 15px;
  font-size: 22px;
  font-weight: 600;
  text-align: center;
}

.login-form {
  display: grid;
  grid-template-columns: 1fr;
  row-gap: 16px;
  
 
  

}

.login-form label {
  display: block;
  margin-bottom: 8px;
  
}

.login-form input {
  width: 100%;
  padding: 1.2rem;
  border-radius: 9px;
  border: none;
}

.login-form input:focus {
  outline: none;
  box-shadow: 0 0 0 4px rgba(253, 242, 233, 0.5);
}

.btn--form {
  background-color: #f48982;
  color: #2b2a2a;
 
  margin-left: 27%;
  width: 90px;
  align-self: end;
  padding: 8px;
}

.btn,
.btn:link,
.btn:visited {
  display: inline-block;
  text-decoration: none;
  font-size: 20px;
  font-weight: 600;
  border-radius: 9px;
  border: none;

  cursor: pointer;
  font-family: inherit;

  transition: all 0.3s;
}

/* button {
  outline: 1px solid #f48982;
} */

.btn--form:hover {
  background-color: #fdf2e9;
  color: #f48982;
}
</style>
