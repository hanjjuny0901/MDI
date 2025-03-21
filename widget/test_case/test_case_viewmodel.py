# viewmodel.py
from typing import List
from widget.test_case.test_case_model import TestCase

class TestCaseViewModel:
    def __init__(self):
        self.test_cases = self._create_default_test_cases()

    def _create_default_test_cases(self):
        """기본 테스트 케이스 데이터 생성"""
        scenarios = ["기본 성능", "패킷 개수", "메시지 드랍율", "Subscriber 개수", "Domain 개수"]
        pub_sub_options = ["AP1", "AP2", "MCU"]
        qos_options = ["Volatile", "Transient-local", "Transit", "Persistent"]

        return [
            TestCase(
                tc_id=i + 1,
                scenario=scenarios[0],
                domain_count=1,
                publisher=pub_sub_options[0],
                subscriber=pub_sub_options[0],
                data_size_min=100,
                data_size_max=100,
                qos_policy=qos_options[0]
            )
            for i in range(18)
        ]

    def update_test_case(self, row, **kwargs):
        """테스트 케이스 업데이트"""
        if row < len(self.test_cases):
            for key, value in kwargs.items():
                setattr(self.test_cases[row], key, value)

    def get_test_case(self, row):
        """특정 테스트 케이스 반환"""
        if row < len(self.test_cases):
            return self.test_cases[row]
        return None

    def get_all_test_cases(self):
        """모든 테스트 케이스 반환"""
        return self.test_cases
