from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pytesseract
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import time
import os
import re

# đường dẫn tới Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

options = Options()
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")
    time.sleep(2)

    # Tìm phần tử captcha và chụp ảnh
    captcha_element = driver.find_element(By.ID, "imgCaptcha")
    captcha_path = "captcha.png"
    captcha_element.screenshot(captcha_path)

    # Mở ảnh và chuyển sang ảnh xám (grayscale)
    image = Image.open(captcha_path).convert("L")

    # Tăng kích thước ảnh captcha để chi tiết rõ hơn
    image = image.resize((image.width * 2, image.height * 2))

    # Tăng độ tương phản và sử dụng bộ lọc để làm sạch ảnh captcha
    image = ImageOps.autocontrast(image)
    image = image.filter(ImageFilter.MedianFilter())
    
    # Chuyển sang ảnh nhị phân (đen trắng) để dễ nhận diện
    threshold = 180 
    image = image.point(lambda p: p > threshold and 255)

    # Lưu ảnh captcha xử lý
    processed_path = "processed_captcha.png"
    image.save(processed_path)

    # Đọc captcha bằng pytesseract
    raw_text = pytesseract.image_to_string(
        image,
        config='--psm 8 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789'
    ).strip()

    # Lọc chỉ lấy các ký tự và đảm bảo mã Captcha có 6 ký tự (vì captcha trên trang này có luôn có 6 ký tự)
    filtered_text = re.sub(r'[^a-z0-9]', '', raw_text.lower())
    captcha_text = filtered_text[-6:] if len(filtered_text) >= 6 else filtered_text.ljust(6, '_')

    print("Mã Captcha đọc được:", captcha_text)
    plate_number_input = driver.find_element(By.XPATH, '//*[@id="formBSX"]/div[2]/div[1]/input')
    plate_number_input.send_keys("43A12345")
    vehicle_type_select = driver.find_element(By.XPATH, '//*[@id="formBSX"]/div[2]/div[2]/select')
    select = Select(vehicle_type_select)
    select.select_by_visible_text("Ô tô")

    # Điền mã captcha vào input
    captcha_input = driver.find_element(By.NAME, "txt_captcha")
    captcha_input.send_keys(captcha_text)
    # Nhấn nút tìm kiếm
    search_button = driver.find_element(By.XPATH, '//*[@id="formBSX"]/div[2]/input[1]')
    search_button.click()
    time.sleep(5)  # Đợi kết quả

    try:
        result_div = driver.find_element(By.XPATH, '//*[@id="bodyPrint123"]')
        result_text = result_div.text.strip()

        if result_text:
            print("🔍 Kết quả phạt nguội:\n")
            print(result_text)
        else:
            print("❌ Không có kết quả phạt nguội.")
    except Exception as e:
        print("❌ Lỗi khi lấy kết quả phạt nguội:", e)

except Exception as e:
    print("❌ Lỗi:", e)

finally:
    driver.quit()
    for f in [captcha_path, processed_path]:
        if os.path.exists(f):
            os.remove(f)
