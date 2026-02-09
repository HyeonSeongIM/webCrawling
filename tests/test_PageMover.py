import unittest
from unittest.mock import MagicMock
from nuriCrawling.PageMover import PageMover

class TestPageMover(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_validator = MagicMock()
        self.mover = PageMover(self.mock_driver, self.mock_validator)

    def test_move_to_next_page_success(self):
        """해피 케이스: 다음 페이지 번호가 존재할 때 이동 성공"""
        self.mock_driver.find_element.return_value = MagicMock()
        result = self.mover.move_to_next_page(2)
        self.assertTrue(result)
        self.mock_validator.wait_for_loading.assert_called()

    def test_move_to_next_page_fail(self):
        """엣지 케이스: 존재하지 않는 페이지 번호(예: 마지막 페이지 이후) 요청 시 False 반환"""
        self.mock_driver.find_element.side_effect = Exception("Not Found")
        result = self.mover.move_to_next_page(999)
        self.assertFalse(result)