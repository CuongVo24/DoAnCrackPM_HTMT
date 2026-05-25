# Đồ Án Crack Phần Mềm - Hệ Thống Máy Tính (HTMT)

![License](https://img.shields.io/badge/license-Educational-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![Reverse Engineering](https://img.shields.io/badge/Reverse%20Engineering-OllyDbg%20%7C%20PEiD-orange.svg)

Đây là kho lưu trữ chứa mã nguồn, tài liệu và các công cụ được sử dụng trong Đồ án môn học **Hệ Thống Máy Tính (HTMT)**. Dự án tập trung vào kỹ thuật dịch ngược (Reverse Engineering), phân tích mã máy (Assembly) và phát triển các công cụ tự động tạo khóa (Keygen) cho các phần mềm crackme.

> ⚠️ **LƯU Ý PHÁP LÝ & ĐẠO ĐỨC:** Đồ án này được thực hiện hoàn toàn với mục đích **nghiên cứu, học tập và hiểu rõ hơn về bảo mật phần mềm**. Tuyệt đối không sử dụng kiến thức hoặc công cụ trong repository này vào các hành vi vi phạm bản quyền hay phá hoại phần mềm thương mại.

## 👥 Thành viên nhóm

- **24120029**
- **24120070**

## 📂 Cấu trúc dự án

Dự án được tổ chức thành các thư mục như sau:

- 📁 **`24120029_24120070/`**: Thư mục chính của nhóm sinh viên.
  - 📄 `24120029_24120070.docx`: Báo cáo chi tiết toàn bộ quá trình phân tích, trace code và phương pháp sinh key.
  - 📁 `Keygen/`: Chứa mã nguồn Python (`keygen.py`) và file thực thi (`keygen.exe`) của các công cụ Keygen tương ứng với 4 bài crackme (crackme1 -> crackme4).
- 📁 **`Project crack phan mem/`**: Chứa các file crackme gốc đang có trong workspace. Riêng crackme2 không còn file `errors_keygenme.exe`, nên phần phân tích dựa trên các file disassembly `crack2_asm_utf8*.txt`.
- 📁 **`Tai lieu Crack/`**: Bộ công cụ và tài liệu hướng dẫn được sử dụng trong quá trình làm đồ án:
  - Các bài hướng dẫn cơ bản (*Basic Cracking Tutorial 1, 2, 3*).
  - Công cụ Debug: **OllyDbg**.
  - Công cụ phân tích tệp PE & Packer: **PEiD**.
- 📄 **`crack1_asm.txt`, `crack2_asm_utf8.txt`, ...**: Các tệp lưu trữ lại đoạn mã Assembly quan trọng được trích xuất từ quá trình phân tích tĩnh và động.

## 🛠️ Công cụ và Kỹ thuật sử dụng

- **OllyDbg**: Trình gỡ lỗi (debugger) ở mức hợp ngữ (assembly) dành cho Windows, dùng để trace theo luồng thực thi của chương trình.
- **PEiD**: Công cụ phát hiện trình đóng gói (packers), bộ mã hóa (cryptors) và trình biên dịch của các tệp thực thi.
- **Python**: Ngôn ngữ kịch bản được sử dụng để xây dựng thuật toán sinh khóa (Keygen) dựa trên các logic mã hóa (MD5, SHA-1, Custom Hash, XOR, Shift bit...) được phân tích từ phần mềm.
- **Kiến trúc x86 / Assembly**: Kỹ năng đọc hiểu các lệnh Assembly cơ bản, phân tích stack, thanh ghi và luồng điều khiển (Control Flow).

## 🚀 Hướng dẫn sử dụng Keygen

Mỗi mục tiêu (crackme) sẽ đi kèm một công cụ sinh khóa tương ứng trong thư mục `Keygen/`. Bạn có thể chạy Keygen bằng Python hoặc sử dụng tệp tin thực thi độc lập (`.exe`).

Xem thêm checklist test và hoàn thiện báo cáo tại [`HUONG_DAN_TEST_VA_HOAN_THIEN_BAO_CAO.md`](HUONG_DAN_TEST_VA_HOAN_THIEN_BAO_CAO.md).

### Cách 1: Chạy bằng mã nguồn Python
1. Mở Terminal / Command Prompt tại thư mục chứa file `keygen.py` (Ví dụ: `24120029_24120070/Keygen/crackme1/`).
2. Thực thi kịch bản bằng lệnh:
   ```bash
   python keygen.py
   ```
3. Bạn có thể truyền thêm các tham số lệnh nếu muốn (sử dụng `python keygen.py -h` để xem chi tiết) hoặc chỉ cần nhập **Username** vào màn hình theo yêu cầu. Chương trình sẽ trả về **Serial / Key** tương ứng.
*(Lưu ý: Một số bài toán lấy thông tin phần cứng hoặc tên máy tính (`ComputerName`) làm tham số đầu vào cho hàm băm).*

### Lưu ý kiểm chứng
- Crackme1 phụ thuộc `ComputerName`, vì vậy serial minh họa trong báo cáo khớp với máy `LAPTOPCUACUONG`.
- Crackme4 phụ thuộc ngày trong tuần và CPUID. Keygen mặc định dùng ngày hiện tại của Windows; có thể dùng `--day` để chọn nhánh cụ thể khi cần tái tạo minh chứng: Sunday=0, Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5. Nhánh Saturday=6 chưa implement.
- Riêng nhánh Monday của crackme4 còn cần file `xor0.rox`; keygen sẽ tự tạo file này nếu tìm thấy thư mục crackme4 gốc trong repo. Khi test thủ công, đặt `xor0.rox` cạnh `WhichKeyIsIt.exe`.
- Crackme2 chưa runtime-verify được trong workspace vì thiếu executable gốc, nhưng keygen và báo cáo đã giữ rõ phần rủi ro này.

### Cách 2: Chạy bằng file thực thi (EXE)
Dành cho người dùng không cài đặt sẵn môi trường Python:
1. Truy cập vào các thư mục `crackme1`, `crackme2`...
2. Chạy tệp `keygen.exe` và nhập các thông tin cần thiết.
3. Nếu mở bằng double-click, cửa sổ sẽ giữ lại ở dòng `Press Enter to exit...` sau khi in serial; nhấn Enter thêm một lần để đóng. Nếu chạy từ Terminal với tham số username, ví dụ `keygen.exe 2412002924120070`, chương trình sẽ in kết quả rồi thoát ngay.

---
*Thực hiện trong khuôn khổ môn học Hệ Thống Máy Tính (HTMT).*
