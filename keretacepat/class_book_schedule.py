from datetime import datetime as dt, timedelta


class BookSchedule:
    date_format = "%Y%m%d"

    def __init__(self, days_diff=None, list_inc_days=None):
        self.days_diff = days_diff
        self.list_inc_days = list_inc_days
        self.new_date = None
        self.new_day_name = None

    def book_date(self) -> str:
        self.new_date = (dt.now() + timedelta(days=self.days_diff)).strftime(self.date_format)
        return self.new_date

    def filtered_date(self) -> bool:
        self.new_day_name = dt.strptime(self.book_date(), self.date_format).strftime("%A")
        return True if self.new_day_name in self.list_inc_days else False

    def add_date(self) -> str:
        return self.new_date if self.filtered_date() else None


""" DEBUG
input_days_diff = 9
input_list_days = ['Saturday', 'Sunday']
if __name__ == "__main__":
    cek_jadwal = BookSchedule(days_diff=input_days_diff, list_inc_days=input_list_days)
    print(f"Book date: {cek_jadwal.add_date()}")
"""
