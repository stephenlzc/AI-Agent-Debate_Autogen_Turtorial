<template>
  <div class="debate-container">
    <!-- 辩论主题 -->
    <div class="debate-header">
      <h1 class="debate-title">辩论主题</h1>
      <div class="debate-topic">{{ debateInfo.topic.title }}</div>
      
      <div class="teams-info">
        <div class="team blue-team">
          <div class="team-name">蓝队</div>
          <div class="team-stance">
            <span class="stance-label"><i class="stance-icon">&#9733;</i></span>
            <span class="stance-value">{{ debateInfo.blueStance }}</span>
          </div>
          <div class="player-type">选手: {{ debateInfo.bluePlayerType }}</div>
        </div>
        
        <div class="team red-team">
          <div class="team-name">红队</div>
          <div class="team-stance">
            <span class="stance-label"><i class="stance-icon">&#9733;</i></span>
            <span class="stance-value">{{ debateInfo.redStance }}</span>
          </div>
          <div class="player-type">选手: {{ debateInfo.redPlayerType }}</div>
        </div>
      </div>
      
     
    </div>
    
    <!-- 辩论内容 -->
    <div class="debate-content">
      <div class="debate-status">辩论中</div>
      
      <div class="chat-container">
        <!-- 主持人消息 -->
        <div class="chat-message host-message">
          <div class="avatar host-avatar">主</div>
          <div class="message-content">
            <div class="message-bubble">
              各位观众朋友们大家好，欢迎来到本次辩论。今天的辩题是《{{ debateInfo.topic.title }}》。蓝队将支持「{{ debateInfo.blueStance }}」，红队将支持「{{ debateInfo.redStance }}」。辩论共计{{ debateRounds }}轮，现在开始第一轮辩论。
            </div>
          </div>
        </div>
        
        <!-- 轮次标记 -->
        <div class="round-marker" data-round="轮次1"></div>
        
        <!-- 蓝队消息 -->
        <div class="chat-message blue-message">
          <div class="avatar blue-avatar">蓝</div>
          <div class="message-content">
            <div class="message-bubble">
              家庭温暖和经济稳定性: 结婚后可以享受家庭的温暖，有人陪伴和照顾，尤其是在遇到困难时有人分担。
            </div>
          </div>
        </div>
        
        <!-- 红队消息 -->
        <div class="chat-message red-message">
          <div class="message-content">
            <div class="message-bubble">
              自由和独立: 单身生活最大的优点是自由，可以自由安排自己的时间和生活，无需考虑他人的感受和需求。经济上也更自由，可以随心所欲地花钱而不用担心另一半的意见
            </div>
          </div>
          <div class="avatar red-avatar">红</div>
        </div>
        
        <!-- 主持人轮次过渡消息 -->
        <div class="chat-message host-message">
          <div class="avatar host-avatar">主</div>
          <div class="message-content">
            <div class="message-bubble">
              第一轮辩论结束，双方观点鲜明。现在进入第二轮辩论，请双方针对对方观点进行深入辩论。
            </div>
          </div>
        </div>
        
        <!-- 轮次标记 -->
        <div class="round-marker" data-round="轮次2"></div>
        
        <!-- 蓝队消息 -->
        <div class="chat-message blue-message">
          <div class="avatar blue-avatar">蓝</div>
          <div class="message-content">
            <div class="message-bubble">
              家庭温暖和经济稳定性: 结婚后可以享受家庭的温暖，有人陪伴和照顾，尤其是在遇到困难时有人分担。
            </div>
          </div>
        </div>
        
        <!-- 红队消息 -->
        <div class="chat-message red-message">
          <div class="message-content">
            <div class="message-bubble">
              自由和独立: 单身生活最大的优点是自由，可以自由安排自己的时间和生活，无需考虑他人的感受和需求。经济上也更自由，可以随心所欲地花钱而不用担心另一半的意见
            </div>
          </div>
          <div class="avatar red-avatar">红</div>
        </div>
        
        <!-- 主持人总结消息 -->
        <div class="chat-message host-message">
          <div class="avatar host-avatar">主</div>
          <div class="message-content">
            <div class="message-bubble">
              本次辩论已经结束。蓝队支持「{{ debateInfo.blueStance }}」，强调家庭温暖和稳定性的重要性。红队支持「{{ debateInfo.redStance }}」，强调个人自由和独立的价值。双方都提出了有说服力的观点，这个话题没有绝对的对错，每个人都可以根据自己的价值观和生活状况做出选择。感谢各位的关注！
            </div>
          </div>
        </div>
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
        useVoice: '是'
      },
      debateRounds: 15,
      currentRound: 2,
      blueArguments: [
        '家庭温暖和经济稳定性: 结婚后可以享受家庭的温暖，有人陪伴和照顾，尤其是在遇到困难时有人分担。',
        '家庭温暖和经济稳定性: 结婚后可以享受家庭的温暖，有人陪伴和照顾，尤其是在遇到困难时有人分担。'
      ],
      redArguments: [
        '自由和独立: 单身生活最大的优点是自由，可以自由安排自己的时间和生活，无需考虑他人的感受和需求。经济上也更自由，可以随心所欲地花钱而不用担心另一半的意见',
        '自由和独立: 单身生活最大的优点是自由，可以自由安排自己的时间和生活，无需考虑他人的感受和需求。经济上也更自由，可以随心所欲地花钱而不用担心另一半的意见'
      ]
    }
  },
  created() {
    // 从本地存储获取辩论信息
    const savedDebateInfo = localStorage.getItem('debateInfo');
    if (savedDebateInfo) {
      this.debateInfo = JSON.parse(savedDebateInfo);
      
      // 初始化辩论内容
      this.initializeDebate();
    }
  },
  methods: {
    initializeDebate() {
      // 模拟辩论过程，这里应该调用后端API获取真实的辩论内容
      // 这里只是简单模拟
      this.blueArguments = [];
      this.redArguments = [];
      
      // 根据选择的立场和选手类型生成辩论内容
      if (this.debateInfo.blueStance === '结婚') {
        this.blueArguments.push('家庭温暖和经济稳定性: 结婚后可以享受家庭的温暖，有人陪伴和照顾，尤其是在遇到困难时有人分担。');
        this.blueArguments.push('家庭温暖和经济稳定性: 结婚后可以享受家庭的温暖，有人陪伴和照顾，尤其是在遇到困难时有人分担。');
      }
      
      if (this.debateInfo.redStance === '单身狗') {
        this.redArguments.push('自由和独立: 单身生活最大的优点是自由，可以自由安排自己的时间和生活，无需考虑他人的感受和需求。经济上也更自由，可以随心所欲地花钱而不用担心另一半的意见');
        this.redArguments.push('自由和独立: 单身生活最大的优点是自由，可以自由安排自己的时间和生活，无需考虑他人的感受和需求。经济上也更自由，可以随心所欲地花钱而不用担心另一半的意见');
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

.debate-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.debate-topic {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f5f5f5;
}

.teams-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
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
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding-bottom: 20px;
}

.round-marker {
  text-align: center;
  margin: 10px 0;
  position: relative;
}

.round-marker::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  width: 100%;
  height: 1px;
  background-color: #f5f5f5;
  z-index: -1;
}

.round-marker::after {
  content: attr(data-round);
  background-color: #f5f5f5;
  padding: 5px 15px;
  border-radius: 15px;
  font-size: 12px;
  color: #666;
  display: inline-block;
  position: relative;
  z-index: 1;
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
  justify-content: center;
  margin: 20px 0;
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
