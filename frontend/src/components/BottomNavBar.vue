<template>
  <footer class="footer">
    <div 
      class="nav-item" 
      :class="{ active: activePage === 'hot-debates' }" 
      @click="navigateTo('/hot-debates')"
    >
      <div class="icon">
        <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
          <path d="M512 85.333333c-282.453333 0-384 142.933333-384 384 0 136.533333 64 256 170.666667 315.733334v72.533333c0 25.6 17.066667 42.666667 42.666666 42.666667h341.333334c25.6 0 42.666667-17.066667 42.666666-42.666667v-72.533333c106.666667-59.733333 170.666667-179.2 170.666667-315.733334 0-241.066667-101.546667-384-384-384z" fill="currentColor"/>
        </svg>
      </div>
      <div class="nav-text">热点</div>
    </div>
    <div 
      class="nav-item" 
      :class="{ active: activePage === 'discover' }" 
      @click="navigateTo('/discover')"
    >
      <div class="icon">
        <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
          <path d="M768 298.666667c0-141.226667-114.773333-256-256-256s-256 114.773333-256 256c0 141.226667 114.773333 256 256 256s256-114.773333 256-256zM426.666667 640c-211.84 0-384 172.16-384 384h938.666666c0-211.84-172.16-384-384-384h-170.666666z" fill="currentColor"/>
        </svg>
      </div>
      <div class="nav-text">发现</div>
    </div>
    <div 
      class="nav-item" 
      :class="{ active: activePage === 'debate' }" 
      @click="navigateTo('/debate')"
    >
      <div class="icon">
        <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
          <path d="M512 85.333333c-235.648 0-426.666667 191.018667-426.666667 426.666667s191.018667 426.666667 426.666667 426.666667 426.666667-191.018667 426.666667-426.666667-191.018667-426.666667-426.666667-426.666667zM320 426.666667c0-58.816 47.850667-106.666667 106.666667-106.666667s106.666667 47.850667 106.666666 106.666667-47.850667 106.666667-106.666666 106.666666-106.666667-47.850667-106.666667-106.666666z m384 170.666666c0 58.816-47.850667 106.666667-106.666667 106.666667s-106.666667-47.850667-106.666666-106.666667 47.850667-106.666667 106.666666-106.666666 106.666667 47.850667 106.666667 106.666666z" fill="currentColor"/>
        </svg>
      </div>
      <div class="nav-text">辩论</div>
    </div>
    <div 
      class="nav-item" 
      :class="{ active: activePage === 'user-profile' }" 
      @click="navigateTo('/user-profile')"
    >
      <div class="icon">
        <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
          <path d="M512 85.333333c-235.648 0-426.666667 191.018667-426.666667 426.666667s191.018667 426.666667 426.666667 426.666667 426.666667-191.018667 426.666667-426.666667-191.018667-426.666667-426.666667-426.666667zM384 384c0-70.688 57.312-128 128-128s128 57.312 128 128-57.312 128-128 128-128-57.312-128-128zM768 725.333333H256c0-141.376 114.624-256 256-256s256 114.624 256 256z" fill="currentColor"/>
        </svg>
      </div>
      <div class="nav-text">我的</div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'BottomNavBar',
  props: {
    activePage: {
      type: String,
      required: true,
      validator: function(value) {
        return ['hot-debates', 'discover', 'debate', 'user-profile'].includes(value);
      }
    }
  },
  methods: {
    navigateTo(path) {
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    }
  }
}
</script>

<style scoped>
.footer {
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  background-color: #f7f7f7;
  border-top: 1px solid #e0e0e0;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 10;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 4px 0;
  width: 25%;
}

.icon {
  height: 24px;
  margin-bottom: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-svg {
  width: 24px;
  height: 24px;
}

.nav-text {
  font-size: 11px;
  color: #333;
}

.nav-item.active {
  color: #07c160;
}

.nav-item.active .nav-text {
  color: #07c160;
}
</style>
