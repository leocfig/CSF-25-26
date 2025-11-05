import hashlib, sys
import argparse
import itertools
from pathlib import Path
from typing import List, Dict


SEED_PATH = Path.cwd() / "seed.txt"
SEED_PATH.touch(exist_ok=True)


def generate_passwords(timestamps: List[str]) -> List[str]:
    with open(SEED_PATH, "r") as f:
        line = f.readline()

    if not line.strip():
        print("For the first run, please just place your password in the seed file.", file=sys.stderr)
        exit(1)

    if len(line.split("\t")) == 2:
        n = int(line.split("\t")[0])
        seed = line.split("\t")[1].strip()
    else:
        n = 0
        seed = line.strip()

    # Generate password for each timestamp
    pwds = list(map(lambda ts: hashlib.sha256(str(seed + ts).encode("utf-8")).hexdigest(), timestamps))
    next_seed = hashlib.sha256(str(seed).encode("utf-8"))
    
    with open(SEED_PATH, "w") as f:
        f.write(str(n + 1) + "\t" + next_seed.hexdigest())

    return pwds


def simulate_passwords(iters: int, timestamps: List[str], secret: str) -> List[List[str]]:
    with open(SEED_PATH, 'w') as f:
        f.write(secret)

    all_passwords = map(lambda _: generate_passwords(timestamps), range(iters))
    #return itertools.chain.from_iterable(all_passwords)
    return list(all_passwords)

def main():
    parser = argparse.ArgumentParser(description="Simulate seeded passwords from a list of timestamp options")
    
    parser.add_argument("iterations", type=int, help="Number of passwords to generate")
    parser.add_argument("secret", type=str, default=None, help="Seed starting condition (initial secret)")
    parser.add_argument("timestamps", nargs="*", help="List of timestamps")
    args = parser.parse_args()

    passwords = simulate_passwords(args.iterations, args.timestamps, args.secret)
    for i in range(len(passwords)):
        print(f"Iteration {i}")
        print(*(passwords[i]), sep='\n')
    #print(*passwords, sep='\n')

if __name__ == "__main__":
    main()
