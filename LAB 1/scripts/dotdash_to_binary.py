#!/usr/bin/env python3
import sys

def convert_dotdash(s: str) -> str:
    out_chars = []
    for ch in s:
        if ch == '.':
            out_chars.append('0')
        elif ch == '-':
            out_chars.append('1')
        else:
            raise ValueError(f"Invalid character in input: {repr(ch)}")
    return ''.join(out_chars)

def main():
    if len(sys.argv) > 1:
        inp = " ".join(sys.argv[1:])
    else:
        try:
            inp = input("")
        except EOFError:
            print("No input provided.", file=sys.stderr)
            sys.exit(1)

    try:
        result = convert_dotdash(inp)
    except ValueError as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

    sys.stdout.write(result)
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()

