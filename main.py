"""
Instruction:
    Add section:
        Amount - here you put value
        Type - Income/Expense
        Date - Date in Format (Y/M/D)
        Description - Description of transaction
        Add button - With that you can add transaction to history
        Undo button - With that you can delete last row if you made mistake
    Statistics section:
        Balance section:
            Balance - current balance
        Summary section:
            Income - income in given date range
            Expense - income in given date range
            Balance - balance in given date range
    Filters section:
        Reset button - It will reset table and all labels to deafult state (SELECT * table)
        Starting/Ending date - Time range
        Search button - It will pass above range to program ,so it will be able to show transaction from this range
    Table:
        Here are transaction

"""
import sys

from PyQt6 import QtCore
# PyQt6
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import QFile, QIODevice, Qt
from PyQt6.uic import loadUi
# Database
from databasemanager import DatabaseManager
# Data structure
from datastructure import Transaction
# Ui
from uimanager import UiManager


class MyMainWindow(QMainWindow):
    def __init__(self):

        super(MyMainWindow, self).__init__()
        ui_file = QFile('./main.ui')
        if ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            loadUi(ui_file, self)

            ui_file.close()
            self.db_manager = DatabaseManager('history.sqlite')
            self.ui = UiManager(self.balanceLabel, self.summaryBalance, self.summaryIncome, self.summaryExpense,
                                self.dataTable)
            self.db_read(1)



            # Some graphic changes
            self.dataTable.setColumnWidth(3, 450)
            self.addDate.setDateTime(QtCore.QDateTime.currentDateTime())
            # Connecting button
            self.filterButton.clicked.connect(self.date_filter)
            self.addButton.clicked.connect(self.transaction_manager)
            self.resetButton.clicked.connect(self.db_read)
            self.undoButton.clicked.connect(self.undo_row)

    def db_read(self, usage):
        self.remove_rows()
        query_str = "SELECT * FROM history"
        query = self.db_manager.execute_query(query_str)
        if usage == 0:
            self.ui.summary_reset()
        # Iterating through query
        while query.next():
            input_type = query.value(1)
            amount = query.value(2)
            # Updating balance
            if usage == 0:
                self.ui.balance_update(input_type, amount, 1)
            if usage == 1:
                self.ui.balance_update(input_type, amount)
                self.ui.balance_update(input_type, amount, 1)
            self.query_handling(query)

    def transaction_manager(self):

        # Data collecting
        date = self.addDate.date()
        input_type = self.input_type.currentText()
        try:
            amount = int(self.amount.text())
        except ValueError:
            return
        description = self.description.toPlainText()

        # Putting obtained data into tables
        date_string = f'{date.year()}-{date.month()}-{date.day()}'
        query_table = [date, input_type, amount, description]
        transaction = Transaction(date_string, input_type, amount, description)

        # Sending info to DB
        query_str = "INSERT INTO history(date, type, amount, description) VALUES (?, ?, ?, ?)"
        query = self.db_manager.execute_query(query_str, query_table)
        self.db_manager.db.commit()

        # Balance Update
        self.ui.balance_update(input_type, amount)
        self.ui.balance_update(input_type, amount, 1)

        # Table Update
        self.table_update(input_type, transaction)

    def table_update(self, input_type, transaction):

        currentRowCount = self.dataTable.rowCount()
        # Insert a new row
        self.dataTable.insertRow(currentRowCount)
        for item in range(0, 4):
            self.dataTable.setItem(currentRowCount, item, transaction.get_details()[item])
            flagChange = self.dataTable.item(currentRowCount, item)
            flagChange.setFlags(flagChange.flags() & ~Qt.ItemFlag.ItemIsEditable)

        # Color of row
        if input_type == "Income":
            color = QColor(144, 238, 144)
        else:
            color = QColor(255, 99, 71)
        for column in range(self.dataTable.columnCount()):
            item = self.dataTable.item(currentRowCount, column)
            if item is not None:
                item.setBackground(color)

    def undo_row(self):
        query_str = "SELECT * FROM history WHERE id = (SELECT max(id) FROM history)"
        query = self.db_manager.execute_query(query_str)

        if query.next():
            query_str2 = "DELETE FROM history WHERE id = (SELECT max(id) FROM history)"
            query2 = self.db_manager.execute_query(query_str2)
            self.ui.zero_labels()
            self.db_read(1)
        else:
            pass
    def remove_rows(self):

        rows = self.dataTable.rowCount()
        for row in range(0, rows):
            self.dataTable.removeRow(0)
    def date_filter(self):

        # Clearing table
        self.remove_rows()
        # Obtaining data
        startDate = self.startDate.date()
        endDate = self.endDate.date()
        # Query
        query_table = [startDate, endDate]
        query_str = "SELECT * FROM history WHERE ? <= date and date <= ?"
        query = self.db_manager.execute_query(query_str, query_table)

        self.ui.summary_reset()
        while query.next():
            self.query_handling(query)
            self.ui.balance_update(query.value(1), query.value(2),1)

    def query_handling(self, query):

        date, input_type, amount, description = query.value(0), query.value(1), query.value(
            2), query.value(3)
        transaction = Transaction(date, input_type, amount, description)
        # Table Update
        self.table_update(input_type, transaction)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    widget = QStackedWidget()
    widget.addWidget(window)
    widget.setFixedHeight(600)
    widget.setFixedWidth(800)
    widget.show()
    app.exec()
