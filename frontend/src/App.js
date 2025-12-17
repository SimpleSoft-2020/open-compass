// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';
import HomePage from './components/HomePage';
import ProjectExplorer from './components/ProjectExplorer';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [apiStatus, setApiStatus] = useState(null);
  const [apiAvailable, setApiAvailable] = useState(false);

  // 检查API状态
  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await fetch('/api/v1/health');
        if (response.ok) {
          const data = await response.json();
          setApiStatus(data);
          setApiAvailable(true);
        } else {
          setApiAvailable(false);
        }
      } catch (error) {
        setApiAvailable(false);
      }
    };

    checkApiStatus();
  }, []);

  // 处理浏览器后退/前进按钮
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.substring(1);
      if (hash === '/project-explorer') {
        setCurrentPage('project-explorer');
      } else {
        setCurrentPage('home');
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    handleHashChange(); // 初始化检查

    return () => {
      window.removeEventListener('hashchange', handleHashChange);
    };
  }, []);

  const navigateTo = (page) => {
    setCurrentPage(page);
    if (page === 'project-explorer') {
      window.location.hash = '/project-explorer';
    } else {
      window.location.hash = '';
    }
  };

  return (
    <div className="App">
      <header style={{ 
        backgroundColor: '#f8f9fa', 
        padding: '20px', 
        textAlign: 'center',
        borderBottom: '1px solid #dee2e6',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h1>🧭 开源罗盘</h1>
        <p>开源贡献者智能导航系统</p>
        <div>
          {apiAvailable ? (
            <span style={{ color: '#28a745', fontWeight: 'bold' }}>✅ API服务正常</span>
          ) : (
            <span style={{ color: '#dc3545', fontWeight: 'bold' }}>❌ API服务不可用</span>
          )}
        </div>
      </header>
      
      <nav style={{ 
        backgroundColor: '#ffffff', 
        padding: '10px 20px',
        borderBottom: '1px solid #dee2e6',
        display: 'flex',
        gap: '20px'
      }}>
        <button
          onClick={() => navigateTo('home')}
          style={{
            padding: '8px 16px',
            backgroundColor: currentPage === 'home' ? '#007bff' : '#f8f9fa',
            color: currentPage === 'home' ? 'white' : 'black',
            border: '1px solid #ddd',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          🏠 首页
        </button>
        <button
          onClick={() => navigateTo('project-explorer')}
          style={{
            padding: '8px 16px',
            backgroundColor: currentPage === 'project-explorer' ? '#007bff' : '#f8f9fa',
            color: currentPage === 'project-explorer' ? 'white' : 'black',
            border: '1px solid #ddd',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          🔍 项目探索
        </button>
        <button
          style={{
            padding: '8px 16px',
            backgroundColor: '#f8f9fa',
            color: 'black',
            border: '1px solid #ddd',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          🎯 任务推荐
        </button>
        <button
          style={{
            padding: '8px 16px',
            backgroundColor: '#f8f9fa',
            color: 'black',
            border: '1px solid #ddd',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          📊 我的成长
        </button>
        <button
          style={{
            padding: '8px 16px',
            backgroundColor: '#f8f9fa',
            color: 'black',
            border: '1px solid #ddd',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          ⚙️ 系统设置
        </button>
      </nav>
      
      <main>
        {currentPage === 'home' && <HomePage />}
        {currentPage === 'project-explorer' && <ProjectExplorer />}
      </main>
      
      <footer style={{ 
        backgroundColor: '#f8f9fa', 
        padding: '20px', 
        textAlign: 'center',
        borderTop: '1px solid #dee2e6',
        marginTop: '20px'
      }}>
        <p>开源罗盘 - 开源贡献者智能导航系统</p>
      </footer>
    </div>
  );
}

export default App;