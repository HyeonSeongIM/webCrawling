import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from nuriCrawling.PageValidator import PageValidator

class TestPageValidator(unittest.TestCase):
    def setUp(self):
        # 1. 의존성 객체(driver)를 Mock으로 생성
        self.mock_driver = MagicMock()

        # 2. PageValidator 인스턴스 생성
        self.validator = PageValidator(driver=self.mock_driver)

    def test_close_popups_with_css_selector(self):
        """CSS 선택자(.w2window_close)로 팝업을 찾아 닫는지 테스트"""
        # 가짜 버튼 객체 설정
        mock_btn = MagicMock()
        mock_btn.is_displayed.return_value = True

        # 1차 시도에서 버튼을 찾은 경우 시뮬레이션
        self.mock_driver.find_elements.side_effect = [[mock_btn], []]

        with patch('time.sleep'): # 테스트 속도를 위해 sleep 무시
            self.validator.close_popups()

        # 검증: 자바스크립트 클릭이 호출되었는지 확인
        self.mock_driver.execute_script.assert_called_with("arguments[0].click();", mock_btn)

    def test_close_popups_with_xpath(self):
        """1차 실패 후 2차 XPath(//button[@aria-label='창닫기'])로 팝업을 닫는지 테스트"""
        mock_btn = MagicMock()
        mock_btn.is_displayed.return_value = True

        # 1차(CSS)는 빈 리스트, 2차(XPath)에서 버튼 발견 시뮬레이션
        self.mock_driver.find_elements.side_effect = [[], [mock_btn]]

        with patch('time.sleep'):
            self.validator.close_popups()

        # 검증: 2차 시도 로직이 실행되어 클릭이 발생했는지 확인
        self.mock_driver.execute_script.assert_called_with("arguments[0].click();", mock_btn)

    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    def test_wait_for_loading_success(self, mock_wait_until):
        """로딩바가 정상적으로 사라질 때까지 대기하는지 테스트"""
        self.validator.wait_for_loading()

        # EC.invisibility_of_element_located 함수가 호출되었는지 확인
        mock_wait_until.assert_called_once()

    def test_wait_for_loading_timeout_ignored(self):
        """로딩바가 안 나타나서 타임아웃이 발생해도 에러를 무시하고 넘어가는지 테스트"""
        from selenium.common.exceptions import TimeoutException

        with patch('selenium.webdriver.support.ui.WebDriverWait.until', side_effect=TimeoutException):
            try:
                self.validator.wait_for_loading()
                execution_passed = True
            except:
                execution_passed = False

            self.assertTrue(execution_passed, "로딩바 대기 중 에러가 발생해도 크롤링 프로세스는 유지되어야 합니다.")

if __name__ == "__main__":
    unittest.main()