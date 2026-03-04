<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-area">
        <h1 class="app-title">思 辩</h1>
        <p class="app-subtitle">有思想 有深度</p>
      </div>
      
      <div class="input-area">
        <div class="phone-input">
          <input 
            type="tel" 
            v-model="phoneNumber" 
            placeholder="请输入手机号" 
            maxlength="11"
            @blur="validatePhone"
            :class="{ 'input-error': phoneError }"
          />
          <span v-if="phoneError" class="error-message">{{ phoneError }}</span>
        </div>
        
        <div class="login-button" @click="handleLogin" :class="{ 'disabled': !isValidPhone }">
          一键登录
        </div>
        
        <div class="other-login-options" @click="goToOtherLogin">
          其它登录方式
        </div>
      </div>
      
      <div class="agreement-area">
        <p class="agreement-text">
          我已阅读并同意《用户协议》《隐私保护协议》以及《中国移动认证服务条款》
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      phoneNumber: '',  // 初始化为空字符串
      phoneError: ''    // 手机号验证错误信息
    }
  },
  computed: {
    // 计算属性：验证手机号格式
    isValidPhone() {
      const phoneRegex = /^1[3-9]\d{9}$/;
      return phoneRegex.test(this.phoneNumber);
    }
  },
  methods: {
    // 手机号格式验证
    validatePhone() {
      this.phoneError = '';
      if (!this.phoneNumber) {
        this.phoneError = '请输入手机号';
        return false;
      }
      const phoneRegex = /^1[3-9]\d{9}$/;
      if (!phoneRegex.test(this.phoneNumber)) {
        this.phoneError = '请输入正确的11位手机号';
        return false;
      }
      return true;
    },
    
    handleLogin() {
      // 验证手机号
      if (!this.validatePhone()) {
        return;
      }
      
      // 模拟登录过程
      console.log('登录中...手机号:', this.phoneNumber);
      
      // 存储token和手机号
      localStorage.setItem('token', 'demo-token');
      localStorage.setItem('userPhone', this.phoneNumber);
      
      // 登录成功后跳转到热点辩论页面
      this.$router.push('/hot-debates');
    },
    
    goToOtherLogin() {
      this.$router.push('/other-login');
    }
  }
}
</script>

<style scoped>
.login-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.logo-area {
  text-align: center;
  margin-bottom: 10px;
}

.app-title {
  font-size: 36px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #333;
}

.app-subtitle {
  font-size: 14px;
  color: #666;
}

.input-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.phone-input {
  width: 100%;
  border-bottom: 1px solid #f5f5f5;
  padding-bottom: 10px;
}

.phone-input input {
  width: 100%;
  border: none;
  outline: none;
  font-size: 16px;
  padding: 8px 0;
}

.phone-input input.input-error {
  border-bottom: 1px solid #ff4a4a;
}

.error-message {
  display: block;
  color: #ff4a4a;
  font-size: 12px;
  margin-top: 5px;
}

.login-button {
  background-color: #07c160;
  color: white;
  text-align: center;
  padding: 12px 0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #06ad56;
}

.login-button.disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.other-login-options {
  text-align: center;
  color: #666;
  font-size: 14px;
  padding: 10px 0;
  cursor: pointer;
}

.agreement-area {
  margin-top: auto;
}

.agreement-text {
  font-size: 12px;
  color: #999;
  text-align: center;
  line-height: 1.5;
}
</style>
