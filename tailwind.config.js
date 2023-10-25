module.exports = {
  content: ['./public/**/*.html', './src/**/*.vue'], // Add paths to your HTML and Vue files here
  theme: {
    extend: {
      colors: {
        primary: '#FF5733', // Example custom primary color
      },
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'], // Example custom font family
      },
      // You can add more theme customizations here as needed
    },
  },
  plugins: [],
};
