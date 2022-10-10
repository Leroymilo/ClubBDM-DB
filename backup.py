from shutil import copyfile
from datetime import date

def backup_db(db_name: str, backup_name: str = None) :
    if backup_name is None :
        suffix_start = db_name.find("_backup")
        str_date = date.today().strftime("%d-%m-%Y")
        if suffix_start == -1 :
            backup_name = db_name + "_backup_" + str_date
        else :
            backup_name = db_name[:suffix_start] + "_backup_" + str_date
    copyfile(db_name + ".sql", "backups\\" + backup_name + ".sql")

if __name__ == "__main__" :
    backup_db("temp")