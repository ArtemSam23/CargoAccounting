from accounting_app import AccountingApp
from database import create_trucks_table

if __name__ == '__main__':
    create_trucks_table()
    app = AccountingApp()
    app.start()
