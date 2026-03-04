<template>
  <div class="add-topic-container">
    <header class="header">
      <div class="back-button" @click="goBack">
        <span>←</span>
      </div>
      <div class="logo-title">
        <img src="../assets/images/debate-logo.svg" alt="辩论系统" class="debate-logo">
        <h1>添加话题</h1>
      </div>
      <div class="placeholder"></div>
    </header>
    
    <main class="main-content">
      <div class="input-section" :class="{ 'minimized': isLoading || generatedTopics.length > 0 || newsOutline }">
        <textarea 
          class="topic-input" 
          v-model="topicInput" 
          placeholder="请输入新闻网页地址或文字内容"
          :disabled="isLoading"
          :rows="(isLoading || generatedTopics.length > 0 || newsOutline) ? 1 : 4"
        ></textarea>
        <button class="generate-button" @click="generateTopic" :disabled="isLoading">
          <span v-if="!isLoading">生成辩论主题</span>
          <span v-else class="loading-spinner">⭯</span>
        </button>
      </div>
      
      <div class="loading-message" v-if="isLoading">
        <div class="loading-text">正在分析内容并生成辩论主题...</div>
      </div>
      
      <div class="news-outline" v-if="newsOutline">
        <div class="section-title">新闻大纲</div>
        <div class="news-content">{{ newsOutline }}</div>
      </div>
      
      <div class="generated-topics" v-if="generatedTopics.length > 0">
        <div class="section-title">辩论主题</div>
        <div class="topic-list">
          <div 
            v-for="topic in generatedTopics" 
            :key="topic.id" 
            class="topic-item"
            @click="goToDebateDetail(topic)"
          >
            <div class="topic-title">{{ topic.title }}</div>
            <div class="topic-description" v-if="topic.description">{{ topic.description }}</div>
            <div class="topic-arrow">→</div>
          </div>
        </div>
      </div>
      

    </main>
    
    <div class="button-footer">
      <button class="next-button" :disabled="!selectedTopic" @click="goToNextStep">
        下一步
      </button>
    </div>
    
    <!-- 底部导航栏 -->
    <BottomNavBar activePage="add-debate-topic" />
  </div>
</template>

<script>
import BottomNavBar from '../components/BottomNavBar.vue';

export default {
  name: 'AddDebateTopicView',
  components: {
    BottomNavBar
  },
  data() {
    return {
      topicInput: '',
      selectedTopic: null,
      generatedTopics: [],
      newsOutline: '',
      isLoading: false
    }
  },
  methods: {
    goBack() {
      this.$router.push('/hot-debates');
    },
    navigateTo(path) {
      this.$router.push(path);
    },
    generateTopic() {
      if (!this.topicInput.trim()) {
        alert('请输入URL或文字内容');
        return;
      }
      
      this.isLoading = true;
      
      // 模拟生成新闻大纲和辩论主题
      console.log('生成辩论主题:', this.topicInput);
      
      // 这里应该调用后端API解析URL或文字内容
      // 这里只是模拟生成结果
      setTimeout(() => {
        // 生成新闻大纲
        if (this.topicInput.startsWith('http')) {
          this.newsOutline = '根据您提供的URL内容，我们提取到以下新闻大纲：\n\n标题：人工智能在教育领域的应用\n\n摘要：本文描述了人工智能如何在教育领域中发挥作用，包括个性化学习、自动评分系统、智能学习助手等方面。文章讨论了AI技术如何提高教学效率，以及可能带来的挑战和风险。';
        } else {
          this.newsOutline = '根据您提供的文字内容："' + this.topicInput + '"，我们生成以下大纲：\n\n核心观点：该话题涉及到现代技术与传统方式的冲突与融合。\n\n相关背景：当前社会快速发展，技术革新与传统价值观念的碰撞日益明显。';
        }
        
        // 生成辩论主题
        this.generatedTopics = [
          {
            id: 101,
            title: '人工智能是否应该在教育中取代传统教师角色？',
            description: ''
          },
          {
            id: 102,
            title: '数字化学习是否会削弱学生的社交能力？',
            description: ''
          },
          {
            id: 103,
            title: '技术进步是否会加大教育资源不平等？',
            description: ''
          }
        ];
        
        this.isLoading = false;
      }, 1500);
    },
    goToDebateDetail(topic) {
      // 将选中的话题存储到本地，以便详情页面使用
      localStorage.setItem('selectedDebateTopic', JSON.stringify(topic));
      
      // 跳转到辩论详情页面
      this.$router.push('/add-debate-detail');
    }
  }
}
</script>

<style scoped>
.add-topic-container {
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

.logo-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.debate-logo {
  width: 24px;
  height: 24px;
}

.header h1 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
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
  padding: 15px;
  overflow-y: auto;
  margin: 0 15px;
}

.input-section {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.input-section.minimized {
  transform: scale(0.92);
  opacity: 0.85;
  margin-bottom: 8px;
  max-height: 80px;
}

.topic-input {
  width: 100%;
  padding: 12px 15px;
  border: none;
  outline: none;
  font-size: 14px;
  resize: none;
  line-height: 1.5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.generate-button {
  background-color: #07c160;
  color: white;
  border: none;
  border-radius: 0 0 8px 8px;
  padding: 12px 0;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.3s ease;
  margin-top: 1px;
}

.minimized .generate-button {
  padding: 6px 0;
  font-size: 13px;
}

.generate-button:hover {
  background-color: #06ad56;
  color: white;
}

.generate-button:disabled {
  background-color: #ccc;
  color: white;
  cursor: not-allowed;
}

.generate-button:disabled:hover {
  background-color: #ccc;
  color: white;
}

.loading-spinner {
  display: inline-block;
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-message {
  background-color: rgba(7, 193, 96, 0.1);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 15px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.loading-text {
  font-size: 14px;
  color: #07c160;
  text-align: center;
}

.section-title {
  font-size: 14px;
  font-weight: 500;
  margin: 15px 0 10px;
  color: #333;
}

.news-outline, .generated-topics, .popular-topics {
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease;
}

.topic-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.topic-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  padding: 12px 15px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  transition: all 0.2s;
}

.topic-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.topic-title {
  flex: 1;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.4;
}

.topic-description {
  flex: 1;
  font-size: 14px;
  color: #666;
  margin-top: 4px;
  line-height: 1.4;
}

.topic-arrow {
  font-size: 18px;
  color: #07c160;
  margin-left: 10px;
}

.button-footer {
  padding: 15px;
  background-color: white;
  border-top: 1px solid #f5f5f5;
  border-radius: 0 0 8px 8px;
  margin: 0 15px;
}

.next-button {
  width: 100%;
  padding: 12px 0;
  background-color: #07c160;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
}

.next-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
/* 底部导航栏样式 */
.footer {
  display: flex;
  justify-content: space-around;
  padding: 12px 0;
  background-color: white;
  border-top: 1px solid #eee;
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
