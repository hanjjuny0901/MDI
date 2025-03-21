import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QMdiArea, QMdiSubWindow, QAction
from PyQt5.QtCore import QSettings, QByteArray, QTimer, Qt
from config_loader import load_subwindow_configs
from main.main_viewmodel import MainViewModel
from functools import partial


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        # ViewModel 연결
        self.viewmodel = MainViewModel()

        # MDI 영역 생성 및 설정
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        # 설정 파일 경로 지정 및 QSettings 초기화 (상대 경로)
    #   //  current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 스크립트의 디렉토리
    #  //   self.settings_file = os.path.join(current_dir, "..//config//settings.ini")  # 상대 경로 지정
    #   //  os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)  # config 폴더 생성
    #  //   self.settings = QSettings(self.settings_file, QSettings.IniFormat)

        settings_file = QtCore.QDir.currentPath() + "../config/settings.ini"
        self.settings = QtCore.QSettings(settings_file, QtCore.QSettings.IniFormat)

        # Config 파일 로드
        self.subwindow_configs = load_subwindow_configs()

        # 서브윈도우 관리 딕셔너리 (위젯별로 하나씩만 생성)
        self.subwindow_map = {}  # key: base_title, value: QMdiSubWindow

        # 메뉴바 생성 및 액션 추가
        self._create_menu_bar()

        # 기본 설정
        self.setWindowTitle("MDI Example with MVVM")
        self.resize(1200, 800)

        # 서브윈도우 복원
        self._restore_subwindows()

    def _create_menu_bar(self):
        """메뉴바 생성 및 액션 추가"""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        for config in self.subwindow_configs:
            action = QAction(config["action_name"], self)
            action.triggered.connect(partial(self._handle_subwindow, config))
            file_menu.addAction(action)

    def _handle_subwindow(self, config):
        """서브윈도우를 Lazy Loading 방식으로 열거나 복원"""
        base_title = config["base_title"]

        # 이미 생성된 서브윈도우가 있는 경우 활성화
        if base_title in self.subwindow_map:
            sub_window = self.subwindow_map[base_title]
            sub_window.setWindowState(sub_window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
            sub_window.raise_()
            return

        geometry_key = self._get_geometry_key(base_title)
        geometry = self.settings.value(geometry_key)

        sub_window = QMdiSubWindow()

        def initialize_widget():
            view_model = config["view_model_class"]()
            widget = config["widget_class"](view_model)
            sub_window.setWidget(widget)

        initialize_widget()  # Lazy Loading 방식으로 위젯 초기화

        sub_window.setWindowTitle(self.viewmodel.create_subwindow_title(base_title))

        if geometry:
            sub_window.restoreGeometry(QByteArray(geometry))
            QTimer.singleShot(100, lambda: sub_window.activateWindow())
        else:
            sub_window.resize(*config["size"])

        sub_window.closeEvent = lambda event: self._save_subwindow_state(sub_window, base_title)

        # 서브윈도우를 관리 딕셔너리에 추가
        self.subwindow_map[base_title] = sub_window

        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

    def _save_subwindow_state(self, sub_window, base_title):
        """서브윈도우의 상태 저장"""
        geometry_key = self._get_geometry_key(base_title)
        state_key = f"{base_title}_state"

        widget = sub_window.widget()

        # Geometry 저장
        self.settings.setValue(geometry_key, sub_window.saveGeometry())

        # 상태 저장 (뷰가 save_state를 지원하는 경우)
        if hasattr(widget, "save_state"):
            state = widget.save_state()
            self.settings.setValue(state_key, state)

    def _restore_subwindows(self):
        """서브윈도우 복원"""
        for config in self.subwindow_configs:
            geometry_key = self._get_geometry_key(config["base_title"])
            state_key = f"{config['base_title']}_state"

            if self.settings.value(geometry_key):  # 저장된 geometry가 있는 경우만 복원
                base_title = config["base_title"]
                sub_window = QMdiSubWindow()
                view_model = config["view_model_class"]()
                widget = config["widget_class"](view_model)

                sub_window.setWidget(widget)
                sub_window.setWindowTitle(self.viewmodel.create_subwindow_title(base_title))
                sub_window.restoreGeometry(QByteArray(self.settings.value(geometry_key)))

                # 상태 복원 (뷰가 restore_state를 지원하는 경우)
                if hasattr(widget, "restore_state"):
                    state = self.settings.value(state_key)
                    if state:
                        widget.restore_state(state)

                # 서브윈도우를 관리 딕셔너리에 추가
                self.subwindow_map[base_title] = sub_window

                self.mdi_area.addSubWindow(sub_window)
                sub_window.show()

    def _get_geometry_key(self, base_title):
        """QSettings에서 사용할 geometry 키 생성"""
        return f"{base_title}_geometry"
