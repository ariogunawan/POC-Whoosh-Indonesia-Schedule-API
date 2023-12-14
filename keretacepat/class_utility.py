import configparser
import os
from datetime import datetime


class GeneralUtility:
    @staticmethod
    def static_get_date_today() -> str:
        return datetime.now().strftime("%Y%m%d")

    @staticmethod
    def static_get_datetime_today() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    @staticmethod
    def static_get_day_today() -> str:
        return datetime.now().strftime("%A")

    @staticmethod
    def static_date_add_dash(str_date=None) -> str:
        date_date = datetime.strptime(str_date, "%Y%m%d")
        str_date = date_date.strftime("%Y-%m-%d")
        return str_date

    @staticmethod
    def static_kereta_cepat_chat(train_date=None, from_station_telecode=None, to_station_telecode=None) -> str:
        url = (f"https://ticket.kcic.co.id/webTrade/#/home/ticketList?from={from_station_telecode}&to={to_station_telecode}"
               f"&trainDate={GeneralUtility.static_date_add_dash(str(train_date))}"
               f"&returnTrainDate={GeneralUtility.static_date_add_dash(str(train_date))}&tripUp=one")
        chat_message = f"\N{Robot Face} Robotnya Ario v2 \N{Robot Face}\n"
        chat_message += (f"\N{Steam Locomotive} Tiket kereta cepat (whoosh) tanggal "
                         f"{GeneralUtility.static_date_add_dash(str(train_date))} udah ada!\n\n")
        chat_message += url
        return chat_message

    @staticmethod
    def static_read_ini_file() -> dict:
        dict_ini_file = {}
        dir_name = os.path.dirname(os.path.abspath(__file__))
        ini_name = "kereta-cepat.ini"
        ini_file_path = f"{dir_name}/ini/{ini_name}"
        config_object = configparser.ConfigParser()
        with open(ini_file_path, "r") as file_object:
            config_object.read_file(file_object)
            for each_section in config_object.sections():
                for (each_key, each_val) in config_object.items(each_section):
                    dict_ini_file[each_key] = each_val
            return dict_ini_file

    @staticmethod
    def static_write_logs(log_message=None):
        dir_name = os.path.dirname(os.path.abspath(__file__))
        log_name = f"kereta-cepat-{GeneralUtility.static_get_date_today()}.log"
        log_file_path = f"{dir_name}/logs/{log_name}"
        log_messages = f"[{GeneralUtility.static_get_datetime_today()}] "
        log_messages += f"{log_message}"
        with open(log_file_path, "a") as file_object:
            file_object.write(log_messages)
            file_object.write("\n")
