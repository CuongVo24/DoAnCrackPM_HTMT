import argparse
import ctypes
import datetime as dt
import hashlib
import os
import subprocess

MASK32 = 0xFFFFFFFF
DEFAULT_DAY = 2


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
    """
    Thuật toán sinh khóa cho nhánh Thứ 3 (Tuesday).
    Sử dụng CPUID mix XOR với 32 byte username lặp lại, sau đó nhân dồn.
    """
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
    multiplier = 0
    for byte in repeated:
        multiplier |= byte
        multiplier = (multiplier * length) & MASK32
        value = ((value ^ multiplier) << 4) & MASK32
        multiplier &= 0xFFFFFF00

    value = (value ^ (value >> 16)) & 0xFFFF
    return f"T10-{value:04X}"


def generate_monday_key(username: str) -> str:
    """
    Thuật toán sinh khóa cho nhánh Thứ 2 (Monday).
    Lấy byte thứ 4 của username XOR với 0x02 hoặc 0x03.
    """
    data = username.encode("ascii", errors="strict")
    if len(data) < 4:
        raise ValueError("Monday branch requires at least 4 username characters.")

    last = data[3] ^ 0x02
    if last == 0x7F:
        last = data[3] ^ 0x03
    return "<3<3" + chr(last)


def generate_wednesday_key(username: str) -> str:
    """
    Thuật toán sinh khóa cho nhánh Thứ 4 (Wednesday).
    Thực hiện các phép nhân, cộng chéo các byte và dịch bit để tạo checksum.
    """
    data = username.encode("ascii", errors="strict")
    if len(data) < 4:
        raise ValueError("Wednesday branch requires at least 4 username characters.")

    total = data[0] + data[1]
    ax = (total * total) & 0xFFFF
    al = ((ax & 0xFF) << 4) & 0xFF
    al = (al + data[2]) & 0xFF
    al ^= data[3]
    ah = (ax >> 8) & 0xFF
    ax = (al * ah) & 0xFFFF
    al = ((ax & 0xFF) << 4) & 0xFF
    al = (al + data[2] + data[0]) & 0xFF
    answer = bswap32(((ax & 0xFF00) | al) & 0xFFFF) | ((ax & 0xFF00) | al)
    return f"{answer & MASK32:08X}"


def generate_thursday_key(username: str) -> str:
    """
    Thuật toán sinh khóa cho nhánh Thứ 5 (Thursday).
    Băm MD5 username và đảo ngược vị trí hai nửa của kết quả băm.
    """
    digest = hashlib.md5(username.encode("latin-1", errors="strict")).digest()
    return (digest[8:16] + digest[:8]).hex().upper()


def generate_friday_key(username: str) -> str:
    """
    Thuật toán sinh khóa cho nhánh Thứ 6 (Friday).
    Sử dụng biến thể của Adler-32 (module 0xFFF1) lên username.
    """
    total = 1
    multi = 0
    for byte in username.encode("latin-1", errors="strict"):
        total += byte
        multi += total

    total %= 0xFFF1
    multi %= 0xFFF1
    value = ((multi << 16) + total) & MASK32
    return f"{value:08X}-0400-0400-1229-03E9"


def generate_saturday_key(username: str) -> str:
    """
    Thuật toán sinh khóa cho nhánh Thứ 7 (Saturday).
    Do target sử dụng dll ngoài chứa tổ hợp hàm băm siêu phức tạp (MD5, SHA-1, RIPEMD),
    nhóm thực hiện "Serial Fishing" thông qua kỹ thuật Memory Patching:
    - Load helper.dll vào RAM thông qua PowerShell (vì dll là 32-bit).
    - Patch lệnh JMP vào offset 0x519E để ép nhảy vào nhánh Thứ 7.
    - Đọc kết quả Serial 8-byte trực tiếp từ vùng nhớ (offset 0xF9D4).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dll_paths = [
        os.path.join(script_dir, "helper.dll"),
        os.path.abspath(os.path.join(script_dir, "..", "..", "..", "Project crack phan mem", "crackme", "crack04", "helper.dll"))
    ]
    dll_path = next((p for p in dll_paths if os.path.exists(p)), None)
    
    if not dll_path:
        raise RuntimeError("helper.dll not found. Saturday branch requires helper.dll to be present.")
        
    csharp_code = """
using System;
using System.Runtime.InteropServices;
public class Helper {
    [DllImport("kernel32.dll")]
    public static extern IntPtr LoadLibrary(string dllToLoad);
    [DllImport("kernel32.dll")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procedureName);
    
    [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    public delegate int Xor0Fun(string username, string serial);
    
    public static string GetDay6(string dllPath, string username) {
        IntPtr hMod = LoadLibrary(dllPath);
        if (hMod == IntPtr.Zero) return "Error LoadLibrary";
        
        IntPtr patchAddr = IntPtr.Add(hMod, 0x519E);
        uint oldProtect;
        VirtualProtect(patchAddr, (UIntPtr)2, 0x40, out oldProtect);
        Marshal.WriteByte(patchAddr, 0, 0xEB);
        Marshal.WriteByte(patchAddr, 1, 0x5D);
        VirtualProtect(patchAddr, (UIntPtr)2, oldProtect, out oldProtect);
        
        IntPtr pFunc = GetProcAddress(hMod, "xor0_fun");
        Xor0Fun func = (Xor0Fun)Marshal.GetDelegateForFunctionPointer(pFunc, typeof(Xor0Fun));
        
        func(username, "0000000000000000");
        
        IntPtr outBuf = IntPtr.Add(hMod, 0xF9D4);
        byte[] result = new byte[8];
        Marshal.Copy(outBuf, result, 0, 8);
        return BitConverter.ToString(result).Replace("-", "");
    }
}
"""
    ps_script = f'''
$code = @"
{csharp_code}
"@
Add-Type -TypeDefinition $code
[Helper]::GetDay6('{dll_path.replace("\\", "\\\\")}', '{username.replace("'", "''")}')
'''
    import base64
    b64 = base64.b64encode(ps_script.encode('utf-16le')).decode('utf-8')
    
    ps_exe = r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe"
    if not os.path.exists(ps_exe):
        ps_exe = "powershell.exe"
        
    try:
        result = subprocess.run([ps_exe, "-NoProfile", "-ExecutionPolicy", "Bypass", "-EncodedCommand", b64],
                                capture_output=True, text=True, check=True)
        serial = result.stdout.strip()
        if "Error" in serial or not serial:
            raise RuntimeError(f"Failed to generate Day 6 key: {serial}")
        return serial
    except Exception as e:
        if isinstance(e, subprocess.CalledProcessError):
            raise RuntimeError(f"PowerShell execution failed: {e.stderr}")
        raise RuntimeError(f"PowerShell execution failed: {e}")



def current_windows_day() -> int:
    # Windows SYSTEMTIME uses Sunday=0, Monday=1, ..., Saturday=6.
    return (dt.datetime.now().weekday() + 1) % 7


def generate_key(username: str, day: int | None = None) -> str:
    selected_day = DEFAULT_DAY if day is None else day
    if selected_day == 0:
        return "A10-57617274-686F67"
    if selected_day == 1:
        return generate_monday_key(username)
    if selected_day == 2:
        return generate_tuesday_key(username)
    if selected_day == 3:
        return generate_wednesday_key(username)
    if selected_day == 4:
        return generate_thursday_key(username)
    if selected_day == 5:
        return generate_friday_key(username)
    if selected_day == 6:
        return generate_saturday_key(username)
    raise RuntimeError(f"Day branch {selected_day} is not implemented in this keygen.")


def pause_if_interactive(enabled: bool) -> None:
    if enabled:
        try:
            input("\nPress Enter to exit...")
        except EOFError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Keygen for Crackme 4 / WhichKeyIsIt.")
    parser.add_argument("username", nargs="?", help="Username entered in the crackme.")
    parser.add_argument(
        "--day",
        type=int,
        choices=range(7),
        default=DEFAULT_DAY,
        help="Windows day of week: Sunday=0 ... Saturday=6. Default: 2 (verified Tuesday branch).",
    )
    parser.add_argument(
        "--current-day",
        action="store_true",
        help="Use today's Windows day instead of the default verified Tuesday branch.",
    )
    args = parser.parse_args()

    interactive = args.username is None
    username = args.username or input("Username: ").strip()
    day = current_windows_day() if args.current_day else args.day
    try:
        serial = generate_key(username, day)
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}")
        pause_if_interactive(interactive)
        raise SystemExit(1)
    print(f"Username: {username}")
    print(f"Day: {day}")
    print(f"Serial: {serial}")
    pause_if_interactive(interactive)


if __name__ == "__main__":
    main()
