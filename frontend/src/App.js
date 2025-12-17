import React from 'react';
import './App.css';
import ProjectExplorer from './components/ProjectExplorer';

function App() {
  return (
    <div className="App">
      <header style={{ 
        backgroundColor: '#f8f9fa', 
        padding: '20px', 
        textAlign: 'center',
        borderBottom: '1px solid #dee2e6'
      }}>
        <h1>🧭 开源罗盘</h1>
        <p>开源贡献者智能导航系统</p>
      </header>
      <main>
        <ProjectExplorer />
      </main>
    </div>
  );
}

export default App;