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
    data = computer_name.encode("mbcs", errors="ignore") + b"\x00\x00"
    eax = ebx = ecx = edx = 0
    index = 0

    while data[index] != 0 or data[index + 1] != 0:
        al = ror(data[index], 4, 8)
        dl = (~data[index + 1]) & 0xFF
        al = (al + dl) & 0xFF

        eax = (eax & 0xFFFFFF00) | al
        ebx = (ebx + eax) & MASK32
        edx = (edx * eax) & MASK32
        ecx = (ecx + edx) & MASK32
        ebx, edx = edx, ebx
        index += 2

    return (bswap32(ebx) + ecx) & MASK32


def generate_key(username: str, computer_name: str | None = None) -> str:
    if not 4 <= len(username) <= 32:
        raise ValueError("Username length must be from 4 to 32 characters.")

    mh = machine_hash(computer_name or get_computer_name())
    user_bytes = username.encode("mbcs", errors="strict")
    ebx, ecx, edx = 0, 0x7FFF, 0

    for index, char in enumerate(user_bytes):
        next_char = user_bytes[index + 1] if index + 1 < len(user_bytes) else 0
        bx = char | (next_char << 8)
        ebx = (bx << 8) & MASK32
        eax = mh & 0x00F8F800
        ebx ^= eax
        ebx = (ebx + 0x006C6F6C) & MASK32
        ebx ^= 0x10101010

        edx = (edx + ebx) & MASK32
        ecx = (ecx + ebx) & MASK32
        ecx = (ecx - 0x002D3D2D) & MASK32
        ecx = (ecx * 8) & MASK32
        ecx = (ecx + eax) & MASK32

    esi = edi = 0
    for _ in range(0x10):
        edi = (edi + ecx) & MASK32
        esi = (esi + edx) & MASK32
        edi = rol(bswap32(edi), 16, 32)
        esi = ror(bswap32(esi), 16, 32)

    return f"{ecx:08X}-{edx:08X}-{edi:08X}-{esi:08X}"


def pause_if_interactive(enabled: bool) -> None:
    if enabled:
        try:
            input("\nPress Enter to exit...")
        except EOFError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Keygen for Crackme 1 / KeygenMe1.")
    parser.add_argument("username", nargs="?", help="Username entered in the crackme.")
    parser.add_argument("--computer-name", help="Override GetComputerNameA for reproducible report examples.")
    args = parser.parse_args()

    interactive = args.username is None
    username = args.username or input("Username: ").strip()
    try:
        serial = generate_key(username, args.computer_name)
    except (RuntimeError, ValueError, UnicodeError) as exc:
        print(f"Error: {exc}")
        pause_if_interactive(interactive)
        raise SystemExit(1)
    print(f"Username: {username}")
    print(f"ComputerName: {args.computer_name or get_computer_name()}")
    print(f"Serial: {serial}")
    pause_if_interactive(interactive)


if __name__ == "__main__":
    main()
