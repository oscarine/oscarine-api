import random
import string


class Base:
    @staticmethod
    def random_lower_string(str_length: int = 32) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=str_length))

    def random_email(self) -> str:
        return f"{self.random_lower_string()}@{self.random_lower_string()}.com"

    @staticmethod
    def random_integer() -> int:
        return random.randint(50, 1000)
