from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from opik.integrations.langchain import OpikTracer
from pydantic import BaseModel

from mpdagents.application.conversation_service.generate_response import (
    get_response,
    # get_streaming_response,
)
from mpdagents.application.conversation_service.reset_conversation import (
    reset_conversation_state,
)
# from mpdagents.domain.philosopher_factory import PhilosopherFactory

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
    new_thread: bool = False



@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        # philosopher_factory = PhilosopherFactory()
        # philosopher = philosopher_factory.get_philosopher(chat_message.philosopher_id)

        response, _ = await get_response(
            messages=chat_message.message,
            thread_id=chat_message.thread_id,
            new_thread=chat_message.new_thread,
            # philosopher_id=chat_message.philosopher_id,
            # philosopher_name=philosopher.name,
            # philosopher_perspective=philosopher.perspective,
            # philosopher_style=philosopher.style,
            # philosopher_context="",
        )
        return {
            "response": response,
            "thread_id": chat_message.thread_id
        }

    except Exception as e:
        opik_tracer = OpikTracer()
        opik_tracer.flush()

        raise HTTPException(status_code=500, detail=str(e))

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
