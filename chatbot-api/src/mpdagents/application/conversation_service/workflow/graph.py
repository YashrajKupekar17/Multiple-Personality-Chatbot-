
from functools import lru_cache
from langgraph.graph import StateGraph, START, END
from mpdagents.application.conversation_service.workflow.node import (
    conversation_node,
    summarize_conversation_node,
)
from mpdagents.application.conversation_service.workflow.egdes  import should_summarize_conversation
from mpdagents.application.conversation_service.workflow.state import ChatbotState
from mpdagents.infrastructure.opik_utils import configure


configure()

@lru_cache(maxsize=1)
def create_workflow_graph():
    graph_builder = StateGraph(ChatbotState)

    # Add all nodes
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)
    
    # Define the flow
    graph_builder.add_edge(START, "conversation_node")
    graph_builder.add_conditional_edges("conversation_node", should_summarize_conversation)
    graph_builder.add_edge("summarize_conversation_node", END)
    

    # configure()
    return graph_builder

# Compiled without a checkpointer. Used for LangGraph Studio
graph = create_workflow_graph().compile()
