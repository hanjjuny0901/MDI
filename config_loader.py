import json
from importlib import import_module


def load_subwindow_configs(config_file="subwindow_configs.json"):
    """JSON 파일에서 서브윈도우 설정을 동적으로 로드"""
    with open(config_file, "r") as file:
        configs = json.load(file)

    for config in configs:
        config["widget_class"] = _import_class(config["widget_class"])
        config["view_model_class"] = _import_class(config["view_model_class"])

    return configs


def _import_class(class_path):
    """클래스 경로를 기반으로 동적으로 클래스 임포트"""
    module_path, class_name = class_path.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, class_name)
