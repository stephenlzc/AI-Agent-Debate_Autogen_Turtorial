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
    }
  },
  data() {
    return {
      isPlaying: false
    }
  },
  methods: {
    togglePlay() {
      this.isPlaying = !this.isPlaying;
      this.$emit('toggle-play', this.isPlaying);
    },
    close() {
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

.play-button, .close-button {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.play-button {
  margin-right: 8px;
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
