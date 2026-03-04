<template>
  <div class="discover-container">
    <!-- 顶部搜索栏 -->
    <div class="search-bar">
      <div class="search-input-container">
        <input type="text" class="search-input" placeholder="大家正在搜：京东美团大战..." />
        <button class="search-button">搜索</button>
      </div>
      <div class="hot-search">
        <i class="hot-icon">🔥</i>
        <span>热搜</span>
      </div>
    </div>

    <!-- 热搜标签列表 -->
    <div class="hot-tags-container">
      <div class="hot-tag" @click="goToDebate">
        <span class="tag-text">京东 美团大战</span>
        <span class="tag-type hot">热</span>
      </div>
      <div class="hot-tag" @click="goToDebate">
        <span class="tag-text">中国美国关税大战</span>
        <span class="tag-type new">新</span>
      </div>
      <div class="hot-tag" @click="goToDebate">
        <span class="tag-text">中国股市涨？跌？</span>
        <span class="tag-type hot">热</span>

      </div>
      <div class="hot-tag" @click="goToDebate">
        <span class="tag-text">生活和工作平衡</span>
      </div>
      
      <div class="hot-tag">
        <span class="tag-more">更多热搜 ></span>
      </div>
    </div>

    <!-- 广告位 -->
    <div class="ad-container">
      <div class="ad-tag">广告</div>
      <img src="https://img.freepik.com/free-photo/electric-car-charging-station_1359-323.jpg" alt="广告" class="ad-image" />
      <div class="ad-title">#14万级长续航智能满配日产N7#</div>
    </div>

  
    <!-- 内容区域 -->
    <div class="content-area">
      <!-- 辩论热榜 -->
      <div class="section-title">
        <h2>辩论热榜</h2>
        <span class="more-link">更多 ></span>
      </div>
      <div class="debate-list">
        <div class="debate-item" @click="goToDebate">
          <div class="rank hot">1</div>
          <div class="debate-info">
            <div class="debate-title">曝拒肖"打招呼医生是盘尼西林成员"</div>
            <div class="debate-meta">
              <span class="tag">TOP1</span>
              <span class="hot-icon">🔥</span>
            </div>
          </div>
        </div>
        <div class="debate-item" @click="goToDebate">
          <div class="rank hot">2</div>
          <div class="debate-info">
            <div class="debate-title">人工智能是否会取代人类工作？</div>
            <div class="debate-meta">
              <span class="views">356万参与</span>
            </div>
          </div>
        </div>
        <div class="debate-item" @click="goToDebate">
          <div class="rank hot">3</div>
          <div class="debate-info">
            <div class="debate-title">网络教育能否替代传统教育？</div>
            <div class="debate-meta">
              <span class="views">298万参与</span>
            </div>
          </div>
        </div>
        <div class="debate-item" @click="goToDebate">
          <div class="rank">4</div>
          <div class="debate-info">
            <div class="debate-title">是否应该推行全民基本收入？</div>
            <div class="debate-meta">
              <span class="views">215万参与</span>
            </div>
          </div>
        </div>
        <div class="debate-item" @click="goToDebate">
          <div class="rank">5</div>
          <div class="debate-info">
            <div class="debate-title">大城市生活与小城市生活哪个更好？</div>
            <div class="debate-meta">
              <span class="views">189万参与</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 热门辩论视频 -->
      <div class="section-title">
        <h2>热门辩论视频</h2>
        <span class="more-link">更多 ></span>
      </div>
      <div class="video-list">
        <div class="video-item">
          <div class="video-cover" style="background-image: url('https://img.freepik.com/free-photo/people-having-business-meeting_23-2149300635.jpg'); background-size: cover;">
            <div class="play-icon">▶</div>
            <div class="video-duration">12:45</div>
          </div>
          <div class="video-title">当AI遇上传统行业，是颠覆还是革新？</div>
          <div class="video-author">
            <div class="author-avatar" style="background-image: url('https://img.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg'); background-size: cover;"></div>
            <div class="author-name">辩论学院</div>
          </div>
        </div>
        <div class="video-item">
          <div class="video-cover" style="background-image: url('https://img.freepik.com/free-photo/people-having-business-meeting_23-2149300635.jpg'); background-size: cover;">
            <div class="play-icon">▶</div>
            <div class="video-duration">18:32</div>
          </div>
          <div class="video-title">中美辩手激烈交锋：谁主导未来科技发展？</div>
          <div class="video-author">
            <div class="author-avatar" style="background-image: url('https://img.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg'); background-size: cover;"></div>
            <div class="author-name">国际辩论场</div>
          </div>
        </div>
      </div>

      <!-- 辩论活动 -->
      <div class="section-title">
        <h2>辩论活动</h2>
        <span class="more-link">更多 ></span>
      </div>
      <div class="activity-list">
        <div class="activity-item">
          <div class="activity-cover" style="background-image: url('https://img.freepik.com/free-photo/audience-watching-presentation-business-conference_107420-63795.jpg'); background-size: cover;"></div>
          <div class="activity-info">
            <div class="activity-title">2025全国大学生辩论赛</div>
            <div class="activity-time">05月15日 - 06月30日</div>
            <div class="activity-status">报名中</div>
          </div>
        </div>
        <div class="activity-item">
          <div class="activity-cover" style="background-image: url('https://img.freepik.com/free-photo/audience-watching-presentation-business-conference_107420-63795.jpg'); background-size: cover;"></div>
          <div class="activity-info">
            <div class="activity-title">AI与人类：未来共存辩论会</div>
            <div class="activity-time">05月20日 19:30</div>
            <div class="activity-status">预约中</div>
          </div>
        </div>
      </div>

      <!-- 辩论周边商品 -->
      <div class="section-title">
        <h2>辩论周边商品</h2>
        <span class="more-link">更多 ></span>
      </div>
      <div class="product-list">
        <div class="product-item">
          <div class="product-image" style="background-image: url('https://img.freepik.com/free-photo/book-composition-with-open-book_23-2147690555.jpg'); background-size: cover;"></div>
          <div class="product-title">《辩论的艺术》精装版</div>
          <div class="product-price">¥68.00</div>
        </div>
        <div class="product-item">
          <div class="product-image" style="background-image: url('https://img.freepik.com/free-photo/book-composition-with-open-book_23-2147690555.jpg'); background-size: cover;"></div>
          <div class="product-title">辩手专业计时器</div>
          <div class="product-price">¥129.00</div>
        </div>
        <div class="product-item">
          <div class="product-image" style="background-image: url('https://img.freepik.com/free-photo/book-composition-with-open-book_23-2147690555.jpg'); background-size: cover;"></div>
          <div class="product-title">辩论赛专用记分板</div>
          <div class="product-price">¥89.00</div>
        </div>
      </div>
    </div>

    <!-- 底部导航栏 -->
    <BottomNavBar activePage="discover" />
  </div>
</template>

<script>
import BottomNavBar from '../components/BottomNavBar.vue';

export default {
  name: 'DiscoverView',
  components: {
    BottomNavBar
  },
  data() {
    return {
      searchQuery: '',
      activeCategory: '热点'
    }
  },
  methods: {
    search() {
      alert('搜索功能即将上线');
    },
    changeCategory(category) {
      alert(`切换到${category}分类`);
    },
    goToDebate() {
      this.$router.push('/debate');
    }
  }
}
</script>

<style scoped>
.discover-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 60px; /* 为底部导航栏留出空间 */
}

/* 顶部搜索栏 */
.search-bar {
  background-color: white;
  padding: 12px 15px;
}

.search-input-container {
  display: flex;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  overflow: hidden;
  background-color: #f8f8f8;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: none;
  outline: none;
  background-color: transparent;
  font-size: 14px;
  color: #666;
}

.search-button {
  padding: 8px 15px;
  background-color: transparent;
  border: none;
  color: #ff8200;
  font-size: 14px;
  cursor: pointer;
}

.hot-search {
  display: flex;
  align-items: center;
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

.hot-icon {
  margin-right: 5px;
  font-style: normal;
}

/* 热搜标签列表 */
.hot-tags-container {
  display: flex;
  flex-wrap: wrap;
  padding: 10px;
  background-color: white;
  margin-bottom: 10px;
}

.hot-tag {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: white;
  border-radius: 4px;
  margin-bottom: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  font-size: 12px;
  cursor: pointer;
}

.tag-text {
  max-width: 150px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tag-type {
  margin-left: 5px;
  padding: 2px 4px;
  border-radius: 2px;
  font-size: 10px;
  color: white;
}

.tag-type.hot {
  background-color: #ff4a4a;
}

.tag-type.new {
  background-color: #4a7bff;
}

.tag-more {
  color: #666;
}

/* 广告位 */
.ad-container {
  position: relative;
  margin-bottom: 10px;
}

.ad-tag {
  position: absolute;
  top: 5px;
  right: 5px;
  padding: 2px 4px;
  background-color: rgba(0, 0, 0, 0.3);
  color: white;
  font-size: 10px;
  border-radius: 2px;
}

.ad-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  background-color: #e0e0e0;
}

.ad-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 14px;
}

/* 分类导航 */
.category-nav {
  display: flex;
  justify-content: space-around;
  padding: 12px 0;
  background-color: white;
  border-bottom: 1px solid #eee;
  margin-bottom: 10px;
}

.nav-item {
  font-size: 15px;
  color: #333;
  cursor: pointer;
}

.nav-item.active {
  color: #ff8200;
  font-weight: 500;
  position: relative;
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background-color: #ff8200;
}

.menu-icon {
  font-style: normal;
  font-size: 18px;
}

/* 内容区域 */
.content-area {
  flex: 1;
  padding: 0 15px;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 15px 0 10px;
}

.section-title h2 {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.more-link {
  font-size: 14px;
  color: #999;
}

/* 辩论热榜 */
.debate-list {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.debate-item {
  display: flex;
  padding: 12px 15px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
}

.debate-item:last-child {
  border-bottom: none;
}

.rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  font-weight: bold;
  color: #999;
}

.rank.hot {
  color: #ff4a4a;
}

.debate-info {
  flex: 1;
}

.debate-title {
  font-size: 14px;
  margin-bottom: 5px;
  line-height: 1.4;
}

.debate-meta {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #999;
}

.tag {
  margin-right: 5px;
  padding: 1px 3px;
  background-color: #ff8200;
  color: white;
  border-radius: 2px;
  font-size: 10px;
}

.views {
  color: #999;
}

/* 热门辩论视频 */
.video-list {
  display: flex;
  overflow-x: auto;
  margin-bottom: 20px;
}

.video-item {
  flex: 0 0 auto;
  width: 200px;
  margin-right: 10px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.video-cover {
  position: relative;
  height: 120px;
  background-color: #e0e0e0;
}

.play-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-duration {
  position: absolute;
  bottom: 5px;
  right: 5px;
  padding: 2px 4px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 10px;
  border-radius: 2px;
}

.video-title {
  padding: 8px;
  font-size: 14px;
  line-height: 1.4;
}

.video-author {
  display: flex;
  align-items: center;
  padding: 0 8px 8px;
}

.author-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 5px;
  background-color: #e0e0e0;
}

.author-name {
  font-size: 12px;
  color: #999;
}

/* 辩论活动 */
.activity-list {
  display: flex;
  overflow-x: auto;
  margin-bottom: 20px;
}

.activity-item {
  flex: 0 0 auto;
  width: 250px;
  margin-right: 10px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.activity-cover {
  height: 100px;
  background-color: #e0e0e0;
}

.activity-info {
  padding: 10px;
}

.activity-title {
  font-size: 14px;
  margin-bottom: 5px;
  font-weight: 500;
}

.activity-time {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.activity-status {
  display: inline-block;
  padding: 2px 6px;
  background-color: #4a7bff;
  color: white;
  font-size: 12px;
  border-radius: 2px;
}

/* 辩论周边商品 */
.product-list {
  display: flex;
  overflow-x: auto;
  margin-bottom: 20px;
}

.product-item {
  flex: 0 0 auto;
  width: 120px;
  margin-right: 10px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.product-image {
  height: 120px;
  background-color: #e0e0e0;
}

.product-title {
  padding: 8px;
  font-size: 12px;
  line-height: 1.4;
}

.product-price {
  padding: 0 8px 8px;
  font-size: 14px;
  color: #ff4a4a;
  font-weight: 500;
}
</style>
