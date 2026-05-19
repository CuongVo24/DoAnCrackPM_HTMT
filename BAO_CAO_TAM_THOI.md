# Báo cáo tạm thời đồ án Crackme / Keygen

Nhóm: 24120029 - 24120070

Username minh họa dùng thống nhất trong báo cáo:

```text
2412002924120070
```

Thư mục nộp bài:

```text
24120029_24120070/
├── 24120029_24120070.docx
└── Keygen/
    ├── crackme1/keygen.py, keygen.exe
    ├── crackme2/keygen.py, keygen.exe
    ├── crackme3/keygen.py, keygen.exe
    └── crackme4/keygen.py, keygen.exe
```

## 1. Tình trạng minh chứng hiện có

| Bài | Target gốc | Keygen chạy được | Target báo đúng key | Ghi chú |
|---|---|---:|---:|---|
| Crackme1 | `Project crack phan mem/crackme/Crack01/KeygenMe1.exe` | Có | Có | Đã chụp ảnh keygen và ảnh target báo `Serial is correct!`. |
| Crackme2 | Thiếu `errors_keygenme.exe` | Có | Chưa | Thầy/đề có vẻ thiếu file chạy gốc, nên chỉ có thể báo cáo theo disassembly `crack2_asm_utf8*.txt` và keygen. |
| Crackme3 | `Project crack phan mem/crackme/crack03/d2k2.crkme.09.exe` | Có | Có | Đã chụp ảnh keygen và ảnh target báo `Serial is OK`. |
| Crackme4 | `Project crack phan mem/crackme/crack04/WhichKeyIsIt.exe` | Có | Có | Đã chụp ảnh target báo `You did it!!` với serial nhánh Tuesday. |

## 2. Danh sách ảnh chèn vào báo cáo Word

### Ảnh đã có

Hình 1. Keygen crackme1 chạy với username `2412002924120070`.

![crackme1_keygen](<C:/Users/admin/Pictures/Screenshots/crackme1_keygen.png>)

Hình 2. Crackme1 xác nhận serial đúng.

![keygen1_correct](<C:/Users/admin/Pictures/Screenshots/keygen1_correct.png>)

Hình 3. Keygen crackme2 chạy với username `2412002924120070`.

![crackme2_keygen](<C:/Users/admin/Pictures/Screenshots/crackme2_keygen.png>)

Hình 4. Keygen crackme3 chạy với username `2412002924120070`.

![crackme3_keygen](<C:/Users/admin/Pictures/Screenshots/crackme3_keygen.png>)

Hình 5. Crackme3 xác nhận serial đúng.

![keygen3_correct](<C:/Users/admin/Pictures/Screenshots/keygen3_correct.png>)

Hình 6. Keygen crackme4 chạy với username `2412002924120070`.

![crackme4_keygen](<C:/Users/admin/Pictures/Screenshots/crackme4_keygen.png>)

Hình 7. Crackme4 xác nhận serial đúng.

![keygen4_correct](minh_chung/crackme4_success.png)

Lưu ý khi đưa Hình 7 vào Word: đây là ảnh runtime success thật của crackme4, có thông báo `Very good! You solved today's challenge 2412002924120070`.

### Ảnh còn thiếu nếu muốn báo cáo đẹp hơn

- Ảnh disassembly/debug cho crackme1 tại đoạn `0x4011A2..0x401296` hoặc đoạn hash máy `0x40132D..0x40136F`.
- Ảnh disassembly/debug cho crackme2 tại đoạn SHA-1/custom hash và đoạn so khớp 20 ký tự serial.
- Ảnh target gốc crackme2 báo đúng key, nếu tìm lại được `errors_keygenme.exe`.
- Ảnh disassembly/debug cho crackme3 tại đoạn xử lý bảng ký tự.
- Ảnh disassembly/debug cho crackme4 tại đoạn lấy ngày trong tuần/nhánh Tuesday.

## 3. Crackme1 - KeygenMe1.exe

### 3.1. File target

```text
Project crack phan mem/crackme/Crack01/KeygenMe1.exe
```

### 3.2. Kết quả chạy keygen

Input:

```text
Username: 2412002924120070
ComputerName: LAPTOPCUACUONG
```

Serial sinh ra:

```text
1823E438-6D94BBC0-E1DFE0E1-0C17DFDC
```

Ảnh minh chứng:

- `crackme1_keygen.png`: keygen sinh serial.
- `keygen1_correct.png`: target báo `Serial is correct!`.

### 3.3. Phân tích thuật toán

Crackme1 không chỉ phụ thuộc vào username mà còn phụ thuộc vào ID sinh từ tên máy. Khi chạy trên máy hiện tại, chương trình hiển thị:

```text
ID: 564130305
```

ID này tương ứng với hash từ `GetComputerNameA`, trong trường hợp này là:

```text
LAPTOPCUACUONG
```

Các đoạn assembly quan trọng:

```asm
401156: call 0x40132d          ; tính machine hash từ GetComputerNameA
40115b: mov  %eax,0x4042c4    ; lưu machine hash / ID

4011a2..401296                ; đọc username, tính serial và so sánh
4011e1: mov  0x4042c4,%eax
4011e6: and  $0xf8f800,%eax
4011eb: xor  %eax,%ebx
4011ed: add  $0x6c6f6c,%ebx
4011f3: xor  $0x10101010,%ebx

40127c..40128f                ; so sánh serial người dùng nhập với serial sinh ra
```

Pseudocode rút gọn:

```text
machine_hash = hash(GetComputerNameA())
for each byte in username:
    word = current_byte + next_byte
    value = transform(word, machine_hash)
    ecx, edx = accumulate(value)

for 16 rounds:
    edi = rol16(bswap32(edi + ecx))
    esi = ror16(bswap32(esi + edx))

serial = "%08X-%08X-%08X-%08X" % (ecx, edx, edi, esi)
```

### 3.4. Cách chạy

```powershell
.\24120029_24120070\Keygen\crackme1\keygen.exe 2412002924120070
```

Khi nhập vào target:

```text
Name: 2412002924120070
Serial: 1823E438-6D94BBC0-E1DFE0E1-0C17DFDC
```

## 4. Crackme2 - errors_keygenme.exe

### 4.1. File target

File target gốc hiện đang thiếu trong workspace:

```text
Project crack phan mem/crackme/crack02/errors_keygenme.exe
```

Do đó phần này chưa thể chụp ảnh runtime success. Bài vẫn có thể trình bày theo các file disassembly đã trích:

```text
crack2_asm_utf8.txt
crack2_asm_utf8_part2.txt
```

### 4.2. Kết quả chạy keygen

Input:

```text
Username: 2412002924120070
```

Serial sinh ra:

```text
4642KL2673302MO7OKJ7
```

Ảnh minh chứng:

- `crackme2_keygen.png`: keygen sinh serial.

### 4.3. Phân tích thuật toán

Qua disassembly, crackme2 có cấu trúc giống SHA-1 nhưng phần xuất serial không phải hex SHA-1 chuẩn. Chương trình tạo message schedule, chạy vòng nén 80 round, sau đó lấy 20 byte digest để map thành 20 ký tự serial.

Dấu hiệu assembly:

```asm
40128e: cmp $0x37,%eax       ; giới hạn input <= 55 byte
401789..40198f              ; vòng xử lý 80 round
40198c: cmp $0x50,%ecx      ; 0x50 = 80
401ac4: lea 0x403a19,%edi
401aca: mov $0x14,%ecx      ; so khớp 20 ký tự
401b64: cmp $0x9,%bl
401b83: mov $0x30,%esi      ; map 0..9 sang '0'..'9'
401bb9: mov $0x40,%esi      ; map 10..15 sang 'J'..'O'
```

Pseudocode rút gọn:

```text
block = pad(username) theo kiểu SHA-1 một block
w[0..15] = parse block
w[16..79] = rol1(w[i-3] xor w[i-8] xor w[i-14] xor w[i-16])

a,b,c,d,e = SHA1 initial constants
for i in 0..79:
    chạy hàm round SHA-1

digest = h0..h4
serial = ""
for each byte in digest:
    nibble = byte & 0x0F
    if nibble <= 9:
        serial += chr(nibble + 0x30)
    else:
        serial += chr(nibble + 0x40)
```

### 4.4. Cách chạy

```powershell
.\24120029_24120070\Keygen\crackme2\keygen.exe 2412002924120070
```

### 4.5. Rủi ro

Do thiếu `errors_keygenme.exe`, nhóm chưa runtime-verify được serial trên target gốc. Vì vậy không nên tự chấm tuyệt đối cho phần này nếu giáo viên yêu cầu ảnh target báo success.

## 5. Crackme3 - d2k2.crkme.09.exe

### 5.1. File target

```text
Project crack phan mem/crackme/crack03/d2k2.crkme.09.exe
```

### 5.2. Kết quả chạy keygen

Input:

```text
Username: 2412002924120070
```

Serial sinh ra:

```text
tNrRu03bTDZPy59B
```

Ảnh minh chứng:

- `crackme3_keygen.png`: keygen sinh serial.
- `keygen3_correct.png`: target báo `Serial is OK`.

### 5.3. Phân tích thuật toán

Crackme3 dùng bảng ký tự:

```text
0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
```

Username chỉ hợp lệ nếu gồm các ký tự nằm trong bảng này. Chương trình xoay bảng theo độ dài username, sau đó biến đổi từng ký tự dựa trên ký tự hiện tại, ký tự kế tiếp và một biến tích lũy 8-bit.

Pseudocode rút gọn:

```text
alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
offset = len(username) * 4
if offset > 0x3C:
    offset = 0x1E
table = rotate(alphabet, offset)

dl = rol8(username[0], 3)
for i in range(len(username)):
    value = (username[i] xor username[i+1]) + dl
    dl += value
    transformed_char = table[value mod len(table)]

for each original_char, transformed_char:
    serial_char = table[(index(transformed_char) + index(original_char)) mod len(table)]
```

### 5.4. Cách chạy

```powershell
.\24120029_24120070\Keygen\crackme3\keygen.exe 2412002924120070
```

Khi nhập vào target:

```text
name: 2412002924120070
serial: tNrRu03bTDZPy59B
```

## 6. Crackme4 - WhichKeyIsIt.exe

### 6.1. File target

```text
Project crack phan mem/crackme/crack04/WhichKeyIsIt.exe
```

### 6.2. Kết quả chạy keygen

Crackme4 phụ thuộc ngày trong tuần và một phần thông tin CPU. Với nhánh Tuesday (`Day: 2`) trên máy hiện tại, keygen mới nhất sinh:

```text
Username: 2412002924120070
Day: 2
Serial: T10-62E2
```

Ảnh runtime `minh_chung/crackme4_success.png` xác nhận target nhận serial `T10-62E2` và báo `You did it!!`.

### 6.3. Phân tích thuật toán

Chương trình chọn thuật toán theo ngày trong tuần. Trong Windows, `wDayOfWeek` thường được hiểu:

```text
Sunday = 0
Monday = 1
Tuesday = 2
Wednesday = 3
Thursday = 4
Friday = 5
Saturday = 6
```

Nhánh Tuesday dùng CPUID để tạo một giá trị mix, XOR giá trị này với username đã được lặp đủ 32 byte, sau đó tích lũy để tạo phần sau tiền tố `T10-`.

Pseudocode nhánh Tuesday:

```text
expanded = username repeated to 32 bytes
mix = cpuid_mix()

for each 4-byte block in expanded:
    block ^= mix

value = 0xB00B
multiplier = 0
for byte in expanded:
    multiplier |= byte
    multiplier *= len(username)
    value = (value xor multiplier) << 4
    multiplier &= 0xFFFFFF00

value = (value >> 16) xor value
serial = "T10-" + hex16(value)
```

### 6.4. Cách chạy

```powershell
.\24120029_24120070\Keygen\crackme4\keygen.exe 2412002924120070
```

Hoặc chọn ngày cụ thể:

```powershell
.\24120029_24120070\Keygen\crackme4\keygen.exe 2412002924120070 --day 2
```

### 6.5. Kiểm chứng và rủi ro

Ảnh runtime hiện tại đã xác nhận nhánh Tuesday thành công với:

```text
Name: 2412002924120070
Serial: T10-62E2
```

Thông báo nhận được từ target:

```text
You did it!!
Very good! You solved today's challenge 2412002924120070.
```

Rủi ro còn lại: crackme4 phụ thuộc ngày trong tuần và thông tin CPU, nên serial nhánh Tuesday có thể khác khi chạy trên máy khác hoặc ngày khác. Khi báo cáo nên ghi rõ ảnh được kiểm chứng với ngày Tuesday và CPU của máy đang làm bài.

## 7. Tổng kết tự đánh giá

| Tiêu chí | Tình trạng |
|---|---|
| Có source keygen cho 4 bài | Đạt |
| Có file `keygen.exe` cho 4 bài | Đạt |
| Có ảnh keygen chạy cho 4 bài | Đạt |
| Có ảnh target success cho crackme1 | Đạt |
| Có ảnh target success cho crackme2 | Chưa đạt do thiếu `errors_keygenme.exe` |
| Có ảnh target success cho crackme3 | Đạt |
| Có ảnh target success cho crackme4 | Đạt |
| Báo cáo thuật toán/pseudocode | Đạt mức tạm, nên bổ sung ảnh disassembly nếu còn thời gian |

Kết luận: bài hiện tại có thể nộp tạm với minh chứng runtime tốt cho crackme1, crackme3 và crackme4. Crackme2 vẫn là phần rủi ro chính vì thiếu `errors_keygenme.exe`, nên chưa có ảnh target gốc báo success.
