# Legislative Brief Generator

An AI-powered tool that connects legislator voting records and bill data to a LangChain RAG pipeline, generating concise one-page briefs summarizing a legislator's climate policy positions.

Built to demonstrate AI infrastructure skills relevant to civic technology and climate data platforms.

## Features

- Loads legislator voting records from JSON or Open States API
- Embeds records into a vector database using ChromaDB
- Retrieves relevant votes using semantic search
- Generates structured briefs using Claude API via LangChain
- CLI tool for generating briefs by legislator name
- Modular, extensible architecture for adding new data sources

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | Anthropic Claude API |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers |
| Data | Open States API, JSON |
| Testing | pytest |

## Project Structure
```
legislative-brief-generator/
├── src/
│   ├── data_loader.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── generator.py
│   └── brief.py
├── data/
│   └── sample_legislators.json
├── tests/
│   └── test_generator.py
├── .env.example
├── requirements.txt
└── README.md
```

## Setup

1. pip install -r requirements.txt
2. cp .env.example .env and fill in your Anthropic API key
3. python -m src.brief --legislator "Jane Smith" --state TX

## Sample Output
```
LEGISLATOR BRIEF: Jane Smith (D - TX)
======================================
Climate Position: Strong Supporter
Confidence: High

Key Votes:
- HB 1234 Clean Energy Grid Act        YES   2025-02-14
- SB 567  Carbon Reduction Standards   YES   2025-01-30
- HB 890  Oil Subsidy Extension        NO    2024-11-12

Summary:
Rep. Jane Smith has consistently voted in favor of clean energy
legislation and against fossil fuel subsidies over the past two
sessions.

Recommended Engagement: High Priority
```

## Roadmap

- [ ] Add Open States API as live data source
- [ ] Batch brief generation for all legislators in a state
- [ ] Export briefs to PDF
- [ ] Build Streamlit UI for non-technical users
- [ ] Deploy to GCP Cloud Run

## License

MIT
