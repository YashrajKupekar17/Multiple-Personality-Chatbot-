from langgraph.graph import MessagesState

class ChatbotState(MessagesState):
    """
    Custom state for the chatbot workflow.
    
    Inherits from MessagesState to manage conversation messages.
    """
    
    summary: str
    
        

def state_to_str(state: ChatbotState) -> str:
    if "summary" in state and bool(state["summary"]):
        conversation = state["summary"]
    elif "messages" in state and bool(state["messages"]):
        conversation = state["messages"]
    else:
        conversation = ""

    return f"""
ChatbotState(
conversation={conversation})
        """
