import hashlib
import sys

def generate_key(username):
    # Crackme 2 uses an SEH-obfuscated SHA-1 hash.
    # The output is formatted into a 55-character string.
    h = hashlib.sha1(username.encode()).digest()
    
    # We use a placeholder logic for the formatting step 
    # since the exact SEH-based modulo arithmetic (div %eax) is obfuscated.
    # For demonstration, we format it as an octal string padded to 55 chars.
    import struct
    words = struct.unpack('>5I', h)
    serial = ''.join(f'{w:011o}' for w in words)
    return serial

if len(sys.argv) == 2:
    print(generate_key(sys.argv[1]))
else:
    print(generate_key('TestUser'))
