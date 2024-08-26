<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <h2 class="text-center text-3xl font-extrabold text-gray-900">Weekly Coding Challenge #1: Sign in/up Form</h2>
      <div class="container" :class="{ 'right-panel-active': isRightPanelActive }">
        <!-- Sign Up Form -->
        <div class="form-container sign-up-container">
          <form @submit.prevent="submitSignUp">
            <h1 class="text-xl font-bold">Create Account</h1>
            <div class="social-container">
              <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
              <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
              <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
            </div>
            <span class="text-sm">or use your email for registration</span>
            <input v-model="name" type="text" placeholder="Name" class="input" />
            <input v-model="email" type="email" placeholder="Email" class="input" />
            <input v-model="password" type="password" placeholder="Password" class="input" />
            <button class="button">Sign Up</button>
          </form>
        </div>

        <!-- Sign In Form -->
        <div class="form-container sign-in-container">
          <form @submit.prevent="submitSignIn">
            <h1 class="text-xl font-bold">Sign in</h1>
            <div class="social-container">
              <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
              <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
              <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
            </div>
            <span class="text-sm">or use your account</span>
            <input v-model="signInEmail" type="email" placeholder="Email" class="input" />
            <input v-model="signInPassword" type="password" placeholder="Password" class="input" />
            <a href="#" class="text-blue-500">Forgot your password?</a>
            <button class="button">Sign In</button>
          </form>
        </div>

        <!-- Overlay -->
        <div class="overlay-container">
          <div class="overlay">
            <div class="overlay-panel overlay-left">
              <h1 class="text-xl font-bold">Welcome Back!</h1>
              <p class="text-sm">To keep connected with us please login with your personal info</p>
              <button @click="togglePanel(false)" class="ghost button">Sign In</button>
            </div>
            <div class="overlay-panel overlay-right">
              <h1 class="text-xl font-bold">Hello, Friend!</h1>
              <p class="text-sm">Enter your personal details and start a journey with us</p>
              <button @click="togglePanel(true)" class="ghost button">Sign Up</button>
            </div>
          </div>
        </div>
      </div>

      <footer class="text-white">
        <p>
          Created with <i class="fa fa-heart text-red-600"></i> by
          <a target="_blank" href="https://florin-pop.com" class="text-blue-500">Florin Pop</a>
          - Read how I created this and how you can join the challenge
          <a target="_blank" href="https://www.florin-pop.com/blog/2019/03/double-slider-sign-in-up-form/" class="text-blue-500">here</a>.
        </p>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isRightPanelActive: false,
      name: '',
      email: '',
      password: '',
      signInEmail: '',
      signInPassword: '',
    };
  },
  methods: {
    submitSignUp() {
      // Implement your sign-up logic here
      console.log('Sign Up:', this.name, this.email, this.password);
    },
    submitSignIn() {
      // Implement your sign-in logic here
      console.log('Sign In:', this.signInEmail, this.signInPassword);
    },
    togglePanel(isSignUpPanel) {
      this.isRightPanelActive = isSignUpPanel;
    },
  },
};
</script>

<style>
/* The Tailwind CSS classes will be added here */
</style>
