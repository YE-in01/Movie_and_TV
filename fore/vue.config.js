const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  // 解决Multiple assets emit different content to the same filename index.html问题
  // 方法：完全禁用copy-webpack-plugin，让html-webpack-plugin单独处理index.html
  // 然后手动配置需要复制的静态资源
  chainWebpack: config => {
    // 移除默认的copy-webpack-plugin
    config.plugins.delete('copy')
    
    // 只保留html-webpack-plugin来处理index.html
    // 确保html-webpack-plugin配置正确
    config.plugin('html').tap(args => {
      args[0].template = 'public/index.html'
      args[0].filename = 'index.html'
      args[0].BASE_URL = './'
      return args
    })
    
    // 如果需要复制其他静态资源，可以手动添加
    // 例如复制public/favicon.ico
    config.plugin('copy-favicon').use(require('copy-webpack-plugin'), [{
      patterns: [
        {
          from: 'public/favicon.ico',
          to: 'favicon.ico'
        }
      ]
    }])
  }
})
