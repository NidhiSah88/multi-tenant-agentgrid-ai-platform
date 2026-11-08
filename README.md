# AgentGrid

AgentGrid is an AI-powered customer engagement and business automation
platform designed for businesses and agencies.

## 1. What exactly are we building?
We are building LegacyIQ – AI-Powered Legacy Application Discovery & Requirements Intelligence Platform for The Talent Grid's TTG-AI-LARD RFP.

This is not a chatbot with a file-upload button. It is an enterprise application modernization intelligence platform.

An enterprise user should be able to upload an existing application, inspect its architecture, understand business rules, generate requirements, discover technical debt and ask questions about the codebase.
Expected product experience

LegacyIQ
Product vision

LEGACY APPLICATION INTELLIGENCE PLATFORM
Dashboard

Overview

Repositories

Upload and manage applications

Architecture

Components and dependencies

Requirements

Business rules and user stories

Test intelligence

Test cases and acceptance criteria

Modernization

Technical debt and migration

AI Assistant

Ask questions about source code



Repository overview – illustrative
125
Files
18
APIs
24
Models

The six core RFP capabilities are:
1. Requirements discovery.
2. Architecture reconstruction.
3. AI-powered testing.
4. Technical documentation.
5. Modernization assessment.
6. AI knowledge assistant.
We must deliver all six, not just ingestion.






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











////////

cd backend

python3 --version
python3 -m venv .venv
source .venv/bin/activate


pip install --upgrade pip
pip install -r requirements.txt

run backend:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
restart:


uvicorn app.main:app --reload --port 8000





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


Step 1 — Install LangGraph dependencies
From your project:
cd ~/Projects/agentgrid-ai-platform/backend
source .venv/bin/activate

pip install langgraph langchain-core
pip freeze > requirements.txt






What I recommend next
Let's implement the AgentGrid agent orchestration first, using a mock LLM response temporarily. This lets us test the complete LangGraph workflow without spending money on Bedrock yet.


Step 1 — Install LangGraph dependencies
Step 2 — Create the shared agent state
Step 3 — Create the Supervisor Agent
Step 4 — Create the specialist agents
Step 5 — Create the LangGraph workflow
Step 6 — Add the agent API

Step 7 — Test the agent workflow
Restart Uvicorn if required:
uvicorn app.main:app --reload --port 8000


Test the knowledge agent:

curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "Tell me about your 2 bedroom apartments" 
}'
{"conversation_id":"18617f37-4c98-4abe-a3af-e7085be62257","tenant_id":"demo-tenant","selected_agent":"knowledge","intent":"property_information","response":"You asked: Tell me about your 2 bedroom apartments. I can help you with property details, pricing, locations and amenities.","lead_data":null,"requires_human_approval":false}%                                              
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I am interested in buying a property and want to schedule a visit"
}'
{"conversation_id":"35a6b852-b5cb-4028-aa63-83222c8ad752","tenant_id":"demo-tenant","selected_agent":"knowledge","intent":"property_information","response":"You asked: I am interested in buying a property and want to schedule a visit. I can help you with property details, pricing, locations and amenities.","lead_data":null,"requires_human_approval":false}%                                                    
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % 




# Router	Responsibility	Endpoint
# router from routes.py	Health checks, general APIs	/api/v1/health
# agent_router from agent_routes.py	AI agent conversations	/api/v1/agents/chat


# General API routes
# endpoint here becomes: /api/v1/health
app.include_router(
    router,
    prefix=f"/api/{settings.API_VERSION}",
)

# AI Agent routes
    # endpoint here becomes:  POST /api/v1/agents/chat
app.include_router(
    agent_router,
    prefix=f"/api/{settings.API_VERSION}/agents",
    tags=["AI Agents"],
)

curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "Tell me about your 2 bedroom apartments" 
}'
{"conversation_id":"18617f37-4c98-4abe-a3af-e7085be62257","tenant_id":"demo-tenant","selected_agent":"knowledge","intent":"property_information","response":"You asked: Tell me about your 2 bedroom apartments. I can help you with property details, pricing, locations and amenities.","lead_data":null,"requires_human_approval":false}%                                              



curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I am interested in buying a property and want to schedule a visit"
}'
{"conversation_id":"3a9550d4-32da-40fa-b44d-9444fb1bae89","tenant_id":"demo-tenant","selected_agent":"lead","intent":"lead_generation","response":"I'd be happy to help arrange a property visit. Could you share your name and contact number?","lead_data":{"status":"pending_details","source":"agentgrid_chat"},"requires_human_approval":true}%                                                                      
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % 

Step 4 — Test a mixed-intent message
Try:
curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "What is the price of your 2 BHK apartment? I want to book a visit."
}'


Expected: selected_agent should be lead, because the customer explicitly wants to book a visit.

 curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "What is the price of your 2 BHK apartment? I want to book a visit."
}'
{"conversation_id":"8817ff8d-20b7-4d6b-9e3e-a23482779342","tenant_id":"demo-tenant","selected_agent":"lead","intent":"lead_generation","response":"I'd be happy to help arrange a property visit. Could you share your name and contact number?","lead_data":{"status":"pending_details","source":"agentgrid_chat"},"requires_human_approval":true}%                                                                      
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % 



Next milestone — Workflow Agent + actual Human-in-the-Loop approval
We'll implement a real approval lifecycle:
1. Customer expresses interest.
2. Lead Agent collects customer details.
3. Workflow Agent validates the details.
4. A lead is created with pending_approval status.
5. An admin can view pending leads.
6. Admin approves or rejects the appointment request.



Step 8 — Test the complete workflow
Restart Uvicorn if it doesn't reload automatically.

Test A: Customer asks for a visit but provides no details.
curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit"
}'


Expected: the Lead Agent asks for the customer's name and contact number. No lead should be submitted for approval yet.

Test B: Customer provides details.

curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit",
  "customer_name": "Rahul Sharma",
  "contact_number": "9876543210"
}'


Expected: a lead is created with pending_approval status, and the response includes a lead_id.

Test C: Admin views pending approvals.
curl "http://localhost:8000/api/v1/approvals/pending?tenant_id=demo-tenant"


Test D: Admin approves the lead.


Copy the lead_id from Test B and replace YOUR_LEAD_ID:
curl -X POST "http://localhost:8000/api/v1/approvals/YOUR_LEAD_ID/approve?tenant_id=demo-tenant"


Test E: Verify approval is complete.
curl "http://localhost:8000/api/v1/approvals/pending?tenant_id=demo-tenant"

The approved lead should no longer appear in the pending list.
Expected business workflow
1. Customer expresses interest.
2. Lead Agent collects details.
3. Workflow Agent creates a pending lead.
4. Admin sees the pending request.
5. Admin approves or rejects it.
End-to-end PoC workflow

Security note: These approval endpoints are currently for local development only. They have no authentication or admin authorization. Before presenting this as a multi-tenant platform, we'll add JWT authentication, admin RBAC, tenant ownership checks, and persistent database storage



3. Test the missing-details flow
Open another Terminal tab and run:
curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit"
}'


Expected behavior:
- Selected agent: lead
- Response: asks for customer name and contact number
- Lead ID: should not be created yet
- requires_human_approval: false



curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit"
}'
{"conversation_id":"714bc75e-e1c4-4ccc-8a11-81f967b6ba47","tenant_id":"demo-tenant","selected_agent":"lead","intent":"lead_generation","response":"I'd be happy to arrange a property visit. Could you share your name and contact number?","lead_id":null,"lead_data":{"status":"pending_details"},"requires_human_approval":false}%   
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % 


4. Test the complete lead flow
curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit",
  "customer_name": "Rahul Sharma",
  "contact_number": "9876543210"
}'


Expected behavior:
- Lead Agent validates the supplied details.
- Workflow Agent creates the lead.
- Lead status becomes pending_approval.
- Response contains a lead_id.
- requires_human_approval is true.


curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit",
  "customer_name": "Rahul Sharma",
  "contact_number": "9876543210"
}'
{"conversation_id":"5459ae6b-b297-4d1b-b7d9-9c7c7d314d93","tenant_id":"demo-tenant","selected_agent":"lead","intent":"lead_generation","response":"Your appointment request has been submitted. Our team will review it and contact you.","lead_id":"9826a5e7-cbcb-4ad2-97d2-6d3932e74204","lead_data":{"lead_id":"9826a5e7-cbcb-4ad2-97d2-6d3932e74204","tenant_id":"demo-tenant","customer_name":"Rahul Sharma","contact_number":"9876543210","status":"pending_approval","created_at":"2026-11-01T21:06:15.884512+00:00"},"requires_human_approval":true}%                                 
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % 




5. Test the human approval queue
Get pending leads:
curl http://localhost:8000/api/v1/approvals/pending?tenant_id=demo-tenant


Copy the lead_id from the response.

Approve the lead:
curl -X POST "http://localhost:8000/api/v1/approvals/YOUR_LEAD_ID/approve?tenant_id=demo-tenant"


IN TER MINAL I TESTED :
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % curl http://localhost:8000/api/v1/health
{"status":"healthy","service":"agentgrid-api"}%                                   
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform %  source /Users/nidhi
kumari/Desktop/agentgrid-ai-platform/backend/.venv/bin/activate
(.venv) (base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit"
}'
{"conversation_id":"99989fdc-fa47-4f12-a845-affa32a66a70","tenant_id":"demo-tenant","selected_agent":"lead","intent":"lead_generation","response":"I'd be happy to arrange a property visit. Could you share your name and contact number?","lead_id":null,"lead_data":{"status":"pending_details"},"requires_human_approval":false}%   
(.venv) (base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % curl -X POST http://localhost:8000/api/v1/agents/chat \
-H "Content-Type: application/json" \
-d '{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit",
  "customer_name": "Rahul Sharma",
  "contact_number": "9876543210"
}'
{"conversation_id":"867ad9b9-04a1-4bb3-b98e-63f6ae91ad21","tenant_id":"demo-tenant","selected_agent":"lead","intent":"lead_generation","response":"Your appointment request has been submitted. Our team will review it and contact you.","lead_id":"0ee53084-fe50-481d-873c-aaf98a2f00fd","lead_data":{"lead_id":"0ee53084-fe50-481d-873c-aaf98a2f00fd","tenant_id":"demo-tenant","customer_name":"Rahul Sharma","contact_number":"9876543210","status":"pending_approval","created_at":"2026-11-08T03:13:58.477528+00:00"},"requires_human_approval":true}%    


Approve Rahul's lead
Your generated lead ID is:
0ee53084-fe50-481d-873c-aaf98a2f00fd


Run:
curl -X POST "http://localhost:8000/api/v1/approvals/0ee53084-fe50-481d-873c-aaf98a2f00fd/approve?tenant_id=demo-tenant"


This simulates an admin approving the customer's appointment request.

4. Verify that approval worked
Run the pending queue command again:
curl "http://localhost:8000/api/v1/approvals/pending?tenant_id=demo-tenant"


The approved lead should no longer appear in the pending list.





(.venv) (base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % curl -X POST "http://localhost:8000/api/v1/approvals/0ee53084-fe50-481d-873c-aaf98a2f00fd/approve?tenant_id=demo-tenant"
{"message":"Appointment request approved","lead":{"lead_id":"0ee53084-fe50-481d-873c-aaf98a2f00fd","tenant_id":"demo-tenant","customer_name":"Rahul Sharma","contact_number":"9876543210","status":"approved","created_at":"2026-11-08T03:13:58.477528+00:00"}}%                                                                        


(.venv) (base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % curl "http://localhost:8000/api/v1/approvals/pending?tenant_id=demo-tenant"
{"pending_leads":[]}%  

2. Pending queue returned an empty list
{
  "pending_leads": []
}


This confirms the approved lead is no longer in the pending approval queue.

You have now tested the complete basic workflow:

Customer message → Supervisor Agent → Lead Agent → Workflow Agent → Human Approval → Approved Lead.




6. What each endpoint does
API endpoint	Purpose
GET /api/v1/health	Checks backend health
POST /api/v1/agents/chat	Sends customer messages to agents
GET /api/v1/approvals/pending	Lists pending leads
POST /api/v1/approvals/{lead_id}/approve	Approves a lead
POST /api/v1/approvals/{lead_id}/reject	Rejects a lead

One important limitation: Your current lead records are stored in memory, not PostgreSQL. Don't restart the backend before finishing this test, or the lead will disappear.




Next development milestone: PostgreSQL


Currently, your leads are stored in an in-memory Python dictionary. This means restarting FastAPI deletes them.

Our next implementation should be:
1. Configure PostgreSQL.
2. Connect FastAPI using SQLAlchemy.
3. Create a leads database table.
4. Replace in-memory lead_service.py with database operations.
5. Test creating, approving and rejecting leads.
6. Restart FastAPI and verify that lead records still exist.
This will move AgentGrid from an in-memory workflow demo toward a persistent backend PoC.



Step 2 — Check your AgentGrid project structure
Go to your project root:
cd ~/Desktop/agentgrid-ai-platform


Run:
ls -la

. Check whether Docker is available
Run:
docker --version
docker compose version


If Docker Desktop is already running, also execute:
docker ps


From your project root, run to check backend structure :
find backend/app -maxdepth 3 -type f | sort




Step 1 — Create docker-compose.yml
First, go to your project root:

Step 2 — Start PostgreSQL
Make sure Docker Desktop is running, then execute:
docker compose up -d postgres


Check the container:
docker ps


You should see:

agentgrid-postgres



docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED              STATUS                        PORTS                    NAMES
51fd0522e001   pgvector/pgvector:pg16   "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:5432->5432/tcp   agentgrid-postgres
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % 



Check its health:
docker inspect --format='{{.State.Health.Status}}' agentgrid-postgres


Expected result:
healthy

Step 3 — Verify PostgreSQL connection
Run:
docker exec -it agentgrid-postgres psql -U agentgrid -d agentgrid


You should see a PostgreSQL prompt similar to:
agentgrid=#


Now run:
SELECT current_database();


Expected result:
 agentgrid


Check the pgvector extension is available:
CREATE EXTENSION IF NOT EXISTS vector;


Then:
SELECT extname FROM pg_extension WHERE extname = 'vector';


Expected result:
vector


Exit PostgreSQL:
\q


output fo all these steps:
docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED              STATUS                        PORTS                    NAMES
51fd0522e001   pgvector/pgvector:pg16   "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:5432->5432/tcp   agentgrid-postgres
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % docker inspect --format='{{.State.Health.Status}}' agentgrid-postgres
healthy
(base) nidhikumari@Nidhis-MacBook-Pro agentgrid-ai-platform % docker exec -it agentgrid-postgres psql -U agentgrid -d agentgrid
psql (16.15 (Debian 16.15-1.pgdg12+2))
Type "help" for help.

agentgrid=# SELECT current_database();
 current_database 
------------------
 agentgrid
(1 row)

agentgrid=# CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION
agentgrid=# SELECT extname FROM pg_extension WHERE extname = 'vector';
 extname 
---------
 vector
(1 row)

agentgrid=# 



Step 4 — Understand what we just created
AgentGrid PostgreSQL

Persistent storage

Configuration	Value
Database	agentgrid
User	agentgrid
Port	5432
Container	agentgrid-postgres
Image	pgvector/pgvector:pg16
Storage	Docker named volume


Your leads will eventually be stored in PostgreSQL tables rather than Python dictionaries. The Docker volume preserves database files when the container is stopped or recreated.

Security note: These credentials are for local development only. We'll move them into environment variables and use stronger credentials before deployment.


Step 5 — Stop here and verify
Please run these commands and share the output:
docker ps
docker inspect --format='{{.State.Health.Status}}' agentgrid-postgres
And confirm that this SQL query works:
SELECT current_database();


Once PostgreSQL is running successfully, we'll implement the next three files:
1. backend/app/database/connection.py — SQLAlchemy engine and session.
2. backend/app/models/lead.py — Lead database model.
3. Updated backend/app/services/lead_service.py — Replace dictionary storage with PostgreSQL CRUD operations.
We'll preserve your already-working AgentGrid chat and human approval APIs.




Step 3 — Create the SQLAlchemy connection
Create:
nano app/database/connection.py

Step 4 — Create your Lead database model
Create:
nano app/models/lead.py


Step 5 — Register the model
Open:
nano app/models/__init__.py

Step 6 — Create a database initialization script
Create:
nano init_db.py

Run:
python init_db.py


Expected output:
Creating AgentGrid database tables...
Database tables created successfully!


Step 7 — Verify the table in PostgreSQL
Run:
docker exec -it agentgrid-postgres psql -U agentgrid -d agentgrid

Inside PostgreSQL:
\dt


You should see:
 public | leads | table | agentgrid


Inspect the table:
\d leads
Exit:
\q


python init_db.py
Creating AgentGrid database tables...
Database tables created successfully!
(.venv) (base) nidhikumari@Nidhis-MacBook-Pro backend % docker exec -it agentgrid-postgres psql -U agentgrid -d agentgrid
psql (16.15 (Debian 16.15-1.pgdg12+2))
Type "help" for help.

agentgrid=# \dt
         List of relations
 Schema | Name  | Type  |   Owner   
--------+-------+-------+-----------
 public | leads | table | agentgrid
(1 row)

agentgrid=# 


agentgrid=# \d leads
                            Table "public.leads"
     Column     |           Type           | Collation | Nullable | Default 
----------------+--------------------------+-----------+----------+---------
 lead_id        | character varying(36)    |           | not null | 
 tenant_id      | character varying(100)   |           | not null | 
 customer_name  | character varying(150)   |           | not null | 
 contact_number | character varying(30)    |           | not null | 
 status         | character varying(30)    |           | not null | 
 created_at     | timestamp with time zone |           | not null | 
Indexes:
    "leads_pkey" PRIMARY KEY, btree (lead_id)
    "idx_leads_tenant_status" btree (tenant_id, status)
    "ix_leads_tenant_id" btree (tenant_id)

agentgrid=# 


update lead_service.py 
Restart FastAPI
If the server is running, stop it with Ctrl + C.

Then start it again:
uvicorn app.main:app --reload


Check that the server starts without import or database errors.
Step 3: Test lead creation
Open Swagger in your browser:

http://127.0.0.1:8000/docs

Find POST /api/v1/agents/chat and submit a request with complete lead details.

Use the same request structure you successfully tested earlier. For example, the customer details should include:


{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit",
  "customer_name": "Rahul Sharma",
  "contact_number": "9876543210"
}
The response should contain a lead_id and:
"requires_human_approval": true



curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/agents/chat' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "tenant_id": "demo-tenant",
  "message": "I want to schedule a property visit",
  "customer_name": "Rahul Sharma",
  "contact_number": "9876543210"
}'

{
  "conversation_id": "48da6dac-6fe1-4b78-9e81-13e6b6c04250",
  "tenant_id": "demo-tenant",
  "selected_agent": "lead",
  "intent": "lead_generation",
  "response": "Your appointment request has been submitted. Our team will review it and contact you.",
  "lead_id": "27654bee-49f8-4879-98f8-e09cb6f07692",
  "lead_data": {
    "lead_id": "27654bee-49f8-4879-98f8-e09cb6f07692",
    "tenant_id": "demo-tenant",
    "customer_name": "Rahul Sharma",
    "contact_number": "9876543210",
    "status": "pending_approval",
    "created_at": "2026-11-08T04:38:07.360597+00:00"
  },
  "requires_human_approval": true
}



Step 4: Verify the database record
In another Terminal tab:
docker exec -it agentgrid-postgres psql -U agentgrid -d agentgrid

Run:
SELECT lead_id, tenant_id, customer_name, contact_number, status, created_at
FROM leads
ORDER BY created_at DESC;



  lead_id                |  tenant_id  | customer_name | contact_number |      status      |          created_at           
--------------------------------------+-------------+---------------+----------------+------------------+-------------------------------
 27654bee-49f8-4879-98f8-e09cb6f07692 | demo-tenant | Rahul Sharma  | 9876543210     | pending_approval | 2026-11-08 04:38:07.360597+00
(1 row)





Next major milestone: Legacy application ingestion



FastAPI requires python-multipart to handle uploaded ZIP files.
pip install python-multipart

Add it to your requirements.txt if it isn't already there:

grep -q "^python-multipart" requirements.txt || echo "python-multipart" >> requirements.txt


mkdir -p app/legacy_discovery/ingestion
mkdir -p app/legacy_discovery/schemas
mkdir -p storage/repositories


touch app/legacy_discovery/__init__.py
touch app/legacy_discovery/ingestion/__init__.py
touch app/legacy_discovery/schemas/__init__.py

4. Step 2 — Inspect your existing backend

echo "========== PROJECT STRUCTURE =========="
find app -maxdepth 3 -type f | sort

echo "========== MAIN.PY =========="
cat app/main.py

echo "========== DATABASE CONNECTION =========="
cat app/database/connection.py

echo "========== MODEL INIT =========="
cat app/models/__init__.py

echo "========== REQUIREMENTS =========="
cat requirements.txt


Step 4 — Create repository schemas
Create:
nano app/legacy_discovery/schemas/repository.py

Step 5 — Implement secure ZIP extraction
Create:
nano app/legacy_discovery/ingestion/zip_extractor.py

Step 6 — Build the repository scanner
Create:
nano app/legacy_discovery/ingestion/repository_scanner.py

Step 7 — Create the Repository database model
We'll store repository metadata and scan results in PostgreSQL. The actual ZIP and extracted files remain on local disk for now.

Create:
nano app/models/repository.py

Step 8 — Register the new model
Open:
nano app/models/__init__.py
Step 9 — Initialize the repositories table
You already have init_db.py in your backend.

Open it:
nano init_db.py

Run:
python init_db.py


Expected:
Creating AgentGrid database tables...
Database tables created successfully!

Verify:
docker exec -it agentgrid-postgres \
psql -U agentgrid -d agentgrid \
-c "\dt"


docker exec -it agentgrid-postgres \
psql -U agentgrid -d agentgrid \
-c "\dt"
             List of relations
 Schema |     Name     | Type  |   Owner   
--------+--------------+-------+-----------
 public | leads        | table | agentgrid
 public | repositories | table | agentgrid
(2 rows)


Step 10 — Create the repository upload API
Now we'll connect the ZIP extractor, scanner and PostgreSQL model.

Create:
nano app/legacy_discovery/ingestion/upload.py
Step 11 — Register the new API in FastAPI
Open:
nano app/main.py

Step 12 — Start FastAPI
uvicorn app.main:app --reload


3. Can you see PostgreSQL tables in pgAdmin?
Yes

Step 1. Open pgAdmin
Open pgAdmin 4 on your Mac.

If you don't have it installed, you can download it from:
Download pgAdmin 4Step 2. Register your PostgreSQL server
Right-click Servers → Register → Server.
Enter:
Field	Value
Name	AgentGrid Local
Host	localhost
Port	5432 (if mapped to 5432)
Maintenance database	agentgrid
Username	agentgrid
Password	Your PostgreSQL password

To verify the Docker port mapping, run:
docker port agentgrid-postgres 5432

Step 3. Navigate to your tables
Expand:
Servers
  └── AgentGrid Local
      └── Databases
          └── agentgrid
              └── Schemas
                  └── public
                      └── Tables
                          ├── leads
                          └── repositories


Right-click repositories.

Choose:

View/Edit Data → All Rows

4. How to see pgvector in PostgreSQL?
This is an important distinction.

pgvector is not a separate database or a separate table.

It is a PostgreSQL extension that provides vector data types, similarity search and vector indexes.

We will use it to store embeddings generated from legacy application source code.






SELECT
    extname,
    extversion
FROM pg_extension
WHERE extname = 'vector';

o/p:
"vector"	"0.8.7"


SELECT typname
FROM pg_type
WHERE typname = 'vector';


vector



## Next milestone — Legacy application ingestion
This is the first major capability of LegacyIQ. The backend will:
1. Accept a legacy application ZIP upload.
2. Validate the ZIP and safely extract its contents.
3. Scan source files and identify programming languages and frameworks.
4. Build a file inventory.
5. Save repository metadata in PostgreSQL.
6. Prepare the extracted source code for the next milestone: code analysis and requirements discovery.



Step 13 — Check your current backend files
cd ~/Desktop/agentgrid-ai-platform/backend

echo "===== LEGACY DISCOVERY FILES ====="
find app/legacy_discovery -type f 2>/dev/null | sort

echo "===== DATABASE MODELS ====="
find app/models -maxdepth 1 -type f | sort

echo "===== STORAGE DIRECTORY ====="
find storage -maxdepth 3 -type f 2>/dev/null | sort

echo "===== MAIN APP ROUTES ====="
cat app/main.py


Step 14 — Register the LegacyIQ ingestion API
Open:
nano app/main.py



Now we'll build the next major capability: Legacy Source Code Intelligence — parsing, chunking, embeddings, and vector storage.


This is where LegacyIQ starts understanding the contents of an uploaded application rather than simply recording its filename, language, and framework.

The processing pipeline will be:
Uploaded legacy repository

Extracted source files


Source-code parser

Filter files, detect languages, read source


Code chunking

Split code into overlapping, searchable chunks


Amazon Bedrock embeddings

Titan Embeddings V2 — 1,024 dimensions


PostgreSQL + pgvector

Store code chunks, metadata, and vectors

Step 17 — Install and configure dependencies
From your backend terminal:

pip install pgvector boto3


Step 18 — Enable pgvector in PostgreSQL
Run:
docker exec -it agentgrid-postgres psql -U agentgrid -d agentgrid


At the PostgreSQL prompt, execute:
CREATE EXTENSION IF NOT EXISTS vector;

SELECT extname, extversion
FROM pg_extension
WHERE extname = 'vector';
You should see the vector extension.

Exit:
\q

Step 19 — Create the CodeChunk database model
Create this file:

app/models/code_chunk.py

Step 20 — Register the new model
Replace app/models/__init__.py with:


Step 21 — Build the source-code chunker
Create:

app/legacy_discovery/ingestion/code_chunker.py

Step 22 — Implement Amazon Bedrock embeddings
Create:

app/services/embedding_service.py
Step 23 — Implement the repository indexing service
Create:

app/legacy_discovery/ingestion/indexing.py


Step 24 — Create the indexing API
Create:

app/legacy_discovery/ingestion/indexing_routes.py

Step 25 — Register the indexing router
Open app/main.py:

Your legacy routes will now include:
Method	Endpoint	Purpose
POST	/api/v1/legacy/upload	Upload and extract a repository
POST	/api/v1/legacy/{repository_id}/index	Parse and index source code

Step 26 — Update database initialization
Replace init_db.py with:


python init_db.py


Step 27 — Verify the database structure
In your terminal:
docker exec -it agentgrid-postgres psql -U agentgrid -d agentgrid


Run:
\dt

\d code_chunks



Check the vector column:
SELECT
    column_name,
    data_type,
    udt_name
FROM information_schema.columns
WHERE table_name = 'code_chunks';


You should see the embedding column with the PostgreSQL vector type.

You can also run these queries in pgAdmin's Query Tool.
Step 28 — Start LegacyIQ
uvicorn app.main:app --reload


Step 29 — Inspect indexed code in pgAdmin
Once a real repository has been uploaded and indexed, run:
SELECT
    file_path,
    language,
    chunk_index,
    start_line,
    end_line,
    LEFT(content, 200) AS content_preview,
    embedding IS NOT NULL AS has_embedding
FROM code_chunks
ORDER BY file_path, chunk_index;


This lets you see exactly which source-code sections have been stored and whether their embeddings are available.



next backend milestone is semantic retrieval and code intelligence:
1. Query pgvector for relevant source-code chunks.
2. Retrieve related functions, classes, and dependencies.
3. Use retrieved source context with an LLM.
4. Generate functional requirements and business rules with source-file references.
This will become the foundation for the Requirements Discovery Agent and Architecture Analysis Agent.

One important distinction: Chunking and vector storage are implemented here, but semantic search is not implemented yet. Also, without AWS credentials and Bedrock model access, chunks will be stored with embedding = NULL; we'll enable embeddings before implementing vector similarity retrieval

You don't need to create a fake application. When the pipeline is ready, we can use a real project ZIP, excluding .env files, credentials, and other secrets.




Our next backend milestone is semantic retrieval and code intelligence:


## Milestone 4: Semantic Code Search and Retrieval (RAG foundation).
So far, LegacyIQ can ingest a repository and split its source code into chunks. Now we'll make those chunks searchable by meaning, not just by filename or exact keywords.

For example, a user should eventually be able to ask:
- "Where is customer authentication implemented?"
- "Which function calculates payment fees?"
- "Where does the application connect to the database?"
- "Which APIs handle order creation?"
LegacyIQ will retrieve the relevant source-code chunks, including file names and line numbers. These retrieved chunks will become the evidence used by our Requirements Discovery and Architecture Analysis agents.

Important prerequisite: semantic search requires actual embeddings. If you have not configured AWS Bedrock yet, we'll add the code now, but the search endpoint will clearly report that embeddings are not ready rather than pretending keyword search is vector search.
Step 30 — Add the semantic search request schema
Create:

app/legacy_discovery/schemas/search.py



Step 31 — Build the vector retrieval service
Create:

app/legacy_discovery/ingestion/retrieval.py

Step 32 — Add an embedding backfill service
This is important because you may have indexed repositories while BEDROCK_EMBEDDINGS_ENABLED=false. Those existing chunks have no vectors yet.

Create:

app/legacy_discovery/ingestion/embedding_jobs.py

Step 33 — Create the semantic search API
Create:

app/legacy_discovery/ingestion/retrieval_routes.py

Step 35 — Add a vector similarity index
For a growing repository, a vector index improves similarity-search performance.

Open init_db.py. Add this SQL after Base.metadata.create_all(bind=engine):



Step 36 — Configure Bedrock when you're ready
In your .env, use:
AWS_REGION=ap-south-1
BEDROCK_EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0
BEDROCK_EMBEDDINGS_ENABLED=true


Before enabling this, make sure your AWS credentials are configured and the Titan embedding model is accessible in your selected region.

For example, if you use an AWS CLI profile:

aws configure
aws sts get-caller-identity



start:
uvicorn app.main:app --reload



Step 38 — Inspect the vector data in pgAdmin
Run this SQL in pgAdmin's Query Tool:
SELECT
    file_path,
    language,
    chunk_index,
    start_line,
    end_line,
    embedding IS NOT NULL AS has_embedding,
    LEFT(content, 150) AS source_preview
FROM code_chunks
ORDER BY file_path, chunk_index;


Check how many chunks have vectors:
SELECT
    COUNT(*) AS total_chunks,
    COUNT(embedding) AS embedded_chunks,
    COUNT(*) FILTER (
        WHERE embedding IS NULL
    ) AS pending_embeddings
FROM code_chunks;


Check the HNSW index:

SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'code_chunks';




What we've built and what comes next
LegacyIQ backend roadmap
1. Repository ingestion
   
   Code provided
   
   ZIP upload, extraction, scanning, metadata persistence.
2. Source-code intelligence
   
   Code provided
   
   Parsing, chunking, embedding and vector retrieval.
3. Requirements Discovery Agent
   
   Extract functional requirements, business rules, workflows, and source-code evidence.
4. Architecture Analysis Agent
   
   Discover components, API dependencies, database relationships, and system architecture.
5. AI Test Generation Agent
   
   Generate test scenarios, edge cases, and acceptance criteria.
6. Modernization Assessment Agent
   
   Identify technical debt, outdated dependencies, risks, and migration opportunities.
7. Technical Documentation Agent
   
   Generate structured technical specifications and architecture reports.
8. LangGraph Supervisor and AI Knowledge Assistant
   
   Coordinate agents, retrieve evidence, and answer questions across the legacy application.

Next milestone: Requirements Discovery Agent. We'll implement it as a real LangGraph workflow that retrieves source-code evidence, uses an LLM to extract requirements and business rules, and persists structured results with file and line references.

One implementation note: the code in this milestone is the implementation to add; it is not evidence that Bedrock indexing or semantic search has already run successfully. We'll verify those when AWS access and a real repository are available.

We can continue with the Requirements Discovery Agent in our next session as well.










