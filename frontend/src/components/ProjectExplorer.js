import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProjectExplorer = () => {
  const [selectedProject, setSelectedProject] = useState('apache/iotdb');
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const famousProjects = {
    "Apache": [
      "apache/iotdb",
      "apache/kafka",
      "apache/spark",
      "apache/hadoop"
    ],
    "Google": [
      "kubernetes/kubernetes",
      "tensorflow/tensorflow",
      "golang/go",
      "google/jax"
    ],
    "Microsoft": [
      "microsoft/vscode",
      "microsoft/TypeScript",
      "dotnet/core",
      "microsoft/PowerToys"
    ],
    "Meta": [
      "facebook/react",
      "facebook/react-native",
      "pytorch/pytorch"
    ],
    "其他热门项目": [
      "X-lab2017/open-digger",
      "easy-graph/Easy-Graph",
      "tiangolo/fastapi",
      "pallets/flask"
    ]
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [owner, repo] = selectedProject.split('/');
      const response = await axios.get(`/api/v1/projects/${owner}/${repo}`);
      
      if (response.data.success) {
        setAnalysisData(response.data.data);
      } else {
        setError('项目分析失败，请稍后重试');
      }
    } catch (err) {
      setError('无法获取项目数据，请检查项目名称是否正确');
      console.error('分析错误:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>项目探索</h1>
      
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <div style={{ flex: 2 }}>
          <h2>选择项目</h2>
          
          <div style={{ marginBottom: '10px' }}>
            <label>选择项目分类:</label>
            <select 
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
              onChange={(e) => {
                const category = e.target.value;
                const firstProject = famousProjects[category][0];
                setSelectedProject(firstProject);
              }}
            >
              {Object.keys(famousProjects).map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>
          
          <div style={{ marginBottom: '10px' }}>
            <label>选择项目:</label>
            <select 
              value={selectedProject}
              onChange={(e) => setSelectedProject(e.target.value)}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            >
              {Object.entries(famousProjects).map(([category, projects]) => (
                <optgroup key={category} label={category}>
                  {projects.map(project => (
                    <option key={project} value={project}>{project}</option>
                  ))}
                </optgroup>
              ))}
            </select>
          </div>
          
          <div style={{ marginBottom: '10px' }}>
            <label>或输入项目 (格式: owner/repo):</label>
            <input
              type="text"
              value={selectedProject}
              onChange={(e) => setSelectedProject(e.target.value)}
              placeholder="例如: apache/iotdb"
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>
          
          <button 
            onClick={handleAnalyze}
            disabled={loading}
            style={{
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              cursor: loading ? 'not-allowed' : 'pointer',
              width: '100%'
            }}
          >
            {loading ? '分析中...' : '🔍 分析项目'}
          </button>
        </div>
        
        <div style={{ flex: 1 }}>
          <h2>操作</h2>
          <div style={{ padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
            <p><strong>当前选中项目：</strong></p>
            <p>{selectedProject}</p>
          </div>
        </div>
      </div>
      
      {error && (
        <div style={{ 
          backgroundColor: '#f8d7da', 
          color: '#721c24', 
          padding: '10px', 
          borderRadius: '5px',
          marginBottom: '20px'
        }}>
          {error}
        </div>
      )}
      
      {analysisData && (
        <div style={{ 
          border: '1px solid #dee2e6', 
          borderRadius: '5px', 
          padding: '20px',
          marginTop: '20px'
        }}>
          <h2>分析结果</h2>
          <p>项目: {analysisData.basic_info?.full_name}</p>
          <p>活跃度分数: {analysisData.activity?.score || 0}</p>
          <p>贡献者数量: {analysisData.community?.total_contributors || 0}</p>
          <p>新手友好度: {analysisData.newbie_friendly_score || 0}%</p>
        </div>
      )}
    </div>
  );
};

export default ProjectExplorer;