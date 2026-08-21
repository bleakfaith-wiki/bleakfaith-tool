import json


class DataTable:
    def __init__(self, data: dict) -> None:
        self.type: str = data["Type"]
        self.name: str = data["Name"]
        self.klass: str = data["Class"]
        self.package: str = data["Package"]
        self.rows: dict = data["Rows"]

    @staticmethod
    def from_file(path: str) -> DataTable:
        with open(path, "r") as f:
            data = json.load(f)[0]
        return DataTable(data)
