class CharacterNameNotFound(Exception):
    """Exception raised when a character's name is not found."""

    def __init__(self, character_id: str):
        self.message = f"character name for {character_id} not found."
        super().__init__(self.message)


class CharacterPerspectiveNotFound(Exception):
    """Exception raised when a character's perspective is not found."""

    def __init__(self, character_id: str):
        self.message = f"character perspective for {character_id} not found."
        super().__init__(self.message)


class CharacterStyleNotFound(Exception):
    """Exception raised when a character's style is not found."""

    def __init__(self, character_id: str):
        self.message = f"character style for {character_id} not found."
        super().__init__(self.message)


class CharacterContextNotFound(Exception):
    """Exception raised when a character's context is not found."""

    def __init__(self, character_id: str):
        self.message = f"character context for {character_id} not found."
        super().__init__(self.message)
