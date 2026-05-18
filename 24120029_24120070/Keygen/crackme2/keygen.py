import argparse

MASK32 = 0xFFFFFFFF


def u32(value: int) -> int:
    return value & MASK32


def rol32(value: int, bits: int) -> int:
    value &= MASK32
    bits &= 31
    return ((value << bits) | (value >> (32 - bits))) & MASK32


def ror32(value: int, bits: int) -> int:
    value &= MASK32
    bits &= 31
    return ((value >> bits) | (value << (32 - bits))) & MASK32


def bswap32(value: int) -> int:
    value &= MASK32
    return int.from_bytes(value.to_bytes(4, "little"), "big")


def build_message_schedule(username: str) -> list[int]:
    """
    Xây dựng message schedule (các từ 32-bit) cho vòng lặp SHA-1.
    Thực hiện padding chuỗi đầu vào theo chuẩn SHA-1.
    """
    data = username.encode("latin-1", errors="strict")
    if not data:
        raise ValueError("Username must not be empty.")
    if len(data) > 55:
        raise ValueError("Username must be at most 55 bytes for this crackme.")

    block = bytearray(64)
    block[: len(data)] = data
    block[len(data)] = 0x80
    block[63] = (len(data) << 3) & 0xFF

    words = [
        bswap32(int.from_bytes(block[index * 4 : index * 4 + 4], "little"))
        for index in range(16)
    ]
    for index in range(16, 80):
        words.append(rol32(words[index - 3] ^ words[index - 8] ^ words[index - 14] ^ words[index - 16], 1))
    return words


def generate_key(username: str) -> str:
    """
    Hàm sinh khóa chính cho Crackme 2.
    Sử dụng một biến thể của thuật toán băm SHA-1.
    """
    words = build_message_schedule(username)
    # Hằng số khởi tạo (Initialization vectors) của SHA-1 nhưng bị thay đổi thứ tự
    initial = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    a, b, c, d, e = initial

    for index in range(80):
        if index < 20:
            f = (b & c) | ((~b) & d)
            k = 0x5A827999
        elif index < 40:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif index < 60:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        else:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        # Tính toán vòng lặp chính của SHA-1, xoay bit và cộng dồn
        temp = u32(rol32(a, 5) + f + e + k + words[index])
        e, d, c, b, a = d, c, ror32(b, 2), a, temp

    # Cộng kết quả vòng lặp vào các hằng số khởi tạo
    digest_words = [u32(left + right) for left, right in zip(initial, [a, b, c, d, e])]
    serial = []
    
    # Custom Hex Encoding: Ánh xạ 4 bit (nibble) thành ký tự ASCII đặc biệt
    for word in digest_words:
        for byte in word.to_bytes(4, "little"):
            nibble = byte & 0x0F
            serial.append(chr(nibble + 0x30 if nibble <= 9 else nibble + 0x40))
    return "".join(serial)


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
