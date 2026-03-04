<template>
  <div class="other-login-container">
    <header class="header">
      <div class="back-button" @click="goBack">
        <span>←</span>
      </div>
      <h1>其他登录方式</h1>
      <div class="placeholder"></div>
    </header>
    
    <main class="main-content">
      <div class="login-options">
        <div class="login-option wechat" @click="handleWechatLogin">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="#07C160">
              <path d="M8.686 13.987c-1.13 0-2.044-.9-2.044-2.046 0-1.142.914-2.046 2.044-2.046 1.132 0 2.043.904 2.043 2.046 0 1.146-.91 2.046-2.043 2.046m6.538 0c-1.132 0-2.043-.9-2.043-2.046 0-1.142.91-2.046 2.043-2.046 1.13 0 2.043.904 2.043 2.046 0 1.146-.913 2.046-2.043 2.046M12 2C6.477 2 2 5.58 2 9.958c0 2.424 1.304 4.59 3.355 6.044-.14.44-.363 1.12-.523 1.627-.2.61.23.61.46.5.17-.1 1.97-1.16 2.28-1.34.823.17 1.73.3 2.43.3 5.522 0 10-3.58 10-7.958C20 5.58 15.522 2 12 2"></path>
            </svg>
          </div>
          <div class="text">微信登录</div>
        </div>
        
        <div class="login-option weibo" @click="handleWeiboLogin">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="#E6162D">
              <path d="M10.098 20c-4.038 0-7.098-1.99-7.098-5.027 0-2.91 3.098-5.973 6.988-5.973 4.018 0 7.012 1.94 7.012 4.973 0 2.909-2.994 6.027-6.902 6.027zm3.908-10.305c-.4-.03-.38-.3-.152-1.003.23-.899-.064-1.662-.872-1.815-2.24-.428-4.3 1.934-5.428 3.31-.855 1.06-1.858 2.251-1.858 3.286 0 1.342 1.763 2.652 3.99 2.652 2.59 0 4.762-1.667 5.428-2.652.38-.559.428-1.214.152-1.815-.19-.428-.38-.899-.26-.963zm-1.313-3.39c-.19-.03-.38-.03-.57-.03-.798 0-1.368.428-1.368 1.003 0 .428.38.899 1.083.899.722 0 1.368-.3 1.368-.899 0-.428-.323-.899-.513-.973zm-2.396.899c-.57 0-.95.428-.95.899 0 .428.38.899.95.899.57 0 1.007-.428 1.007-.899 0-.471-.437-.899-1.007-.899zM20 9.239c0-.642-.513-1.156-1.14-1.156h-1.026c-.153 0-.305.043-.427.128a.707.707 0 0 0-.305.385l-.457 1.563c-.076.214-.076.471 0 .685.076.214.228.385.38.471.153.086.305.129.458.129h.532c.38 0 .684.3.684.685 0 .385-.305.685-.684.685h-.989c-.38 0-.684-.3-.684-.685 0-.385.305-.685.684-.685h.076l-.228-.77h-.38c-.153 0-.305-.043-.458-.129a1.12 1.12 0 0 1-.38-.471 1.308 1.308 0 0 1 0-.685l.457-1.563c.076-.214.228-.385.38-.471a.995.995 0 0 1 .533-.129h1.824c.38 0 .684.3.684.685 0 .385-.305.685-.684.685h-.077l.229.77h.38c.627 0 1.14-.514 1.14-1.156zm-2.244-2.183c-.076-.214-.228-.385-.38-.471a.995.995 0 0 0-.533-.129h-1.824c-.38 0-.684.3-.684.685 0 .385.305.685.684.685h.076l-.228.77h-.38c-.627 0-1.14.514-1.14 1.156 0 .642.513 1.156 1.14 1.156h1.026c.153 0 .305-.043.457-.128a.707.707 0 0 0 .305-.385l.457-1.563c.076-.214.076-.471 0-.685.076-.043.076-.086.076-.086z"></path>
            </svg>
          </div>
          <div class="text">微博登录</div>
        </div>
      </div>
    </main>
    
    <div class="agreement-area">
      <p class="agreement-text">
        我已阅读并同意《用户协议》《隐私保护协议》以及《中国移动认证服务条款》
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OtherLoginView',
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    handleWechatLogin() {
      console.log('微信登录');
      // 这里应该调用微信登录API
      alert('微信登录功能即将上线');
    },
    handleWeiboLogin() {
      console.log('微博登录');
      // 这里应该调用微博登录API
      alert('微博登录功能即将上线');
    }
  }
}
</script>

<style scoped>
.other-login-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border-radius: 8px 8px 0 0;
  margin: 15px 15px 0;
}

.header h1 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.back-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 20px;
}

.placeholder {
  width: 40px;
}

.main-content {
  flex: 1;
  padding: 30px 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 15px;
  background-color: white;
  border-radius: 0 0 8px 8px;
}

.login-options {
  width: 100%;
  max-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.login-option {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.2s;
}

.login-option:hover {
  transform: translateY(-2px);
}

.login-option .icon {
  margin-right: 12px;
}

.login-option .text {
  font-size: 14px;
  font-weight: 400;
}

.login-option.wechat {
  border: 1px solid #07C160;
}

.login-option.weibo {
  border: 1px solid #E6162D;
}

.agreement-area {
  padding: 15px;
  text-align: center;
  margin-top: 15px;
}

.agreement-text {
  font-size: 12px;
  color: #999;
  line-height: 1.5;
}
</style>
