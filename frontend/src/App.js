import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [agentStatus, setAgentStatus] = useState('idle');
  const [currentCompany, setCurrentCompany] = useState(null);
  const [accountPlans, setAccountPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [showPlanModal, setShowPlanModal] = useState(false);
  const [editingPlan, setEditingPlan] = useState(null);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch agent status periodically
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await axios.get(`${API_URL}/status`);
        setAgentStatus(response.data.state);
        setCurrentCompany(response.data.current_company);
      } catch (error) {
        console.error('Error fetching status:', error);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  // Fetch account plans
  const fetchPlans = async () => {
    try {
      const response = await axios.get(`${API_URL}/plans`);
      setAccountPlans(response.data.plans);
    } catch (error) {
      console.error('Error fetching plans:', error);
    }
  };

  useEffect(() => {
    fetchPlans();
  }, []);

  // Send message to agent
  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage;
    setInputMessage('');
    setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: userMessage
      });

      // Check if response includes a plan summary
      let displayContent = response.data.response;
      if (response.data.plan_summary) {
        displayContent += "\n\n**Account Plan Summary:**\n" + response.data.plan_summary;
      }

      setMessages(prev => [...prev, { 
        type: 'agent', 
        content: displayContent 
      }]);

      // Refresh plans if a new one was created
      if (response.data.state === 'complete' || response.data.plan_created) {
        fetchPlans();
      }

      // If editing mode, update the editing plan
      if (response.data.editing_plan) {
        setEditingPlan(response.data.editing_plan);
      }
    } catch (error) {
      setMessages(prev => [...prev, { 
        type: 'error', 
        content: 'Error communicating with agent: ' + error.message 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // View account plan
  const viewPlan = async (filename) => {
    try {
      const response = await axios.get(`${API_URL}/plan/${filename}`);
      setSelectedPlan(response.data.content);
      setShowPlanModal(true);
    } catch (error) {
      console.error('Error fetching plan:', error);
    }
  };

  // Edit plan section
  const editPlanSection = async (section, instructions) => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${API_URL}/edit-plan`, {
        section: section,
        instructions: instructions
      });

      setMessages(prev => [...prev, { 
        type: 'agent', 
        content: response.data.response 
      }]);

      // Refresh plans after edit
      if (response.data.success) {
        fetchPlans();
      }
    } catch (error) {
      setMessages(prev => [...prev, { 
        type: 'error', 
        content: 'Error editing plan: ' + error.message 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Get status badge color
  const getStatusColor = () => {
    switch (agentStatus) {
      case 'idle': return '#6b7280';
      case 'researching': return '#3b82f6';
      case 'generating_plan': return '#f59e0b';
      case 'complete': return '#10b981';
      default: return '#6b7280';
    }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <h1>🏢 Company Research Agent</h1>
        <div className="status-bar">
          <span className="status-badge" style={{ backgroundColor: getStatusColor() }}>
            {agentStatus.replace('_', ' ').toUpperCase()}
          </span>
          {currentCompany && (
            <span className="current-company">
              Researching: <strong>{currentCompany}</strong>
            </span>
          )}
        </div>
      </header>

      <div className="main-container">
        {/* Chat Section */}
        <div className="chat-section">
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.type}`}>
                <div className="message-label">
                  {msg.type === 'user' ? '👤 You' : msg.type === 'agent' ? '🤖 Agent' : '⚠️ Error'}
                </div>
                <div className="message-content">
                  {msg.type === 'agent' ? (
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  ) : (
                    msg.content
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message agent">
                <div className="message-label">🤖 Agent</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask about a company or type 'help' for assistance..."
              disabled={isLoading}
            />
            <button onClick={sendMessage} disabled={isLoading}>
              Send
            </button>
          </div>
        </div>

        {/* Sidebar */}
        <div className="sidebar">
          {/* Account Plans */}
          <div className="plans-section">
            <h3>📄 Account Plans</h3>
            <div className="plans-list">
              {accountPlans.length === 0 ? (
                <p className="no-plans">No plans generated yet</p>
              ) : (
                accountPlans.map((plan, index) => (
                  <div key={index} className="plan-item" onClick={() => viewPlan(plan.filename)}>
                    <div className="plan-company">{plan.company}</div>
                    <div className="plan-timestamp">{plan.timestamp}</div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Current Research Status */}
          {currentCompany && agentStatus !== 'idle' && (
            <div className="current-research">
              <h3>📊 Current Research</h3>
              <div className="research-info">
                <p><strong>Company:</strong> {currentCompany}</p>
                <p><strong>Status:</strong> {agentStatus.replace('_', ' ')}</p>
                {agentStatus === 'complete' && (
                  <button onClick={() => setInputMessage('Show me a summary of the plan')}>
                    View Summary
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="quick-actions">
            <h3>⚡ Quick Actions</h3>
            <button onClick={() => setInputMessage('help')}>Get Help</button>
            <button onClick={() => setInputMessage('status')}>Check Status</button>
            <button onClick={() => setInputMessage('Research Tesla')}>Research Tesla</button>
          </div>
        </div>
      </div>

      {/* Plan Modal */}
      {showPlanModal && (
        <div className="modal-overlay" onClick={() => setShowPlanModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setShowPlanModal(false)}>
              ✕
            </button>
            <div className="plan-content">
              <ReactMarkdown>{selectedPlan}</ReactMarkdown>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
