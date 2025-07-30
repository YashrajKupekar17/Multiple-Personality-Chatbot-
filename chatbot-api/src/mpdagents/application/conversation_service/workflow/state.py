from langgraph.graph import MessagesState
from typing import Optional

class ChatbotState(MessagesState):
    """
    Custom state for the chatbot workflow.
    
    Inherits from MessagesState to manage conversation messages.
    """
    
    summary: str
    context: Optional[str]
    character_id: Optional[str] = None
    character_style: Optional[str] = None
    character_perspective: Optional[str] = None
    character_name: Optional[str] = None
    
    
        

def state_to_str(state: ChatbotState) -> str:
    if "summary" in state and bool(state["summary"]):
        summary = state["summary"]
    elif "messages" in state and bool(state["messages"]):
        conversation = state["messages"]
    elif "context" in state and state["context"]:
        context = state["context"]
    else:
        conversation = ""

    return f"""
ChatbotState(
conversation={conversation}, summary = {summary}, context = {context})
        """
