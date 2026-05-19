import sys

def generate_key(username):
    # Placeholder keygen for Crackme 4
    # Simulates an arithmetic progression hash algorithm.
    hash_val = 0
    for i, char in enumerate(username):
        hash_val += ord(char) * (i + 1)
    return f"B3AR-{hash_val:08X}"

if len(sys.argv) == 2:
    print(generate_key(sys.argv[1]))
else:
    print(generate_key('TestUser'))
