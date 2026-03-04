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
       <!-- 辩论海报 -->
       <div class="debate-poster-container" v-if="selectedTopic && selectedTopic.originalData && selectedTopic.originalData.poster">
        <div class="section-title">辩论海报</div>
        <div class="debate-poster">
          <img :src="selectedTopic.originalData.poster" alt="辩论海报" class="poster-image" />
        </div>
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
            <div class="topic-content">
              <div class="topic-title-row">
                <div class="topic-title">{{ topic.title }}</div>
                <div class="topic-arrow">→</div>
              </div>
              <div class="topic-stances" v-if="topic.pros || topic.cons">
                <div class="stance-item pro-stance">
                  <div class="stance-label">正方：</div>
                  <div class="stance-content">{{ topic.pros }}</div>
                </div>
                <div class="stance-item con-stance">
                  <div class="stance-label">反方：</div>
                  <div class="stance-content">{{ topic.cons }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
     
      

    </main>
    
    <!-- <div class="button-footer">
      <button class="next-button" :disabled="!selectedTopic" @click="goToNextStep">
        下一步
      </button>
    </div> -->
    
    <!-- 底部导航栏 -->
    <BottomNavBar activePage="hot-debates" />
  </div>
</template>

<script>
import BottomNavBar from '../components/BottomNavBar.vue';
import axios from 'axios';
import apiConfig from '../config/api.js';

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
      
      // 检查输入是否是URL
      if (!this.topicInput.startsWith('http')) {
        alert('请输入有效的网页URL，必须以http或https开头');
        return;
      }
      
      this.isLoading = true;
      this.generatedTopics = [];
      this.newsOutline = '';
      
      // 调用后端API生成辩论主题
      console.log('调用API生成辩论主题:', this.topicInput);
      
      // 发送请求到/api/generate_debate接口
      axios.post(`${apiConfig.baseURL}/api/generate_debate`, {
        url: this.topicInput
      })
      .then(response => {
        console.log('API返回数据:', response.data);
        
        // 处理返回的数据
        if (response.data) {
          // 提取新闻大纲
          const topic = response.data.topic;
          const outline = response.data.outline || '';
          const proArgument = response.data.pros.argument;
          const conArgument = response.data.cons.argument;
          
          // 显示新闻大纲，直接使用API返回的outline字段
          this.newsOutline = outline;
          
          // 生成辩论主题
          this.generatedTopics = [
            {
              id: response.data.id,
              title: response.data.topic,
              description: `正方：${proArgument}，反方：${conArgument}`,
              pros: proArgument,
              cons: conArgument,
              originalData: response.data
            }
          ];
          
          // 自动选择生成的主题
          this.selectedTopic = this.generatedTopics[0];
        } else {
          alert('生成辩论主题失败，请重试');
        }
      })
      .catch(error => {
        console.error('API请求错误:', error);
        alert('生成辩论主题时出错: ' + (error.response?.data?.error || error.message || '未知错误'));
      })
      .finally(() => {
        this.isLoading = false;
      });
    },
    goToDebateDetail(topic) {
      // 选中主题
      this.selectedTopic = topic;
      
      // 跳转到辩论详情页面
      this.$router.push({
        path: '/debate',
        query: { id: topic.id }
      });
    },
    
    goToNextStep() {
      if (this.selectedTopic) {
        this.$router.push({
          path: '/debate',
          query: { id: this.selectedTopic.id }
        });
      }
    },
    
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

.topic-content {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.topic-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.topic-title {
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;
  color: #333;
  flex: 1;
}

.topic-description {
  flex: 1;
  font-size: 14px;
  color: #666;
  margin-top: 4px;
  line-height: 1.4;
}

.topic-stances {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
  margin-bottom: 4px;
}

.stance-item {
  display: flex;
  align-items: flex-start;
  line-height: 1.4;
}

.stance-label {
  font-size: 13px;
  font-weight: 500;
  margin-right: 6px;
  white-space: nowrap;
}

.stance-content {
  font-size: 13px;
  color: #444;
  flex: 1;
}

.pro-stance .stance-label {
  color: #1976d2;
}

.con-stance .stance-label {
  color: #d32f2f;
}

.topic-arrow {
  font-size: 18px;
  color: #07c160;
  margin-left: 10px;
}

/* 辩论海报样式 */
.debate-poster-container {
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease;
}

.debate-poster {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
}

.poster-image {
  width: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 4px;
}

.poster-placeholder {
  width: 100%;
  height: 200px;
  background-color: #f5f5f5;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  text-align: center;
}

.poster-topic {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 15px;
  color: #333;
}

.poster-vs {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 10px;
}

.blue-team-name {
  color: #1976d2;
  font-weight: 500;
}

.vs-text {
  font-size: 18px;
  font-weight: bold;
  color: #666;
}

.red-team-name {
  color: #d32f2f;
  font-weight: 500;
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
