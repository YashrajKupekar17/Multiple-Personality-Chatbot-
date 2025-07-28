from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from mpdagents.config import settings
from mpdagents.domain.prompts import (
    CHATBOT_CHARACTER_CARD,SUMMARY_PROMPT, EXTEND_SUMMARY_PROMPT
)

def get_chat_model(temperature: float = 0.7, model_name: str = settings.OPENAI_LLM_MODEL) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model_name=model_name,
        temperature=temperature,
    )


def get_chatbot_response_chain():
    model = get_chat_model()
    # model = model.bind_tools(tools)
    system_message = CHATBOT_CHARACTER_CARD

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ],
        template_format="jinja2",
    )

    return prompt | model



def get_conversation_summary_chain(summary: str = ""):
    model = get_chat_model(model_name=settings.OPENAI_LLM_MODEL_SUMMARY)

    summary_message = EXTEND_SUMMARY_PROMPT if summary else SUMMARY_PROMPT

    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="messages"),
            ("human", summary_message.prompt),
        ],
        template_format="jinja2",
    )

    return prompt | model

