import argparse

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def rol8(value: int, bits: int) -> int:
    return ((value << bits) | (value >> (8 - bits))) & 0xFF


def rotate(text: str, offset: int) -> str:
    offset %= len(text)
    return text[offset:] + text[:offset]


def build_table(username: str) -> str:
    # Tính toán độ lệch xoay dựa vào độ dài username nhân 4
    offset = len(username) * 4
    # Nếu lớn hơn 0x3C thì cố định ở mức 0x1E
    if offset > 0x3C:
        offset = 0x1E
    # Trả về bảng ALPHABET sau khi đã được xoay vòng
    return rotate(ALPHABET, offset)


def transform_username(username: str, table: str) -> str:
    # Thêm byte null vào cuối username
    data = username.encode("ascii") + b"\x00"
    # Khởi tạo giá trị dl bằng cách lấy byte đầu tiên xoay trái 3 bit
    dl = rol8(data[0], 3)
    output = []

    # Vòng lặp XOR và cộng dồn các giá trị của username
    for index in range(len(username)):
        # XOR ký tự hiện tại với ký tự kế tiếp (có thể là byte null ở cuối)
        value = data[index] ^ data[index + 1]
        # Cộng thêm giá trị dl hiện tại
        value = (value + dl) & 0xFF
        # Cập nhật lại dl cho vòng lặp tiếp theo
        dl = (dl + value) & 0xFF
        # Ánh xạ giá trị vừa tính với bảng (modulo cho độ dài bảng)
        output.append(table[value % len(table)])

    return "".join(output)


def generate_key(username: str) -> str:
    if not username:
        raise ValueError("Username must not be empty.")
    if any(char not in ALPHABET for char in username):
        raise ValueError("Username may only contain 0-9, a-z, and A-Z.")

    # Bước 1: Xây dựng bảng thay thế (substitution table) từ chuỗi ALPHABET
    table = build_table(username)
    # Bước 2: Biến đổi username qua phép toán XOR và phép cộng rolling (dl)
    transformed = transform_username(username, table)
    serial = []

    # Bước 3: Tạo serial dựa trên chỉ số (index) trong bảng thay thế
    for plain_char, transformed_char in zip(username, transformed):
        transformed_index = table.index(transformed_char)
        plain_index = table.index(plain_char)
        # Ký tự serial là ký tự ở vị trí bằng tổng 2 index (modulo độ dài bảng)
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
