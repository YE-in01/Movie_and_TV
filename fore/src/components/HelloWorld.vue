<template>
  <!-- 组件的模板部分，定义了页面的结构，这里是一个名为 hello 的容器，包含各类展示内容 -->
  <div class="hello">
    <!-- 展示通过 props 传递进来的 msg 数据，通常用于显示标题类信息 -->
    <h1>{{ msg }}</h1>
    <p>
      For a guide and recipes on how to configure / customize this project,<br>
      check out the
      <!-- 超链接，点击跳转到 vue-cli 文档页面，target="_blank" 表示在新窗口打开，rel="noopener" 是安全相关设置 -->
      <a href="https://cli.vuejs.org" target="_blank" rel="noopener">vue-cli documentation</a>.
    </p>
    <h3>Installed CLI Plugins</h3>
    <ul>
      <!-- 列表项，展示已安装的 CLI 插件相关链接 -->
      <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-babel" target="_blank" rel="noopener">babel</a></li>
      <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-eslint" target="_blank" rel="noopener">eslint</a></li>
    </ul>
    <h3>Essential Links</h3>
    <ul>
      <!-- 核心链接列表，指向 Vue 相关的核心文档、论坛等页面 -->
      <li><a href="https://vuejs.org" target="_blank" rel="noopener">Core Docs</a></li>
      <li><a href="https://forum.vuejs.org" target="_blank" rel="noopener">Forum</a></li>
      <li><a href="https://chat.vuejs.org" target="_blank" rel="noopener">Community Chat</a></li>
      <li><a href="https://twitter.com/vuejs" target="_blank" rel="noopener">Twitter</a></li>
      <li><a href="https://news.vuejs.org" target="_blank" rel="noopener">News</a></li>
    </ul>
    <h3>Ecosystem</h3>
    <ul>
      <!-- Vue 生态系统相关库的链接列表，如路由 vue-router、状态管理 vuex 等 -->
      <li><a href="https://router.vuejs.org" target="_blank" rel="noopener">vue-router</a></li>
      <li><a href="https://vuex.vuejs.org" target="_blank" rel="noopener">vuex</a></li>
      <li><a href="https://github.com/vuejs/vue-devtools#vue-devtools" target="_blank" rel="noopener">vue-devtools</a></li>
      <li><a href="https://vue-loader.vuejs.org" target="_blank" rel="noopener">vue-loader</a></li>
      <li><a href="https://github.com/vuejs/awesome-vue" target="_blank" rel="noopener">awesome-vue</a></li>
    </ul>
  </div>
</template>

<script>
// 组件的脚本部分，使用 Vue 2 的选项式 API 定义组件逻辑（Vue 3 也支持这种写法，同时有组合式 API 新写法）
export default {
  // 定义组件名称，用于标识组件，在 Vue 开发工具等场景中显示，也可用于递归组件等
  name: 'HelloWorld',
  // 定义组件接收的属性（props），这里 msg 是字符串类型，父组件可通过传递 msg 属性给该组件传值
  props: {
    msg: String
  }
}
</script>

<style scoped>
/* 样式部分，scoped 表示样式仅作用于当前组件的 DOM 元素，避免样式污染 */
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>