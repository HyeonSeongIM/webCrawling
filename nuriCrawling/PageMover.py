import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageMover:
    def __init__(self, driver, validator):
        self.driver = driver
        self.validator = validator
        self.wait = WebDriverWait(self.driver, 15)

    """누리장터 > 입찰공고 > 입찰공고 목록 메뉴로 이동"""

    def move_to_menu(self, menu_name, sub_menu_name):
        """텍스트 기반으로 메뉴 이동 (확장성 확보)"""
        print(f"[Mover] {menu_name} > {sub_menu_name} 메뉴로 이동 중...")

        # 1. 메인 메뉴 클릭
        main_xpath = f"//span[contains(normalize-space(), '{menu_name}')]"
        menu_main = self.wait.until(EC.element_to_be_clickable((By.XPATH, main_xpath)))
        self.driver.execute_script("arguments[0].click();", menu_main)
        time.sleep(1.5)

        # 2. 서브 메뉴 클릭
        sub_xpath = f"//span[contains(., '{sub_menu_name}')]"
        menu_sub = self.wait.until(EC.presence_of_element_located((By.XPATH, sub_xpath)))
        self.driver.execute_script("arguments[0].click();", menu_sub)

        # 이동 후 로딩 대기
        self.validator.wait_for_loading()
        print("[Mover] 목록 페이지 진입 완료.")

    """하단 페이지네이션에서 지정된 숫자를 클릭하여 이동"""

    def move_to_next_page(self, page_num):
        print(f"[Mover] {page_num}페이지로 이동 시도...")
        try:
            next_xpath = f"//div[contains(@class, 'w2pageList')]//a[text()='{page_num}']"
            next_btn = self.driver.find_element(By.XPATH, next_xpath)
            self.driver.execute_script("arguments[0].click();", next_btn)
            self.validator.wait_for_loading()
            return True
        except:
            return False