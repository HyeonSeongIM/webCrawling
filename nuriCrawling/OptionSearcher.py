# 검색 상세 조건들 나열
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OptionSearcher:
    def __init__(self, driver, validator):
        self.driver = driver
        self.validator = validator # 로딩 대기를 위해 validator 활용

    """공고명 검색어 입력 (필요 시 사용)"""

    def set_search_keyword(self, keyword):
        if not keyword:
            return
        print(f"[Searcher] 검색어 입력 중: {keyword}")
        # 공고명 입력창 ID (누리장터 기준: mf_wfm_container_ibxBidPbancNm)
        input_box = self.driver.find_element(By.ID, "mf_wfm_container_ibxBidPbancNm")
        input_box.clear()
        input_box.send_keys(keyword)

    """검색 버튼 클릭 및 데이터 로드 대기"""

    def execute_search(self):
        print("[Searcher] 검색 버튼 클릭...")

        # 검색 버튼 ID: mf_wfm_container_btnS0001
        search_btn = self.driver.find_element(By.ID, "mf_wfm_container_btnS0001")
        self.driver.execute_script("arguments[0].click();", search_btn)

        # 1. 로딩 바가 사라질 때까지 대기
        self.validator.wait_for_loading()

        # 2. 데이터가 테이블에 뿌려지는 물리적인 시간 확보
        print("[Searcher] 데이터 렌더링 대기 중 (5초)...")
        time.sleep(5)
        print("[Searcher] 검색 결과 로드 완료.")

    """상세 페이지에서 에러 발생 시 목록으로 돌아왔는지 확인하는 안전장치"""

    def ensure_list_page(self):
        try:
            # 목록 버튼이 있는지 확인하거나 검색 버튼이 다시 보이는지 체크
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "mf_wfm_container_btnS0001"))
            )
        except:
            print("[Searcher] 목록 페이지 복귀 확인 실패. 강제 조치 필요.")