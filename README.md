# AI Contact Intelligence

AI Contact Intelligence is a Python/FastAPI project for searching and matching professional contacts with natural-language queries. It combines LLM planning, OpenAI embeddings, Pinecone semantic search, optional OpenSearch keyword search, Redis caching, and DynamoDB contact storage behind a simple API and MCP server.

The project is useful for recruiter-style workflows such as:

- "Find senior React engineers in Bangalore"
- "Show backend engineers with Python and AWS experience"
- "Match candidates for this job description"
- "Summarize the best contacts for a hiring need"

## Features

- Natural-language contact search through a FastAPI endpoint.
- LangGraph workflow with planner, retriever, and summarizer agents.
- OpenAI chat completions for query planning, reranking, and final summaries.
- OpenAI embeddings with `text-embedding-3-small`.
- Pinecone vector index for semantic contact retrieval.
- DynamoDB as the contact source of truth.
- Redis caching for repeated searches.
- Optional OpenSearch keyword search support.
- MCP server exposing contact search tools to MCP-compatible clients.
- Seed data and ingestion scripts for a sample contact dataset.

## Architecture

The main search path is:

1. A user submits a query to `POST /search`.
2. The planner agent asks the LLM to extract intent and filters such as location, title, and skills.
3. The retriever agent generates an embedding for the query and searches Pinecone.
4. OpenSearch keyword search is attempted as an additional retrieval path.
5. Results are reranked by the LLM.
6. Contact details are loaded from DynamoDB.
7. Results are cached in Redis.
8. The summarizer agent asks the LLM to produce a response using only the retrieved contacts.

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- LangGraph
- OpenAI Python SDK
- Pinecone
- AWS DynamoDB via Boto3
- Redis
- OpenSearch
- MCP Python SDK

## Project Structure

```text
.
├── run.py                         # Local FastAPI server entry point
├── requirements.txt               # Runtime dependencies
├── pyproject.toml                 # Package metadata
├── scripts/
│   ├── contacts_seed.py           # Sample contact data and DynamoDB seeding
│   └── ingest_contacts.py         # Embeds contacts and upserts vectors to Pinecone
├── src/
│   ├── main.py                    # FastAPI app setup
│   ├── config.py                  # Environment-based settings
│   ├── api/                       # HTTP routes
│   ├── agents/                    # Planner, retriever, summarizer agents
│   ├── graph/                     # LangGraph workflow
│   ├── mcp/                       # MCP server
│   ├── models/                    # Pydantic and TypedDict models
│   ├── repositories/              # Contact repository abstraction
│   └── services/                  # OpenAI, Pinecone, DynamoDB, Redis, OpenSearch services
└── test/                          # Experimental/manual scripts
```

## Prerequisites

You need the following before running the full project:

- Python 3.11 or newer
- OpenAI API key
- Pinecone API key and index name
- AWS credentials with DynamoDB access
- A DynamoDB table for contacts
- Redis server
- Optional OpenSearch cluster if you want keyword search

The DynamoDB contact table is expected to use `contactId` as its partition key.

## Environment Variables

Create a local `.env` file in the project root. Do not commit this file.

```bash
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=your_pinecone_index_name
AWS_REGION=us-east-1
DYNAMODB_TABLE_NAME=your_contacts_table
OPENSEARCH_HOST=https://your-opensearch-host
OPENSEARCH_USERNAME=your_username
OPENSEARCH_PASSWORD=your_password
REDIS_HOST=localhost
REDIS_PORT=6379
```

Only `OPENAI_API_KEY` and `PINECONE_API_KEY` are currently shown in `.env.example`, but the application reads all of the variables above from `src/config.py`.

## Installation

Clone the repository, create a virtual environment, and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you want to install the project in editable mode:

```bash
pip install -e .
```

## Data Setup

The project includes a sample contact list in `scripts/contacts_seed.py`.

Seed contacts into DynamoDB:

```bash
python scripts/contacts_seed.py
```

Generate embeddings and index contacts in Pinecone:

```bash
python scripts/ingest_contacts.py
```

The ingestion script builds a text representation from each contact's name, title, location, and skills, generates an OpenAI embedding, and upserts the vector into Pinecone with contact metadata.

## Running the API

Start the local FastAPI server:

```bash
python run.py
```

The API runs at:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{
  "status": "healthy"
}
```

## API Endpoints

### Search Contacts

```http
POST /search
```

Request:

```json
{
  "query": "Find React engineers in Bangalore with AWS experience"
}
```

Response:

```json
{
  "response": "LLM-generated answer based on retrieved contacts",
  "contacts": [
    {
      "contactId": "1",
      "name": "John Doe",
      "title": "Frontend Engineer",
      "location": "Bangalore",
      "skills": ["React", "TypeScript", "AWS"]
    }
  ]
}
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Find backend engineers with Python and AWS"}'
```

### Contact Count

```http
GET /contacts/count
```

Current implementation returns a placeholder count from the API route. The repository layer already includes DynamoDB-backed count support.

### Get Contact

```http
GET /contacts/{contact_id}
```

Current implementation returns the requested `contactId` placeholder from the API route. The repository layer already includes DynamoDB-backed contact lookup support.

## MCP Server

The project includes an MCP server in `src/mcp/server.py`.

Run it with:

```bash
python -m src.mcp.server
```

Available MCP tools:

- `search_contacts(query: str)`
- `get_contact(contact_id: str)`
- `count_contacts()`
- `match_candidates(job_description: str)`

These tools call the same workflow and repository layer used by the API.

## How Search Works

The LangGraph workflow is defined in `src/graph/workflow.py`:

```text
planner -> retriever -> summarizer
```

The planner extracts structured search intent from the user query. The retriever performs semantic search, applies supported filters, reranks results, and fetches contact records. The summarizer turns the retrieved contacts into a concise natural-language answer.

Location filtering has special handling for broad country-level terms such as `india`, `in`, and `indian`, so those do not overconstrain the Pinecone metadata filter.

## Notes and Current Limitations

- `GET /contacts/count` and `GET /contacts/{contact_id}` currently return placeholder API responses.
- OpenSearch search is attempted in the repository, but Pinecone results are the primary retrieval source used by the current retriever.
- Reranking expects the LLM to return comma-separated contact IDs.
- Redis must be reachable for the retriever cache functions.
- Pinecone index creation uses AWS `us-east-1` serverless configuration.
- The sample dataset is intentionally small and lives in `scripts/contacts_seed.py`.

## Development Tips

- Keep secrets in `.env`; commit only `.env.example`.
- Do not commit `venv/`, `__pycache__/`, `.egg-info/`, or generated output files.
- Use `python run.py` for local API development.
- Use `scripts/contacts_seed.py` and `scripts/ingest_contacts.py` after changing seed contacts.

## License

No license has been added yet. Add one before publishing if you want to define how others may use the code.
