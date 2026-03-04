// API配置文件
// 优先使用环境变量 VUE_APP_API_URL，否则根据环境判断
const envApiUrl = process.env.VUE_APP_API_URL;
const isDevelopment = process.env.NODE_ENV === 'development';

// 根据环境选择不同的API基础URL
// 默认使用相对路径 '/api'，便于反向代理配置
const API_BASE_URL = envApiUrl || (isDevelopment 
  ? 'http://localhost:9000' 
  : '/api');

// Axios全局默认配置
import axios from 'axios';

// 设置全局超时时间（10秒）
axios.defaults.timeout = 10000;
axios.defaults.baseURL = API_BASE_URL;

// 请求拦截器 - 添加认证token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 统一错误处理
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED' && error.message.includes('timeout')) {
      console.error('请求超时，请稍后重试');
    }
    return Promise.reject(error);
  }
);

export default {
  baseURL: API_BASE_URL,
  
  // API端点
  endpoints: {
    debates: '/api/debates',
    debateDetail: '/api/debate',
    // 可以添加其他API端点
  },
  
  // 获取完整的API URL
  getUrl(endpoint) {
    // 如果 baseURL 是相对路径，直接拼接
    if (this.baseURL.startsWith('/')) {
      return `${this.baseURL}${endpoint}`;
    }
    return `${this.baseURL}${endpoint}`;
  },

  // 带超时的请求方法封装
  async request(config) {
    return axios.request({
      ...config,
      timeout: config.timeout || 10000
    });
  },

  async get(url, config = {}) {
    return axios.get(url, { 
      timeout: config.timeout || 10000,
      ...config 
    });
  },

  async post(url, data, config = {}) {
    return axios.post(url, data, { 
      timeout: config.timeout || 10000,
      ...config 
    });
  }
};
