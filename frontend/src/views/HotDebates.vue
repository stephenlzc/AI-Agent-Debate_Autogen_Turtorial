<template>
  <div class="hot-debates-container">
    <header class="header">
      <div class="placeholder"></div>
      <h1>热点辩论</h1>
      <div class="add-button" @click="addNewDebate">
        <span>+</span>
      </div>
    </header>
    
    <main class="main-content">
      <div class="debate-list">
        <div v-for="(debate, index) in debates" :key="index" class="debate-item">
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
      :isVisible="showMiniPlayer" 
      :title="currentDebate.title" 
      :subtitle="currentDebate.source"
      @close="closeMiniPlayer"
      @toggle-play="togglePlay"
    />
    
    <BottomNavBar activePage="hot-debates" />
  </div>
</template>

<script>
import BottomNavBar from '../components/BottomNavBar.vue';
import MiniPlayer from '../components/MiniPlayer.vue';

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
      debates: [
        {
          id: 1,
          title: 'P人也要时间管理? 2024的实践小结',
          source: 'sspai.com',
          image: 'https://via.placeholder.com/80',
          hasVideo: true
        },
        {
          id: 2,
          title: 'CES成芯片巨头"斗秀场"，新品巅峰对决',
          source: '36kr.com',
          image: 'https://via.placeholder.com/80',
          hasVideo: true
        },
        {
          id: 3,
          title: '中国人为何唯爱孙悟空?',
          source: 'www.thepaper.cn',
          image: 'https://via.placeholder.com/80',
          hasVideo: true
        },
        {
          id: 4,
          title: '段永平浙大见面会万字实录：最重要的不是勤奋，而是做对事情',
          source: 'www.thepaper.cn',
          image: 'https://via.placeholder.com/80',
          hasVideo: true
        },
        {
          id: 5,
          title: '人工智能是否会取代人类工作？',
          source: 'debate.ai',
          image: 'https://via.placeholder.com/80',
          hasVideo: false
        },
        {
          id: 6,
          title: '网络教育能否替代传统教育？',
          source: 'debate.ai',
          image: 'https://via.placeholder.com/80',
          hasVideo: false
        },
        {
          id: 7,
          title: '是否应该推行全民基本收入？',
          source: 'debate.ai',
          image: 'https://via.placeholder.com/80',
          hasVideo: true
        },
        {
          id: 8,
          title: '大城市生活与小城市生活哪个更好？',
          source: 'debate.ai',
          image: 'https://via.placeholder.com/80',
          hasVideo: false
        }
      ]
    }
  },
  methods: {
    viewDebate(debate) {
      console.log('查看辩论:', debate);
      // 这里应该跳转到辩论详情页面
      this.$router.push('/debate');
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
      this.currentDebate = debate;
      this.showMiniPlayer = true;
    },
    
    closeMiniPlayer() {
      this.showMiniPlayer = false;
    },
    
    togglePlay(isPlaying) {
      console.log('播放状态:', isPlaying ? '播放中' : '已暂停');
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
</style>
