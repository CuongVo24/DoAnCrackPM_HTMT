import ctypes
import struct

def ror(val, bits, size=8):
    return ((val >> bits) | (val << (size - bits))) & ((1 << size) - 1)

def rol(val, bits, size=32):
    return ((val << bits) | (val >> (size - bits))) & ((1 << size) - 1)

def get_machine_hash():
    buf = ctypes.create_string_buffer(256)
    size = ctypes.c_uint32(256)
    ctypes.windll.kernel32.GetComputerNameA(buf, ctypes.byref(size))
    cname = buf.value + b'\x00\x00\x00\x00'
    
    eax, ebx, ecx, edx = 0, 0, 0, 0
    i = 0
    while True:
        al = cname[i]
        dl = cname[i+1]
        
        al = ror(al, 4, 8)
        dl = (~dl) & 0xFF
        al = (al + dl) & 0xFF
        
        eax = (eax & 0xFFFFFF00) | al
        ebx = (ebx + eax) & 0xFFFFFFFF
        edx = (edx * eax) & 0xFFFFFFFF
        ecx = (ecx + edx) & 0xFFFFFFFF
        
        ebx, edx = edx, ebx
        
        i += 2
        if cname[i] == 0 and cname[i+1] == 0:
            break
            
    ebx_bswap = struct.unpack(">I", struct.pack("<I", ebx))[0]
    ebx = (ebx_bswap + ecx) & 0xFFFFFFFF
    return ebx

def generate_key(username: str) -> str:
    machine_hash = get_machine_hash()
    
    ebx, ecx, edx = 0, 0x7FFF, 0
    user_bytes = username.encode('ascii')
    
    for char in user_bytes:
        bx = char
        ebx = (bx << 8) & 0xFFFFFFFF
        eax = machine_hash & 0xF8F800
        ebx ^= eax
        ebx = (ebx + 0x6C6F6C) & 0xFFFFFFFF
        ebx ^= 0x10101010
        
        edx = (edx + ebx) & 0xFFFFFFFF
        ecx = (ecx + ebx) & 0xFFFFFFFF
        ecx = (ecx - 0x2D3D2D) & 0xFFFFFFFF
        ecx = (ecx * 8) & 0xFFFFFFFF
        ecx = (ecx + eax) & 0xFFFFFFFF
        
    esi, edi = 0, 0
    for _ in range(0x10):
        edi = (edi + ecx) & 0xFFFFFFFF
        esi = (esi + edx) & 0xFFFFFFFF
        edi = struct.unpack(">I", struct.pack("<I", edi))[0]
        esi = struct.unpack(">I", struct.pack("<I", esi))[0]
        edi = rol(edi, 16, 32)
        esi = ror(esi, 16, 32)
        
    # The format string order: push esi, push edi, push edx, push ecx -> %08lX-%08lX-%08lX-%08lX
    # Note: wsprintf reads right-to-left for arguments, so: ecx, edx, edi, esi
    return f"{ecx:08X}-{edx:08X}-{edi:08X}-{esi:08X}"

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "TestUser"
    key = generate_key(name)
    print(f"Username: {name}")
    print(f"Key: {key}")
