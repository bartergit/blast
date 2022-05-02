import subprocess
import sys

import yaml

from codegen.generate import generate
from parser.Parser import Parser
from parser.parse_program import parse_program
from parser.tokenizer import tokenize


def main():
    assert len(sys.argv) >= 2
    file = sys.argv[1]
    args = sys.argv[2:]
    with open(f"examples/{file}.barter") as f:
        parser = Parser(tokenize(f.read()))
        # print(dump(parser.tokens))
        program = parse_program(parser)
    listing = generate(program)
    if "--ast" in args:
        print(yaml.dump(program))
    if "--listing" in args:
        print(listing)
    if "run" in args:
        with open(f"junk/{file}.cpp", "w+") as f:
            f.write(listing)
        build = subprocess.run(f"clang junk/{file}.cpp -o junk/{file}.exe", shell=True)
        if build.returncode != 0:
            return
        result = subprocess.run(fr".\junk\{file}.exe", shell=True, capture_output=True)
        print(result.stderr.decode('utf-8') or result.stdout.decode('utf-8'))


if __name__ == '__main__':
    main()
