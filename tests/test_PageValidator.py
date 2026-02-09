import unittest
from unittest.mock import MagicMock, patch
from nuriCrawling.PageValidator import PageValidator

class TestPageValidator(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.validator = PageValidator(self.mock_driver)

    def test_close_popups_happy_case(self):
        """해피 케이스: 팝업 버튼이 존재하고 표시될 때 정상적으로 클릭되는지 확인"""
        mock_btn = MagicMock()
        mock_btn.is_displayed.return_value = True
        self.mock_driver.find_elements.return_value = [mock_btn]

        self.validator.close_popups()
        self.mock_driver.execute_script.assert_called_with("arguments[0].click();", mock_btn)

    def test_close_popups_no_popups(self):
        """엣지 케이스: 팝업창이 아예 없을 때 에러 없이 통과하는지 확인"""
        self.mock_driver.find_elements.return_value = []
        try:
            self.validator.close_popups()
        except Exception as e:
            self.fail(f"팝업이 없을 때 예외가 발생했습니다: {e}")

    def test_wait_for_loading_exception(self):
        """예외 케이스: 로딩바 대기 중 타임아웃이 발생해도 프로그램이 죽지 않는지 확인"""
        with patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_wait:
            mock_wait.side_effect = Exception("Timeout")
            self.validator.wait_for_loading() # 예외를 pass 하도록 설계됨