# viewmodel.py
from widget.test_options.test_options_model import Category, Parameter

class TestOptionsViewModel:
    def __init__(self):
        self.categories = self._create_categories()

    def _create_categories(self):
        """카테고리 및 파라미터 정의"""
        qos_parameters = [
            Parameter("Reliability", ["Yes", "No"], "Yes"),
            Parameter("Durability", ["Volatile", "Transient-local", "Transit", "Persistent"], "Volatile"),
            Parameter("Durability service", ["Yes", "No"], "No"),
            Parameter("Deadline", ["Yes", "No"], "No"),
            Parameter("Liveliness", ["Yes", "No"], "No"),
            Parameter("Lifespan", ["Yes", "No"], "No"),
            Parameter("History", ["Yes", "No"], "No"),
            Parameter("Resource Limits", ["Yes", "No"], "No"),
            Parameter("Partition", ["Yes", "No"], "No")
        ]

        security_parameters = [
            Parameter("Authentication", ["Yes", "No"], "Yes"),
            Parameter("Access Control", ["Yes", "No"], "Yes"),
            Parameter("Message encryption", ["Yes", "No"], "No"),
            Parameter("Message Authentication", ["Yes", "No"], "No")
        ]

        return [
            Category("QoS", qos_parameters),
            Category("Security", security_parameters)
        ]

    def get_categories(self):
        """카테고리 데이터를 반환"""
        return self.categories
