import argparse
import hashlib
import struct


def generate_key(username: str) -> str:
    if not username:
        raise ValueError("Username must not be empty.")

    digest = hashlib.sha1(username.encode("utf-8")).digest()
    words = struct.unpack(">5I", digest)
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
