# main/main_viewmodel.py

from main.main_model import MainModel

class MainViewModel:
    def __init__(self):
        self.model = MainModel()

    def create_subwindow_title(self, base_title: str) -> str:
        """서브윈도우 제목 생성"""
        self.model.increment_subwindow_count()
        count = self.model.get_subwindow_count()
        return f"{base_title} {count}"
