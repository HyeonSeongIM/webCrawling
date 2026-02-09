import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DataCrawler:
    def __init__(self, driver, validator, mover):
        self.driver = driver
        self.validator = validator
        self.mover = mover
        self.collected_data = []
        self.wait = WebDriverWait(self.driver, 15)

    def clean_text(self, text):
        if not text: return ""
        # 줄바꿈, 탭 제거 및 연속 공백 정리
        return re.sub(r'\s+', ' ', text).strip()

    def collect_data_at_index(self, index):
        try:
            # 1. 행 목록 최신화
            self.validator.wait_for_loading()

            data_rows_xpath = "//table[@id='mf_wfm_container_grdBidPbancList_body_table']//tr[td]"

            # 2. 해당 인덱스의 행을 다시 찾음
            # index가 0이면 첫 번째 데이터 행을 정확히 지목합니다.
            target_row_xpath = f"({data_rows_xpath})[{index + 1}]"

            row = self.wait.until(EC.presence_of_element_located((By.XPATH, target_row_xpath)))
            cells = row.find_elements(By.TAG_NAME, "td")

            # 누리장터 그리드 기준 (스크린샷 참고):
            # index 1: 입찰공고번호
            # index 2: 입찰공고명 (링크가 있는 칸)
            bid_no = self.clean_text(cells[1].get_attribute('textContent'))

            print(f"   -> ({index + 1}) 상세 진입 시도: {bid_no}")

            # 3. 상세 진입 (td 자체를 클릭하거나 내부 a 태그 강제 클릭)
            try:
                # 해당 칸(cells[2]) 내부의 a 태그를 찾아서 클릭
                target_link = cells[2].find_element(By.TAG_NAME, "a")
                self.driver.execute_script("arguments[0].click();", target_link)
            except:
                # a 태그가 직접 안 잡히면 칸(td) 자체를 자바스크립트로 클릭
                self.driver.execute_script("arguments[0].click();", cells[2])

            # 4. 상세 페이지 로드 대기 (안정성을 위해 넉넉히)
            self.validator.wait_for_loading()

            # 5. 상세 데이터 수집 (딕셔너리 구조)
            detail_info = {"목록_입찰공고번호": bid_no}

            # 상세 페이지의 모든 테이블 항목 수집
            detail_tables = self.driver.find_elements(By.CSS_SELECTOR, "table.w2tb")
            for table in detail_tables:
                ths = table.find_elements(By.TAG_NAME, "th")
                tds = table.find_elements(By.TAG_NAME, "td")
                for h, v in zip(ths, tds):
                    h_text = self.clean_text(h.get_attribute('textContent'))
                    v_text = self.clean_text(v.get_attribute('textContent'))
                    if h_text:
                        detail_info[h_text] = v_text

            # 6. 목록 버튼 클릭 복귀 (ID 기반 실패 대비)
            try:
                # 방법 1: ID로 직접 클릭
                back_btn = self.driver.find_element(By.ID, "mf_wfm_container_btnLst2")
                self.driver.execute_script("arguments[0].click();", back_btn)
            except:
                # 방법 2: '목록' 텍스트를 가진 버튼 찾기
                back_btns = self.driver.find_elements(By.TAG_NAME, "input")
                for b in back_btns:
                    if b.get_attribute('value') == "목록":
                        self.driver.execute_script("arguments[0].click();", b)
                        break

            self.validator.wait_for_loading()

            return detail_info

        except Exception as e:
            print(f"      ! {index+1}번째 공고 상세 수집 중 예외 발생: {str(e)[:50]}")
            return None

    def start_collection(self, target_pages):
        for p in range(1, target_pages + 1):
            print(f"\n[Crawler] {p}페이지 데이터 수집 시작")
            self.validator.wait_for_loading()

            rows = self.driver.find_elements(By.CSS_SELECTOR, "#mf_wfm_container_grdBidPbancList_body_table tr")
            row_count = len(rows) - 1
            print(f"   (발견된 행: {row_count}개)")

            for i in range(row_count):
                data = self.collect_data_at_index(i)
                if data:
                    self.collected_data.append(data)

            if p < target_pages:
                if not self.mover.move_to_next_page(p + 1):
                    break
        return self.collected_data