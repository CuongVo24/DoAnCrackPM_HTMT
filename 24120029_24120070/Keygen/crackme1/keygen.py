import argparse
import ctypes
import platform
import struct

MASK32 = 0xFFFFFFFF


def ror(value: int, bits: int, size: int) -> int:
    mask = (1 << size) - 1
    return ((value >> bits) | (value << (size - bits))) & mask


def rol(value: int, bits: int, size: int) -> int:
    mask = (1 << size) - 1
    return ((value << bits) | (value >> (size - bits))) & mask


def bswap32(value: int) -> int:
    return struct.unpack(">I", struct.pack("<I", value & MASK32))[0]


def get_computer_name() -> str:
    if hasattr(ctypes, "windll"):
        buf = ctypes.create_string_buffer(256)
        size = ctypes.c_uint32(len(buf))
        if ctypes.windll.kernel32.GetComputerNameA(buf, ctypes.byref(size)):
            return buf.value.decode("mbcs", errors="ignore")
    return platform.node()


def machine_hash(computer_name: str) -> int:
    # Lấy chuỗi tên máy tính và thêm null padding đủ dài để tránh lỗi index
    data = computer_name.encode("mbcs", errors="ignore") + b"\x00\x00\x00\x00"
    eax = ebx = ecx = edx = 0
    index = 0

    # Vòng lặp duyệt qua từng cụm 2 byte (word) của tên máy tính
    while data[index] != 0 or data[index + 1] != 0:
        al = data[index]
        dl = data[index + 1]
        
        # Mô phỏng chính xác giá trị các thanh ghi theo Assembly
        eax = (eax & 0xFFFFFF00) | al
        edx = (edx & 0xFFFFFF00) | dl
        
        # Xoay phải 4 bit byte đầu tiên
        al = ror(al, 4, 8)
        # Đảo bit byte thứ 2
        dl = (~dl) & 0xFF
        
        eax = (eax & 0xFFFFFF00) | al
        edx = (edx & 0xFFFFFF00) | dl
        
        # Cộng dồn vào al
        al = (al + dl) & 0xFF
        eax = (eax & 0xFFFFFF00) | al

        # Cập nhật các thanh ghi dựa trên eax, ebx, ecx, edx theo logic của hàm hash
        ebx = (ebx + eax) & MASK32
        edx = (edx * eax) & MASK32
        ecx = (ecx + edx) & MASK32
        
        # Hoán đổi ebx và edx
        ebx, edx = edx, ebx
        index += 2

    # Kết quả trả về là tổng của ebx (đã bị đảo byte theo little-endian thành big-endian) và ecx
    return (bswap32(ebx) + ecx) & MASK32


def generate_key(username: str, computer_name: str | None = None) -> str:
    # Độ dài username phải từ 4 đến 32 ký tự
    if not 4 <= len(username) <= 32:
        raise ValueError("Username length must be from 4 to 32 characters.")

    # Bước 1: Sinh giá trị machine_hash từ Computer Name
    mh = machine_hash(computer_name or get_computer_name())
    user_bytes = username.encode("mbcs", errors="strict")
    
    # Khởi tạo giá trị thanh ghi
    ebx, ecx, edx = 0, 0x7FFF, 0

    # Bước 2: Vòng lặp biến đổi từng byte của username
    for index, char in enumerate(user_bytes):
        # Lấy byte hiện tại và byte kế tiếp tạo thành 1 word (16-bit)
        next_char = user_bytes[index + 1] if index + 1 < len(user_bytes) else 0
        bx = char | (next_char << 8)
        
        # Sửa lỗi chí mạng: Lệnh `mov (%esi), %bx` trong Assembly chỉ ghi đè 16 bit thấp (%bx)
        # của thanh ghi 32-bit ebx. Ta phải giữ nguyên 16 bit cao của ebx từ vòng lặp trước!
        ebx = (ebx & 0xFFFF0000) | bx
        
        # Shift ebx sang trái 8 bit
        ebx = (ebx << 8) & MASK32
        
        # Trích xuất 1 phần của machine hash
        eax = mh & 0x00F8F800
        ebx ^= eax
        
        # Cộng với hằng số magic 0x006C6F6C ('lol\x00')
        ebx = (ebx + 0x006C6F6C) & MASK32
        
        # XOR với hằng số 0x10101010
        ebx ^= 0x10101010

        # Cập nhật ecx và edx
        edx = (edx + ebx) & MASK32
        ecx = (ecx + ebx) & MASK32
        ecx = (ecx - 0x002D3D2D) & MASK32
        ecx = (ecx * 8) & MASK32
        ecx = (ecx + eax) & MASK32

    # Bước 3: 16 vòng lặp bswap và rotate kết quả cuối cùng
    esi = edi = 0
    for _ in range(0x10):
        edi = (edi + ecx) & MASK32
        esi = (esi + edx) & MASK32
        
        # Rotate Left 16 bits sau khi Byte Swap
        edi = rol(bswap32(edi), 16, 32)
        # Rotate Right 16 bits sau khi Byte Swap
        esi = ror(bswap32(esi), 16, 32)

    # Bước 4: Định dạng Serial thành 4 phần tử DWORD hệ Hexa viết hoa
    return f"{ecx:08X}-{edx:08X}-{edi:08X}-{esi:08X}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Keygen for Crackme 1 / KeygenMe1.")
    parser.add_argument("username", nargs="?", help="Username entered in the crackme.")
    parser.add_argument("--computer-name", help="Override GetComputerNameA for reproducible report examples.")
    args = parser.parse_args()

    username = args.username or input("Username: ").strip()
    serial = generate_key(username, args.computer_name)
    print(f"Username: {username}")
    print(f"ComputerName: {args.computer_name or get_computer_name()}")
    print(f"Serial: {serial}")


if __name__ == "__main__":
    main()
