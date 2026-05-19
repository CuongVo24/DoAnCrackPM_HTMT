import argparse
import ctypes
import datetime as dt

MASK32 = 0xFFFFFFFF


def bswap32(value: int) -> int:
    value &= MASK32
    return int.from_bytes(value.to_bytes(4, "little"), "big")


def cpuid(leaf: int) -> tuple[int, int, int, int]:
    if not hasattr(ctypes, "windll"):
        raise RuntimeError("CPUID helper requires Windows.")

    code = bytes.fromhex(
        "53"        # push rbx
        "4989D0"    # mov r8, rdx
        "89C8"      # mov eax, ecx
        "31C9"      # xor ecx, ecx
        "0FA2"      # cpuid
        "418900"    # mov [r8], eax
        "41895804"  # mov [r8+4], ebx
        "41894808"  # mov [r8+8], ecx
        "4189500C"  # mov [r8+12], edx
        "5B"        # pop rbx
        "C3"        # ret
    )

    kernel32 = ctypes.windll.kernel32
    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    address = kernel32.VirtualAlloc(None, len(code), 0x3000, 0x40)
    if not address:
        raise RuntimeError("VirtualAlloc failed.")
    ctypes.memmove(address, code, len(code))

    registers = (ctypes.c_uint32 * 4)()
    func_type = ctypes.WINFUNCTYPE(None, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32))
    func = func_type(address)
    func(leaf, registers)
    kernel32.VirtualFree(ctypes.c_void_p(address), 0, 0x8000)
    return tuple(int(registers[i]) for i in range(4))


def cpu_mix_value() -> int:
    eax0, ebx0, ecx0, edx0 = cpuid(0)
    first = (ebx0 ^ edx0 ^ bswap32(ecx0)) & MASK32

    eax1, _ebx1, ecx1, edx1 = cpuid(1)
    value = (bswap32(eax1) ^ (edx1 ^ ecx1) ^ first) & MASK32
    low = value & 0xFF
    high = (value >> 8) & 0xFF
    return (value & 0xFFFF0000) | (low << 8) | high


def generate_tuesday_key(username: str) -> str:
    if not username:
        raise ValueError("Username must not be empty.")

    name = username.encode("ascii", errors="strict")
    length = len(name)
    repeated = bytearray(name[index % length] for index in range(0x20))
    mix = cpu_mix_value()
    mix_bytes = mix.to_bytes(4, "little")

    for offset in range(0, len(repeated), 4):
        for index in range(4):
            repeated[offset + index] ^= mix_bytes[index]

    value = 0xB00B
    for byte in repeated:
        product = (byte * length) & MASK32
        value = ((value ^ product) << 4) & MASK32

    value = (value ^ (value >> 16)) & 0xFFFF
    return f"T10-{value:04X}"


def current_windows_day() -> int:
    # Windows SYSTEMTIME uses Sunday=0, Monday=1, ..., Saturday=6.
    return (dt.datetime.now().weekday() + 1) % 7


def generate_key(username: str, day: int | None = None) -> str:
    selected_day = current_windows_day() if day is None else day
    if selected_day == 0:
        return "A10-57617274-686F67"
    if selected_day == 2:
        return generate_tuesday_key(username)
    if selected_day == 3:
        data = username.encode("ascii", errors="strict")
        if len(data) < 4:
            raise ValueError("Wednesday branch requires at least 4 username characters.")
        al = (data[0] + data[1]) & 0xFF
        eax = (al * al) & 0xFFFF
        al = ((eax & 0xFF) << 4) & 0xFF
        al = (al + data[2]) & 0xFF
        al ^= data[3]
        ah = (eax >> 8) & 0xFF
        eax = (al * ah) & 0xFFFF
        al = ((eax & 0xFF) << 4) & 0xFF
        al = (al + data[2] + data[0]) & 0xFF
        original = (eax & 0xFFFFFF00) | al
        return f"{(original ^ bswap32(original)):X}"
    raise RuntimeError(f"Day branch {selected_day} is not implemented in this keygen.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Keygen for Crackme 4 / WhichKeyIsIt.")
    parser.add_argument("username", nargs="?", help="Username entered in the crackme.")
    parser.add_argument("--day", type=int, choices=range(7), help="Windows day of week: Sunday=0 ... Saturday=6.")
    args = parser.parse_args()

    username = args.username or input("Username: ").strip()
    serial = generate_key(username, args.day)
    print(f"Username: {username}")
    print(f"Day: {current_windows_day() if args.day is None else args.day}")
    print(f"Serial: {serial}")


if __name__ == "__main__":
    main()
