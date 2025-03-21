# view.py
from PyQt5.QtWidgets import (
    QTableWidget, QComboBox, QSpinBox, QWidget,QVBoxLayout,
    QHBoxLayout, QLineEdit, QLabel, QTableWidgetItem
)
from widget.test_case.test_case_viewmodel import TestCaseViewModel


class TestCaseTableView(QTableWidget):
    def __init__(self, view_model):
        super().__init__(18, 7)  # 18행 7열 테이블 생성
        self.view_model = view_model

        # 테이블 헤더 설정
        headers = ["TC ID", "Scenario", "Domain Count", "Publisher", "Subscriber", "Data Size Range", "QoS Policy"]
        self.setHorizontalHeaderLabels(headers)

        # 테이블 초기화
        self._populate_table()

    def _populate_table(self):
        """테이블을 ViewModel 데이터를 기반으로 채움"""
        for row in range(len(self.view_model.get_all_test_cases())):
            test_case = self.view_model.get_test_case(row)

            # TC ID (읽기 전용)
            self.setItem(row, 0, QTableWidgetItem(str(test_case.tc_id)))

            # Scenario (콤보 박스)
            scenario_combo = self._create_combo_box(
                ["Basic Performance", "Packet Count", "Message Drop Rate", "Subscriber Count", "Domain Count"],
                test_case.scenario,
                lambda value, r=row: self.view_model.update_test_case(r, scenario=value)
            )
            self.setCellWidget(row, 1, scenario_combo)

            # Domain Count (스핀 박스)
            domain_spinbox = self._create_spin_box(
                1, 100,
                test_case.domain_count,
                lambda value, r=row: self.view_model.update_test_case(r, domain_count=value)
            )
            self.setCellWidget(row, 2, domain_spinbox)

            # Publisher (콤보 박스)
            publisher_combo = self._create_combo_box(
                ["AP1", "AP2", "MCU"],
                test_case.publisher,
                lambda value, r=row: self.view_model.update_test_case(r, publisher=value)
            )
            self.setCellWidget(row, 3, publisher_combo)

            # Subscriber (콤보 박스)
            subscriber_combo = self._create_combo_box(
                ["AP1", "AP2", "MCU"],
                test_case.subscriber,
                lambda value, r=row: self.view_model.update_test_case(r, subscriber=value)
            )
            self.setCellWidget(row, 4, subscriber_combo)

            # Data Size Range (입력 필드)
            data_size_widget = self._create_data_size_widget(
                test_case.data_size_min,
                test_case.data_size_max,
                row
            )
            self.setCellWidget(row, 5, data_size_widget)

            # QoS Policy (콤보 박스)
            qos_combo = self._create_combo_box(
                ["Volatile", "Transient-local", "Transit", "Persistent"],
                test_case.qos_policy,
                lambda value, r=row: self.view_model.update_test_case(r, qos_policy=value)
            )
            self.setCellWidget(row, 6, qos_combo)

    def _create_combo_box(self, items, current_value, on_change):
        """콤보 박스 생성"""
        combo_box = QComboBox()
        combo_box.addItems(items)
        combo_box.setCurrentText(current_value)
        combo_box.currentTextChanged.connect(on_change)  # 값 변경 시 호출
        return combo_box

    def _create_spin_box(self, min_val, max_val, current_value, on_change):
        """스핀 박스 생성"""
        spin_box = QSpinBox()
        spin_box.setRange(min_val, max_val)
        spin_box.setValue(current_value)
        spin_box.valueChanged.connect(on_change)  # 값 변경 시 호출
        return spin_box

    def _create_data_size_widget(self, min_value, max_value, row):
        """데이터 크기 범위를 위한 위젯 생성"""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        min_edit = QLineEdit(str(min_value))
        max_edit = QLineEdit(str(max_value))

        min_edit.textChanged.connect(lambda value: self._update_data_size(value, row=row, is_min=True))
        max_edit.textChanged.connect(lambda value: self._update_data_size(value, row=row, is_min=False))

        layout.addWidget(min_edit)
        layout.addWidget(QLabel("~"))
        layout.addWidget(max_edit)

        layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
        return widget

    def _to_int(value):
        """문자열을 정수로 변환 (유효하지 않으면 None 반환)"""
        return int(value) if value.isdigit() else None

    def _update_data_size(self, value, row, is_min):
        """데이터 크기 범위 업데이트"""
        int_value = self._to_int(value)
        if int_value is not None:
            if is_min:
                self.view_model.update_test_case(row=row, data_size_min=int_value)
            else:
                self.view_model.update_test_case(row=row, data_size_max=int_value)


    def save_state(self):
        """테이블 상태 저장"""
        state = {}
        for row in range(self.rowCount()):
            test_case = self.view_model.get_test_case(row)
            if test_case:
                state[row] = {
                    "scenario": test_case.scenario,
                    "domain_count": test_case.domain_count,
                    "publisher": test_case.publisher,
                    "subscriber": test_case.subscriber,
                    "data_size_min": test_case.data_size_min,
                    "data_size_max": test_case.data_size_max,
                    "qos_policy": test_case.qos_policy,
                }
        return state


    def restore_state(self, state):
        """테이블 상태 복원"""
        for row, values in state.items():
            print(f"Restoring row {row}: {values}")  # 각 행의 데이터 로그 출력
            self.view_model.update_test_case(
                row,
                scenario=values["scenario"],
                domain_count=values["domain_count"],
                publisher=values["publisher"],
                subscriber=values["subscriber"],
                data_size_min=values["data_size_min"],
                data_size_max=values["data_size_max"],
                qos_policy=values["qos_policy"],
            )
            self._populate_table()  # 테이블 다시 채우기

