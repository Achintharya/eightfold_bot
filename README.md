# Company Research & Account Plan Agent 🤖

An intelligent conversational agent that helps users research companies and generate comprehensive account plans through natural, interactive dialogue.

## 🎯 Overview

This agent provides an intuitive, conversation-first approach to company research. Rather than complex commands or forms, users simply chat with the agent to:
- Research companies from multiple sources
- Generate detailed account plans
- Edit and refine sections interactively
- Get real-time progress updates during research

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **API Keys** (add to `config/.env`):
   ```env
   GROQ_API_KEY=your_groq_api_key
   MISTRAL_API_KEY=your_mistral_api_key
   SERPER_API_KEY=your_serper_api_key  # Optional, falls back to DuckDuckGo
   ```

### Installation

```bash
# Install required packages
pip install -r requirements.txt

# Create necessary directories
mkdir -p data articles account_plans config
```

### Running the Agent

```bash
# Main interactive agent
python company_research_agent.py

# Run demo scenarios
python demo_scenarios.py

# Run tests
python demo_scenarios.py  # Choose option 2 for tests
```

## 💬 Conversation Modes

The agent supports different conversation styles to match user preferences:

### 1. **Efficient Mode** 🎯
- Quick, direct responses
- Minimal explanations
- Perfect for users who know what they want
- Example: "Ready. Company name?" → "Tesla" → "Researching..."

### 2. **Chatty Mode** 😊
- Friendly, detailed responses
- Provides context and explanations
- Great for users who enjoy interaction
- Uses emojis and enthusiasm

### 3. **Confused Mode** 🤔
- Asks for clarification frequently
- Double-checks understanding
- Ideal for testing edge cases
- Shows uncertainty in responses

### 4. **Normal Mode** ⚖️
- Balanced approach
- Professional yet approachable
- Default mode for most users

## 🏗️ Architecture & Design Decisions

### Core Design Philosophy

**Conversation First**: The agent prioritizes natural dialogue over command-based interaction. Users shouldn't need to learn special syntax or commands.

### Key Design Decisions

#### 1. **Modular Architecture**
```
company_research_agent.py
├── CompanyResearchAgent (Main logic)
│   ├── Intent Detection
│   ├── State Management
│   ├── Response Generation
│   └── Research Orchestration
├── InteractiveSession (User interface)
└── Integration with existing modules
    ├── web_context_extract.py (Web scraping)
    ├── context_summarizer.py (Summarization)
    └── article_writer.py (Content generation)
```

**Rationale**: Leverages existing robust modules while adding conversational layer on top.

#### 2. **State-Based Conversation Management**
```python
class ResearchState(Enum):
    IDLE = "idle"
    GATHERING_INFO = "gathering_info"
    RESEARCHING = "researching"
    SUMMARIZING = "summarizing"
    GENERATING_PLAN = "generating_plan"
    EDITING = "editing"
    COMPLETE = "complete"
```

**Rationale**: Clear state tracking enables:
- Contextual responses
- Progress updates
- Error recovery
- User guidance

#### 3. **Intent Detection System**
- Pattern-based intent recognition
- Fallback to general conversation
- Context-aware interpretation

**Rationale**: Balances accuracy with flexibility, allowing natural conversation while maintaining functionality.

#### 4. **Progressive Information Gathering**
```python
queries = [
    f"{company_name} company overview products services",
    f"{company_name} leadership team executives",
    f"{company_name} recent news announcements",
    f"{company_name} challenges problems issues"
]
```

**Rationale**: Comprehensive research from multiple angles ensures thorough account plans.

#### 5. **Real-Time Progress Updates**
- "I'm finding conflicting information about X, should I dig deeper?"
- "Currently researching leadership team..."
- "Summarizing findings..."

**Rationale**: Keeps users engaged and informed, building trust in the process.

## 🎭 Demo Scenarios

### The Confused User 😕
- Unsure what they want
- Needs guidance
- Agent provides gentle steering

### The Efficient User ⚡
- Knows exactly what they need
- Wants quick results
- Agent responds concisely

### The Chatty User 💬
- Enjoys conversation
- Goes off-topic
- Agent redirects politely

### Edge Cases 🔧
- Empty inputs
- Gibberish
- Multiple companies
- Emoji inputs

## 📊 Account Plan Structure

Generated account plans include:
1. **Executive Summary** - High-level overview
2. **Company Overview** - Products, services, market position
3. **Key Stakeholders** - Leadership and decision makers
4. **Business Challenges** - Current pain points
5. **Opportunities** - Potential value propositions
6. **Proposed Solutions** - Tailored recommendations
7. **Engagement Strategy** - Approach for engagement
8. **Success Metrics** - KPIs and measurements
9. **Next Steps** - Actionable items

## 🧪 Testing & Evaluation

### Automated Tests
- Intent detection accuracy
- Company name extraction
- State management
- Conversation mode behavior

### Evaluation Criteria

#### 1. **Conversational Quality** ⭐⭐⭐⭐⭐
- Natural language understanding
- Context awareness
- Appropriate responses
- Personality consistency

#### 2. **Agentic Behavior** ⭐⭐⭐⭐⭐
- Proactive information gathering
- Progress updates
- Error handling
- User guidance

#### 3. **Technical Implementation** ⭐⭐⭐⭐
- Modular design
- Error recovery
- State management
- Integration quality

#### 4. **Intelligence & Adaptability** ⭐⭐⭐⭐⭐
- Multiple conversation modes
- Intent recognition
- Context synthesis
- Plan generation quality

## 🛠️ Technical Features

### Web Scraping & Research
- **Crawl4AI** for advanced extraction (when available)
- **BeautifulSoup** fallback for simple extraction
- **DuckDuckGo** search as primary
- **Serper API** as enhanced search option

### Content Processing
- **CrewAI** for intelligent summarization
- **Mistral AI** for content generation
- Context-aware synthesis

### Data Management
- Atomic file operations
- Thread-safe writes
- Automatic backups
- Version control

## 📁 Project Structure

```
eightfold_bot/
├── company_research_agent.py  # Main agent
├── demo_scenarios.py          # Demo & tests
├── web_context_extract.py     # Web scraping
├── context_summarizer.py      # Summarization
├── article_writer.py          # Content generation
├── README.md                  # Documentation
├── requirements.txt           # Dependencies
├── config/
│   └── .env                  # API keys
├── data/                     # Working data
│   ├── context.json
│   ├── context.txt
│   ├── sources.md
│   └── writing_style.txt
├── articles/                 # Generated articles
└── account_plans/           # Generated plans
```

## 🔄 Workflow

1. **User Input** → Natural language request
2. **Intent Detection** → Understand user's goal
3. **Information Gathering** → Clarify if needed
4. **Research Phase** → Web scraping & extraction
5. **Synthesis** → Summarize findings
6. **Plan Generation** → Create account plan
7. **Interactive Editing** → Refine sections
8. **Output** → Save and present results

## 🎯 Use Cases

### Sales Teams
- Pre-meeting research
- Account planning
- Opportunity identification

### Business Development
- Market research
- Competitive analysis
- Partnership evaluation

### Consultants
- Client research
- Industry analysis
- Strategy development

## 🚧 Known Limitations

1. **API Dependencies** - Requires API keys for full functionality
2. **Research Scope** - Limited to publicly available information
3. **Language** - Currently English only
4. **Rate Limits** - Subject to API rate limitations

## 🔮 Future Enhancements

- [ ] Voice interaction support
- [ ] Multi-language support
- [ ] Historical research tracking
- [ ] Collaborative editing
- [ ] Export to CRM systems
- [ ] Custom research templates
- [ ] Sentiment analysis
- [ ] Competitor comparison

## 📝 Example Interaction

```
Agent: Hello! I'm here to help you research companies and create account plans. 
       Which company would you like to research?

You: I'm interested in Tesla but not sure what I need exactly

Agent: No problem! Let me research Tesla for you. I'll gather information about 
       their products, leadership, recent news, and challenges. This will help 
       us create a comprehensive account plan.

Agent: Starting research on Tesla...
       I'll search for information about this company...

[Progress updates during research...]

Agent: Research complete! I've generated an account plan for Tesla.
       Account plan generated and saved to account_plan_Tesla_20231123_194500.md

You: Can you edit the opportunities section to focus more on sustainability?

Agent: Current opportunities content:
       [Shows current content]
       
       Please provide the new content or describe the changes you'd like:
```

## 🏆 Why This Design?

### Prioritizing Conversation Quality
- Multiple personality modes cater to different users
- Natural language processing for intuitive interaction
- Context-aware responses maintain conversation flow

### Demonstrating Agentic Behavior
- Proactive research from multiple angles
- Real-time progress updates build trust
- Autonomous decision-making in research process

### Technical Excellence
- Modular architecture for maintainability
- Robust error handling and recovery
- Integration with proven tools

### Intelligence & Adaptability
- Adapts conversation style to user preference
- Learns from conversation context
- Synthesizes complex information into actionable plans

## 📧 Support & Contribution

For issues, suggestions, or contributions, please create an issue or pull request.

## 📄 License

MIT License - Feel free to use and modify as needed.

---

**Built with ❤️ for natural, intelligent company research**
