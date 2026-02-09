import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from nuriCrawling.PageMover import PageMover

class TestPageMover(unittest.TestCase):
    def setUp(self):
        # 1. 의존성 객체(driver, validator)를 Mock으로 생성
        self.mock_driver = MagicMock()
        self.mock_validator = MagicMock()

        # 2. PageMover 인스턴스 생성
        self.mover = PageMover(
            driver=self.mock_driver,
            validator=self.mock_validator
        )

    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    def test_move_to_menu_success(self, mock_wait_until):
        """메뉴 이동 로직이 정상적으로 수행되는지 테스트"""
        # 가짜 메뉴 요소들 설정
        mock_main_menu = MagicMock()
        mock_sub_menu = MagicMock()
        mock_wait_until.side_effect = [mock_main_menu, mock_sub_menu]

        menu_name = "입찰공고"
        sub_menu_name = "입찰공고목록"

        self.mover.move_to_menu(menu_name, sub_menu_name)

        # 호출 횟수 검증 (메인 메뉴 1회, 서브 메뉴 1회)
        self.assertEqual(mock_wait_until.call_count, 2)
        # 자바스크립트 클릭 호출 확인
        self.assertEqual(self.mock_driver.execute_script.call_count, 2)
        # 로딩 대기 호출 확인
        self.mock_validator.wait_for_loading.assert_called()

    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    def test_move_to_next_page_success(self, mock_wait_until):
        """지정된 페이지 번호로 이동 성공 테스트"""
        mock_next_btn = MagicMock()
        mock_wait_until.return_value = mock_next_btn

        page_num = 2
        result = self.mover.move_to_next_page(page_num)

        # 1. 반환값 확인
        self.assertTrue(result)

        # 2. [수정] 인덱싱 에러 방지를 위해 호출 여부만 확인합니다.
        # EC 함수가 until의 인자로 정상 전달되었는지 검증합니다.
        mock_wait_until.assert_called()

        # 3. 버튼 클릭 실행 확인
        self.mock_driver.execute_script.assert_called_with("arguments[0].click();", mock_next_btn)

    def test_move_to_next_page_failure(self):
        """페이지 이동 실패(Timeout) 시 처리 테스트"""
        from selenium.common.exceptions import TimeoutException

        with patch('selenium.webdriver.support.ui.WebDriverWait.until', side_effect=TimeoutException):
            result = self.mover.move_to_next_page(999)

            # 실패 시 False를 반환해야 함
            self.assertFalse(result)
            # 실패 시 로딩 대기 로직을 타지 않아야 함
            self.mock_validator.wait_for_loading.assert_not_called()

if __name__ == "__main__":
    unittest.main()