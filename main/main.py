from selenium import webdriver
from PageValidator import PageValidator
from PageMover import PageMover
from OptionSearcher import OptionSearcher
from DataCrawler import DataCrawler
from DataHandler import DataHandler

def main():
    # 드라이버 설정
    driver = webdriver.Chrome()
    driver.maximize_window()

    # 클래스 인스턴스화
    validator = PageValidator(driver)
    mover = PageMover(driver, validator)
    searcher = OptionSearcher(driver, validator) # 추가됨
    crawler = DataCrawler(driver, validator, mover)
    handler = DataHandler()

    try:
        # 사이트 접속 및 상태 검증
        driver.get("https://nuri.g2b.go.kr/")
        validator.close_popups()    # 팝업 닫기
        validator.wait_for_loading() # 페이지 안정화 대기

        # 메뉴 이동
        mover.move_to_bid_list()

        # 검색 옵션 설정 및 실행
        searcher.execute_search()

        # 상세 수집 및 루프
        final_data = crawler.start_collection(target_pages=2)

        # 데이터 핸들러에 전달
        for item in final_data:
            handler.add_data(item)

    except Exception as e:
        print(f"\n[Main] 프로세스 중 오류 발생: {e}")

    finally:
        # 데이터 저장
        handler.save_to_csv()
        print("[Main] 브라우저를 종료합니다.")
        driver.quit()

if __name__ == "__main__":
    main()