<template>
  <div class="debate-container">
    <!-- 辩论主题 -->
    <div class="debate-header">
      <div class="debate-poster">
        <!-- 如果有海报图片则显示 -->
        <div v-if="debateInfo.poster" class="poster-image-container">
          <img :src="debateInfo.poster" alt="辩论海报" class="poster-image">
        </div>
        <!-- 没有海报图片时显示默认设计 -->
        <div v-else class="poster-content">
          <h1 class="debate-title">辩题</h1>
          <div class="debate-topic">{{ debateInfo.topic.title }}</div>
          
          <div class="poster-vs">
            <div class="poster-team blue-side">
              <div class="poster-stance">{{ debateInfo.blueStance }}</div>
              <div class="poster-player">{{ debateInfo.bluePlayerType }}</div>
            </div>
            <div class="vs-circle">VS</div>
            <div class="poster-team red-side">
              <div class="poster-stance">{{ debateInfo.redStance }}</div>
              <div class="poster-player">{{ debateInfo.redPlayerType }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 正反方信息简洁展示 -->
      <div class="stance-summary">
        <div class="stance-item blue-stance">
          <span class="stance-label">正方：</span>
          <span class="stance-text">{{ debateInfo.blueStance }}</span>
        </div>
        <div class="stance-item red-stance">
          <span class="stance-label">反方</span>
          <span class="stance-text">{{ debateInfo.redStance }}</span>
        </div>
      </div>
    </div>
    
    <!-- 辩论内容 -->
    <div class="debate-content">
      <div class="debate-status">
        <span v-if="debateStarted">辩论中</span>
        <span v-else>辩论准备就绪</span>
        <!-- 控制按钮区域 -->
        <div class="controls">
          <!-- 开始按钮 -->
          <button @click="startDebate" class="start-btn" v-if="!debateStarted">
            <i class="start-icon">&#9658;</i> 开始辩论
          </button>
          <!-- 音频控制按钮 -->
          <div class="audio-controls" v-if="debateStarted">
            <button @click="toggleAudio" class="audio-btn" :class="{'muted': isMuted}">
              <i class="audio-icon" v-if="isMuted">&#128263;</i>
              <i class="audio-icon" v-else>&#128266;</i>
            </button>
          </div>
        </div>
      </div>
      
      <div class="chat-container" ref="chatContainer">
        <!-- 动态显示辩论内容 -->
        <template v-for="(message, index) in messages.slice(0, currentRound)" :key="index">
          <!-- 蓝队消息 -->
          <div class="chat-message blue-message" v-if="message.type === 'blue'" v-show="message.displayContent.length > 0">
            <div class="avatar blue-avatar">蓝</div>
            <div class="message-content">
              <div class="message-bubble">
                {{ message.displayContent }}
              </div>
            </div>
          </div>
          
          <!-- 红队消息 -->
          <div class="chat-message red-message" v-if="message.type === 'red'" v-show="message.displayContent.length > 0">
            <div class="message-content">
              <div class="message-bubble">
                {{ message.displayContent }}
              </div>
            </div>
            <div class="avatar red-avatar">红</div>
          </div>
          
          <!-- 主持人消息 -->
          <div class="chat-message host-message" v-if="message.type === 'host'" v-show="message.displayContent.length > 0">
            <div class="avatar host-avatar">主</div>
            <div class="message-content">
              <div class="message-bubble">
                {{ message.displayContent }}
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
    
    <!-- 底部操作栏 -->
    <div class="debate-footer">
      <button class="back-button" @click="goBack">返回</button>
      <button class="share-button" @click="shareDebate">分享</button>
    </div>
    
    <!-- 底部导航栏 -->
    <BottomNavBar activePage="debate" />
  </div>
</template>

<script>
import BottomNavBar from '../components/BottomNavBar.vue';
import axios from 'axios';
import apiConfig from '../config/api';

export default {
  name: 'DebateView',
  components: {
    BottomNavBar
  },
  data() {
    return {
      debateInfo: {
        topic: { id: 0, title: '结婚还是做单身狗', description: '' },
        selectedTeam: 'blue',
        blueStance: '结婚',
        redStance: '单身狗',
        bluePlayerType: '保守型',
        redPlayerType: '激进型',
        useVoice: true
      },
      debateRounds: 15,
      currentRound: 4,
      messages: [
        {
          type: 'host',
          content: '各位观众朋友们大家好，欢迎来到本次辩论。今天的辩题是《结婚还是做单身狗》。蓝队将支持「结婚」，红队将支持「单身狗」。辩论共计15轮，现在开始第一轮辩论。',
          displayContent: '',
          isTyping: false,
          typingIndex: 0
        },
        {
          type: 'blue',
          content: '家庭温暖和经济稳定性: 结婚后可以享受家庭的温暖，有人陪伴和照顾，尤其是在遇到困难时有人分担。',
          displayContent: '',
          isTyping: false,
          typingIndex: 0
        },
        {
          type: 'red',
          content: '自由和独立: 单身生活最大的优点是自由，可以自由安排自己的时间和生活，无需考虑他人的感受和需求。经济上也更自由，可以随心所欲地花钱而不用担心另一半的意见',
          displayContent: '',
          isTyping: false,
          typingIndex: 0
        },
        {
          type: 'host',
          content: '第一轮辩论结束，双方观点鲜明。现在进入第二轮辩论，请双方针对对方观点进行深入辩论。',
          displayContent: '',
          isTyping: false,
          typingIndex: 0
        },
        {
          type: 'blue',
          content: '对于红队提到的自由问题，我认为婚姻并不会完全剪除个人自由。婚姻是两个人共同成长的过程，可以通过沟通和相互尊重来保持各自的空间和自由。',
          displayContent: '',
          isTyping: false,
          typingIndex: 0
        },
        {
          type: 'red',
          content: '蓝队提到的家庭温暖确实存在，但这种温暖也可以从朋友和家人关系中获得。而且，婚姻生活中的矛盾和压力可能会让这种温暖变成负担，单身生活可以避免这些问题。',
          displayContent: '',
          isTyping: false,
          typingIndex: 0
        }
      ],
      typingSpeed: 200, // 打字速度，毫秒/字符（比原来慢2倍）
      activeMessageIndex: 0, // 当前正在打字的消息索引
      audioPlayer: null, // 音频播放器
      isMuted: false, // 是否静音
      audioInitialized: false, // 音频是否已初始化
      audioFinished: true, // 音频是否播放完成
      textFinished: true, // 文字是否显示完成
      debateStarted: false // 辩论是否已开始
    }
  },
  created() {
    // 从本地存储获取辩论信息
    const savedDebateInfo = localStorage.getItem('debateInfo');
    if (savedDebateInfo) {
      this.debateInfo = JSON.parse(savedDebateInfo);
    }
    
    // 初始化辩论内容
    this.initializeDebate();
    
    // 不自动启动打字机效果，等待用户点击开始按钮
  },
  methods: {
    // 开始辩论
    startDebate() {
      this.debateStarted = true;
      // 启动打字机效果
      this.startTypingEffect();
    },
    initializeDebate() {
      // 先从本地存储获取辩论信息
      const savedDebateInfo = localStorage.getItem('debateInfo');
      if (savedDebateInfo) {
        this.debateInfo = JSON.parse(savedDebateInfo);
      } else {
        // 如果没有保存的辩论信息，使用默认值
        this.debateInfo = {
          topic: { id: 0, title: '结婚还是做单身狗', description: '' },
          selectedTeam: 'blue',
          blueStance: '结婚',
          redStance: '单身狗',
          bluePlayerType: '保守型',
          redPlayerType: '激进型',
          useVoice: '是'
        };
      }
      
      // 从 API 获取辩论数据
      this.fetchDebateData();
    },
    
    // 从 API 获取辩论数据
    async fetchDebateData() {
      try {
        // 从URL获取辩论ID
        const urlParams = new URLSearchParams(window.location.search);
        const debateId = urlParams.get('id');
        
        if (!debateId) {
          console.error('未找到辩论ID');
          return;
        }
        
        // 请求辩论详情数据
        const response = await axios.get(`${apiConfig.getUrl(apiConfig.endpoints.debateDetail)}?debate_id=${debateId}`);
        
        if (response.data && response.data.code === 200) {
          const debateData = response.data.data;
          
          // 更新辩论信息
          this.debateInfo = {
            topic: { id: debateData.id, title: debateData.topic, description: '' },
            selectedTeam: 'blue',
            blueStance: debateData.pros.argument,
            redStance: debateData.cons.argument,
            bluePlayerType: debateData.pros.team,
            redPlayerType: debateData.cons.team,
            useVoice: true,
            poster: debateData.poster || null // 添加海报字段
          };
          
          // 如果API返回了rounds数据，则将其转换为消息列表
          if (debateData.rounds && debateData.rounds.length > 0) {
            this.messages = debateData.rounds.map(round => ({
              type: this.mapRoundTypeToMessageType(round.type),
              content: round.msg,
              audioPath: round.path,
              displayContent: '',
              isTyping: false,
              typingIndex: 0
            }));
            
            // 更新当前轮次为消息总数
            this.currentRound = this.messages.length;
            this.debateRounds = Math.max(this.debateRounds, this.messages.length);
          }
          
          // 保存辩论信息到本地存储
          localStorage.setItem('debateInfo', JSON.stringify(this.debateInfo));
          
          console.log('辩论数据获取成功', debateData);
        }
      } catch (error) {
        console.error('获取辩论数据失败:', error);
        // 如果获取数据失败，使用默认数据
        if (!this.messages || this.messages.length === 0) {
          // 使用data中预定义的messages数组
          // 注意：这里不需要重新赋值，因为data中已经定义了默认值
        }
      }
    },
    
    // 启动打字机效果
    startTypingEffect() {
      // 重置所有消息的显示状态
      this.messages.forEach(message => {
        message.displayContent = '';
        message.isTyping = false;
        message.typingIndex = 0;
      });
      
      // 开始第一条消息的打字效果
      this.activeMessageIndex = 0;
      this.typeNextMessage();
    },
    
    // 处理下一条消息的打字效果
    typeNextMessage() {
      // 如果所有消息都已经处理完毕，则返回
      if (this.activeMessageIndex >= Math.min(this.currentRound, this.messages.length)) {
        // 所有消息处理完毕，停止音频播放
        this.stopAudio();
        return;
      }
      
      // 重置状态
      this.audioFinished = false;
      this.textFinished = false;
      
      // 获取当前消息
      const message = this.messages[this.activeMessageIndex];
      message.isTyping = true;
      
      // 如果有音频路径，则播放音频
      if (message.audioPath && !this.isMuted) {
        this.playAudio(message.audioPath);
      } else {
        // 如果没有音频或者静音，标记音频已完成
        this.audioFinished = true;
      }
      
      // 开始打字效果
      this.typeMessage(message);
    },
    
    // 实现打字机效果
    typeMessage(message) {
      // 如果所有字符都已经显示完毕
      if (message.typingIndex >= message.content.length) {
        message.isTyping = false;
        
        // 滚动到消息底部
        this.scrollToLatestMessage();
        
        // 标记文字已完成
        this.textFinished = true;
        
        // 检查是否可以进行下一条消息
        this.checkNextMessage();
        
        return;
      }
      
      // 每次添加一个字符
      message.displayContent += message.content.charAt(message.typingIndex);
      message.typingIndex++;
      
      // 每添加几个字符滚动一次，使页面滚动更平滑
      if (message.typingIndex % 5 === 0) {
        this.scrollToLatestMessage();
      }
      
      // 设置下一个字符的延迟
      setTimeout(() => {
        this.typeMessage(message);
      }, this.typingSpeed);
    },
    
    // 检查是否可以进行下一条消息
    checkNextMessage() {
      // 如果文字和音频都已完成，或者静音状态下文字已完成
      if ((this.textFinished && this.audioFinished) || (this.textFinished && this.isMuted)) {
        // 延迟一段时间后显示下一条消息
        setTimeout(() => {
          // 当前消息播放完毕，准备下一条消息
          this.stopAudio(); // 停止当前音频
          this.activeMessageIndex++;
          this.typeNextMessage();
        }, 500);
      }
    },
    
    // 滚动到最新消息
    scrollToLatestMessage() {
      this.$nextTick(() => {
        const chatContainer = this.$refs.chatContainer;
        if (chatContainer) {
          // 查找所有消息元素
          const messageElements = chatContainer.querySelectorAll('.chat-message');
          // 过滤出实际可见的消息（即有内容的消息）
          const visibleMessages = Array.from(messageElements).filter(el => {
            // 检查是否有显示内容
            const content = el.querySelector('.message-bubble');
            return content && content.textContent.trim().length > 0;
          });
          
          if (visibleMessages.length > 0) {
            // 滚动到最后一条可见消息
            const latestMessage = visibleMessages[visibleMessages.length - 1];
            latestMessage.scrollIntoView({ behavior: 'smooth', block: 'end' });
          } else {
            // 如果没有找到消息元素，直接滚动到容器底部
            chatContainer.scrollTop = chatContainer.scrollHeight;
          }
        }
      });
    },
    
    // 播放音频
    playAudio(audioPath) {
      // 如果静音，则不播放音频
      if (this.isMuted) {
        this.audioFinished = true;
        return;
      }
      
      // 重置音频完成状态
      this.audioFinished = false;
      
      // 停止之前的音频
      this.stopAudio();
      
      // 处理音频路径，确保使用正确的路径
      // 如果路径已经是完整URL，则直接使用
      // 否则，使用后端服务器的URL来访问音频文件
      let fullPath;
      if (audioPath.startsWith('http')) {
        // 已经是HTTP路径，直接使用
        fullPath = audioPath;
      } else {
        // 使用API服务器的URL
        const apiBaseUrl = apiConfig.baseURL; // 直接使用导入的apiConfig
        
        if (audioPath.includes('audio_output/')) {
          // 如果已经包含audio_output路径
          fullPath = `${apiBaseUrl}/${audioPath}`;
        } else {
          // 如果只是文件名，构建完整路径
          const fileName = audioPath.split('/').pop();
          fullPath = `${apiBaseUrl}/audio_output/${fileName}`;
        }
      }
      
      console.log('播放音频:', fullPath);
      
      // 创建新的音频对象
      this.audioPlayer = new Audio(fullPath);
      
      // 设置音频属性
      this.audioPlayer.volume = 1.0;
      // 设置播放速率为2倍速
      this.audioPlayer.playbackRate = 1.5;
      
      // 添加音频事件监听
      this.audioPlayer.onended = () => {
        console.log('音频播放完成');
        // 标记音频已完成
        this.audioFinished = true;
        // 检查是否可以进行下一条消息
        this.checkNextMessage();
      };
      
      this.audioPlayer.onerror = (e) => {
        console.error('音频加载错误:', e);
        // 音频加载错误时，标记音频已完成，以便继续下一条消息
        this.audioFinished = true;
        this.checkNextMessage();
      };
      
      // 播放音频
      this.audioPlayer.play().catch(error => {
        console.error('音频播放失败:', error, fullPath);
        // 如果是由于浏览器策略导致的错误，则标记音频未初始化
        if (error.name === 'NotAllowedError') {
          this.audioInitialized = false;
        }
        // 音频播放失败时，标记音频已完成，以便继续下一条消息
        this.audioFinished = true;
        this.checkNextMessage();
      });
    },
    
    // 切换音频状态
    toggleAudio() {
      this.isMuted = !this.isMuted;
      
      if (this.isMuted) {
        // 如果静音，停止当前音频
        this.stopAudio();
      } else {
        // 如果取消静音，并且有活动消息，则播放当前消息的音频
        const currentMessage = this.messages[this.activeMessageIndex];
        if (currentMessage && currentMessage.audioPath) {
          this.playAudio(currentMessage.audioPath);
        }
        
        // 标记音频已初始化（用户交互已完成）
        this.audioInitialized = true;
      }
    },
    
    // 停止音频播放
    stopAudio() {
      if (this.audioPlayer) {
        this.audioPlayer.pause();
        this.audioPlayer.currentTime = 0;
        this.audioPlayer = null;
      }
    },
    
    goBack() {
      this.$router.go(-1);
    },
    shareDebate() {
      alert('分享功能即将上线');
    },
    navigateTo(path) {
      this.$router.push(path);
    },
    
    // 将API返回的round类型映射到消息类型
    mapRoundTypeToMessageType(roundType) {
      const typeMap = {
        'emcee': 'host',  // 主持人
        'pro': 'blue',    // 正方/蓝队
        'con': 'red'      // 反方/红队
      };
      return typeMap[roundType] || 'host';
    },
    
    // 保存辩论信息到服务器
    async saveDebateInfo() {
      try {
        // 使用API配置中的baseURL
        const apiBaseUrl = apiConfig.baseURL; // 直接使用导入的apiConfig
        
        // 请求保存辩论信息
        const response = await axios.post(`${apiBaseUrl}/debate_view/save`, {
          debateInfo: this.debateInfo,
          debateRounds: this.debateRounds,
          currentRound: this.currentRound,
          messages: this.messages
        });
        
        if (response.data && response.data.success) {
          console.log('辩论信息保存成功', response.data);
          return true;
        } else {
          console.error('辩论信息保存失败', response.data);
          return false;
        }
      } catch (error) {
        console.error('辩论信息保存失败:', error);
        return false;
      }
    }
  }
}
</script>

<style scoped>
.debate-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  padding-bottom: 60px; /* 为底部导航栏留出空间 */
}

/* 辩论头部样式 */
.debate-header {
  padding: 15px;
  background-color: white;
  border-bottom: 1px solid #f5f5f5;
  border-radius: 8px 8px 0 0;
  margin: 15px 15px 0;
}

/* 海报样式 */
.debate-poster {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #4a7bff 0%, #ff4a4a 100%);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  position: relative;
}

.poster-image-container {
  width: 100%;
  height: 250px;
  overflow: hidden;
  position: relative;
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.poster-content {
  padding: 20px;
  text-align: center;
  color: white;
}

.debate-title {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.debate-topic {
  font-size: 20px;
  line-height: 1.4;
  font-weight: bold;
  color: white;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.poster-vs {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 15px 0;
  position: relative;
}

.poster-team {
  flex: 1;
  padding: 10px;
  text-align: center;
}

.blue-side {
  background-color: rgba(74, 123, 255, 0.3);
  border-radius: 8px 0 0 8px;
}

.red-side {
  background-color: rgba(255, 74, 74, 0.3);
  border-radius: 0 8px 8px 0;
}

.vs-circle {
  width: 40px;
  height: 40px;
  background-color: white;
  color: #333;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
  z-index: 1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.poster-stance {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.poster-player {
  font-size: 14px;
  opacity: 0.9;
}

/* 正反方简洁展示样式 */
.stance-summary {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  padding: 0 10px;
}

.stance-item {
  flex: 1;
  padding: 10px 15px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.blue-stance {
  background-color: rgba(74, 123, 255, 0.1);
  margin-right: 5px;
}

.red-stance {
  background-color: rgba(255, 74, 74, 0.1);
  margin-left: 5px;
}

.stance-label {
  font-size: 12px;
  font-weight: bold;
  color: #666;
  margin-bottom: 5px;
}

.stance-text {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  text-align: center;
}

.teams-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  margin-top: 15px;
}

.team {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.blue-team {
  background-color: rgba(74, 123, 255, 0.1);
  margin-right: 5px;
}

.red-team {
  background-color: rgba(255, 74, 74, 0.1);
  margin-left: 5px;
}

/* 辩论内容样式 */
.debate-content {
  flex: 1;
  padding: 15px;
  display: flex;
  flex-direction: column;
  margin: 0 15px;
}

.debate-status {
  background-color: white;
  padding: 10px;
  text-align: center;
  font-weight: 500;
  font-size: 14px;
  border-radius: 8px;
  margin-bottom: 12px;
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.controls {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.audio-controls {
  display: flex;
  align-items: center;
}

.start-btn {
  background-color: #07c160;
  color: white;
  border: none;
  border-radius: 18px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0 15px;
  font-size: 14px;
}

.start-btn:hover {
  background-color: #06b057;
}

.start-icon {
  margin-right: 5px;
  font-style: normal;
}

.audio-btn {
  background-color: #f5f5f5;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
  margin-left: 10px;
}

.audio-btn.muted {
  background-color: #e0e0e0;
}

.audio-btn:hover {
  background-color: #e0e0e0;
}

.audio-icon {
  font-size: 18px;
  color: #333;
  font-style: normal;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding-bottom: 20px;
}

.chat-message {
  display: flex;
  margin-bottom: 15px;
  align-items: flex-start;
}

.blue-message {
  justify-content: flex-start;
}

.red-message {
  justify-content: flex-end;
}

.host-message {
  justify-content: flex-start;
  margin: 20px 0;
  position: relative;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: white;
  flex-shrink: 0;
}

.blue-avatar {
  background-color: #4a7bff;
  margin-right: 10px;
}

.red-avatar {
  background-color: #ff4a4a;
  margin-left: 10px;
}

.host-avatar {
  background-color: #07c160;
  margin-right: 10px;
}

.message-content {
  max-width: 70%;
}

.host-content {
  margin: 0 auto;
  display: flex;
  justify-content: center;
  width: 100%;
}

.message-bubble {
  padding: 12px 15px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.5;
  position: relative;
  word-break: break-word;
}

.blue-message .message-bubble {
  background-color: #4a7bff;
  color: white;
  border-bottom-left-radius: 5px;
}

.red-message .message-bubble {
  background-color: #ff4a4a;
  color: white;
  border-bottom-right-radius: 5px;
}

.host-message .message-bubble {
  background-color: #07c160;
  color: white;
  border-radius: 18px;
  max-width: 80%;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  text-align: right;
}

/* 底部操作栏样式 */
.debate-footer {
  display: flex;
  padding: 15px;
  background-color: white;
  border-top: 1px solid #f5f5f5;
  border-radius: 0 0 8px 8px;
  margin: 0 15px;
}

.back-button, .share-button {
  flex: 1;
  padding: 10px 0;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
}

.back-button {
  background-color: #f0f0f0;
  color: #333;
  margin-right: 10px;
}

.share-button {
  background-color: #07c160;
  color: white;
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
