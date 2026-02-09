import os

class DataValidator:
    def __init__(self, storage_path="results/collected_ids.txt"):
        """
        저장된 ID 목록을 로드하여 재시작 시 중복 수집을 방지합니다.
        """
        self.storage_path = storage_path
        self.output_dir = os.path.dirname(self.storage_path)

        # 저장 폴더가 없으면 생성
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # 기수집된 ID 목록 로드 (메모리 최적화를 위해 set 사용)
        self.collected_ids = self._load_checkpoints()

    def _load_checkpoints(self):
        """저장된 파일에서 이전에 수집 성공한 ID 리스트를 읽어옵니다."""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    def is_already_collected(self, bid_no):
        """
        이미 수집된 데이터인지 확인합니다.
        이 로직이 리트라이(Retry) 시 중복 작업을 막는 핵심입니다.
        """
        return bid_no in self.collected_ids

    def record_success(self, bid_no):
        if bid_no and bid_no not in self.collected_ids:
            self.collected_ids.add(bid_no)
            # 'a' 모드로 열어서 즉시 기록
            with open(self.storage_path, "a", encoding="utf-8") as f:
                f.write(f"{bid_no}\n")
                f.flush()            # 메모리 버퍼 비우기
                os.fsync(f.fileno()) # OS 레벨에서 물리적 저장 강제
            print(f"      [Validator] 체크포인트 기록 완료: {bid_no}")

    def get_summary(self):
        """현재까지 수집 완료된 전체 데이터 개수를 반환합니다."""
        return len(self.collected_ids)