
from mpdagents.application.conversation_service.workflow.chains import get_chatbot_response_chain, get_conversation_summary_chain
from mpdagents.application.conversation_service.workflow.state import ChatbotState
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from mpdagents.config import settings

async def conversation_node(state: ChatbotState, config: RunnableConfig):
    summary = state.get("summary", "")
    conversation_chain = get_chatbot_response_chain()

    response = await conversation_chain.ainvoke(
        {
            "messages": state["messages"],
            "summary": summary,
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


