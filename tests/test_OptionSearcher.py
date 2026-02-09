import unittest
from unittest.mock import MagicMock, patch
from nuriCrawling.OptionSearcher import OptionSearcher

class TestOptionSearcher(unittest.TestCase):
    def setUp(self):
        # 드라이버와 밸리데이터를 목(Mock) 객체로 생성하여 주입
        self.mock_driver = MagicMock()
        self.mock_validator = MagicMock()
        self.searcher = OptionSearcher(self.mock_driver, self.mock_validator)

    def test_set_search_keyword_happy_case(self):
        """해피 케이스: 키워드 입력 시 input box를 찾고 clear 후 값을 입력하는지 확인"""
        mock_input = MagicMock()
        self.mock_driver.find_element.return_value = mock_input

        self.searcher.set_search_keyword("테스트 공고")

        # 입력창을 제대로 찾았는지, 기존 내용을 지우고 키워드를 보냈는지 검증
        mock_input.clear.assert_called_once()
        mock_input.send_keys.assert_called_with("테스트 공고")

    def test_set_search_keyword_empty(self):
        """엣지 케이스: 키워드가 None이나 빈 문자열일 때 불필요한 동작을 하지 않는지 확인"""
        self.searcher.set_search_keyword("")
        self.mock_driver.find_element.assert_not_called()

    def test_execute_search_happy_case(self):
        """해피 케이스: 검색 버튼 클릭 후 자바스크립트 실행과 로딩 대기가 수행되는지 확인"""
        mock_btn = MagicMock()
        self.mock_driver.find_element.return_value = mock_btn

        self.searcher.execute_search()

        # 검색 버튼을 자바스크립트로 클릭했는지 확인
        self.mock_driver.execute_script.assert_called()
        # 클릭 후 로딩바 대기가 실행되었는지 확인
        self.mock_validator.wait_for_loading.assert_called()

    def test_ensure_list_page_success(self):
        """해피 케이스: 목록 페이지 확인 요소를 성공적으로 찾을 때 예외 없이 통과하는지 확인"""
        with patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_until:
            mock_until.return_value = True
            try:
                self.searcher.ensure_list_page()
            except Exception as e:
                self.fail(f"목록 확인 성공 시나리오에서 예외가 발생했습니다: {e}")

    def test_ensure_list_page_timeout(self):
        """예외 케이스: 타임아웃 발생 시 프로그램이 중단되지 않고 에러 로그만 출력하는지 확인"""
        with patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_until:
            # WebDriverWait가 실패(Timeout)하는 상황 시뮬레이션
            mock_until.side_effect = Exception("Timeout")

            try:
                self.searcher.ensure_list_page()
                # 메서드 내부에서 예외를 처리(try-except)하므로 밖으로 던져지면 안 됨
            except:
                self.fail("ensure_list_page 내부에서 예외 처리가 되지 않았습니다.")