from shutil import copyfile
from datetime import datetime, timedelta
import os

folder = "backups\\"

def backup_db(db_name: str, backup_name: str = None) :
    return
    if backup_name is None :
        suffix_start = db_name.find("_backup")
        str_date = datetime.today().strftime("%Y%m%d")
        if suffix_start == -1 :
            backup_name = db_name + "_backup_" + str_date
        else :
            backup_name = db_name[:suffix_start] + "_backup_" + str_date
    copyfile(db_name + ".sql", folder + backup_name + ".sql")
    
    delete_date = datetime.today() - timedelta(days=7)
    for file_name in os.listdir(folder) :
        direct = folder + file_name
        date_bkp = datetime.fromtimestamp(os.stat(direct).st_mtime)
        if "_backup" in file_name and \
                date_bkp < delete_date :
            os.remove(direct)

if __name__ == "__main__" :
    backup_db("temp")