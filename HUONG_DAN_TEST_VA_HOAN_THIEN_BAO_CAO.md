# Huong dan test va hoan thien bao cao

Repo dung tren may local:

```text
E:\Downloads\Đồ án crack phần mềm\Đồ án crack phần mềm
```

Thu muc nop bai cuoi cung:

```text
24120029_24120070\
```

## 1. Test keygen bang double-click

Vao tung thu muc:

```text
24120029_24120070\Keygen\crackme1
24120029_24120070\Keygen\crackme2
24120029_24120070\Keygen\crackme3
24120029_24120070\Keygen\crackme4
```

Double-click `keygen.exe`, nhap username:

```text
2412002924120070
```

Sau khi serial hien ra, cua so se dung o dong:

```text
Press Enter to exit...
```

Hay chup anh man hinh luc nay neu muon lam bang chung keygen chay duoc.

Ket qua mong doi tren may `LAPTOPCUACUONG`:

| Crackme | Serial mong doi |
|---|---|
| crackme1 | `89041C38-13838BC0-686AA2A0-B9B75D5E` |
| crackme2 | `3427100330436634406253240446315271072377652222726405577` |
| crackme3 | `tNrRu03bTDZPy59B` |
| crackme4 | `T10-67E7` voi `Day: 2` |

Luu y: crackme1 phu thuoc ComputerName. Neu chay tren may khac, serial co the khac.

## 2. Test keygen bang Terminal

Mo PowerShell tai thu muc repo:

```powershell
cd "E:\Downloads\Đồ án crack phần mềm\Đồ án crack phần mềm"
```

Chay lan luot:

```powershell
.\24120029_24120070\Keygen\crackme1\keygen.exe 2412002924120070
.\24120029_24120070\Keygen\crackme2\keygen.exe 2412002924120070
.\24120029_24120070\Keygen\crackme3\keygen.exe 2412002924120070
.\24120029_24120070\Keygen\crackme4\keygen.exe 2412002924120070
```

Neu chay bang Terminal voi username truyen san, chuong trinh se in ket qua roi thoat ngay. Do la dung thiet ke.

## 3. Test voi crackme goc va chup anh minh chung

Can chup it nhat 2 anh cho moi crackme:

1. Anh debug/disassembly: man hinh x64dbg/IDA/Ghidra tai vung code kiem tra serial.
2. Anh runtime success: man hinh crackme goc nhap username + serial va bao dung key.

Vi tri target goc dang co:

| Crackme | File target |
|---|---|
| crackme1 | `Project crack phan mem\crackme\Crack01\KeygenMe1.exe` |
| crackme2 | Chua co lai `errors_keygenme.exe` trong repo main |
| crackme3 | `Project crack phan mem\crackme\crack03\d2k2.crkme.09.exe` |
| crackme4 | `Project crack phan mem\crackme\crack04\WhichKeyIsIt.exe` |

Rui ro lon nhat hien tai: crackme2 thieu executable goc nen chua the chup anh runtime success that. Muon dat diem toi da, can tim lai `errors_keygenme.exe`, dua vao khu vuc tai lieu rieng, test keygen, va chen anh success vao bao cao.

## 4. Checklist bao cao muc diem toi da

Moi crackme nen co du cac muc sau:

- Ten file target goc va cong cu dung de phan tich.
- Dia chi/hang lenh assembly quan trong, khong viet chung chung.
- Pseudocode hoac cong thuc sinh serial.
- Username minh hoa thong nhat: `2412002924120070`.
- Serial minh hoa sinh ra tu keygen.
- Anh man hinh keygen chay.
- Anh man hinh crackme bao success.
- Ghi ro gioi han neu co: crackme1 phu thuoc ComputerName, crackme4 phu thuoc ngay trong tuan, crackme2 dang thieu executable goc.

Chi nen tu cham 100% khi co anh runtime success that cho ca 4 crackme. Neu crackme2 van thieu file goc, hay ghi ro rui ro nay thay vi khang dinh da verify 100%.

## 5. Cach lam crackme4 chac hon khi bao cao

Keygen crackme4 hien mac dinh dung `Day: 2` de tao serial minh hoa `T10-67E7`.

Khi chup anh runtime success, nen lam trong moi truong kiem soat:

- Cach tot nhat: dung may ao/sandbox va dat ngay he thong ve Tuesday truoc khi mo target.
- Hoac neu phan tich them duoc tat ca nhanh ngay trong crackme4, cap nhat keygen de ho tro day hien tai that.

Khong nen chup anh vao mot ngay khac roi dung serial cua `Day: 2`, vi target co the tinh theo ngay hien tai va tu choi serial.
