import argparse

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def rol8(value: int, bits: int) -> int:
    return ((value << bits) | (value >> (8 - bits))) & 0xFF


def rotate(text: str, offset: int) -> str:
    offset %= len(text)
    return text[offset:] + text[:offset]


def build_table(username: str) -> str:
    """
    Tạo bảng ký tự thay thế (substitution table) bằng cách dịch vòng (rotate)
    bảng chữ cái gốc dựa trên độ dài của username.
    """
    offset = len(username) * 4
    if offset > 0x3C:
        offset = 0x1E
    return rotate(ALPHABET, offset)


def transform_username(username: str, table: str) -> str:
    """
    Thực hiện biến đổi (transform) username thành một chuỗi mã hóa trung gian
    sử dụng các phép toán XOR, cộng dồn (add) và dịch bit (rol8).
    """
    data = username.encode("ascii") + b"\x00"
    dl = rol8(data[0], 3)
    output = []

    # Duyệt qua từng ký tự của username
    for index in range(len(username)):
        value = data[index] ^ data[index + 1]
        value = (value + dl) & 0xFF
        dl = (dl + value) & 0xFF
        # Ánh xạ giá trị vừa tính qua bảng ký tự custom
        output.append(table[value % len(table)])

    return "".join(output)


def generate_key(username: str) -> str:
    """
    Hàm sinh khóa chính cho Crackme 3.
    Dựa trên việc đối chiếu chỉ số (index) của username gốc và chuỗi biến đổi
    để sinh ra Serial từ bảng ký tự.
    """
    if not username:
        raise ValueError("Username must not be empty.")
    if any(char not in ALPHABET for char in username):
        raise ValueError("Username may only contain 0-9, a-z, and A-Z.")

    # Bước 1: Xây dựng bảng thay thế
    table = build_table(username)
    # Bước 2: Tạo chuỗi username bị biến đổi
    transformed = transform_username(username, table)
    serial = []

    # Bước 3: Tính toán Serial bằng cách cộng index của từng ký tự trong bảng
    for plain_char, transformed_char in zip(username, transformed):
        transformed_index = table.index(transformed_char)
        plain_index = table.index(plain_char)
        serial.append(table[(transformed_index + plain_index) % len(table)])

    return "".join(serial)


def pause_if_interactive(enabled: bool) -> None:
    if enabled:
        try:
            input("\nPress Enter to exit...")
        except EOFError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Keygen for Crackme 3 / d2k2.crkme.09.")
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
