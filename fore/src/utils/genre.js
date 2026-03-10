// 类型映射对象：将后端返回的类型ID转换为用户友好的中文名称
export const genreMap = {
  1: '动作',
  2: '喜剧',
  3: '爱情',
  4: '科幻',
  5: '悬疑',
  6: '惊悚',
  7: '恐怖',
  8: '犯罪',
  9: '剧情',
  10: '历史',
  11: '战争',
  12: '西部',
  13: '奇幻',
  14: '冒险',
  15: '动画',
  16: '纪录片',
  17: '短片',
  18: '情色',
  19: '同性',
  20: '音乐',
  21: '歌舞',
  22: '家庭',
  23: '儿童',
  24: '传记',
  25: '体育',
  26: '武侠',
  27: '古装',
  28: '灾难',
  29: '青春',
  30: '励志'
}

// 格式化类型数据，将ID转换为中文名称
export const formatGenre = (genreData) => {
  if (!genreData) return '';
  
  // 如果是字符串类型
  if (typeof genreData === 'string') {
    // 尝试解析为数字
    const genreId = parseInt(genreData);
    // 如果能解析为有效的数字，返回对应的中文名称
    if (!isNaN(genreId) && genreMap[genreId]) {
      return genreMap[genreId];
    } else {
      // 如果无法解析为数字或没有对应的中文名称，直接返回原始字符串
      return genreData;
    }
  }
  
  // 如果是数字类型，直接返回对应的中文名称
  if (typeof genreData === 'number') {
    return genreMap[genreData] || genreData;
  }
  
  // 如果是数组类型，递归处理每个元素并使用' / '连接
  if (Array.isArray(genreData)) {
    return genreData
      .map(genre => formatGenre(genre))
      .filter(Boolean)
      .join(' / ');
  }
  
  // 如果是其他类型，直接返回
  return genreData;
}