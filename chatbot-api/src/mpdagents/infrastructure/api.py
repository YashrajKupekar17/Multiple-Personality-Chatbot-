from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from opik.integrations.langchain import OpikTracer
from pydantic import BaseModel

from mpdagents.domain.character_factory import CharacterFactory
from mpdagents.application.conversation_service.generate_response import (
    get_response,
    get_streaming_response,
)
from mpdagents.application.conversation_service.reset_conversation import (
    reset_conversation_state,
)
# from mpdagents.domain.character_factory import characterFactory

from .opik_utils import configure

configure()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for the API."""
    # Startup code (if any) goes here
    yield
    # Shutdown code goes here
    opik_tracer = OpikTracer()
    opik_tracer.flush()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str
    thread_id: str | None = None
    character_id: str | None = None
    new_thread: bool = False

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        character_factory = CharacterFactory()
        character = character_factory.get_character(chat_message.character_id)
        
        response, *_ = await get_response(  # Fixed the function call
            messages=chat_message.message,
            thread_id=chat_message.thread_id,
            character_id=chat_message.character_id,
            character_name=character.name,
            character_style=character.style,
            character_perspective=character.perspective,
            new_thread=chat_message.new_thread,
        )
        
        return {
            "response": response,
            "thread_id": chat_message.thread_id,
            "character_id": chat_message.character_id
        }
    except Exception as e:
        opik_tracer = OpikTracer()
        opik_tracer.flush()
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Validate required fields
            if "message" not in data or "character_id" not in data:
                await websocket.send_json({
                    "error": "Invalid message format. Required fields: 'message' and 'character_id'"
                })
                continue
            
            try:
                character_factory = CharacterFactory()
                character = character_factory.get_character(data["character_id"])
                
                # Extract thread_id from data, not from undefined chat_message
                thread_id = data.get("thread_id")
                
                # Use streaming response
                response_stream = get_streaming_response(
                    messages=data["message"],
                    character_id=data["character_id"],
                    thread_id=thread_id,  # Fixed: use data["thread_id"] instead of chat_message.thread_id
                    character_name=character.name,
                    character_perspective=character.perspective,
                    character_style=character.style,
                    new_thread=data.get("new_thread", False),  # Added new_thread parameter if needed
                )
                
                # Send initial message to indicate streaming has started
                await websocket.send_json({"streaming": True})
                
                # Stream each chunk of the response
                full_response = ""
                async for chunk in response_stream:
                    full_response += chunk
                    await websocket.send_json({"chunk": chunk})
                
                # Send final response
                await websocket.send_json({
                    "response": full_response, 
                    "streaming": False,
                    "thread_id": thread_id,  # Include thread_id in response
                    "character_id": data["character_id"]  # Include character_id in response
                })
                
            except Exception as e:
                opik_tracer = OpikTracer()
                opik_tracer.flush()
                await websocket.send_json({"error": str(e)})
                
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")  # Optional: log disconnection
        pass

@app.post("/reset-memory")
async def reset_conversation():
    """Resets the conversation state. It deletes the two collections needed for keeping LangGraph state in MongoDB.

    Raises:
        HTTPException: If there is an error resetting the conversation state.
    Returns:
        dict: A dictionary containing the result of the reset operation.
    """
    try:
        result = await reset_conversation_state()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
