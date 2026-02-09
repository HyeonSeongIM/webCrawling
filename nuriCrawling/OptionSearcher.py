# 검색 상세 조건들 나열
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OptionSearcher:
    def __init__(self, driver, validator):
        self.driver = driver
        self.validator = validator # 로딩 대기를 위해 validator 활용
        self.wait = WebDriverWait(self.driver, 15)

    """검색 버튼 클릭 및 데이터 로드 대기"""

    def execute_search(self, button_text):
        print(f"[Searcher] '{button_text}' 버튼 클릭 시도...")

        # 1. 확장성: ID 대신 텍스트로 버튼 탐색 (추후 '검색' 등으로 바껴도 대응 가능)
        search_xpath = f"//input[@value='{button_text}']"

        # 버튼이 클릭 가능할 때까지 대기
        search_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, search_xpath)))

        # 2. 안전성: 자바스크립트 클릭
        self.driver.execute_script("arguments[0].click();", search_btn)

        # TODO : 데이터가 0건일 수도 있으므로 Timeout 처리
        print("[Searcher] 데이터 결과 렌더링 확인 중...")

    """상세 페이지에서 에러 발생 시 목록으로 돌아왔는지 확인하는 안전장치"""

    def ensure_list_page(self):
        try:
            # 목록 버튼이 있는지 확인하거나 검색 버튼이 다시 보이는지 체크
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "mf_wfm_container_btnS0001"))
            )
        except:
            print("[Searcher] 목록 페이지 복귀 확인 실패. 강제 조치 필요.")


    # TODO : 필터링 및 검색 고도화 로직
    # """공고명 검색어 입력 (필요 시 사용)"""
    #
    # def set_search_keyword(self, keyword):
    #     if not keyword:
    #         return
    #     print(f"[Searcher] 검색어 입력 중: {keyword}")
    #     # 공고명 입력창 ID (누리장터 기준: mf_wfm_container_ibxBidPbancNm)
    #     input_box = self.driver.find_element(By.ID, "mf_wfm_container_ibxBidPbancNm")
    #     input_box.clear()
    #     input_box.send_keys(keyword)