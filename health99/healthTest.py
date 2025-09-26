from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import pandas as pd
import time, random

class HealthAssessmentBot:
    def __init__(self, sample_size=100):
        self.url = "https://cdrc.hpa.gov.tw/hra-openservice-menupage.jsp?all"
        self.sample_size = sample_size
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.results = []
        
        # 變數定義
        self.gender = [0, 1]
        self.age = range(35, 71, 5)
        self.height = range(120, 211, 10)
        self.weight = range(40, 141, 10)
        self.waistline = range(40, 121, 10)
        self.bloodpressure = range(65, 150, 10)
        self.cholesterol = range(120, 250, 20)
        self.hcholesterol = range(35, 100, 10)
        self.lcholesterol = range(65, 166, 20)
        self.triglycerides = range(75, 185, 20)
        self.bloodsuger = range(70, 151, 20)
        self.diabetes = [0, 1]
        self.hypertension = [0, 1]
        self.smoke = [0, 1]

    def start(self):
        self.driver.get(self.url)
        time.sleep(5)
        self.handle_alert()
        self.run_tests()
        self.driver.quit()
        print("🎉 測試完成")

    def handle_alert(self):
        try:
            alert = self.driver.switch_to.alert
            print("📢 發現對話框:", alert.text)
            alert.accept()
            print("✅ 已點擊 '確定'")
        except NoAlertPresentException:
            print("❌ 沒有找到對話框")

    def generate_random_samples(self):
        samples = []
        for _ in range(self.sample_size):
            samples.append([
                random.choice(self.gender), random.choice(self.age), random.choice(self.height),
                random.choice(self.weight), random.choice(self.waistline), random.choice(self.bloodpressure),
                random.choice(self.cholesterol), random.choice(self.hcholesterol), random.choice(self.lcholesterol),
                random.choice(self.triglycerides), random.choice(self.bloodsuger), random.choice(self.diabetes),
                random.choice(self.hypertension), random.choice(self.smoke)
            ])
        return samples

    def clear_inputs(self):
        fields = ["age", "height", "weight", "waist", "sbp", "chol", "hdlc", "ldlc", "tg", "glu"]
        for field in fields:
            try:
                input_element = self.driver.find_element(By.NAME, field)
                input_element.clear()
                time.sleep(0.5)
            except NoSuchElementException:
                print(f"⚠️ 欄位 {field} 不存在，跳過清除。")

    def run_tests(self):
        samples = self.generate_random_samples()
        for index, values in enumerate(samples):
            print(f"📝 測試組合 {index+1}/{len(samples)}: {values}")
            try:
                self.clear_inputs()
                time.sleep(1)

                self.driver.find_element(By.NAME, "gender").click()
                self.driver.find_element(By.NAME, "age").send_keys(str(values[1]))
                self.driver.find_element(By.NAME, "height").send_keys(str(values[2]))
                self.driver.find_element(By.NAME, "weight").send_keys(str(values[3]))
                self.driver.find_element(By.NAME, "waist").send_keys(str(values[4]))
                self.driver.find_element(By.NAME, "sbp").send_keys(str(values[5]))
                self.driver.find_element(By.NAME, "chol").send_keys(str(values[6]))
                self.driver.find_element(By.NAME, "hdlc").send_keys(str(values[7]))
                self.driver.find_element(By.NAME, "ldlc").send_keys(str(values[8]))
                self.driver.find_element(By.NAME, "tg").send_keys(str(values[9]))
                self.driver.find_element(By.NAME, "glu").send_keys(str(values[10]))
                self.driver.find_element(By.NAME, "diabetes").click()
                self.driver.find_element(By.NAME, "hbp").click()
                self.driver.find_element(By.NAME, "smoke").click()

                # 送出表單
                time.sleep(2)
                self.driver.find_element(By.ID, "btnComputeAllModel").click()
                time.sleep(5)
                
                # 點擊所有「檢視健康指引」按鈕
                self.extract_health_guidance()

            except (NoSuchElementException, ElementClickInterceptedException) as e:
                print(f"⚠️ 發生錯誤: {e}")
                continue

    def extract_health_guidance(self):
        try:
            health_buttons = self.driver.find_elements(By.CLASS_NAME, "btnCheck")
            print(f"✅ 找到 {len(health_buttons)} 個『檢視健康指引』按鈕")
            for i, button in enumerate(health_buttons):
                self.driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(1)
                button.click()
                time.sleep(5)

                # 取得 HTML 結果
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                with open(f"page_source.html", "w", encoding="utf-8") as file:
                    file.write(soup.prettify())
                print(f"✅ 已存檔: page_source.html")

                result_section = self.driver.find_element(By.CLASS_NAME, "result-content")
                result_text = result_section.text.strip()
                print(f"✅ 健康指引 {i+1}: {result_text[:50]}...")
                self.results.append({"指引索引": i+1, "內容": result_text})
                self.driver.back()
                time.sleep(5)
        except NoSuchElementException:
            print("❌ 沒有找到『檢視健康指引』按鈕")

if __name__ == "__main__":
    bot = HealthAssessmentBot(sample_size=5)
    bot.start()
