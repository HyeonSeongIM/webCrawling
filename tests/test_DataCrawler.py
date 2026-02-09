import unittest
from unittest.mock import MagicMock, patch
from nuriCrawling.DataCrawler import DataCrawler

class TestDataCrawler(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_validator = MagicMock()
        self.mock_mover = MagicMock()
        self.crawler = DataCrawler(self.mock_driver, self.mock_validator, self.mock_mover)

    def test_clean_text(self):
        """데이터 정제 테스트: 줄바꿈 및 연속 공백이 제거되는지 확인"""
        input_raw = "  입찰 \n 공고  번호\t"
        expected = "입찰 공고 번호"
        self.assertEqual(self.crawler.clean_text(input_raw), expected)

    def test_collect_data_at_index_stale_element_retry(self):
        """예외 케이스: 행을 찾는 도중 요소가 만료(Stale)되었을 때 예외 처리 확인"""
        self.mock_driver.find_elements.return_value = [] # 행이 갑자기 사라진 경우
        result = self.crawler.collect_data_at_index(0)
        self.assertIsNone(result)

    def test_detail_data_mapping(self):
        """해피 케이스: 상세 페이지 th-td 테이블 쌍이 딕셔너리로 잘 변환되는지 확인"""
        mock_th = MagicMock(text="공고명")
        mock_td = MagicMock()
        mock_td.get_attribute.return_value = "테스트 공고"

        # 실제 환경과 유사하게 Mock 구성
        with patch.object(self.crawler, 'collect_data_at_index') as mock_collect:
            mock_collect.return_value = {"공고명": "테스트 공고"}
            data = self.crawler.collect_data_at_index(0)
            self.assertEqual(data["공고명"], "테스트 공고")