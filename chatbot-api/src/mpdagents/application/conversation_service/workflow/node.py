
from mpdagents.application.conversation_service.workflow.chains import get_chatbot_response_chain, get_conversation_summary_chain
from mpdagents.application.conversation_service.workflow.state import ChatbotState
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from mpdagents.config import settings
from mpdagents.application.rag.rag import get_rag_context,Rag_Input_Schema
from typing import Optional
from langchain_core.messages import HumanMessage

async def conversation_node(state: ChatbotState, config: RunnableConfig):
    summary = state.get("summary", "")
    rag_context = state.get("context","")
    conversation_chain = get_chatbot_response_chain()

    response = await conversation_chain.ainvoke(
        {
            "messages": state["messages"],
            "summary": summary,
            "context": rag_context,
            "character_id": state.get("character_id"),
            "character_name": state.get("character_name"),
            "character_style": state.get("character_style"),
            "character_perspective": state.get("character_perspective"),
        },
        config,
    )
    
    return {"messages": response}

async def summarize_conversation_node(state: ChatbotState):
    summary = state.get("summary", "")
    summary_chain = get_conversation_summary_chain(summary)

    response = await summary_chain.ainvoke(
        {
            "messages": state["messages"],
            "summary": summary,
        }
    )

    delete_messages = [
        RemoveMessage(id=m.id)
        for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
    ]
    return {"summary": response.content, "messages": delete_messages}


async def rag_context_injection_node(state: ChatbotState):
    """
    Context injection node to add RAG context to the conversation.
    Retrieves relevant documents based on the user's latest message.
    """
    
    # Extract the latest user message
    if not state["messages"]:
        return {"context": None}
    
    # Get the last user message (skip AI messages)
    user_query = ""
    for message in reversed(state["messages"]):
        if isinstance(message, HumanMessage):
            user_query = message.content
            break
    
    if not user_query.strip():
        return {"context": None}
    
    try:
        # Create RAG input
        rag_input = Rag_Input_Schema(
            query=user_query,
            k=3,
            namespace="motion"
        )
        
        # Get RAG context
        results = await get_rag_context(rag_input)
        
        # Format context for the LLM
        formatted_context = format_rag_context(results)
        
        return {"context": formatted_context}
        
    except Exception as e:
        print(f"Error in RAG context injection: {e}")
        return {"context": None}

def format_rag_context(query_results) -> Optional[str]:
    """Format RAG results into a context string for the LLM"""
    
    if not query_results or not hasattr(query_results, 'matches') or not query_results.matches:
        return None
    
    context_parts = []
    context_parts.append("Here is relevant context from the knowledge base:\n")
    
    for i, match in enumerate(query_results.matches[:3]):  # Top 3 results
        text = match.metadata.get('text', 'No content available')
        source = match.metadata.get('source', 'Unknown source')
        score = match.score
        
        context_parts.append(f"**Context {i+1}** (Relevance: {score:.3f}):")
        context_parts.append(f"Source: {source}")
        context_parts.append(f"Content: {text[:500]}...")  # Limit length
        context_parts.append("")  # Empty line for separation
    
    return "\n".join(context_parts)
