import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from nuriCrawling.DataCrawler import DataCrawler

class TestDataCrawler(unittest.TestCase):
    def setUp(self):
        # 1. 의존성 객체들을 Mock으로 생성
        self.mock_driver = MagicMock()
        self.mock_validator = MagicMock()
        self.mock_mover = MagicMock()
        self.mock_data_validator = MagicMock()

        # 2. DataCrawler 인스턴스 생성
        self.crawler = DataCrawler(
            driver=self.mock_driver,
            validator=self.mock_validator,
            mover=self.mock_mover,
            data_validator=self.mock_data_validator
        )

    def test_clean_text(self):
        """텍스트 정제 기능 테스트"""
        raw_text = "  공고번호 \n 12345 \t "
        expected = "공고번호 12345"
        self.assertEqual(self.crawler.clean_text(raw_text), expected)
        self.assertEqual(self.crawler.clean_text(None), "")

    def test_collect_data_at_index_already_collected(self):
        """이미 수집된 데이터인 경우 스킵(Skip)하는지 테스트"""
        # Mock 설정: 이미 수집된 ID라고 가정
        self.mock_data_validator.is_already_collected.return_value = True

        # 가짜 테이블 행(Row) 생성
        mock_row = MagicMock()
        mock_cell = MagicMock()
        mock_cell.get_attribute.return_value = "20240101-00"
        mock_row.find_elements.return_value = [MagicMock(), mock_cell, MagicMock()]

        with patch('selenium.webdriver.support.ui.WebDriverWait.until') as mock_wait:
            mock_wait.return_value = mock_row

            result = self.crawler.collect_data_at_index(0)

            # 검증: 상세 페이지로 넘어가지 않고 None을 반환해야 함
            self.assertIsNone(result)
            self.mock_data_validator.is_already_collected.assert_called_once()
            # 상세 클릭 메서드가 실행되지 않았는지 확인
            self.mock_driver.execute_script.assert_not_called()

    def test_extract_detail_data(self):
        """상세 페이지 테이블 데이터 추출 기능 테스트"""
        # Mock 상세 테이블 구성
        mock_table = MagicMock()
        mock_th = MagicMock()
        mock_th.get_attribute.return_value = "공고명"
        mock_td = MagicMock()
        mock_td.get_attribute.return_value = "테스트 입찰 공고"

        mock_table.find_elements.side_effect = [[mock_th], [mock_td]]
        self.mock_driver.find_elements.return_value = [mock_table]

        bid_no = "20240101-00"
        result = self.crawler._extract_detail_data(bid_no)

        expected = {
            "목록_입찰공고번호": bid_no,
            "공고명": "테스트 입찰 공고"
        }
        self.assertEqual(result, expected)

    def test_start_collection_pagination(self):
        """여러 페이지 수집 및 페이지 이동 로직 테스트"""
        # 1페이지에 2개의 행이 있다고 가정
        self.mock_driver.find_elements.return_value = [MagicMock(), MagicMock()]

        # 각 인덱스 수집 시 가짜 데이터 반환하도록 설정
        self.crawler.collect_data_at_index = MagicMock(return_value={"data": "sample"})
        # 2페이지 이동 성공 설정
        self.mock_mover.move_to_next_page.return_value = True

        # 2페이지 분량 수집 시작
        self.crawler.start_collection(target_pages=2)

        # 검증: move_to_next_page가 호출되었는지 확인
        self.mock_mover.move_to_next_page.assert_called_with(2)
        # 총 4번(2개 행 * 2페이지) 수집 시도가 있었는지 확인
        self.assertEqual(self.crawler.collect_data_at_index.call_count, 4)

if __name__ == "__main__":
    unittest.main()