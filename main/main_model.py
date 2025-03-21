# main/main_model.py

class MainModel:
    def __init__(self):
        self.subwindow_count = 0

    def increment_subwindow_count(self):
        """서브윈도우 카운트를 증가"""
        self.subwindow_count += 1

    def get_subwindow_count(self):
        """현재 서브윈도우 카운트를 반환"""
        return self.subwindow_count
