import os
import sqlite3
import sys
from datetime import datetime


class DBTools:
    # os.path.dirname(os.path.abspath(__file__))
    # os.path.abspath(os.getcwd())
    dir_name = os.path.dirname(os.path.abspath(__file__))
    db_name = "db-kereta-cepat.db"
    db_file_path = f"{dir_name}/db/{db_name}"

    def __init__(self):
        self.db_connect = None
        self.db_cursor = None
        self.list_unsent_records = None

    def connect_db(self):
        try:

            self.db_connect = sqlite3.connect(self.db_file_path)
        except sqlite3.OperationalError as oe:
            print(f"Path = {self.db_file_path}")
            sys.exit(f"ERROR: Cannot open DB, Operational Error - exiting ... ({oe})")
        else:
            # self.db_connect.row_factory = self.dict_factory
            self.db_connect.row_factory = sqlite3.Row
            self.db_cursor = self.db_connect.cursor()

    def disconnect_db(self):
        if self.db_connect:
            if self.db_cursor:
                self.db_cursor.close()
                self.db_cursor = None
            self.db_connect.close()
            self.db_connect = None

    def create_config_table(self):
        sql_query = """
            create table if not exists kereta_cepat_config(
            config_id integer primary key autoincrement,
            config_name text default 'kereta_cepat',
            config_status text default 'A',
            last_checked text not null
            );        
        """
        self.db_connect.execute(sql_query)
        self.db_connect.commit()

    def create_table_kereta_cepat(self):
        sql_query = """
            create table if not exists kereta_cepat(
            ticket_id integer primary key autoincrement,
            train_date text not  null,
            from_station text not null,
            to_station text not null,
            notification_sent text default 'N'
            );        
        """
        self.db_connect.execute(sql_query)
        self.db_connect.commit()

    def static_show_table(self):
        self.connect_db()
        self.create_config_table()
        self.create_table_kereta_cepat()
        sql_query = "select * from kereta_cepat_config"
        result = self.db_connect.execute(sql_query)
        records = result.fetchall()
        print(f"========= SHOW TABLE: KERETA_CEPAT_CONFIG ===========")
        for record in records:
            print(f"Record = CONFIG_NAME: {record['config_name']} | "
                  f"CONFIG_STATUS: {record['config_status']} | "
                  f"LAST_CHECKED: {record['last_checked']}")
        print(f"========= /SHOW TABLE ===========")
        sql_query = "select * from kereta_cepat"
        result = self.db_connect.execute(sql_query)
        records = result.fetchall()
        print(f"========= SHOW TABLE: KERETA_CEPAT ===========")
        for record in records:
            print(f"Record = TICKET_ID: {record['ticket_id']} | "
                  f"TRAIN_DATE: {record['train_date']} | "
                  f"FROM STATION: {record['from_station']} | "
                  f"TO STATION: {record['to_station']} | "
                  f"NOTIF: {record['notification_sent']}")
        print(f"========= /SHOW TABLE ===========")
        result.close()

    def insert_config_table(self):
        sql_query = (f"insert into kereta_cepat_config (config_name, last_checked)\n"
                     f"select 'kereta_cepat', '{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}'\n"
                     f"where not exists (select 1 from kereta_cepat_config where config_name = 'kereta_cepat');")
        self.db_cursor.execute(sql_query)
        self.db_connect.commit()
        print(f"{self.db_cursor.rowcount} config record(s) inserted") if self.db_cursor.rowcount > 0 else None

    def insert_schedule_to_monitor(self, train_date=None, from_station=None, to_station=None):
        sql_query = (f"insert into kereta_cepat (train_date, from_station, to_station)\n"
                     f"select '{train_date}', '{from_station}', '{to_station}'\n"
                     f"where not exists (select 1 from kereta_cepat where train_date = '{train_date}');")
        self.db_cursor.execute(sql_query)
        self.db_connect.commit()
        print(f"{self.db_cursor.rowcount} schedule record(s) inserted") if self.db_cursor.rowcount > 0 else None

    def get_list_unsent_records(self):
        sql_query = "select * from kereta_cepat where notification_sent = 'N' order by ticket_id asc;"
        result = self.db_connect.execute(sql_query)
        records = result.fetchall()
        result.close()
        return records

    def cleanup_old_notification(self):
        sql_query = (f"update kereta_cepat set notification_sent = 'X' where notification_sent = 'N' and train_date < "
                     f"'{datetime.now().strftime('%Y%m%d')}';")
        self.db_cursor.execute(sql_query)
        self.db_connect.commit()
        print(f"{self.db_cursor.rowcount} notification(s) removed") if self.db_cursor.rowcount > 0 else None

    def update_notification(self, train_date=None, from_station=None, to_station=None):
        sql_query = (f"update kereta_cepat set notification_sent = 'Y' where train_date = '{train_date}' and "
                     f"from_station = '{from_station}' and to_station = '{to_station}';")
        self.db_cursor.execute(sql_query)
        self.db_connect.commit()
        print(f"{self.db_cursor.rowcount} notification(s) updated")

    def wrapper_monitor_records(self, train_date=None, from_station_telecode=None, to_station_telecode=None) -> list:
        self.connect_db()
        self.create_config_table()
        self.insert_config_table()
        self.create_table_kereta_cepat()
        self.insert_schedule_to_monitor(train_date=train_date, from_station=from_station_telecode, to_station=to_station_telecode)
        self.cleanup_old_notification()  # Clean up old records
        self.list_unsent_records = self.get_list_unsent_records()
        # self.static_show_table()
        self.disconnect_db()
        return self.list_unsent_records

    def wrapper_update_notification(self, train_date=None, from_station_telecode=None, to_station_telecode=None):
        self.connect_db()
        # self.show_table()
        self.update_notification(train_date=train_date, from_station=from_station_telecode, to_station=to_station_telecode)
        self.disconnect_db()

    def wrapper_show_db(self):
        self.connect_db()
        self.create_config_table()
        self.create_table_kereta_cepat()
        self.static_show_table()
        self.disconnect_db()

    def update_config(self):
        sql_query = (f"update kereta_cepat_config set last_checked = '{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}' "
                     f"where config_name = 'kereta_cepat';")  # '2018-09-05T14:09:03Z'
        self.db_cursor.execute(sql_query)
        self.db_connect.commit()

    def wrapper_update_config(self):
        self.connect_db()
        # self.show_table()
        self.update_config()
        self.disconnect_db()
