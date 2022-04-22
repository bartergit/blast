from dataclasses import dataclass
from tokenize import TokenInfo


def eq(first, second):
    assert first == second, (first, second)


@dataclass
class Parser:
    tokens: list[TokenInfo]
    i: int = -1

    def peek(self) -> str:
        self.i += 1
        return self.tokens[self.i].string

    def expect(self, expected):
        self.i += 1
        eq(self.tokens[self.i].string, expected)

    def lookahead(self, n=0) -> str:
        return self.tokens[self.i + 1].string

    def eat(self) -> None:
        self.i += 1

    def empty(self):
        return self.i >= len(self.tokens) - 1

    def until(self, s: str) -> list[str]:
        tmp = []
        while True:
            token = self.peek()
            if token == s:
                return tmp
            tmp.append(token)

    def err(self):
        dumped = ([token.string for token in self.tokens[self.i:]])
        raise Exception(dumped)
