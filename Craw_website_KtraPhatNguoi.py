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
import schedule

# đường dẫn tới Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def setup_driver():
    """
    Khởi tạo trình duyệt Chrome với các tùy chọn cần thiết.
    """
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    return webdriver.Chrome(options=options)

def preprocess_captcha(image_path: str, output_path: str) -> Image.Image:
    """
    Tiền xử lý ảnh captcha để tối ưu cho OCR.
    - Chuyển sang grayscale
    - Phóng to
    - Tăng độ tương phản
    - Lọc nhiễu
    - Nhị phân hóa
    """
    image = Image.open(image_path).convert("L")
    image = image.resize((image.width * 2, image.height * 2))
    image = ImageOps.autocontrast(image)
    image = image.filter(ImageFilter.MedianFilter())
    threshold = 180
    image = image.point(lambda p: p > threshold and 255)
    image.save(output_path)
    return image

def read_captcha(image: Image.Image) -> str:
    """
    Nhận diện mã captcha từ ảnh đã xử lý.
    Chỉ lấy 6 ký tự chữ thường và số.
    """
    raw_text = pytesseract.image_to_string(
        image,
        config='--psm 8 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789'
    ).strip()

    filtered_text = re.sub(r'[^a-z0-9]', '', raw_text.lower())
    return filtered_text[-6:] if len(filtered_text) >= 6 else filtered_text.ljust(6, '_')

def fill_form_and_submit(driver, captcha_text: str):
    """
    Nhập thông tin biển số, loại xe, captcha và nhấn tìm kiếm.
    """
    plate_number_input = driver.find_element(By.XPATH, '//*[@id="formBSX"]/div[2]/div[1]/input')
    plate_number_input.send_keys("43A12345")

    vehicle_type_select = driver.find_element(By.XPATH, '//*[@id="formBSX"]/div[2]/div[2]/select')
    select = Select(vehicle_type_select)
    select.select_by_visible_text("Ô tô")

    captcha_input = driver.find_element(By.NAME, "txt_captcha")
    captcha_input.send_keys(captcha_text)

    search_button = driver.find_element(By.XPATH, '//*[@id="formBSX"]/div[2]/input[1]')
    search_button.click()

def get_violation_result(driver):
    """
    Lấy kết quả tra cứu phạt nguội nếu có.
    """
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

def check_vehicle_violation():
    """
    Hàm chính để thực hiện toàn bộ quy trình tra cứu phạt nguội.
    """
    driver = setup_driver()
    captcha_path = "captcha.png"
    processed_path = "processed_captcha.png"

    try:
        driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")
        time.sleep(2)

        captcha_element = driver.find_element(By.ID, "imgCaptcha")
        captcha_element.screenshot(captcha_path)

        processed_image = preprocess_captcha(captcha_path, processed_path)
        captcha_text = read_captcha(processed_image)
        print("Mã Captcha đọc được:", captcha_text)

        fill_form_and_submit(driver, captcha_text)
        time.sleep(5)

        get_violation_result(driver)

    except Exception as e:
        print("❌ Lỗi:", e)

    finally:
        driver.quit()
        for f in [captcha_path, processed_path]:
            if os.path.exists(f):
                os.remove(f)


# Lập lịch chạy hàng ngày
schedule.every().day.at("06:00").do(check_vehicle_violation)
schedule.every().day.at("12:00").do(check_vehicle_violation)

# Vòng lặp kiểm tra lịch
while True:
    schedule.run_pending()
    time.sleep(60)