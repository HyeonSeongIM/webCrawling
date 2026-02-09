# 해당 페이지 이동 로직들 넣기
import time
from selenium.webdriver.common.by import By

class PageMover:
    def __init__(self, driver, validator):
        self.driver = driver
        self.validator = validator # 로딩 대기를 위해 validator 객체를 전달받음

    """누리장터 > 입찰공고 > 입찰공고 목록 메뉴로 이동"""

    def move_to_bid_list(self):
        print("[Mover] 입찰공고 목록 페이지로 이동 중...")

        # 1. 메인 메뉴 '입찰공고' 클릭
        menu_bid = self.driver.find_element(By.ID, "mf_wfm_gnb_wfm_gnbMenu_genDepth1_1_btn_menuLvl1_span")
        self.driver.execute_script("arguments[0].click();", menu_bid)
        time.sleep(1)

        # 2. 서브 메뉴 '입찰공고 목록' 클릭
        menu_list = self.driver.find_element(By.ID, "mf_wfm_gnb_wfm_gnbMenu_genDepth1_1_genDepth2_0_genDepth3_0_btn_menuLvl3_span")
        self.driver.execute_script("arguments[0].click();", menu_list)

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