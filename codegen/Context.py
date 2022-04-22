from dataclasses import dataclass, field


@dataclass
class Ctx:
    listing: list = field(default_factory=list)

    def add(self, text: str) -> None:
        self.listing.append(text)
