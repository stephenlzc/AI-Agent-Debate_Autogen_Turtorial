<template>
  <div class="user-profile">
    <!-- 顶部导航栏 -->
    <div class="top-nav">
      <div class="back-button" @click="goBack">
        <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
          <path d="M657.493333 686.08l-195.413333-195.413333 195.413333-195.413334-60.586666-60.586666-256 256 256 256z" fill="currentColor"/>
        </svg>
      </div>
      <div class="page-title">个人信息</div>
      <div class="placeholder"></div>
    </div>
    
    <!-- 用户信息区域 -->
    <div class="user-info-section">
      <div class="user-header">
        <div class="avatar-container">
          <div class="user-avatar">
            <span class="avatar-text">F</span>
          </div>
        </div>
        <div class="user-details">
          <h2 class="username">FICO</h2>
          <p class="user-id">ID：FicoHu</p>
          <div class="user-stats">
            <span class="status-tag">辩论达人</span>
            <span class="friends-count">参与辩论：5场</span>
          </div>
        </div>
        <div class="qr-code">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M128 213.333333h768v85.333334H128v-85.333334z m0 256h768v85.333334H128v-85.333334z m0 256h768v85.333334H128v-85.333334z" fill="currentColor"/>
          </svg>
        </div>
      </div>
    </div>
    
    <!-- 菜单列表 -->
    <div class="menu-list">
      <div class="menu-item">
        <div class="menu-icon debate-history-icon">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M512 85.333333l118.784 241.152 265.216 38.592-192 187.136 45.269334 264.32L512 701.866667l-237.269333 124.757333 45.269333-264.32-192-187.136 265.216-38.592L512 85.333333z" fill="currentColor"/>
          </svg>
        </div>
        <div class="menu-text">辩论历史</div>
        <div class="arrow">&#8250;</div>
      </div>
      
      <div class="menu-item">
        <div class="menu-icon collection-icon">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M512 85.333333l118.784 241.152 265.216 38.592-192 187.136 45.269334 264.32L512 701.866667l-237.269333 124.757333 45.269333-264.32-192-187.136 265.216-38.592L512 85.333333z" fill="currentColor" stroke="currentColor" stroke-width="40" fill-opacity="0.2"/>
          </svg>
        </div>
        <div class="menu-text">收藏辩题</div>
        <div class="arrow">&#8250;</div>
      </div>
      
      <div class="menu-item">
        <div class="menu-icon stats-icon">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M426.666667 85.333333v426.666667h-256L554.666667 938.666667V512h256L426.666667 85.333333z" fill="currentColor"/>
          </svg>
        </div>
        <div class="menu-text">辩论数据</div>
        <div class="arrow">&#8250;</div>
      </div>
      
      <div class="menu-item">
        <div class="menu-icon video-icon">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M896 213.333333v597.333334H128V213.333333h768z m-597.333333 128v341.333334l256-170.666667-256-170.666667z" fill="currentColor"/>
          </svg>
        </div>
        <div class="menu-text">辩论视频</div>
        <div class="arrow">&#8250;</div>
      </div>
      
      <div class="menu-item">
        <div class="menu-icon team-icon">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M682.666667 426.666667c58.816 0 106.666667-47.850667 106.666666-106.666667s-47.850667-106.666667-106.666666-106.666667-106.666667 47.850667-106.666667 106.666667 47.850667 106.666667 106.666667 106.666667z m-341.333334 0c58.816 0 106.666667-47.850667 106.666667-106.666667s-47.850667-106.666667-106.666667-106.666667-106.666667 47.850667-106.666666 106.666667 47.850667 106.666667 106.666666 106.666667z m0 85.333333c-92.928 0-277.333333 46.506667-277.333333 139.392v111.274667h554.666667v-111.274667c0-92.885333-184.405333-139.392-277.333334-139.392z m341.333334 0c-11.562667 0-24.661333 0.768-38.826667 1.962667 46.549333 33.365333 79.146667 78.293333 79.146667 137.429333v111.274667h234.666666v-111.274667c0-92.885333-184.405333-139.392-277.333333-139.392z" fill="currentColor"/>
          </svg>
        </div>
        <div class="menu-text">我的团队</div>
        <div class="arrow">&#8250;</div>
      </div>
      
      <div class="menu-item">
        <div class="menu-icon badge-icon">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M512 85.333333c-164.949333 0-298.666667 133.717333-298.666667 298.666667 0 164.949333 133.717333 298.666667 298.666667 298.666667 164.949333 0 298.666667-133.717333 298.666667-298.666667 0-164.949333-133.717333-298.666667-298.666667-298.666667z m-170.666667 597.333334l-128 256 170.666667-42.666667 85.333333 128 128-341.333333h-256z m341.333334 0l128 341.333333 85.333333-128 170.666667 42.666667-128-256h-256z" fill="currentColor"/>
          </svg>
        </div>
        <div class="menu-text">成就徽章</div>
        <div class="arrow">&#8250;</div>
      </div>
      
      <div class="menu-item settings-item">
        <div class="menu-icon settings-icon">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M512 661.333333c-82.474667 0-149.333333-66.858667-149.333333-149.333333s66.858667-149.333333 149.333333-149.333333 149.333333 66.858667 149.333333 149.333333-66.858667 149.333333-149.333333 149.333333z m269.653333-115.968l42.709334 32.554667c11.946667 9.130667 15.189333 25.6 7.509333 38.826667l-40.533333 70.144c-7.68 13.226667-23.893333 18.773333-38.101334 12.8l-50.346666-20.224c-21.034667 16.213333-44.373333 29.866667-69.632 40.106666l-7.509334 53.76c-2.133333 17.066667-16.64 29.866667-33.706666 29.866667h-81.066667c-17.066667 0-31.573333-12.8-33.706667-29.866667l-7.509333-53.76c-25.258667-10.24-48.597333-23.893333-69.632-40.106666l-50.346667 20.224c-14.208 5.973333-30.421333 0.426667-38.101333-12.8l-40.533333-70.144c-7.68-13.226667-4.437333-29.696 7.509333-38.826667l42.709333-32.554667c-1.28-12.373333-2.133333-24.746667-2.133333-37.12s0.853333-24.746667 2.133333-37.12l-42.709333-32.554666c-11.946667-9.130667-15.189333-25.6-7.509333-38.826667l40.533333-70.144c7.68-13.226667 23.893333-18.773333 38.101333-12.8l50.346667 20.224c21.034667-16.213333 44.373333-29.866667 69.632-40.106667l7.509333-53.76c2.133333-17.066667 16.64-29.866667 33.706667-29.866666h81.066667c17.066667 0 31.573333 12.8 33.706666 29.866666l7.509334 53.76c25.258667 10.24 48.597333 23.893333 69.632 40.106667l50.346666-20.224c14.208-5.973333 30.421333-0.426667 38.101334 12.8l40.533333 70.144c7.68 13.226667 4.437333 29.696-7.509333 38.826667l-42.709334 32.554666c1.28 12.373333 2.133333 24.746667 2.133334 37.12s-0.853333 24.746667-2.133334 37.12z" fill="currentColor"/>
          </svg>
        </div>
        <div class="menu-text">设置</div>
        <div class="arrow">&#8250;</div>
      </div>
    </div>
    
    <!-- 底部导航栏 -->
    <BottomNavBar activePage="user-profile" />
  </div>
</template>

<script>
import BottomNavBar from '../components/BottomNavBar.vue';

export default {
  name: 'UserProfile',
  components: {
    BottomNavBar
  },
  data() {
    return {
      userData: {
        name: 'FICO',
        id: 'FicoHu',
        debateCount: 5
      }
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    navigateTo(path) {
      this.$router.push(path);
    }
  }
}
</script>

<style scoped>
.user-profile {
  width: 100%;
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  position: relative;
  display: flex;
  flex-direction: column;
  padding-bottom: 60px; /* 为底部导航栏留出空间 */
}

/* 顶部导航栏样式 */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 10;
  border-radius: 8px 8px 0 0;
  margin: 15px 15px 0;
}

.back-button {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.back-button .icon-svg {
  width: 24px;
  height: 24px;
  color: #07c160;
}

.page-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.placeholder {
  width: 30px;
}

/* 用户信息区域样式 */
.user-info-section {
  background-color: white;
  padding: 15px;
  border-bottom: 1px solid #f5f5f5;
  margin: 0 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.user-header {
  display: flex;
  align-items: center;
}

.avatar-container {
  width: 70px;
  height: 70px;
  margin-right: 15px;
}

.user-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: #07c160;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: bold;
}

.user-details {
  flex: 1;
}

.username {
  font-size: 20px;
  font-weight: 500;
  margin: 0 0 5px 0;
  color: #333;
}

.user-id {
  font-size: 14px;
  color: #888;
  margin: 0 0 8px 0;
}

.user-stats {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-tag {
  background-color: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  padding: 2px 10px;
  font-size: 12px;
  color: #666;
}

.friends-count {
  font-size: 12px;
  color: #888;
}

.qr-code {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
}

.qr-code .icon-svg {
  width: 24px;
  height: 24px;
}

/* 菜单列表样式 */
.menu-list {
  background-color: white;
  border-radius: 8px;
  margin: 15px 15px 0;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f5f5f5;
  transition: background-color 0.2s;
}

.menu-item:active {
  background-color: #f9f9f9;
}

.menu-icon {
  width: 36px;
  height: 36px;
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: #f0f5ff;
  color: #4a7bff;
}

.icon-svg {
  width: 24px;
  height: 24px;
  color: currentColor;
}

.debate-history-icon {
  color: #07c160;
}

.collection-icon {
  color: #ffaa4a;
  background-color: #fff8f0;
}

.stats-icon {
  color: #44cc77;
  background-color: #f0fff5;
}

.video-icon {
  color: #ff4a4a;
  background-color: #fff0f0;
}

.team-icon {
  color: #07c160;
  background-color: #f0fff5;
}

.badge-icon {
  color: #ffaa4a;
  background-color: #fff8f0;
}

.settings-icon {
  color: #07c160;
  background-color: #f0fff5;
}

.menu-text {
  flex: 1;
  font-size: 14px;
  color: #333;
  font-weight: 400;
}

.arrow {
  color: #ccc;
  font-size: 20px;
}

.settings-item {
  margin-top: 10px;
  border-top: 10px solid #f5f5f5;
}

/* 底部导航栏样式 */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  background-color: #ffffff;
  border-top: 1px solid #e0e0e0;
  padding: 10px 0;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 25%;
  cursor: pointer;
}

.nav-icon {
  font-size: 24px;
  color: #999;
  margin-bottom: 4px;
  transition: color 0.2s;
}

.nav-text {
  font-size: 12px;
  color: #999;
  transition: color 0.2s;
}

.nav-item.active .nav-icon,
.nav-item.active .nav-text {
  color: #07c160;
  font-weight: 500;
}

.nav-item:hover .nav-icon,
.nav-item:hover .nav-text {
  color: #07c160;
}
</style>
