import time

from keretacepat.class_book_schedule import BookSchedule
from keretacepat.class_bot_line import BotLine
from keretacepat.class_db_tools import DBTools
from keretacepat.class_kereta_cepat import KeretaCepat
from keretacepat.class_utility import GeneralUtility

book_date = None
list_db_records = None

if __name__ == "__main__":
    GeneralUtility.static_write_logs(f"Process started")

    # READ CONFIGURATION FILES TO EXTRACT THE INPUT VARIABLES """
    input_dict_ini = GeneralUtility.static_read_ini_file()
    # CREATE NEW BOOKING OBJECT BASED ON THE INPUT DATE """
    book = BookSchedule(days_diff=int(input_dict_ini['input_next_days']), list_inc_days=input_dict_ini['input_list_inc_days'])
    # ADD A DATE - VALIDATE BASED ON INCLUSION OF ONLY SATURDAY AND SUNDAY """
    book_date = book.add_date()
    GeneralUtility.static_write_logs(f"Book date: {book_date}")
    # CREATE NEW OBJECT TO ADD THE DATE INTO DATABASE FOR MONITORING """
    db_kereta = DBTools()
    # IF DATE IS AVAILABLE, THEN """
    if book_date:
        # ADD THE DATE INTO MONITORING DATABASE, AND PULL ANY RECORDS THAT HASN'T GOT NOTIIFCATION SENT """
        list_db_record = db_kereta.wrapper_monitor_records(train_date=book_date, from_station_telecode=str(input_dict_ini['from_station']), to_station_telecode=str(input_dict_ini['to_station']))
        for db_record in list_db_record:
            GeneralUtility.static_write_logs(f"Monitored date {db_record['train_date']}")
            # IF TODAY IS THE NOTIFICATION CHECKING DAYS (SATURDAY, SUNDAY, MONDAY) """
            if GeneralUtility.static_get_day_today() in input_dict_ini['days_to_check']:
                GeneralUtility.static_write_logs(f"Today is a checking day ...")
                # SEND THE LOOP DATE ACROSS TO KERETA CEPAT WEBSITE TO CHECK IF SCHEDULE IS AVAILABLE """
                kereta = KeretaCepat(train_date=db_record['train_date'], from_station_telecode=db_record['from_station'], to_station_telecode=db_record['to_station'])
                if kereta.is_available():
                    GeneralUtility.static_write_logs(f"Train schedule {book_date} is available")
                    chat_message = GeneralUtility.static_kereta_cepat_chat(train_date=db_record['train_date'], from_station_telecode=db_record['from_station'], to_station_telecode=db_record['to_station'])
                    # IF SCHEDULE IS AVAILABLE - SEND IT TO THE BOT FOR NOTIFICATION """
                    bot = BotLine(test_mode=str(input_dict_ini['test_bot']))
                    GeneralUtility.static_write_logs(f"Bot response = {bot.send_to_chat(chat=chat_message)}")
                    # ONCE SENT,  UPDATE THE DATABASE TO TICK THE RECORD """
                    db_kereta.wrapper_update_notification(train_date=db_record['train_date'], from_station_telecode=db_record['from_station'], to_station_telecode=db_record['to_station'])
                else:
                    GeneralUtility.static_write_logs(f"Train schedule {book_date} is NOT available")
            else:
                GeneralUtility.static_write_logs(f"Today is NOT a checking day ...")
            time.sleep(int(input_dict_ini['sleep_seconds']))  # Delay 30 secs to avoid banning
        else:
            GeneralUtility.static_write_logs(f"Nothing to check with whoosh")
    else:
        GeneralUtility.static_write_logs(f"No date {book_date} to add")
    # Update last checked datetime in config table
    db_kereta.wrapper_update_config()
    GeneralUtility.static_write_logs(f"============= Process completed =============")
