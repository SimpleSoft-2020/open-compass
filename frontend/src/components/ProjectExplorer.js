// frontend/src/components/ProjectExplorer.js
import React, { useState } from 'react';
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
    setAnalysisData(null);
    
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

  const clearResults = () => {
    setAnalysisData(null);
  };

  // 活跃度分析组件
  const ActivityAnalysis = ({ activityData }) => {
    const score = activityData?.score || 0;
    const trend = activityData?.trend || "unknown";
    
    const trendEmojis = {
      "increasing": "↗️",
      "decreasing": "↘️",
      "stable": "➡️",
      "unknown": "❓"
    };
    
    const trendDescriptions = {
      "increasing": "增长中",
      "decreasing": "下降中",
      "stable": "稳定",
      "unknown": "未知"
    };
    
    // 计算颜色 based on score
    let gaugeColor = 'lightcoral';
    if (score > 700) gaugeColor = 'lightgreen';
    else if (score > 300) gaugeColor = 'gold';
    
    return (
      <div>
        <h3>项目活跃度分析</h3>
        <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
          <div style={{ flex: 1 }}>
            <div style={{ 
              width: '200px', 
              height: '200px', 
              borderRadius: '50%', 
              backgroundColor: gaugeColor,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexDirection: 'column'
            }}>
              <span style={{ fontSize: '24px', fontWeight: 'bold' }}>{score}</span>
              <span>活跃度评分</span>
            </div>
          </div>
          <div style={{ flex: 1 }}>
            <h4>趋势分析</h4>
            <p style={{ fontSize: '20px' }}>
              {trendEmojis[trend] || '❓'} <strong>{trendDescriptions[trend] || '未知趋势'}</strong>
            </p>
            {trend === "increasing" && (
              <div style={{ padding: '10px', backgroundColor: '#d4edda', borderColor: '#c3e6cb', color: '#155724' }}>
                项目活跃度正在增长，是一个积极的信号
              </div>
            )}
            {trend === "decreasing" && (
              <div style={{ padding: '10px', backgroundColor: '#fff3cd', borderColor: '#ffeaa7', color: '#856404' }}>
                项目活跃度有所下降，可能需要关注
              </div>
            )}
            {trend === "stable" && (
              <div style={{ padding: '10px', backgroundColor: '#d1ecf1', borderColor: '#bee5eb', color: '#0c5460' }}>
                项目活跃度保持稳定
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // 社区分析组件
  const CommunityAnalysis = ({ communityData }) => {
    const totalContributors = communityData?.total_contributors || 0;
    const activeContributors = communityData?.active_contributors || 0;
    const busFactor = communityData?.bus_factor || 0;
    const keyContributors = communityData?.key_contributors || [];
    
    return (
      <div>
        <h3>社区健康度分析</h3>
        <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>👥 总贡献者数</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{totalContributors}</p>
          </div>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>🏃 活跃贡献者数</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{activeContributors}</p>
          </div>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>🚌 Bus Factor</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{busFactor}</p>
          </div>
        </div>
        
        {busFactor <= 2 ? (
          <div style={{ padding: '10px', backgroundColor: '#f8d7da', borderColor: '#f5c6cb', color: '#721c24', marginBottom: '20px' }}>
            ⚠️ Bus Factor 过低，项目风险较高（关键人员流失可能严重影响项目）
          </div>
        ) : busFactor <= 4 ? (
          <div style={{ padding: '10px', backgroundColor: '#fff3cd', borderColor: '#ffeaa7', color: '#856404', marginBottom: '20px' }}>
            ℹ️ Bus Factor 适中，建议培养更多核心贡献者
          </div>
        ) : (
          <div style={{ padding: '10px', backgroundColor: '#d4edda', borderColor: '#c3e6cb', color: '#155724', marginBottom: '20px' }}>
            ✅ Bus Factor 良好，项目人员分布较为均衡
          </div>
        )}
        
        {keyContributors.length > 0 && (
          <div>
            <h4>🔑 关键贡献者</h4>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#f8f9fa' }}>
                  <th style={{ border: '1px solid #ddd', padding: '8px' }}>姓名</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px' }}>贡献数</th>
                </tr>
              </thead>
              <tbody>
                {keyContributors.map((contributor, index) => (
                  <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f8f9fa' }}>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{contributor.name}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{contributor.contributions}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    );
  };

  // 问题分析组件
  const IssueAnalysis = ({ issuesData }) => {
    const newIssues = issuesData?.new_issues || 0;
    const closedIssues = issuesData?.closed_issues || 0;
    const resolutionEfficiency = issuesData?.resolution_efficiency || 0;
    const avgResponseTime = issuesData?.avg_response_time || 0;
    
    return (
      <div>
        <h3>问题处理分析</h3>
        <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>🆕 新问题数</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{newIssues}</p>
          </div>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>✅ 已关闭问题</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{closedIssues}</p>
          </div>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>⏱️ 解决效率</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{resolutionEfficiency}%</p>
          </div>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
            <h4>⏰ 平均响应时间</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{avgResponseTime}小时</p>
          </div>
        </div>
        
        {resolutionEfficiency >= 80 ? (
          <div style={{ padding: '10px', backgroundColor: '#d4edda', borderColor: '#c3e6cb', color: '#155724' }}>
            ✅ 问题解决效率很高
          </div>
        ) : resolutionEfficiency >= 60 ? (
          <div style={{ padding: '10px', backgroundColor: '#d1ecf1', borderColor: '#bee5eb', color: '#0c5460' }}>
            ℹ️ 问题解决效率适中
          </div>
        ) : (
          <div style={{ padding: '10px', backgroundColor: '#fff3cd', borderColor: '#ffeaa7', color: '#856404' }}>
            ⚠️ 问题解决效率较低，可能存在积压
          </div>
        )}
      </div>
    );
  };

  // 贡献建议组件
  const ContributionRecommendations = ({ owner, repo }) => {
    const [recommendations, setRecommendations] = useState([]);
    const [recLoading, setRecLoading] = useState(false);
    
    React.useEffect(() => {
      const fetchRecommendations = async () => {
        if (!owner || !repo) return;
        
        setRecLoading(true);
        try {
          const response = await axios.get(`/api/v1/projects/${owner}/${repo}/recommendations`);
          if (response.data.success) {
            setRecommendations(response.data.data.recommendations || []);
          }
        } catch (err) {
          console.error('获取贡献建议失败:', err);
        } finally {
          setRecLoading(false);
        }
      };
      
      fetchRecommendations();
    }, [owner, repo]);
    
    const priorityColors = {
      "high": "🔴",
      "medium": "🟡",
      "low": "🟢"
    };
    
    const priorityNames = {
      "high": "高优先级",
      "medium": "中优先级",
      "low": "低优先级"
    };
    
    // 按优先级分组
    const groupedRecommendations = recommendations.reduce((acc, rec) => {
      if (!acc[rec.priority]) {
        acc[rec.priority] = [];
      }
      acc[rec.priority].push(rec);
      return acc;
    }, {});
    
    return (
      <div>
        <h3>个性化贡献建议</h3>
        
        {recLoading ? (
          <p>正在加载贡献建议...</p>
        ) : Object.keys(groupedRecommendations).length > 0 ? (
          <div>
            {['high', 'medium', 'low'].map(priority => {
              const recs = groupedRecommendations[priority];
              return recs ? (
                <div key={priority} style={{ marginBottom: '20px' }}>
                  <h4>{priorityColors[priority]} {priorityNames[priority]}建议</h4>
                  {recs.map((rec, index) => (
                    <div key={index} style={{ 
                      border: '1px solid #ddd', 
                      borderRadius: '5px', 
                      padding: '15px', 
                      marginBottom: '10px',
                      backgroundColor: '#f8f9fa'
                    }}>
                      <h5>{rec.title}</h5>
                      <p>{rec.description}</p>
                      <small>类型: {rec.type}</small>
                    </div>
                  ))}
                </div>
              ) : null;
            })}
          </div>
        ) : (
          <p>暂无具体的贡献建议</p>
        )}
        
        <div style={{ marginTop: '20px' }}>
          <h4>通用贡献指南</h4>
          <ul>
            <li><strong>阅读贡献指南</strong> - 在开始之前，请务必阅读项目的 CONTRIBUTING.md 文件</li>
            <li><strong>从小事做起</strong> - 可以从修复拼写错误、改进文档开始</li>
            <li><strong>参与讨论</strong> - 在问题或PR下发表建设性意见也是重要贡献</li>
            <li><strong>遵守规范</strong> - 遵循项目的代码风格和提交规范</li>
            <li><strong>保持耐心</strong> - 开源社区的响应可能需要一些时间</li>
          </ul>
        </div>
      </div>
    );
  };

  // 主要分析结果显示组件
  const AnalysisDisplay = ({ data }) => {
    const basicInfo = data.basic_info || {};
    const activityScore = data.activity?.score || 0;
    const contributorCount = data.community?.total_contributors || 0;
    const newbieScore = data.newbie_friendly_score || 0;
    
    const [activeTab, setActiveTab] = useState('activity');
    
    return (
      <div style={{ 
        border: '1px solid #dee2e6', 
        borderRadius: '5px', 
        padding: '20px',
        marginTop: '20px'
      }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '20px'
        }}>
          <h2>📋 项目基本信息 - {basicInfo.full_name || ''}</h2>
          <button 
            onClick={clearResults}
            style={{
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              cursor: 'pointer',
              borderRadius: '4px'
            }}
          >
            🗑️ 清除结果
          </button>
        </div>
        
        <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px', textAlign: 'center' }}>
            <h4>📈 活跃度分数</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{activityScore}</p>
          </div>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px', textAlign: 'center' }}>
            <h4>👥 贡献者数量</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{contributorCount}</p>
          </div>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px', textAlign: 'center' }}>
            <h4>👶 新手友好度</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{newbieScore}%</p>
          </div>
          <div style={{ flex: 1, padding: '15px', border: '1px solid #ddd', borderRadius: '5px', textAlign: 'center' }}>
            <h4>📁 平台</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{basicInfo.platform?.toUpperCase() || 'GITHUB'}</p>
          </div>
        </div>
        
        <div>
          <div style={{ 
            display: 'flex', 
            borderBottom: '1px solid #dee2e6',
            marginBottom: '20px'
          }}>
            <button
              onClick={() => setActiveTab('activity')}
              style={{
                padding: '10px 20px',
                border: 'none',
                backgroundColor: activeTab === 'activity' ? '#007bff' : '#f8f9fa',
                color: activeTab === 'activity' ? 'white' : 'black',
                cursor: 'pointer',
                borderBottom: activeTab === 'activity' ? '3px solid #007bff' : 'none'
              }}
            >
              📊 活跃度分析
            </button>
            <button
              onClick={() => setActiveTab('community')}
              style={{
                padding: '10px 20px',
                border: 'none',
                backgroundColor: activeTab === 'community' ? '#007bff' : '#f8f9fa',
                color: activeTab === 'community' ? 'white' : 'black',
                cursor: 'pointer',
                borderBottom: activeTab === 'community' ? '3px solid #007bff' : 'none'
              }}
            >
              👥 社区分析
            </button>
            <button
              onClick={() => setActiveTab('issues')}
              style={{
                padding: '10px 20px',
                border: 'none',
                backgroundColor: activeTab === 'issues' ? '#007bff' : '#f8f9fa',
                color: activeTab === 'issues' ? 'white' : 'black',
                cursor: 'pointer',
                borderBottom: activeTab === 'issues' ? '3px solid #007bff' : 'none'
              }}
            >
              🐛 问题分析
            </button>
            <button
              onClick={() => setActiveTab('recommendations')}
              style={{
                padding: '10px 20px',
                border: 'none',
                backgroundColor: activeTab === 'recommendations' ? '#007bff' : '#f8f9fa',
                color: activeTab === 'recommendations' ? 'white' : 'black',
                cursor: 'pointer',
                borderBottom: activeTab === 'recommendations' ? '3px solid #007bff' : 'none'
              }}
            >
              💡 贡献建议
            </button>
          </div>
          
          <div>
            {activeTab === 'activity' && <ActivityAnalysis activityData={data.activity} />}
            {activeTab === 'community' && <CommunityAnalysis communityData={data.community} />}
            {activeTab === 'issues' && <IssueAnalysis issuesData={data.issues} />}
            {activeTab === 'recommendations' && (
              <ContributionRecommendations 
                owner={basicInfo.owner} 
                repo={basicInfo.name} 
              />
            )}
          </div>
        </div>
      </div>
    );
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
              width: '100%',
              fontSize: '16px'
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
          
          {analysisData && (
            <button 
              onClick={clearResults}
              style={{
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                padding: '10px 20px',
                cursor: 'pointer',
                width: '100%',
                marginTop: '10px',
                fontSize: '16px'
              }}
            >
              🗑️ 清除结果
            </button>
          )}
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
      
      {analysisData && <AnalysisDisplay data={analysisData} />}
    </div>
  );
};

export default ProjectExplorer;