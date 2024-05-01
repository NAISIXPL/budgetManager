from PyQt6.QtWidgets import QTableWidgetItem


class Transaction:

    def __init__(self, date, input_type, amount, description):
        self.date = QTableWidgetItem(date)
        self.input_type = QTableWidgetItem(input_type)
        self.amount = QTableWidgetItem(str(amount))
        self.description = QTableWidgetItem(description)

    def get_details(self):
        return [self.date, self.input_type, self.amount, self.description]