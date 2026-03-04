<template>
  <div class="hot-debates-container">
    <header class="header">
      <div class="placeholder"></div>
      <h1>热点话题</h1>
      <div class="add-button" @click="addNewDebate">
        <span>+</span>
      </div>
    </header>
    
    <main class="main-content">
  <div v-if="loading" class="loading-container">
    <div class="loading-spinner"></div>
    <p>加载中...</p>
  </div>
  <div v-else-if="debates.length === 0" class="empty-container">
    <p>暂无辩论数据</p>
  </div>
  <div v-else class="debate-list">
    <div v-for="debate in debates" :key="debate.id" class="debate-item">
      <div class="debate-content" @click="viewDebate(debate)">
        <h2 class="debate-title">{{ debate.title }}</h2>
        <div class="debate-source">{{ debate.source }}</div>
      </div>
      <div class="play-button" @click.stop="playDebate(debate)">
        <div class="play-icon">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M341.333333 213.333333v597.333334l469.333334-298.666667z" fill="currentColor"/>
          </svg>
        </div>
      </div>
    </div>
  </div>
</main>
    
    <MiniPlayer 
      ref="miniPlayer"
      :isVisible="showMiniPlayer" 
      :title="currentDebate.title" 
      :subtitle="currentDebate.source"
      :debateData="currentDebate"
      @close="closeMiniPlayer"
      @toggle-play="togglePlay"
    />
    
    <BottomNavBar activePage="hot-debates" />
  </div>
</template>

<script>
import BottomNavBar from '../components/BottomNavBar.vue';
import MiniPlayer from '../components/MiniPlayer.vue';
import axios from 'axios';
import apiConfig from '../config/api.js';

export default {
  name: 'HotDebatesView',
  components: {
    BottomNavBar,
    MiniPlayer
  },
  data() {
  return {
    showMiniPlayer: false,
    currentDebate: {},
    debates: [],
    loading: false,
    page: 1,
    per_page: 10,
    total: 0
  }
},
created() {
  this.fetchDebates();
},
  methods: {
    fetchDebates() {
  this.loading = true;
  axios.get(`${apiConfig.getUrl(apiConfig.endpoints.debates)}?page=${this.page}&per_page=${this.per_page}`)
    .then(response => {
      if (response.data.code === 200) {
        this.debates = response.data.data.debates.map(debate => ({
          id: debate.id,
          title: debate.topic,
          source: new URL(debate.url).hostname,
          hasVideo: true,
          originalData: debate
        }));
        this.total = response.data.data.total;
      } else {
        console.error('获取辩论列表失败:', response.data.message);
      }
    })
    .catch(error => {
      console.error('获取辩论列表出错:', error);
    })
    .finally(() => {
      this.loading = false;
    });
},
viewDebate(debate) {
  console.log('查看辩论:', debate);
  // 跳转到辩论详情页面，并传递辩论ID
  this.$router.push(`/debate?id=${debate.id}`);
},
    addNewDebate() {
      // 跳转到添加辩论话题页面
      this.$router.push('/add-debate-topic');
    },
    goToDiscover() {
      // 跳转到发现页面
      this.$router.push('/discover');
    },
    goToProfile() {
      // 跳转到个人中心页面
      this.$router.push('/user-profile');
    },
    
    playDebate(debate) {
      // 设置当前辩论数据
      this.currentDebate = debate;
      // 显示迷你播放器
      this.showMiniPlayer = true;
      console.log('播放辩论:', debate.title, '音频数据:', debate.originalData?.rounds);
      
      // 使用$nextTick确保迷你播放器已经渲染完成
      this.$nextTick(() => {
        // 通过引用调用迷你播放器的播放方法
        if (this.$refs.miniPlayer) {
          this.$refs.miniPlayer.startPlayingImmediately();
        }
      });
    },
    
    closeMiniPlayer() {
      this.showMiniPlayer = false;
    },
    
    togglePlay(isPlaying) {
      console.log('播放状态:', isPlaying ? '播放中' : '已暂停');
      // 可以在这里添加播放状态的其他处理逻辑
    }
  }
}
</script>

<style scoped>
.hot-debates-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 60px; /* 为底部导航栏留出空间 */
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
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

.placeholder {
  width: 40px;
}

.add-button {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 22px;
  color: #07c160;
  border: 1px solid #07c160;
  border-radius: 50%;
  background-color: transparent;
  transition: all 0.2s ease;
}

.add-button:hover {
  background-color: #07c160;
  color: white;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 15px;
}

.debate-list {
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.debate-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 15px;
  border-bottom: 1px solid #f5f5f5;
  background-color: white;
  cursor: pointer;
}

.debate-content {
  flex: 1;
  margin-right: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.debate-title {
  font-size: 14px;
  font-weight: 400;
  margin-bottom: 5px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.debate-source {
  font-size: 12px;
  color: #999;
  display: flex;
  align-items: center;
}

.play-button {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 12px;
}

.play-icon {
  width: 40px;
  height: 40px;
  background-color: #07c160;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(7, 193, 96, 0.3);
}

.icon-svg {
  width: 20px;
  height: 20px;
  color: white;
}

.footer {
  display: flex;
  justify-content: space-around;
  padding: 12px 0;
  background-color: white;
  border-top: 1px solid #eee;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 12px;
  cursor: pointer;
}

.nav-item .icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.nav-item.active {
  color: #07c160;
}
.loading-container, .empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #999;
  background-color: white;
  border-radius: 8px;
  margin-top: 15px;
}

.loading-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #07c160;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
