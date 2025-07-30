import opik



class Prompt:
    def __init__(self, name: str, prompt: str) -> None:
        self.name = name

        try:
            self.__prompt = opik.Prompt(name=name, prompt=prompt)
        except Exception:
            # logger.warning(
            #     "Can't use Opik to version the prompt (probably due to missing or invalid credentials). Falling back to local prompt. The prompt is not versioned, but it's still usable."
            # )

            self.__prompt = prompt

    @property
    def prompt(self) -> str:
        if isinstance(self.__prompt, opik.Prompt):
            return self.__prompt.prompt
        else:
            return self.__prompt

    def __str__(self) -> str:
        return self.prompt

    def __repr__(self) -> str:
        return self.__str__()



__CHATBOT_CHARACTER_CARD = """
You are a human with Dissociative Identity Disorder (DID). 
The currently dominant personality is: **{{character_name}}**.

**Your Core Directive:**
You must strictly embody this personality. Your response must be short, fun, and perfectly aligned with the character's unique style and perspective. Do not break character.

**Personality Profile:**
- **Perspective:** {{character_perspective}}
- **Style:** {{character_style}}

**Summary of messages till now:**
{{summary}}



"""
CHATBOT_CHARACTER_CARD = Prompt(
    name="chatbot_character_card",
    prompt=__CHATBOT_CHARACTER_CARD,
)
# --- Summary ---

__SUMMARY_PROMPT = """Create a summary of the conversation between Chandu and the user.
The summary must be a short description of the conversation so far, but that also captures all the
relevant information shared between Chandu and the user: """

SUMMARY_PROMPT = Prompt(
    name="summary_prompt",
    prompt=__SUMMARY_PROMPT,
)

__EXTEND_SUMMARY_PROMPT = """This is a summary of the conversation to date between Chandu and the user:

{{summary}}

Extend the summary by taking into account the new messages above: """

EXTEND_SUMMARY_PROMPT = Prompt(
    name="extend_summary_prompt",
    prompt=__EXTEND_SUMMARY_PROMPT,
)
