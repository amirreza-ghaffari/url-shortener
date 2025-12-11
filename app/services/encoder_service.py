import uuid_utils as uuid
from uuid import UUID

BASE62_CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


class EncoderService:

    @staticmethod
    def uuid_to_base62(uid: UUID) -> str:
        """
        Convert UUID to base62 string for short URLs.

        Args:
            uid: UUID object to encode

        Returns:
            Base62 encoded string (~22 characters)
        """
        num = uid.int

        if num == 0:
            return BASE62_CHARACTERS[0]

        result = []
        while num:
            num, remainder = divmod(num, 62)
            result.append(BASE62_CHARACTERS[remainder])

        return ''.join(reversed(result))

    @staticmethod
    def generate_uuid7() -> UUID:
        """
        Generate a time-ordered UUID.

        Returns:
            UUID: A new UUID7 instance
        """
        return uuid.uuid7()

    @staticmethod
    def base62_to_uuid(code: str) -> UUID:
        """
        Convert base62 string back to UUID.

        Args:
            code: Base62 encoded string

        Returns:
            UUID object

        Raises:
            ValueError: If code contains invalid characters
        """
        num = 0

        for char in code:
            if char not in BASE62_CHARACTERS:
                raise ValueError(f"Invalid character '{char}' in base62 code")
            num = num * 62 + BASE62_CHARACTERS.index(char)

        return UUID(int=num)