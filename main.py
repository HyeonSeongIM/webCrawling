import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from nuriCrawling.PageValidator import PageValidator
from nuriCrawling.PageMover import PageMover
from nuriCrawling.OptionSearcher import OptionSearcher
from nuriCrawling.DataCrawler import DataCrawler
from nuriCrawling.DataHandler import DataHandler
from nuriCrawling.DataValidator import DataValidator

def main():
    # 드라이버 설정
    driver = webdriver.Chrome()
    driver.maximize_window()

    # 클래스 인스턴스화
    validator = PageValidator(driver)
    mover = PageMover(driver, validator)
    searcher = OptionSearcher(driver, validator)
    data_validator = DataValidator()
    crawler = DataCrawler(driver, validator, mover, data_validator)
    handler = DataHandler()


    try:
        # 사이트 접속 및 상태 검증
        driver.get("https://nuri.g2b.go.kr/")
        validator.close_popups()    # 팝업 닫기
        validator.wait_for_loading() # 페이지 안정화 대기

        # 메뉴 이동
        mover.move_to_menu("입찰공고", "입찰공고목록")

        # 검색 옵션 설정 및 실행
        searcher.execute_search("검색")

        # 상세 수집 및 루프
        final_data = crawler.start_collection(10)

        # 데이터 핸들러에 전달
        for item in final_data:
            handler.add_data(item)

    except Exception as e:
        print(f"\n[Main] 프로세스 중 오류 발생: {e}")

    finally:
        # 데이터 저장
        handler.save()
        print("[Main] 브라우저를 종료합니다.")
        driver.quit()

if __name__ == "__main__":
    main()