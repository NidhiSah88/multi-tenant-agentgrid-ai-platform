# AgentGrid

AgentGrid is an AI-powered customer engagement and business automation
platform designed for businesses and agencies.

## Initial PoC capabilities

- FastAPI backend
- AWS Bedrock LLM integration
- LangGraph-based agent orchestration (next milestone)
- Retrieval-Augmented Generation (RAG) (planned)
- Lead qualification and capture (planned)
- Human-in-the-loop workflows (planned)
- Multi-tenant architecture (planned)
- Next.js dashboard (planned)

## Tech Stack

- Python
- FastAPI
- AWS Bedrock
- LangGraph
- PostgreSQL
- pgvector
- Next.js
- TypeScript
- Docker

## Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload







cd backend

python3 --version
python3 -m venv .venv
source .venv/bin/activate


pip install --upgrade pip
pip install -r requirements.txt

run backend:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000



Open these URLs:
- API: AgentGrid API
- Swagger documentation: Interactive API docs
- Health endpoint: Health check
You should receive:
{
  "status": "healthy",
  "service": "agentgrid-api"
}


Step 9 — Connect AWS Bedrock
First, check whether the AWS CLI is installed:
aws --version


If it is not installed, install it on macOS:
brew install awscli


Configure your AWS credentials:
aws configure


Enter your AWS access key, secret key, default region (us-east-1, or another region where you have Bedrock access), and output format (json).

Use an IAM identity with permission to invoke the Bedrock model. Do not use root-account credentials.

Check that your credentials work:
aws sts get-caller-identity


Next, in the AWS Console:
1. Open Amazon Bedrock.
2. Select the same region configured in your .env.
3. Check that the chosen model is available to your account in that region.
4. Ensure your IAM identity can invoke it.
Our initial model is amazon.nova-lite-v1:0. You can change BEDROCK_MODEL_ID in .env if you select another supported model.

Test Bedrock through the API:
curl -X POST http://localhost:8000/api/v1/ai/test \
  -H "Content-Type: application/json" \
  -d '{"prompt":"You are AgentGrid, an AI customer engagement assistant. Introduce yourself in two sentences."}'


A successful response should look like:
{
  "response": "Hello! I'm AgentGrid, your AI customer engagement assistant..."
}













