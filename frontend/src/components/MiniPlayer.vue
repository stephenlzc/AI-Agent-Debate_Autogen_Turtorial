<template>
  <div class="mini-player" v-if="isVisible">
    <div class="player-content">
      <div class="player-left">
        <div class="thumbnail">
          <div class="thumbnail-placeholder">
            <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
              <path d="M512 85.333333c-235.648 0-426.666667 191.018667-426.666667 426.666667s191.018667 426.666667 426.666667 426.666667 426.666667-191.018667 426.666667-426.666667-191.018667-426.666667-426.666667-426.666667zM320 426.666667c0-58.816 47.850667-106.666667 106.666667-106.666667s106.666667 47.850667 106.666666 106.666667-47.850667 106.666667-106.666666 106.666666-106.666667-47.850667-106.666667-106.666666z m384 170.666666c0 58.816-47.850667 106.666667-106.666667 106.666667s-106.666667-47.850667-106.666666-106.666667 47.850667-106.666667 106.666666-106.666666 106.666667 47.850667 106.666667 106.666666z" fill="currentColor"/>
            </svg>
          </div>
        </div>
        <div class="info">
          <div class="title">{{ title }}</div>
        </div>
      </div>
      <div class="player-controls">
        <div class="play-button" @click="togglePlay">
          <svg v-if="!isPlaying" class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M341.333333 213.333333v597.333334l469.333334-298.666667z" fill="currentColor"/>
          </svg>
          <svg v-else class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M298.666667 213.333333h170.666666v597.333334H298.666667z m256 0h170.666666v597.333334h-170.666666z" fill="currentColor"/>
          </svg>
        </div>
        <!-- 测试按钮已隐藏 -->
        <div v-if="false" class="test-button" @click="testAudio" title="测试音频">
          <span>测试</span>
        </div>
        <div class="close-button" @click="close">
          <svg class="icon-svg" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
            <path d="M810.666667 273.493333L750.506667 213.333333 512 451.84 273.493333 213.333333 213.333333 273.493333 451.84 512 213.333333 750.506667 273.493333 810.666667 512 572.16 750.506667 810.666667 810.666667 750.506667 572.16 512z" fill="currentColor"/>
          </svg>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import apiConfig from '../config/api.js';

export default {
  name: 'MiniPlayer',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: '你没说的话（电影《不说话的爱》片段）'
    },
    subtitle: {
      type: String,
      default: '辩论片段'
    },
    thumbnail: {
      type: String,
      default: ''
    },
    audioPath: {
      type: String,
      default: ''
    },
    debateData: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      isPlaying: false,
      audioPlayer: null,
      currentAudioIndex: 0,
      audioPaths: [],
      apiConfig: apiConfig // 将导入的apiConfig添加到数据中
    }
  },
  watch: {
    isVisible(newVal) {
      if (newVal) {
        // 当播放器显示时，准备音频列表
        this.prepareAudioList();
      } else {
        // 当播放器隐藏时，停止播放并重置
        this.stopAudio();
        this.isPlaying = false;
      }
    }
  },
  mounted() {
    // 组件挂载时，如果可见则准备音频列表
    if (this.isVisible) {
      this.prepareAudioList();
    }
  },
  beforeUnmount() {
    // 组件卸载前停止音频播放
    this.stopAudio();
  },
  methods: {
    // 立即开始播放音频
    startPlayingImmediately() {
      console.log('立即开始播放音频');
      // 准备音频列表
      this.prepareAudioList();
      // 如果有音频路径，则开始播放
      if (this.audioPaths && this.audioPaths.length > 0) {
        this.currentAudioIndex = 0;
        this.playCurrentAudio();
        this.isPlaying = true;
      }
    },
    
    // 测试音频播放
    testAudio() {
      console.log('测试音频播放');
      
      // 直接指定一个音频文件进行测试
      // 使用前端服务器的URL
      const baseUrl = window.location.origin; // 如http://localhost:3001
      const testAudioUrl = `${baseUrl}/audio_output/audio_90167f02.mp3`;
      console.log('测试音频URL:', testAudioUrl);
      
      // 创建音频对象并播放
      const audio = new Audio(testAudioUrl);
      audio.onloadeddata = () => {
        console.log('音频加载成功，开始播放');
        audio.play().catch(error => {
          console.error('音频播放失败:', error);
        });
      };
      
      audio.onerror = (e) => {
        console.error('音频加载错误:', e);
      };
    },
    prepareAudioList() {
      // 如果有传入辩论数据，则提取音频路径
      if (this.debateData && this.debateData.originalData && this.debateData.originalData.rounds) {
        console.log('原始辩论数据:', this.debateData.originalData);
        
        this.audioPaths = this.debateData.originalData.rounds
          .filter(round => round.path) // 只保留有音频路径的轮次
          .map(round => round.path);
        
        console.log('提取的音频路径列表:', this.audioPaths);
        this.currentAudioIndex = 0;
      } else if (this.audioPath) {
        // 如果只有单个音频路径
        this.audioPaths = [this.audioPath];
        this.currentAudioIndex = 0;
      }
    },
    togglePlay() {
      if (this.isPlaying) {
        this.pauseAudio();
      } else {
        this.playCurrentAudio();
      }
      this.isPlaying = !this.isPlaying;
    },
    playCurrentAudio() {
      if (this.audioPaths && this.audioPaths.length > 0 && this.currentAudioIndex < this.audioPaths.length) {
        const audioPath = this.audioPaths[this.currentAudioIndex];
        this.playAudio(audioPath);
      }
    },
    playAudio(audioPath) {
      if (!audioPath) {
        console.warn('没有指定音频路径');
        return;
      }
      
      // 停止当前正在播放的音频
      this.stopAudio();
      
      // 将相对路径改造成HTTP路径进行播放
      let fullPath;
      if (audioPath.startsWith('http')) {
        // 已经是HTTP路径，直接使用
        fullPath = audioPath;
      } else {
        // 使用API服务器的URL
        // 使用API配置中的baseURL
        const apiBaseUrl = apiConfig.baseURL; // 直接使用导入的apiConfig
        
        if (audioPath.includes('audio_output/')) {
          // 如果已经包含audio_output路径
          fullPath = `${apiBaseUrl}/${audioPath}`;
        } else {
          // 如果只是文件名，构建完整路径
          const fileName = audioPath.split('/').pop();
          fullPath = `${apiBaseUrl}/audio_output/${fileName}`;
        }
        
        console.log('音频文件路径:', fullPath);
      }
      
      console.log('构建的音频URL:', fullPath);
      this.audioPlayer = new Audio(fullPath);
      
      // 设置音频播放速率
      this.audioPlayer.playbackRate = 1.5;
      
      // 音频播放完成后的处理
      this.audioPlayer.onended = () => {
        console.log('当前音频播放完成');
        // 播放下一个音频
        this.playNextAudio();
      };
      
      // 音频加载错误处理
      this.audioPlayer.onerror = (e) => {
        console.error('音频加载错误:', e);
        // 尝试播放下一个音频
        this.playNextAudio();
      };
      
      // 播放音频
      this.audioPlayer.play().catch(error => {
        console.error('音频播放失败:', error);
        this.isPlaying = false;
      });
    },
    pauseAudio() {
      if (this.audioPlayer) {
        this.audioPlayer.pause();
      }
    },
    stopAudio() {
      if (this.audioPlayer) {
        this.audioPlayer.pause();
        this.audioPlayer.currentTime = 0;
        this.audioPlayer = null;
      }
    },
    playNextAudio() {
      // 停止当前音频
      this.stopAudio();
      
      // 移动到下一个音频
      this.currentAudioIndex++;
      
      // 如果还有下一个音频，则播放
      if (this.currentAudioIndex < this.audioPaths.length) {
        // 播放下一个音频
        const nextAudioPath = this.audioPaths[this.currentAudioIndex];
        this.playAudio(nextAudioPath);
      } else {
        // 所有音频播放完毕
        this.currentAudioIndex = 0;
        this.isPlaying = false;
        console.log('所有音频播放完毕');
      }
    },
    close() {
      // 停止音频播放
      this.stopAudio();
      this.isPlaying = false;
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
.mini-player {
  position: fixed;
  bottom: 56px; /* 底部导航栏的高度 */
  left: 0;
  right: 0;
  background-color: #fff;
  z-index: 999; /* 提高z-index确保在最上层 */
  padding: 10px 12px;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

.player-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.player-left {
  display: flex;
  align-items: center;
  flex: 1;
  overflow: hidden;
}

.thumbnail {
  width: 28px;
  height: 28px;
  border-radius: 2px;
  overflow: hidden;
  margin-right: 10px;
  flex-shrink: 0;
}

.thumbnail-placeholder {
  width: 100%;
  height: 100%;
  background-color: #07c160;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.thumbnail-placeholder .icon-svg {
  width: 16px;
  height: 16px;
  color: white;
}

.info {
  overflow: hidden;
}

.title {
  font-size: 14px;
  color: #000;
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 220px;
}

.player-controls {
  display: flex;
  align-items: center;
}

.play-button {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-right: 8px;
}

.test-button {
  background-color: #ff9800;
  color: white;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 12px;
  margin: 0 10px;
  cursor: pointer;
}

.close-button {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-left: 10px;
}

.icon-svg {
  width: 20px;
  height: 20px;
  color: #333;
}

.play-button .icon-svg {
  color: #07c160;
  width: 24px;
  height: 24px;
}

.close-button .icon-svg {
  width: 16px;
  height: 16px;
  color: #999;
}
</style>
