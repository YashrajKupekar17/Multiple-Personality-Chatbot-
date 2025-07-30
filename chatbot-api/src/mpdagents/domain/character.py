
from pydantic import BaseModel, Field

class Character(BaseModel):
    """A class representing a character agent with memory capabilities.

    Args:
        id (str): Unique identifier for the character.
        name (str): Name of the character.
        perspective (str): Description of the character's theoretical views
            about AI.
        style (str): Description of the character's talking style.
    """

    id: str = Field(description="Unique identifier for the character")
    name: str = Field(description="Name of the character")
    perspective: str = Field(
        description="Description of the character's theoretical views about AI"
    )
    style: str = Field(description="Description of the character's talking style")

    def __str__(self) -> str:
        return f"Character(id={self.id}, name={self.name}, perspective={self.perspective}, style={self.style})"

