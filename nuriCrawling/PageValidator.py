import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageValidator:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    """화면에 뜬 모든 공지사항 팝업창을 찾아 닫음"""

    def close_popups(self):
        print("[Validator] 팝업창 확인 및 제거 중...")
        time.sleep(2) # 팝업이 렌더링될 시간을 잠시 주어야 함

        try:
            # 클래스명 'w2window_close' 또는 aria-label '창닫기'를 가진 모든 버튼 수집
            close_btns = self.driver.find_elements(By.CSS_SELECTOR, ".w2window_close")
            if not close_btns:
                close_btns = self.driver.find_elements(By.XPATH, "//button[@aria-label='창닫기']")

            for btn in close_btns:
                if btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", btn)
                    print("   -> 팝업 하나를 닫았습니다.")
                    time.sleep(0.5)
        except Exception as e:
            print(f"   ! 팝업 처리 중 오류(무시 가능): {e}")


    """웹스퀘어 전용 로딩바(___processbar2)가 사라질 때까지 대기"""

    def wait_for_loading(self):
        try:
            self.wait.until(EC.invisibility_of_element_located((By.ID, "___processbar2")))
        except:
            pass # 로딩바가 아예 안 뜨는 경우도 있으므로 예외 처리