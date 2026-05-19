import sys

def generate_key(username):
    # Placeholder keygen for Crackme 3
    # Simulates a standard XOR-based name mangling algorithm.
    serial = ""
    for char in username:
        serial += hex(ord(char) ^ 0x3A)[2:].upper()
    return f"CRK3-{serial}"

if len(sys.argv) == 2:
    print(generate_key(sys.argv[1]))
else:
    print(generate_key('TestUser'))
