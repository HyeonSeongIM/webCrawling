import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataCrawler:
    def __init__(self, driver, validator, mover, data_validator):
        self.driver = driver
        self.validator = validator
        self.mover = mover
        self.collected_data = []
        self.wait = WebDriverWait(self.driver, 15)
        self.data_validator = data_validator

        # 주요 선택자를 변수로 관리
        # 나중에 ID가 바뀌면 이 부분만 수정
        self.SELECTORS = {
            "LIST_TABLE_TR": "//table[@id='mf_wfm_container_grdBidPbancList_body_table']//tr[td]",
            "DETAIL_TABLE": "table.w2tb",
            "BACK_BUTTON_ID": "mf_wfm_container_btnLst2"
        }

    def clean_text(self, text):
        if not text: return ""
        return re.sub(r'\s+', ' ', text).strip()

    """데이터 수집을 위한 크롤링 처리"""

    def collect_data_at_index(self, index):
        try:
            self.validator.wait_for_loading()

            # 1. 동적 XPath 생성
            target_row_xpath = f"({self.SELECTORS['LIST_TABLE_TR']})[{index + 1}]"
            row = self.wait.until(EC.presence_of_element_located((By.XPATH, target_row_xpath)))
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) < 3: return None

            # 인덱스 번호를 직접 쓰지 않고 의미 있는 변수에 할당
            bid_no = self.clean_text(cells[1].get_attribute('textContent'))

            if self.data_validator.is_already_collected(bid_no):
                print(f"   -> ({index + 1}) [Skip] 이미 수집된 공고: {bid_no}")
                return None

            print(f"   -> ({index + 1}) 상세 진입 시도: {bid_no}")

            # 2. 상세 페이지 진입
            # a 태그가 없는 경우를 대비한 방어적 코드
            self._click_to_detail(cells[2])

            self.validator.wait_for_loading()

            # 상세 페이지 내용이 뜰 때까지 기다리는 '명시적 대기' 추가
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SELECTORS["DETAIL_TABLE"])))

            # 3. 상세 데이터 수집
            detail_info = self._extract_detail_data(bid_no)

            if detail_info:
                self.data_validator.record_success(bid_no)

            # 4. 목록으로 안전하게 복귀
            self._return_to_list()

            return detail_info

        except Exception as e:
            print(f"      ! {index+1}번째 수집 예외: {str(e)[:50]}")
            return None


    """상세 페이지로 이동하기 위한 클릭 처리"""

    def _click_to_detail(self, cell):
        try:
            target_link = cell.find_element(By.TAG_NAME, "a")
            self.driver.execute_script("arguments[0].click();", target_link)
        except:
            self.driver.execute_script("arguments[0].click();", cell)


    """상세 페이지의 테이블에서 데이터를 추출"""

    def _extract_detail_data(self, bid_no):
        data = {"목록_입찰공고번호": bid_no}
        tables = self.driver.find_elements(By.CSS_SELECTOR, self.SELECTORS["DETAIL_TABLE"])
        for table in tables:
            ths = table.find_elements(By.TAG_NAME, "th")
            tds = table.find_elements(By.TAG_NAME, "td")
            for h, v in zip(ths, tds):
                key = self.clean_text(h.get_attribute('textContent'))
                if key:
                    data[key] = self.clean_text(v.get_attribute('textContent'))
        return data


    """목록 페이지로 복귀"""

    def _return_to_list(self):
        try:
            # ID 또는 가시적인 '목록' 텍스트로 찾기 (XPath 결합으로 확장성 확보)
            back_xpath = f"//*[@id='{self.SELECTORS['BACK_BUTTON_ID']}'] | //input[@value='목록'] | //button[contains(text(), '목록')]"
            back_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, back_xpath)))
            self.driver.execute_script("arguments[0].click();", back_btn)
            self.validator.wait_for_loading()
        except:
            print("      [Warning] 목록 버튼 클릭 실패, 브라우저 뒤로가기 시도")
            self.driver.back()


    """전체 데이터 행 수집"""

    def start_collection(self, target_pages):
        for p in range(1, target_pages + 1):
            print(f"\n[Crawler] {p}페이지 수집 시작")
            self.validator.wait_for_loading()

            # 데이터 행(tr[td])만 정확하게 카운트
            rows = self.driver.find_elements(By.XPATH, self.SELECTORS["LIST_TABLE_TR"])
            row_count = len(rows)
            print(f"   (실제 데이터 행: {row_count}개)")

            for i in range(row_count):
                data = self.collect_data_at_index(i)
                if data:
                    self.collected_data.append(data)

            if p < target_pages:
                if not self.mover.move_to_next_page(p + 1):
                    break
        return self.collected_data