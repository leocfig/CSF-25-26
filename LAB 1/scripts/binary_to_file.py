#!/usr/bin/env python3
import sys

def binary_to_bytes(binary: str) -> bytes:
    # pad to nearest byte if necessary
    if len(binary) % 8 != 0:
        binary = binary.ljust((len(binary) + 7) // 8 * 8, '0')
    chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return bytes(int(chunk, 2) for chunk in chunks if chunk)

def main():
    if len(sys.argv) == 1:
        print("An output file must be provided (e.g. \"output.bin\").")
        sys.exit(1)
    elif len(sys.argv) > 1:
        filename = sys.argv[1]
        if len(sys.argv) > 2:
            binary_input = sys.argv[2]
        else:
            try:
                binary_input = input("")
            except EOFError:
                print("No input provided.", file=sys.stderr)
                sys.exit(1)

    try:
        data = binary_to_bytes(binary_input)
        with open(filename, "wb") as f:
            f.write(data)
        print(f"Wrote {len(data)} bytes to {filename}")
    except Exception as e:
        print(f"Error:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
