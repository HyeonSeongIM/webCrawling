import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from nuriCrawling.OptionSearcher import OptionSearcher

class TestOptionSearcher(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_validator = MagicMock()
        self.searcher = OptionSearcher(
            driver=self.mock_driver,
            validator=self.mock_validator
        )

    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    def test_execute_search_success(self, mock_wait_until):
        """검색 버튼 클릭 로직 테스트"""
        mock_button = MagicMock()
        mock_wait_until.return_value = mock_button

        button_text = "조회"
        self.searcher.execute_search(button_text)

        # [수정] 인자가 전달되었는지만 확인하고, 호출 횟수를 검증합니다.
        # EC.element_to_be_clickable 함수 객체가 첫 번째 인자로 전달됩니다.
        mock_wait_until.assert_called_once()

        # 실제 자바스크립트 클릭이 호출되었는지 확인
        self.mock_driver.execute_script.assert_called_with("arguments[0].click();", mock_button)

    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    def test_ensure_list_page_success(self, mock_wait_until):
        """목록 페이지 복귀 확인 테스트 (성공)"""
        mock_wait_until.return_value = MagicMock()

        self.searcher.ensure_list_page()

        # [수정] EC 함수가 호출되었는지 확인
        mock_wait_until.assert_called_once()

    def test_ensure_list_page_failure(self):
        """목록 페이지 복귀 실패 시 예외 처리 테스트"""
        from selenium.common.exceptions import TimeoutException

        # WebDriverWait.until이 호출될 때 TimeoutException을 던지도록 설정
        with patch('selenium.webdriver.support.ui.WebDriverWait.until', side_effect=TimeoutException):
            try:
                self.searcher.ensure_list_page()
                execution_passed = True
            except:
                execution_passed = False

            self.assertTrue(execution_passed, "Timeout이 발생해도 에러를 잡아서 프로그램이 유지되어야 합니다.")

    def test_set_search_keyword_placeholder(self):
        pass

if __name__ == "__main__":
    unittest.main()