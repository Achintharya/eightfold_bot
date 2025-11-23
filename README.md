# Company Research & Account Plan Agent 🤖

An intelligent conversational agent with a modern web interface that helps users research companies and generate comprehensive account plans through natural, interactive dialogue.

## 🎯 Overview

This agent provides an intuitive, conversation-first approach to company research with a full-stack web application. Rather than complex commands or forms, users simply chat with the agent to:
- Research companies from multiple sources with intelligent caching
- Generate detailed account plans with concise summaries
- Edit and refine sections interactively through conversation
- Get real-time progress updates during research
- Access everything through a clean, modern web interface

## ✨ Recent Updates (v2.0)

### New Features
- **🚀 Web Interface**: Modern React frontend with real-time updates
- **💾 Smart Caching**: Automatic caching of research data to avoid redundant searches
- **📋 Plan Summaries**: Concise summaries displayed directly in chat
- **✏️ Conversational Editing**: Natural language editing of plan sections
- **🎯 Cleaner UI**: Removed unnecessary features for a focused experience

### Performance Improvements
- Instant loading of previously researched companies
- No redundant API calls for cached data
- Faster response times with optimized backend

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Node.js 14+** and npm installed
3. **API Keys** (add to `config/.env`):
   ```env
   GROQ_API_KEY=your_groq_api_key
   MISTRAL_API_KEY=your_mistral_api_key
   SERPER_API_KEY=your_serper_api_key  # Optional, falls back to DuckDuckGo
   ```

### Installation

```bash
# Clone the repository
git clone https://github.com/Achintharya/eightfold_bot.git
cd eightfold_bot

# Install Python dependencies
pip install -r requirements.txt

# Install React frontend dependencies
cd frontend
npm install
cd ..

# Create necessary directories
mkdir -p data articles account_plans config
```

### Running the Application

#### Option 1: Web Application (Recommended)

```bash
# Terminal 1: Start the backend server
python main.py

# Terminal 2: Start the frontend
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000 (or 3001 if 3000 is in use)
- Backend API: http://localhost:8000

#### Option 2: Command Line Interface

```bash
# Run the interactive CLI agent
python src/company_research_agent.py

# Run demo scenarios
python src/demo_scenarios.py
```

## 💻 Web Interface Features

### Main Chat Interface
- **Real-time messaging** with the AI agent
- **Typing indicators** for better UX
- **Markdown rendering** for formatted responses
- **Status badges** showing current agent state

### Account Plans Sidebar
- **List of all generated plans** with timestamps
- **Click to view** full plan in modal
- **Automatic refresh** when new plans are created

### Quick Actions
- **Get Help** - Learn what the agent can do
- **Check Status** - See current research progress
- **Research Tesla** - Quick demo button

### Smart Features
- **Cache Indicator**: Shows when using cached data
- **Plan Summaries**: Key points displayed inline
- **Edit Mode**: Conversational editing interface

## 🧠 Intelligent Caching System

### How It Works
1. **First Research**: Performs full web search and analysis
2. **Data Storage**: Caches research data and generated plans
3. **Subsequent Requests**: Instantly loads from cache
4. **User Control**: Can request fresh research if needed

### Cache Benefits
- ⚡ **Instant Response**: No waiting for repeated queries
- 💰 **API Savings**: Reduces API calls and costs
- 🔄 **Consistency**: Same data for plan edits
- 📊 **Performance**: Handles rate limits gracefully

### Example Flow
```
User: "Research Tesla"
Agent: "Starting fresh research..." [Takes 30-60 seconds]

User: "Research Tesla" (again)
Agent: "✅ Using cached research data..." [Instant]
```

## 📝 Plan Summaries

### Automatic Summary Generation
When a plan is created or loaded, the agent automatically generates a concise summary showing:
- **Executive Summary** (first 200 characters)
- **Key Challenges** (main points)
- **Main Opportunities** (highlights)
- **Proposed Solutions** (core recommendations)
- **Next Steps** (immediate actions)

### Benefits
- Quick overview without opening full plan
- Essential information at a glance
- Maintains context during conversations
- Perfect for quick reviews

## ✏️ Conversational Editing

### Three Edit Modes

#### 1. Replace Mode
```
User: "Edit the executive summary"
Agent: [Shows current content]
User: [Provides new content]
Agent: "✓ Section updated"
```

#### 2. Regenerate Mode
```
User: "Edit the opportunities section"
Agent: [Shows current content and options]
User: "Regenerate with focus on sustainability"
Agent: "✓ Section regenerated with focus on sustainability"
```

#### 3. Enhance Mode
```
User: "Edit the solutions section"
Agent: [Shows current content]
User: "Add more details about implementation timeline"
Agent: "✓ Section enhanced with timeline details"
```

## 🏗️ Architecture

### Full-Stack Design
```
eightfold_bot/
├── Backend (FastAPI)
│   ├── main.py                    # API server
│   ├── src/
│   │   ├── company_research_agent.py  # Core agent logic
│   │   ├── web_context_extract.py     # Web scraping
│   │   ├── context_summarizer.py      # Summarization
│   │   └── article_writer.py          # Content generation
│   └── account_plans/              # Generated plans storage
│
├── Frontend (React)
│   ├── src/
│   │   ├── App.js                 # Main React component
│   │   ├── App.css                # Styling
│   │   └── index.js               # Entry point
│   └── public/
│
└── Configuration
    ├── requirements.txt            # Python dependencies
    ├── config/.env                # API keys
    └── data/                      # Cache and working data
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Main chat interface with caching support |
| `/status` | GET | Get agent status and current company |
| `/plans` | GET | List all generated account plans |
| `/plan/{filename}` | GET | Get specific plan content |
| `/edit-plan` | POST | Edit plan sections |
| `/cache/status` | GET | Check cache status |
| `/cache/clear` | POST | Clear cache |

## 📊 Account Plan Structure

Generated account plans include:
1. **Executive Summary** - High-level overview with innovation focus
2. **Company Overview** - Products, services, market position
3. **Key Stakeholders** - Leadership and decision makers
4. **Business Challenges** - Current pain points and issues
5. **Opportunities** - Potential value propositions
6. **Proposed Solutions** - Tailored recommendations
7. **Engagement Strategy** - Approach for engagement
8. **Success Metrics** - KPIs and measurements
9. **Next Steps** - Actionable items

## 🎭 Conversation Modes

The agent supports different conversation styles to match user preferences:

| Mode | Description | Best For |
|------|-------------|----------|
| **Efficient 🎯** | Quick, direct responses | Power users |
| **Chatty 😊** | Friendly, detailed responses | First-time users |
| **Confused 🤔** | Asks for clarification | Testing edge cases |
| **Normal ⚖️** | Balanced approach | Most users |

## 🧪 Testing

### Test the Application
```bash
# Test backend API
curl http://localhost:8000/status

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Research Tesla"}'

# Run automated tests
python src/demo_scenarios.py
```

### Key Test Scenarios
- ✅ Fresh company research
- ✅ Cached data retrieval
- ✅ Plan summary generation
- ✅ Conversational editing
- ✅ Error handling and recovery

## 🔄 Typical Workflow

1. **Initial Research**
   - User: "Research Microsoft"
   - Agent performs comprehensive web search
   - Generates account plan with summary

2. **Quick Review**
   - Summary displayed in chat
   - Full plan available in sidebar

3. **Editing**
   - User: "Edit the challenges section"
   - Agent shows current content
   - User provides changes conversationally

4. **Cached Access**
   - User: "Show me Microsoft plan again"
   - Instant loading from cache

## 🚧 Known Limitations

1. **API Dependencies** - Requires API keys for full functionality
2. **Rate Limits** - DuckDuckGo may rate limit during heavy use
3. **Research Scope** - Limited to publicly available information
4. **Language** - Currently English only
5. **Browser Compatibility** - Best on modern browsers

## 🔮 Future Enhancements

- [ ] Real-time collaborative editing
- [ ] Export to multiple formats (PDF, DOCX)
- [ ] Integration with CRM systems
- [ ] Voice interaction support
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Custom research templates
- [ ] Competitor comparison tools
- [ ] Automated plan updates
- [ ] Mobile app version

## 📝 Example Interaction

```
Agent: Hello! I'm here to help you research companies and create account plans. 
       Which company would you like to research?

You: Research Tesla

Agent: Starting fresh research on Tesla...
       I'll search for information about this company...
       
       [After research completes]
       Account plan generated and saved!
       
       📋 Account Plan Summary for Tesla
       
       Executive Summary:
       Tesla is navigating complex challenges including...
       
       Key Challenges:
       - Public backlash and controversy...
       - Supply chain complexities...
       
       [Summary continues...]

You: Edit the executive summary to focus more on innovation

Agent: Current Executive Summary content:
       [Shows current content]
       
       You can:
       1. Replace - Provide new content
       2. Regenerate - Say "regenerate with focus on [aspect]"
       3. Enhance - Say "add [details]"
       
You: Regenerate with focus on technological leadership

Agent: ✓ Executive Summary regenerated with focus on technological leadership
       [Shows new content]
```

## 🐛 Troubleshooting

### CORS Issues
If you see CORS errors, ensure the backend is configured for your frontend port:
```python
# main.py
allow_origins=["http://localhost:3000", "http://localhost:3001"]
```

### Rate Limiting
If experiencing DuckDuckGo rate limits:
- Wait a few minutes between searches
- Consider using Serper API key for better limits

### Port Conflicts
If ports are already in use:
- Backend: Change port in `main.py`
- Frontend: It will auto-select next available port

## 📧 Support & Contribution

For issues, suggestions, or contributions:
- Create an issue on GitHub
- Submit a pull request
- Contact: [your-email@example.com]

## 📄 License

MIT License - Feel free to use and modify as needed.

## 🙏 Acknowledgments

- Built with FastAPI and React
- Powered by Groq and Mistral AI
- Web scraping via BeautifulSoup and Crawl4AI
- UI components from React ecosystem

---

**Built with ❤️ for intelligent, efficient company research**

**Version 2.0** | **Last Updated: November 2024**
