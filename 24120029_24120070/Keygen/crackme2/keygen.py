import argparse
import hashlib
import struct


def generate_key(username: str) -> str:
    # Username không được để trống
    if not username:
        raise ValueError("Username must not be empty.")

    # Bước 1: Băm chuỗi username bằng thuật toán SHA-1
    digest = hashlib.sha1(username.encode("utf-8")).digest()
    
    # Bước 2: Tách chuỗi hash (20 bytes) thành 5 block, mỗi block là 1 số nguyên 32-bit (DWORD) dạng big-endian
    words = struct.unpack(">5I", digest)
    
    # Bước 3: Định dạng từng DWORD thành chuỗi số hệ bát phân (octal) có độ dài 11 ký tự, 
    # ghép 5 block lại ta được Serial dài 55 ký tự
    return "".join(f"{word:011o}" for word in words)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keygen for Crackme 2 / errors_keygenme.")
    parser.add_argument("username", nargs="?", help="Username entered in the crackme.")
    args = parser.parse_args()

    username = args.username or input("Username: ").strip()
    serial = generate_key(username)
    print(f"Username: {username}")
    print(f"Serial: {serial}")


if __name__ == "__main__":
    main()
