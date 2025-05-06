# 📘 BTL_Craw_website_phat_nguoi
## Môn học: Tự động hóa quy trình  
**Sinh viên thực hiện**: Lê Văn Hậu - 2251220053  
**Giảng viên hướng dẫn**: Thầy Nguyễn Văn Rô

---

# Tự động tra cứu phạt nguội

Dự án này tự động tra cứu thông tin phạt nguội từ trang web CSGT (Cảnh sát giao thông) bằng cách sử dụng **Selenium** để tự động điền thông tin vào form và giải mã Captcha để nhận kết quả. Mã Captcha được xử lý thông qua **Tesseract OCR**. Và chạy tự động vào lúc 6h sáng và 12h trưa, được xử lý thông qua **schedule**.

## Mô tả

- Truy cập trang web [CSGT.vn](https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html).
- Chụp ảnh captcha, xử lý ảnh và sử dụng Tesseract OCR để đọc mã captcha.
- Điền thông tin biển số xe và loại phương tiện.
- Tra cứu kết quả phạt nguội và hiển thị thông tin phạt nếu có.
- Được lập lịch để tự động chạy vào các thời gian cố định trong ngày (6h sáng và 12h trưa).

## Các yêu cầu

1. **Python**: Phiên bản 3.x.
2. **Selenium**: Thư viện điều khiển trình duyệt tự động.
3. **Tesseract**: Công cụ OCR (Optical Character Recognition) để đọc mã captcha. Tải Tesseract tại link GitHub: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract).
4. **Chrome WebDriver**: Để chạy Selenium với Chrome.

## Cài đặt

Để triển khai dự án, bạn cần thực hiện các bước cài đặt sau:

1. **Cài đặt các thư viện cần thiết**  
   Để cài đặt các thư viện Python yêu cầu, bạn có thể sử dụng `pip`:

   ```bash
   pip install selenium
   pip install pytesseract
   pip install pillow
   pip install schedule

2. **Cài Đặt Tesseract OCR**
    Tải Tesseract từ tesseract-ocr/tesseract.
    Cài đặt Tesseract vào máy của bạn và thêm đường dẫn của Tesseract vào PATH để có thể sử dụng trong file python Craw_website_KtraPhatNguoi.py
    Ví dụ: Nếu bạn sử dụng Windows, đường dẫn có thể là C:\Program Files\Tesseract-OCR\tesseract.exe.
    Sau khi cài đặt, bạn có thể kiểm tra việc cài đặt bằng cách gõ:

    ```bash
    tesseract --version

3. **Cài Đặt Chrome WebDriver**
    Tải Chrome WebDriver tương thích với phiên bản Chrome của bạn từ ChromeDriver.
    Đảm bảo rằng WebDriver đã được tải và cài đặt đúng cách.

4. **Đảm Bảo Cài Đặt Chrome**
    Đảm bảo rằng bạn đã cài đặt Chrome và phiên bản của Chrome phải tương thích với WebDriver.
## Cách sử dụng
1. **Chạy script:**
    Sau khi đã cài đặt tất cả các thư viện và công cụ cần thiết, bạn có thể chạy script tự động tra cứu phạt nguội bằng lệnh:
    ```bash
    python Craw_website_KtraPhatNguoi.py
2. **Lịch trình tự động:**
    Dự án này được lập lịch để chạy tự động vào các thời gian cố định trong ngày (6h sáng và 12h trưa) thông qua thư viện schedule. Bạn có thể thay đổi thời gian chạy hoặc tần suất chạy trong mã nguồn nếu cần.

## Liên Hệ
    Nếu bạn có bất kỳ câu hỏi nào hoặc gặp sự cố khi sử dụng, bạn có thể mở issue trên GitHub hoặc liên hệ với tôi qua email: levanhaum@email.com.
