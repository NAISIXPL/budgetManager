class UiManager:
    def __init__(self, balanceLabel, summBalanceLabel, summIncomeLabel, summExpensesLabel, table):
        super(UiManager, self).__init__()
        self.balanceLabel = balanceLabel
        self.summaryBalance = summBalanceLabel
        self.summaryIncome = summIncomeLabel
        self.summaryExpense = summExpensesLabel
        self.dataTable = table

        self.balance = 0
        self.summBal = 0
        self.summInc = 0
        self.summExp = 0

    def zero_labels(self):
        self.balance = 0
        self.summBal = 0
        self.summInc = 0
        self.summExp = 0
        self.balanceLabel.setText(str(self.balance))
        self.summaryBalance.setText(str(self.summBal))
        self.summaryIncome.setText(str(self.summInc))
        self.summaryExpense.setText(str(self.summExp))
    def balance_update(self, input_type, amount, usage=0):
        if usage == 0:  # main balance update
            if input_type == 'Expense':
                self.balance -= amount
            else:
                self.balance += amount
            self.balanceLabel.setText(str(self.balance))
        elif usage == 1:  # Summary update
            if input_type == 'Expense':
                self.summExp += amount
                self.summBal -= amount
            else:
                self.summInc += amount
                self.summBal += amount
            self.summaryBalance.setText(str(self.summBal))
            self.summaryIncome.setText(str(self.summInc))
            self.summaryExpense.setText(str(self.summExp))

    def summary_reset(self):
        self.summBal = 0
        self.summInc = 0
        self.summExp = 0
        self.summaryBalance.setText(str(0))
        self.summaryIncome.setText(str(0))
        self.summaryExpense.setText(str(0))
