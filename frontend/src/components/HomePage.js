// frontend/src/components/HomePage.js
import React from 'react';

const HomePage = () => {
  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>欢迎使用开源罗盘</h1>
      
      <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
        <div style={{ flex: 2 }}>
          <div style={{ 
            backgroundColor: '#f8f9fa', 
            padding: '20px', 
            borderRadius: '5px',
            marginBottom: '20px'
          }}>
            <h2>🌟 项目介绍</h2>
            <p><strong>开源罗盘</strong>是一个智能化的开源贡献者导航系统，旨在帮助：</p>
            <ul>
              <li>🚀 <strong>开源新人</strong>：快速找到合适的贡献起点</li>
              <li>📈 <strong>成长中贡献者</strong>：规划清晰的成长路径</li>
              <li>🛠️ <strong>项目维护者</strong>：高效管理社区和发现人才</li>
            </ul>
          </div>
          
          <div style={{ 
            backgroundColor: '#f8f9fa', 
            padding: '20px', 
            borderRadius: '5px',
            marginBottom: '20px'
          }}>
            <h2>🔧 当前状态</h2>
            <ul>
              <li>✅ 项目框架已搭建</li>
              <li>🔄 核心功能开发中</li>
              <li>📚 数据连接准备中</li>
            </ul>
          </div>
          
          <div style={{ 
            backgroundColor: '#f8f9fa', 
            padding: '20px', 
            borderRadius: '5px'
          }}>
            <h2>🎯 即将实现</h2>
            <ol>
              <li>GitHub项目数据分析</li>
              <li>智能任务推荐算法</li>
              <li>贡献者成长可视化</li>
              <li>社区健康度监控</li>
            </ol>
          </div>
        </div>
        
        <div style={{ flex: 1 }}>
          <div style={{ 
            backgroundColor: '#f8f9fa', 
            padding: '20px', 
            borderRadius: '5px',
            marginBottom: '20px'
          }}>
            <h2>📊 项目统计</h2>
            <div style={{ textAlign: 'center', padding: '10px' }}>
              <h3>关注项目</h3>
              <p style={{ fontSize: '24px', fontWeight: 'bold' }}>3</p>
            </div>
            <div style={{ textAlign: 'center', padding: '10px' }}>
              <h3>API状态</h3>
              <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#28a745' }}>正常</p>
            </div>
            <div style={{ textAlign: 'center', padding: '10px' }}>
              <h3>数据源</h3>
              <p style={{ fontSize: '24px', fontWeight: 'bold' }}>GitHub API</p>
            </div>
          </div>
          
          <div style={{ 
            backgroundColor: '#f8f9fa', 
            padding: '20px', 
            borderRadius: '5px'
          }}>
            <h2>⚡ 快速开始</h2>
            <button
              onClick={() => window.location.hash = '/project-explorer'}
              style={{
                width: '100%',
                padding: '12px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '16px',
                marginBottom: '10px'
              }}
            >
              🔍 探索项目
            </button>
            <button
              style={{
                width: '100%',
                padding: '12px',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '16px',
                marginBottom: '10px'
              }}
            >
              🎯 获取推荐
            </button>
            <button
              style={{
                width: '100%',
                padding: '12px',
                backgroundColor: '#ffc107',
                color: 'black',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '16px'
              }}
            >
              📊 查看示例
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;