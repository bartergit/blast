from dataclasses import dataclass, field

btype_to_ctype_dict: dict = {'byte': 'char'}


@dataclass
class Ctx:
    listing: list = field(default_factory=list)
    structs: set[str] = field(default_factory=set)
    header: list[str] = field(default_factory=list)

    def add(self, text: str) -> None:
        self.listing.append(text)

    def btype_to_ctype(self, btype):
        if btype in self.structs:
            return f"std::shared_ptr<{btype}>"
        return btype_to_ctype_dict.get(btype, btype)

    def format_listing(self) -> str:
        return '\n'.join(self.listing)

    def format_header(self) -> str:
        return '; '.join(self.header) + ";"
