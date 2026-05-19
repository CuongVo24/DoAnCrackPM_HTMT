import argparse

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def rol8(value: int, bits: int) -> int:
    return ((value << bits) | (value >> (8 - bits))) & 0xFF


def rotate(text: str, offset: int) -> str:
    offset %= len(text)
    return text[offset:] + text[:offset]


def build_table(username: str) -> str:
    offset = len(username) * 4
    if offset > 0x3C:
        offset = 0x1E
    return rotate(ALPHABET, offset)


def transform_username(username: str, table: str) -> str:
    data = username.encode("ascii") + b"\x00"
    dl = rol8(data[0], 3)
    output = []

    for index in range(len(username)):
        value = data[index] ^ data[index + 1]
        value = (value + dl) & 0xFF
        dl = (dl + value) & 0xFF
        output.append(table[value % len(table)])

    return "".join(output)


def generate_key(username: str) -> str:
    if not username:
        raise ValueError("Username must not be empty.")
    if any(char not in ALPHABET for char in username):
        raise ValueError("Username may only contain 0-9, a-z, and A-Z.")

    table = build_table(username)
    transformed = transform_username(username, table)
    serial = []

    for plain_char, transformed_char in zip(username, transformed):
        transformed_index = table.index(transformed_char)
        plain_index = table.index(plain_char)
        serial.append(table[(transformed_index + plain_index) % len(table)])

    return "".join(serial)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keygen for Crackme 3 / d2k2.crkme.09.")
    parser.add_argument("username", nargs="?", help="Username entered in the crackme.")
    args = parser.parse_args()

    username = args.username or input("Username: ").strip()
    serial = generate_key(username)
    print(f"Username: {username}")
    print(f"Serial: {serial}")


if __name__ == "__main__":
    main()
