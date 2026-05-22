import argparse
import hashlib
import struct


def generate_key(username: str) -> str:
    if not username:
        raise ValueError("Username must not be empty.")

    digest = hashlib.sha1(username.encode("utf-8")).digest()
    words = struct.unpack(">5I", digest)
    return "".join(f"{word:011o}" for word in words)


def pause_if_interactive(enabled: bool) -> None:
    if enabled:
        try:
            input("\nPress Enter to exit...")
        except EOFError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Keygen for Crackme 2 / errors_keygenme.")
    parser.add_argument("username", nargs="?", help="Username entered in the crackme.")
    args = parser.parse_args()

    interactive = args.username is None
    username = args.username or input("Username: ").strip()
    try:
        serial = generate_key(username)
    except (RuntimeError, ValueError, UnicodeError) as exc:
        print(f"Error: {exc}")
        pause_if_interactive(interactive)
        raise SystemExit(1)
    print(f"Username: {username}")
    print(f"Serial: {serial}")
    pause_if_interactive(interactive)


if __name__ == "__main__":
    main()
