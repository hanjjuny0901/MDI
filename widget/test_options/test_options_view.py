# view.py
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QComboBox
from widget.test_options.test_options_viewmodel import TestOptionsViewModel


class TestOptionsTreeView(QTreeWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        # 트리 헤더 설정
        self.setHeaderLabels(["Parameter", "Value"])
        self.setColumnWidth(0, 200)

        # ViewModel에서 카테고리 데이터를 가져와 트리에 추가
        self._populate_tree()

    def _populate_tree(self):
        """트리를 ViewModel 데이터를 기반으로 채움"""
        categories = self.view_model.get_categories()

        for category in categories:
            category_item = QTreeWidgetItem(self, [category.name])

            for parameter in category.parameters:
                parameter_item = QTreeWidgetItem(category_item, [parameter.name])
                combo_box = self._create_combo_box(parameter.options, parameter.default_value)
                combo_box.currentTextChanged.connect(
                    lambda value, p=parameter: self._update_parameter(p, value)
                )
                self.setItemWidget(parameter_item, 1, combo_box)

    def _create_combo_box(self, items, default_value):
        """콤보 박스 생성"""
        combo_box = QComboBox()
        combo_box.addItems(items)
        combo_box.setCurrentText(default_value)
        return combo_box

    def _update_parameter(self, parameter, value):
        """파라미터 값 업데이트"""
        parameter.default_value = value
