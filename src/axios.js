// axios.js

import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://172.18.100.240:9999', // Replace with your server's base URL
  // You can add other Axios configurations here if needed
});

export default instance;
