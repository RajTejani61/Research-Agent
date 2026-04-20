<div align="center">

# Research Agent 🤖

An intelligent AI-powered research assistant that automatically generates research questions, searches the web, creates comprehensive documents with proper citations, and self-evaluates its output quality. Built with **LangGraph** for robust workflow orchestration and **Streamlit** for an intuitive UI.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0%2B-green?logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIj48cGF0aCBkPSJNMjAgNHYxNmEzIDMgMCAwIDEtMyAzSDdhMyAzIDAgMCAxLTMtM1Y0YTMgMyAwIDAgMSAzLTNoMTBhMyAzIDAgMCAxIDMgM3oiLz48cGF0aCBkPSJNMTIgOGw0IDRtLTQgNGwtNC00Ii8+PC9zdmc+)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Mistral AI](https://img.shields.io/badge/Mistral%20AI-2512-orange?logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIvPjxwYXRoIGQ9Ik0xMiA4bDQgNG00LTQ0bC00IDQiLz48L3N2Zz4=)](https://mistral.ai/)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20Store-purple?logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIj48cGF0aCBkPSJNMTIgMmwxMCAxMHYxMEgyVjEyTDEyIDJ6Ii8+PC9zdmc+)](https://www.pinecone.io/)
[![Tavily](https://img.shields.io/badge/Tavily-Search-cyan?logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIj48Y2lyY2xlIGN4PSIxMSIgY3k9IjExIiByPSI4Ii8+PHBhdGggZD0iTTE1IDE1bDQtNG00LTQ0bC00IDQiLz48L3N2Zz4=)](https://tavily.com/)

</div>

## 🌟 Features

| Feature                  | Description                                                                      |
| ------------------------ | -------------------------------------------------------------------------------- |
| **Intelligent Research** | Automatically breaks down complex queries into focused research questions        |
| **Web Search**           | Searches the web using Tavily API for up-to-date information                     |
| **Citation Management**  | Properly cites all sources using numbered citations with full URLs               |
| **Semantic Caching**     | Caches research results to provide instant responses for repeat queries          |
| **Auto-Retry**           | Automatically rewrites questions or documents if quality score is low (<70%)     |
| **Real-time Streaming**  | Streams the research document as it's being written                              |
| **Quality Evaluation**   | Self-evaluates research relevance and coverage, provides improvement suggestions |
| **Dual Interface**       | Both terminal-based CLI and beautiful Streamlit web UI                           |

---

## 📑 Quick Navigation

- [🏗️ Architecture](#-architecture)
- [🚀 Quick Start](#-quick-start)
- [🎯 Usage](#-usage)
- [🔧 Configuration](#-configuration)
- [📊 Research Workflow](#-research-workflow)
- [🎨 UI Features](#-ui-features)
- [🗂️ Project Structure](#️-project-structure)
- [🔍 Technical Details](#-technical-details)
- [🐛 Troubleshooting](#-troubleshooting)

---

## 🏗️ Architecture

```mermaid
flowchart TD
    Start([User Query]) --> Cache[Cache Check<br/>Pinecone]
    Cache -->|Cache Hit| Return[Return Cached Results]
    Cache -->|Cache Miss| Questions[Create Questions<br/>Mistral AI]
    Questions --> Search[Tavily Web Search]
    Search --> Document[Create Document<br/>with Citations]
    Document --> Evaluate[Evaluate Quality<br/>Relevance + Coverage]
    Evaluate -->|Score ≥ 0.7| Return
    Evaluate -->|Score < 0.7<br/>Relevance Low| Questions
    Evaluate -->|Score < 0.7<br/>Coverage Low| Document

    style Start fill:#e1f5ff,stroke:#0277bd,color:#01579b
    style Return fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
    style Cache fill:#fff3e0,stroke:#ef6c00,color:#e65100
    style Questions fill:#e3f2fd,stroke:#0288d1,color:#01579b
    style Search fill:#f3e5f5,stroke:#7b1fa2,color:#4a148c
    style Document fill:#e8f5e9,stroke:#388e3c,color:#1b5e20
    style Evaluate fill:#fce4ec,stroke:#c2185b,color:#880e4f
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- API keys for:
  - **Mistral AI** (for LLM)
  - **Google AI** (for embeddings)
  - **Pinecone** (for vector store)
  - **Tavily** (for web search)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Research-Agent
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv

   # On Windows (Command Prompt)
   venv\Scripts\activate

   # On Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # On Windows (Git Bash)
   source venv/Scripts/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```env
   # Required API Keys
   MISTRAL_API_KEY=your_mistral_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

   **Getting API Keys:**
   - **Mistral AI**: [Sign up at mistral.ai](https://console.mistral.ai/)
   - **Google AI**: [Get API key](https://makersuite.google.com/app/apikey)
   - **Pinecone**: [Create free account](https://www.pinecone.io/)
   - **Tavily**: [Get API key](https://tavily.com/)

## 🎯 Usage

### Option 1: Streamlit Web UI (Recommended)

Launch the beautiful web interface:

```bash
streamlit run Frontend.py
```

The UI features:

- Clean, modern design with real-time streaming
- Live status updates for each research phase
- Downloadable research documents
- Source citations with clickable links
- Quality evaluation scores with visual indicators
- Sidebar with helpful information

### Option 2: Terminal/CLI

Run research directly from the terminal:

```bash
python main.py
```

You'll be prompted to enter a research query, and the document will stream directly to your terminal.

## 🔧 Configuration

### Models & Services (config.py)

The system uses the following configuration (can be customized in `config.py`):

```python
# LLM Model
model = ChatMistralAI(model_name="mistral-large-2512")

# Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# Vector Store for Semantic Cache
VECTORSTORE = PineconeVectorStore(
    index_name="research-agent-semantic-cache",
    embedding=embeddings,
)

# Cache Similarity Threshold
CACHE_DISTANCE = 0.7
```

## 📊 Research Workflow

The research agent follows this intelligent workflow:

1. **Check Cache** → Check if similar query exists in semantic cache
2. **Generate Questions** → Create 4-6 focused research questions based on query
3. **Web Research** → Search web using Tavily API for each question
4. **Create Document** → Write comprehensive document with proper citations
5. **Evaluate Quality** → Score relevance and coverage (0-1 scale)
6. **Auto-Retry** → If score < 0.7, rewrite questions or document (up to 3 attempts)
7. **Return Results** → Provide final document with evaluation and sources

## 📝 Example Usage

### Query: "Best specialty coffee shops in India"

**What happens behind the scenes:**

1. **Cache Check**: Looks for similar queries in cache
2. **Question Generation**: Creates questions like:
   - "What are the top-rated specialty coffee shops in major Indian cities?"
   - "Which Indian coffee shops are known for sourcing high-quality beans?"
   - "What unique brewing methods do Indian specialty coffee shops offer?"
3. **Web Search**: Tavily searches for each question
4. **Document Creation**: Writes structured document with sections for each question
5. **Citation Management**: Every factual sentence ends with citation `[1](url)`
6. **Quality Evaluation**: Scores relevance (how well it answers "best shops") and coverage
7. **Auto-Retry**: If needed, rewrites questions with better focus or regenerates document

## 🎨 UI Features

### Streamlit Interface

The Streamlit UI (`Frontend.py`) provides:

- **Real-time Streaming**: Watch the document being written live
- **Status Updates**: Clear indicators for each phase of research
- **Source Display**: Clickable links to all sources used
- **Quality Metrics**: Visual score with progress bar and color coding
- **Download Button**: Save research as Markdown file
- **Sidebar Info**: Helpful tips and feature explanations
- **Clear Results**: Reset and run new research

### Quality Score Visualization

- 🟢 **80-100%**: Excellent quality
- 🟡 **50-79%**: Good quality
- 🔴 **0-49%**: Needs improvement (triggers retry)

## 🗂️ Project Structure

```
Research-Agent/
├── main.py                 # CLI entry point
├── Frontend.py            # Streamlit UI
├── graph.py               # LangGraph workflow
├── config.py              # Model & API configuration
├── States.py              # State schemas
├── nodes.py               # Workflow nodes
├── cache.py               # Semantic cache logic
├── Prompts.py             # Prompt templates
├── requirements.txt       # Python dependencies
└── .env                   # API keys (create this)
```

## 🔍 Technical Details

### State Management (States.py)

The agent uses a centralized state object (`AgnentState`) that tracks:

- User query and research questions
- Research chunks from web search
- Generated document
- Quality scores and improvement suggestions
- Retry counts for questions and documents

### Prompt Templates (Prompts.py)

Three specialized prompts:

1. **Question Generation**: Creates focused, researchable questions
2. **Document Creation**: Writes factual documents with strict citation rules
3. **Evaluation**: Scores relevance and coverage, suggests improvements

### LangGraph Workflow (graph.py)

Directed graph with conditional routing:

- **Linear flow**: Cache → Questions → Research → Document → Evaluation
- **Conditional loops**: Evaluation can route back to Questions or Document
- **End condition**: Reaches END when quality is sufficient or max retries hit

## 🐛 Troubleshooting

### Common Issues

**Issue**: "API key not found" error

- **Solution**: Ensure `.env` file exists with all required API keys

**Issue**: "Module not found" errors

- **Solution**: Make sure virtual environment is activated and dependencies installed

**Issue**: Research quality consistently low

- **Solution**: Check Tavily API key and internet connectivity

**Issue**: Cache not working

- **Solution**: Verify Pinecone index exists and API key is correct

## 🚀 Performance Tips

- **Use cache**: Similar queries will be much faster on repeat
- **Clear queries**: More specific queries yield better research quality
- **Monitor scores**: Check evaluation scores to understand quality
- **API limits**: Be mindful of API rate limits for free tiers

## 📚 Example Research Topics

The agent excels at:

- "Best [service/product] in [location]"
- "How to [accomplish task] step by step"
- "Comparison of [product A] vs [product B]"
- "History and evolution of [topic]"
- "Key trends in [industry] for [year]"

---

## 📞 Support

- **Email**: [work.raj.38@gmail.com](mailto:work.raj.38@gmail.com)
- **Issues**: [GitHub Issues](https://github.com/RajTejani61/Research-Agent/issues)

---

<div align="center">

[⬆️ Back to Top](#research-agent)

</div>
