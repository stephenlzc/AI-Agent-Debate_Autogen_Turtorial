<template>
  <div class="debate-detail-container">
    <!-- 顶部LOGO -->
    <div class="logo-container">
      <div class="logo">
        <div class="logo-circle">
          <span class="logo-text">辩</span>
          <div class="logo-bird"></div>
        </div>
      </div>
    </div>
    
    <!-- 辩论海报 -->
    <div class="debate-poster-container">
      <div class="debate-poster" :class="{ 'loading': isGeneratingPoster }">
        <div v-if="isGeneratingPoster" class="poster-loading">
          <div class="loading-spinner">⭯</div>
          <div class="loading-text">正在生成辩论海报...</div>
        </div>
        <img v-else-if="posterUrl" :src="posterUrl" alt="辩论海报" class="poster-image" />
        <div v-else class="poster-placeholder">
          <div class="poster-topic">{{ topic.title }}</div>
          <div class="poster-vs">
            <span class="blue-team-name">{{ blueStance }}</span>
            <span class="vs-text">VS</span>
            <span class="red-team-name">{{ redStance }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 蓝队红队选择 -->
    <div class="teams-container">
      <div class="team blue-team" :class="{ active: selectedTeam === 'blue' }" @click="selectTeam('blue')">
        <div class="team-name">蓝队</div>
        <div class="team-stance">观点: {{ blueStance }}</div>
        <div class="player-type">
          <span>选手: </span>
          <div class="select-container">
            <select v-model="bluePlayerType">
              <option value="激进型">激进型</option>
              <option value="保守型">保守型</option>
              <option value="平衡型">平衡型</option>
            </select>
            <span class="select-arrow">▼</span>
          </div>
        </div>
      </div>
      
      <div class="team red-team" :class="{ active: selectedTeam === 'red' }" @click="selectTeam('red')">
        <div class="team-name">红队</div>
        <div class="team-stance">观点: {{ redStance }}</div>
        <div class="player-type">
          <span>选手: </span>
          <div class="select-container">
            <select v-model="redPlayerType">
              <option value="激进型">激进型</option>
              <option value="保守型">保守型</option>
              <option value="平衡型">平衡型</option>
            </select>
            <span class="select-arrow">▼</span>
          </div>
        </div>
      </div>
    </div>
    

    
    <!-- 开始辩论按钮 -->
    <div class="start-debate-container">
      <button class="start-debate-button" @click="startDebate" :disabled="!selectedTeam">
        辩论开始
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DebateDetailView',
  data() {
    return {
      topic: { id: 0, title: '结婚还是做单身狗', description: '' },
      selectedTeam: '',
      blueStance: '结婚',
      redStance: '单身狗',
      bluePlayerType: '激进型',
      redPlayerType: '保守型',
      posterUrl: '',
      isGeneratingPoster: false,
      posterColors: [
        '#4a7bff', // 蓝色
        '#ff4a4a', // 红色
        '#ffcc00', // 黄色
        '#44cc77', // 绿色
        '#aa66cc'  // 紫色
      ]
    }
  },
  created() {
    // 从本地存储获取选中的话题
    const savedTopic = localStorage.getItem('selectedDebateTopic');
    if (savedTopic) {
      this.topic = JSON.parse(savedTopic);
      
      // 根据话题生成蓝队红队立场
      this.generateTeamStances();
      
      // 生成辩论海报
      this.generateDebatePoster();
    }
  },
  methods: {
    generateTeamStances() {
      // 这里应该调用后端API生成更精确的蓝队红队立场
      // 这里只是根据话题简单生成
      
      if (this.topic.title.includes('是否')) {
        const parts = this.topic.title.split('是否');
        this.blueStance = parts[0];
        this.redStance = `不${parts[0]}`;
      } else if (this.topic.title.includes('还是')) {
        const parts = this.topic.title.split('还是');
        this.blueStance = parts[0];
        this.redStance = parts[1].replace('？', '');
      } else {
        // 默认立场
        this.blueStance = '正方';
        this.redStance = '反方';
      }
    },
    
    generateDebatePoster() {
      this.isGeneratingPoster = true;
      
      // 模拟大模型生成海报的过程
      setTimeout(() => {
        // 创建Canvas元素
        const canvas = document.createElement('canvas');
        canvas.width = 600;
        canvas.height = 400;
        const ctx = canvas.getContext('2d');
        
        // 绘制渐变背景
        const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
        gradient.addColorStop(0, this.getRandomColor(0.2));
        gradient.addColorStop(1, this.getRandomColor(0.2));
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // 绘制装饰元素
        this.drawDecorativeElements(ctx, canvas.width, canvas.height);
        
        // 绘制标题
        ctx.font = 'bold 36px Arial';
        ctx.textAlign = 'center';
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
        ctx.shadowBlur = 10;
        ctx.fillText(this.topic.title, canvas.width / 2, 80);
        ctx.shadowBlur = 0;
        
        // 绘制VS对战区域
        this.drawVersusSection(ctx, canvas.width, canvas.height);
        
        // 转换为URL
        this.posterUrl = canvas.toDataURL('image/png');
        this.isGeneratingPoster = false;
      }, 1500);
    },
    
    drawDecorativeElements(ctx, width, height) {
      // 绘制彩色圆圈和形状
      for (let i = 0; i < 15; i++) {
        const x = Math.random() * width;
        const y = Math.random() * height;
        const radius = 5 + Math.random() * 30;
        
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = this.getRandomColor(0.4);
        ctx.fill();
      }
      
      // 绘制辩论相关图形
      for (let i = 0; i < 5; i++) {
        const x = Math.random() * width;
        const y = Math.random() * height;
        const size = 20 + Math.random() * 40;
        
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(Math.random() * Math.PI * 2);
        
        // 随机绘制不同形状
        const shapeType = Math.floor(Math.random() * 3);
        ctx.fillStyle = this.getRandomColor(0.6);
        
        if (shapeType === 0) {
          // 绘制五边形
          this.drawPolygon(ctx, 0, 0, size, 5);
        } else if (shapeType === 1) {
          // 绘制星形
          this.drawStar(ctx, 0, 0, size, 5);
        } else {
          // 绘制波浪形
          this.drawWave(ctx, 0, 0, size);
        }
        
        ctx.restore();
      }
    },
    
    drawVersusSection(ctx, width, height) {
      // 绘制蓝队区域
      ctx.fillStyle = 'rgba(74, 123, 255, 0.7)';
      ctx.beginPath();
      ctx.moveTo(0, height / 2 - 60);
      ctx.lineTo(width / 2 - 50, height / 2 - 60);
      ctx.lineTo(width / 2 - 20, height / 2);
      ctx.lineTo(width / 2 - 50, height / 2 + 60);
      ctx.lineTo(0, height / 2 + 60);
      ctx.closePath();
      ctx.fill();
      
      // 绘制红队区域
      ctx.fillStyle = 'rgba(255, 74, 74, 0.7)';
      ctx.beginPath();
      ctx.moveTo(width, height / 2 - 60);
      ctx.lineTo(width / 2 + 50, height / 2 - 60);
      ctx.lineTo(width / 2 + 20, height / 2);
      ctx.lineTo(width / 2 + 50, height / 2 + 60);
      ctx.lineTo(width, height / 2 + 60);
      ctx.closePath();
      ctx.fill();
      
      // 绘制VS文字
      ctx.font = 'bold 48px Arial';
      ctx.textAlign = 'center';
      ctx.fillStyle = '#ffffff';
      ctx.shadowColor = 'rgba(0, 0, 0, 0.7)';
      ctx.shadowBlur = 15;
      ctx.fillText('VS', width / 2, height / 2 + 15);
      ctx.shadowBlur = 0;
      
      // 绘制蓝队立场
      ctx.font = 'bold 28px Arial';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.fillText(this.blueStance, width / 4, height / 2 + 5);
      
      // 绘制红队立场
      ctx.fillText(this.redStance, width * 3 / 4, height / 2 + 5);
    },
    
    drawPolygon(ctx, x, y, radius, sides) {
      ctx.beginPath();
      for (let i = 0; i < sides; i++) {
        const angle = (i * 2 * Math.PI / sides) - Math.PI / 2;
        const px = x + radius * Math.cos(angle);
        const py = y + radius * Math.sin(angle);
        if (i === 0) {
          ctx.moveTo(px, py);
        } else {
          ctx.lineTo(px, py);
        }
      }
      ctx.closePath();
      ctx.fill();
    },
    
    drawStar(ctx, x, y, radius, points) {
      ctx.beginPath();
      for (let i = 0; i < points * 2; i++) {
        const angle = (i * Math.PI / points) - Math.PI / 2;
        const r = i % 2 === 0 ? radius : radius * 0.4;
        const px = x + r * Math.cos(angle);
        const py = y + r * Math.sin(angle);
        if (i === 0) {
          ctx.moveTo(px, py);
        } else {
          ctx.lineTo(px, py);
        }
      }
      ctx.closePath();
      ctx.fill();
    },
    
    drawWave(ctx, x, y, size) {
      ctx.beginPath();
      for (let i = 0; i <= 20; i++) {
        const angle = (i / 20) * Math.PI * 2;
        const r = size * (0.8 + 0.2 * Math.sin(angle * 6));
        const px = x + r * Math.cos(angle);
        const py = y + r * Math.sin(angle);
        if (i === 0) {
          ctx.moveTo(px, py);
        } else {
          ctx.lineTo(px, py);
        }
      }
      ctx.closePath();
      ctx.fill();
    },
    
    getRandomColor(alpha = 1) {
      const colorIndex = Math.floor(Math.random() * this.posterColors.length);
      const color = this.posterColors[colorIndex];
      
      // 如果需要透明度，将其转换为rgba
      if (alpha < 1) {
        const r = parseInt(color.slice(1, 3), 16);
        const g = parseInt(color.slice(3, 5), 16);
        const b = parseInt(color.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
      }
      
      return color;
    },
    selectTeam(team) {
      this.selectedTeam = team;
    },
    startDebate() {
      if (!this.selectedTeam) {
        alert('请选择一个队伍');
        return;
      }
      
      // 将辩论信息存储到本地
      const debateInfo = {
        topic: this.topic,
        selectedTeam: this.selectedTeam,
        blueStance: this.blueStance,
        redStance: this.redStance,
        bluePlayerType: this.bluePlayerType,
        redPlayerType: this.redPlayerType
      };
      
      localStorage.setItem('debateInfo', JSON.stringify(debateInfo));
      
      // 返回热点辩论页面并显示提示信息
      alert('辩论即将开始，辩论页面正在开发中');
      this.$router.push('/hot-debates');
    }
  }
}
</script>

<style scoped>
.debate-detail-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
}

/* 顶部LOGO样式 */
.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 0;
  background-color: white;
}

.logo {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

/* 辩论海报样式 */
.debate-poster-container {
  padding: 15px;
  background-color: white;
}

.debate-poster {
  position: relative;
  width: 100%;
  height: 200px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.debate-poster.loading {
  background-color: #f5f5f5;
}

.poster-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #4a7bff;
}

.loading-spinner {
  font-size: 24px;
  animation: spin 1.5s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 14px;
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poster-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: linear-gradient(135deg, #4a7bff, #ff4a4a);
  color: white;
  padding: 20px;
}

.poster-topic {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.poster-vs {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.blue-team-name {
  color: #ffffff;
  font-size: 18px;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.red-team-name {
  color: #ffffff;
  font-size: 18px;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.vs-text {
  margin: 0 15px;
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.logo-circle {
  position: relative;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: white;
  border: 2px solid black;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 30px;
  font-weight: bold;
  color: black;
}

.logo-bird {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 20px;
  height: 20px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22,3.5C21.4,3.5 21,3.9 21,4.5C21,5.1 21.4,5.5 22,5.5C22.6,5.5 23,5.1 23,4.5C23,3.9 22.6,3.5 22,3.5M10.5,2C8,2 6,4 6,6.5C6,9 8,11 10.5,11C13,11 15,9 15,6.5C15,4 13,2 10.5,2M10.5,10C8.6,10 7,8.4 7,6.5C7,4.6 8.6,3 10.5,3C12.4,3 14,4.6 14,6.5C14,8.4 12.4,10 10.5,10M16,13C16,11.9 15.1,11 14,11H7C5.9,11 5,11.9 5,13V21H16V13M15,20H6V13.5C6,13.2 6.2,13 6.5,13H14.5C14.8,13 15,13.2 15,13.5V20M19.5,20H17V13.2C16.5,12.5 15.8,12 15,11.7V20H19.5V20M22,19H21V15H22V19Z" /></svg>');
  background-repeat: no-repeat;
  background-size: contain;
}

.debate-topic {
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  padding: 0 20px;
}

/* 蓝队红队选择样式 */
.teams-container {
  display: flex;
  margin: 15px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.team {
  flex: 1;
  padding: 15px;
  background-color: white;
  display: flex;
  flex-direction: column;
  gap: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.blue-team {
  border-right: 1px solid #eee;
}

.team.active {
  background-color: rgba(74, 123, 255, 0.1);
  border: 2px solid #4a7bff;
}

.team-name {
  font-size: 16px;
  font-weight: bold;
  text-align: center;
}

.blue-team .team-name {
  color: #4a7bff;
}

.red-team .team-name {
  color: #ff4a4a;
}

.team-stance {
  font-size: 14px;
  margin-bottom: 5px;
}

.player-type {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.select-container {
  position: relative;
  margin-left: 5px;
}

select {
  appearance: none;
  padding: 5px 20px 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  font-size: 14px;
}

.select-arrow {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 10px;
  pointer-events: none;
}

/* 辩论设置样式 */
.debate-settings {
  margin: 15px;
  padding: 15px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-label {
  font-size: 14px;
}

.setting-value select,
.setting-value input {
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 80px;
  text-align: center;
}

/* 开始辩论按钮样式 */
.start-debate-container {
  padding: 15px;
  margin-top: auto;
}

.start-debate-button {
  width: 100%;
  padding: 12px 0;
  background-color: #4a7bff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.start-debate-button:hover {
  background-color: #3a6bef;
}

.start-debate-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
