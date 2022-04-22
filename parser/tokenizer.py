import itertools
from io import BytesIO
from tokenize import tokenize as py_tokenize, TokenInfo


def tokenize(s: str) -> list[TokenInfo]:
    tokens = list(py_tokenize(BytesIO(s.encode('utf-8')).readline))[1:]
    lines = []
    tmp = []
    is_comment = False
    for token in tokens:
        if token.string == "\n":
            is_comment = False
            lines.append(tmp.copy())
            tmp.clear()
            continue
        if token.string == '//':
            is_comment = True
        if not is_comment:
            tmp.append(token)
    lines.append(tmp)
    tokens = list(filter(lambda x: x.string.strip() != '', itertools.chain.from_iterable(lines)))
    return tokens

