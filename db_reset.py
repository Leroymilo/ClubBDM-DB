from backup import backup_db
from sqlite3 import *

def reset(db: Connection, db_name: str, cursor: Cursor) :

    backup_db(db_name)
    print("database backed-up")

    cursor.execute("PRAGMA foreign_keys = ON;")

    table_names = ["Categories", "Series", "Books", "Members", "Loans", "Authors", "Editors", "Srs-Auth", "Srs-Edit"]

    tables = {
    "Categories" : """--sql
        CREATE TABLE Categories
        (
            cat_id INTEGER PRIMARY KEY,    --Auto increment
            cat_name VARCHAR(64) UNIQUE NOT NULL
        );
    """,

    "Series" : """--sql
        CREATE TABLE Series
        (
            series_id VARCHAR(5) PRIMARY KEY,
            series_name VARCHAR(256) NOT NULL,
            book_type VARCHAR(16),
            book_category INTEGER NOT NULL,
            FOREIGN KEY (book_category) REFERENCES Categories(cat_id)
                ON DELETE RESTRICT ON UPDATE RESTRICT,
            CONSTRAINT blank_name CHECK (series_name != ""),
            CONSTRAINT id_format CHECK (series_id REGEXP '^[A-Z0-9]{5}$'),
            CONSTRAINT type_chk CHECK (book_type IN ("bd", "comics", "manga", "roman"))
        );
    """,

    "Books" : """--sql
        CREATE TABLE Books
        (
            book_id VARCHAR(12) PRIMARY KEY,
            book_name VARCHAR(256),
            series_id VARCHAR(5) NOT NULL,
            vol_nb INTEGER NOT NULL,        -- Volume number
            dup_nb INTEGER NOT NULL,        -- Duplicata number
            available BOOLEAN DEFAULT TRUE,
            condition INTEGER,
            added_on DATE DEFAULT NULL,
            comment VARCHAR(1024),
            FOREIGN KEY (series_id) REFERENCES Series(series_id)
                ON DELETE RESTRICT ON UPDATE RESTRICT,
            CONSTRAINT book_unicity UNIQUE (series_id, vol_nb, dup_nb),
            CONSTRAINT id_format CHECK
            (
                book_id REGEXP '^[0-9]{2}[A-Z0-9]{5}[0-9]{5}$'
                AND SUBSTRING(book_id, 3, 5) = series_id
                AND SUBSTRING(book_id, 8, 3) = LPAD(vol_nb, '0', 3)
                AND SUBSTRING(book_id, 11, 2) = LPAD(dup_nb, '0', 2)
            ),
            CONSTRAINT condition_rating CHECK (condition BETWEEN 1 AND 10),
            CONSTRAINT volume_number CHECK (vol_nb > 0)
        );
    """,

    "Members" : """--sql
        CREATE TABLE Members
        (
            member_id INTEGER PRIMARY KEY,    --Auto increment
            member_name VARCHAR(256) UNIQUE NOT NULL,
            mail VARCHAR(256),
            tel VARCHAR(12),
            max_loans INTEGER NOT NULL,     -- Maximum number of simultaneous loans
            loan_length INTEGER,            -- Maximum loan duration in days
            bail FLOAT DEFAULT 0,           -- Caution (€)
            last_loan DATE DEFAULT NULL,    -- Last loan taken or returned
            status_BDM VARCHAR(64),
            status_ALIR VARCHAR(64),
            archived BOOLEAN DEFAULT FALSE,
            comment VARCHAR(1024),
            CONSTRAINT contact CHECK (mail IS NOT NULL OR tel IS NOT NULL)
        );
    """,

    "Loans" : """--sql
        CREATE TABLE Loans
        (
            loan_id INTEGER PRIMARY KEY,    --Auto increment
            member_id INTEGER NOT NULL,
            book_id VARCHAR(12) NOT NULL,
            loan_start DATE NOT NULL,
            late_return DATE DEFAULT NULL,       -- Date after which the loan is late
            loan_return DATE DEFAULT NULL,
            archived BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (member_id) REFERENCES Members(member_id)
                ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (book_id) REFERENCES Books(book_id)
                ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT archiving CHECK (archived = (loan_return IS NOT NULL)),
            CONSTRAINT unique_val UNIQUE (member_id, book_id, loan_start)
        );
    """,

    "Authors" : """--sql
        CREATE TABLE Authors
        (
            auth_id INTEGER PRIMARY KEY,    --Auto increment
            auth_name VARCHAR(256) UNIQUE
        );
    """,

    "Srs-Auth" : """--sql
        CREATE TABLE `Srs-Auth`
        (
            series_id VARCHAR(5) NOT NULL,
            auth_id INTEGER NOT NULL,
            PRIMARY KEY (series_id, auth_id),
            FOREIGN KEY (series_id) REFERENCES Series(series_id)
                ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (auth_id) REFERENCES Authors(auth_id)
                ON DELETE RESTRICT ON UPDATE CASCADE
        );
    """,

    "Editors" : """--sql
        CREATE TABLE Editors
        (
            edit_id INTEGER PRIMARY KEY,    --Auto increment
            edit_name VARCHAR(256) UNIQUE
        );
    """,

    "Srs-Edit" : """--sql
        CREATE TABLE `Srs-Edit`
        (
            series_id VARCHAR(5) NOT NULL,
            edit_id INTEGER NOT NULL,
            PRIMARY KEY (series_id, edit_id),
            FOREIGN KEY (series_id) REFERENCES Series(series_id)
                ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (edit_id) REFERENCES Editors(edit_id)
                ON DELETE RESTRICT ON UPDATE CASCADE
        );
    """}



    for table_name in table_names[::-1] :
        cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
    print("database cleaned")
    for table_name in table_names :
        cursor.execute(tables[table_name])
    print("database set")
    db.commit()

if __name__ == "__main__" :
    from db_init import *
    reset(db, db_name, cursor)
    db.close()