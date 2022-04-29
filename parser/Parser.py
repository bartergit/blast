from dataclasses import dataclass, field
from tokenize import TokenInfo


def eq(first, second):
    assert first == second, (first, second)


@dataclass
class Parser:
    tokens: list[TokenInfo]
    i: int = -1
    macros: dict = field(default_factory=dict)

    def peek(self) -> str:
        return self.peek_token().string

    def peek_token(self) -> TokenInfo:
        self.i += 1
        return self.tokens[self.i]

    def expect(self, expected):
        self.i += 1
        eq(self.tokens[self.i].string, expected)

    def lookahead(self, n=0) -> str:
        return self.tokens[self.i + 1].string

    def eat(self) -> None:
        self.i += 1

    def empty(self):
        return self.i >= len(self.tokens) - 1

    def until_tokens(self, s: str) -> list[TokenInfo]:
        tmp = []
        while True:
            token = self.peek_token()
            if token.string == s:
                return tmp
            tmp.append(token)

    def until(self, s: str) -> list[str]:
        return [token.string for token in self.until_tokens(s)]

    def dumped(self) -> list[str]:
        return [token.string for token in self.tokens[self.i + 1:]]

    def err(self):
        raise Exception(self.dumped())
