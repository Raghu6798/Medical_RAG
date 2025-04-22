# Clinical Medicine RAG 

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10-green)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-blue)
![Chainlit](https://img.shields.io/badge/Chainlit-latest-orange)

A production-ready medical AI assistant leveraging knowledge graphs for reliable and accurate medical information retrieval. This system integrates Neo4j graph databases, LangChain, and semantic caching to provide context-aware responses to healthcare professionals.

## 🚀 Features

- **Advanced Medical Knowledge Retrieval**: Leverages Neo4j knowledge graphs to provide accurate medical information
- **Semantic Caching**: Optimizes response times with Redis-based semantic caching
- **Conversational Memory**: Persists conversation history in Neo4j for contextual responses
- **Clinical Response Structure**: Formats responses according to clinical communication standards
- **Observability**: Full observability with Langfuse integration and structured logging
- **Security**: OAuth integration for secure authentication (GitHub, Google)
- **Containerization**: Docker-ready for easy deployment

## 📋 Prerequisites

- Python 3.10+
- Neo4j database instance
- Redis instance (for semantic caching)
- Langfuse account (for observability)
- OAuth credentials (optional, for authentication)

## 🛠️ Installation

### Option 1: Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd agent2agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env` (you'll need to create this)
   - Fill in the required environment variables

### Option 2: Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t agent2agent .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env agent2agent
   ```

## 🔧 Configuration

Create a `.env` file with the following variables:

```env
# Neo4j Configuration
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

# Redis Configuration
REDIS_URI=redis://username:password@your-instance.redns.redis-cloud.com:port
REDIS_PASSWORD=your-redis-password
REDIS_PORT=your-redis-port

# Langfuse Configuration
LANGFUSE_HOST_URL=https://cloud.langfuse.com
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_PUBLIC_KEY=your-public-key

# OpenRouter Configuration
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=your-api-key

# OAuth Configuration (Optional)
OAUTH_GITHUB_CLIENT_ID=your-client-id
OAUTH_GITHUB_CLIENT_SECRET=your-client-secret
CHAINLIT_AUTH_SECRET=your-auth-secret

OAUTH_GOOGLE_CLIENT_ID=your-client-id
OAUTH_GOOGLE_CLIENT_SECRET=your-client-secret
```

## 📊 Project Structure

```
agent2agent/
├── config/                 # Configuration files
├── databases/              # Database connections
│   ├── Neo4j/              # Neo4j database utilities
│   └── Redis/              # Redis cache utilities
├── models/                 # AI models
│   ├── embedding_model/    # Text embedding models
│   └── llm_model/          # Language models
├── obvservability/         # Monitoring and tracing
├── prompts/                # LLM prompts
├── routes/                 # API endpoints
│   └── query_route.py      # Main query handling route
├── tests/                  # Unit and integration tests
├── utils/                  # Utility functions
├── .env                    # Environment variables
├── Dockerfile              # Docker configuration
├── main.py                 # Application entry point
├── pyproject.toml          # Project metadata
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🚀 Usage

### Starting the Server

```bash
python main.py
```

This will start a FastAPI server on http://0.0.0.0:8000

### Accessing the Chainlit Interface

Navigate to http://localhost:8000/chainlit in your web browser.

## 📝 API Endpoints

The service exposes the following endpoints:

- **Web UI**: `/chainlit` - Chainlit interactive interface for medical queries
- **API**: (Further API endpoints can be documented here)

## 🧪 Testing

Run the test suite:

```bash
pytest
```

## 📊 Observability

- **Logging**: Logs are saved to `app.log` and `chainlit_app.log`
- **Tracing**: All LLM interactions are traced with Langfuse

## 🔒 Security

This project implements:
- OAuth authentication via GitHub and Google
- Session-based user management
- Secure storage of credentials in environment variables

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Neo4j](https://neo4j.com/) - Graph database
- [LangChain](https://langchain.com/) - LLM framework
- [Chainlit](https://chainlit.io/) - Interactive chat interfaces
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Redis](https://redis.io/) - Semantic caching
- [Langfuse](https://langfuse.com/) - LLM observability
