"""
FastAPI backend for Company Research Agent
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import asyncio
import json
import os
from datetime import datetime

# Import the agent and modules
from src.company_research_agent import CompanyResearchAgent, ConversationMode
from src.web_context_extract import extract
from src.context_summarizer import summarize_context
from src.article_writer import generate_chat_response_stream, generate_chat_response

# Create FastAPI app
app = FastAPI(
    title="Company Research Agent API",
    description="API for researching companies and generating account plans",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance (in production, use proper session management)
agent = CompanyResearchAgent(ConversationMode.NORMAL)

# Request/Response models
class ResearchRequest(BaseModel):
    company_name: str
    
class ChatRequest(BaseModel):
    message: str
    
class GenerateRequest(BaseModel):
    context: str
    query: str

class StatusResponse(BaseModel):
    status: str
    current_company: Optional[str]
    state: str

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "Company Research Agent API",
        "version": "1.0.0",
        "endpoints": {
            "POST /research": "Research a company",
            "POST /chat": "Chat with the agent",
            "GET /status": "Get agent status",
            "POST /generate/stream": "Generate content with streaming",
            "GET /health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/research")
async def research_company(request: ResearchRequest, background_tasks: BackgroundTasks):
    """
    Research a company and generate account plan
    """
    try:
        # Start research in background
        response = await agent._handle_company_research(request.company_name)
        
        return {
            "success": True,
            "message": response,
            "company": request.company_name,
            "state": agent.state.value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """
    Chat with the agent
    """
    try:
        response = await agent.process_input(request.message)
        
        return {
            "success": True,
            "response": response,
            "state": agent.state.value,
            "current_company": agent.current_company
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_agent_status() -> StatusResponse:
    """
    Get current agent status
    """
    return StatusResponse(
        status=agent._get_status_update(),
        current_company=agent.current_company,
        state=agent.state.value
    )

@app.post("/generate/stream")
async def generate_stream(request: GenerateRequest):
    """
    Generate content with streaming
    """
    async def event_generator():
        """Generate Server-Sent Events"""
        try:
            # Use the streaming function
            for chunk in generate_chat_response_stream(request.context, request.query):
                # Each chunk is already JSON formatted
                yield f"data: {chunk}\n\n"
            
            # Send completion event
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.post("/generate")
async def generate_content(request: GenerateRequest):
    """
    Generate content (non-streaming)
    """
    try:
        response = generate_chat_response(
            request.context,
            request.query,
            silent_mode=True
        )
        
        return {
            "success": True,
            "content": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/plans")
async def list_account_plans():
    """
    List all generated account plans
    """
    try:
        plans_dir = "./account_plans"
        if not os.path.exists(plans_dir):
            return {"plans": []}
        
        plans = []
        for filename in os.listdir(plans_dir):
            if filename.endswith(".md"):
                # Extract company name from filename
                parts = filename.replace(".md", "").split("_")
                company = " ".join(parts[2:-2]) if len(parts) > 2 else "Unknown"
                timestamp = "_".join(parts[-2:]) if len(parts) > 2 else ""
                
                plans.append({
                    "filename": filename,
                    "company": company,
                    "timestamp": timestamp,
                    "path": f"{plans_dir}/{filename}"
                })
        
        return {"plans": plans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/plan/{filename}")
async def get_account_plan(filename: str):
    """
    Get a specific account plan
    """
    try:
        file_path = f"./account_plans/{filename}"
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Plan not found")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return {
            "success": True,
            "filename": filename,
            "content": content
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plan not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    
    print("Starting Company Research Agent API...")
    print("React frontend should run on: http://localhost:3000")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
