// API配置文件
const isDevelopment =false;

// 根据环境选择不同的API基础URL
const API_BASE_URL = isDevelopment 
  ? 'http://localhost:9000' 
  : 'http://1.95.188.183:9000';

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
    return `${this.baseURL}${endpoint}`;
  }
};
