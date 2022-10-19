from db_init import *
from backup import backup_db

backup_db(db_name)

tables = {
"Categories" : """
    --sql
    CREATE TABLE Categories
    (
        cat_id INTEGER PRIMARY KEY,    --Auto increment
        cat_name VARCHAR(64)
    );
""",

"Series" : """
    --sql
    CREATE TABLE Series
    (
        series_id VARCHAR(5),
        series_name VARCHAR(256),
        book_type VARCHAR(16),
        book_category INTEGER,
        PRIMARY KEY (series_id),
        FOREIGN KEY (book_category) REFERENCES Categories(cat_id),
        CONSTRAINT blank_name CHECK (series_name != ""),
        CONSTRAINT id_format CHECK (series_id REGEXP '^[A-Z0-9]{5}$'),
        CONSTRAINT type_chk CHECK (book_type IN ("bd", "comics", "manga", "roman"))
    );
""",

"Books" : """
    --sql
    CREATE TABLE Books
    (
        book_id VARCHAR(12),
        book_name VARCHAR(256),
        series_id VARCHAR(5),
        vol_nb INTEGER,         -- Volume number
        dup_nb INTEGER,         -- Duplicata number
        available BOOLEAN DEFAULT TRUE,
        condition INTEGER,
        added_on DATE DEFAULT NULL,
        comment VARCHAR(1024),
        PRIMARY KEY (book_id),
        FOREIGN KEY (series_id) REFERENCES Series(series_id),
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

"Users" : """
    --sql
    CREATE TABLE Users
    (
        user_id INTEGER PRIMARY KEY,    --Auto increment
        user_name VARCHAR(256) NOT NULL,
        mail VARCHAR(256),
        tel VARCHAR(12),
        max_loans INTEGER,      -- Maximum number of simultaneous loans
        loan_length INTEGER,    -- Maximum loan duration in days
        bail FLOAT,             -- Caution (€)
        last_loan DATE,         -- Last loan taken or returned
        status_BDM VARCHAR(64),
        status_ALIR VARCHAR(64),
        archived BOOLEAN DEFAULT FALSE,
        comment VARCHAR(1024),
        CONSTRAINT contact CHECK (mail IS NOT NULL OR tel IS NOT NULL)
    );
""",

"Loans" : """
    --sql
    CREATE TABLE Loans
    (
        loan_id INTEGER PRIMARY KEY,    --Auto increment
        user_id INTEGER,
        book_id VARCHAR(12),
        loan_start DATE,
        late_return DATE,       -- Date after which the loan is late
        loan_return DATE DEFAULT NULL,
        archived BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (book_id) REFERENCES Books(book_id),
        CONSTRAINT archiving CHECK (archived = (loan_return IS NOT NULL))
    );
""",

"Authors" : """
    --sql
    CREATE TABLE Authors
    (
        auth_id INTEGER PRIMARY KEY,    --Auto increment
        auth_name VARCHAR(256),
        UNIQUE (auth_name)
    );
""",

"Srs-Auth" : """
    --sql
    CREATE TABLE `Srs-Auth`
    (
        series_id VARCHAR(5),
        auth_id INTEGER,
        PRIMARY KEY (series_id, auth_id),
        FOREIGN KEY (series_id) REFERENCES Series(series_id),
        FOREIGN KEY (auth_id) REFERENCES Authors(auth_id)
    );
""",

"Editors" : """
    --sql
    CREATE TABLE Editors
    (
        edit_id INTEGER PRIMARY KEY,    --Auto increment
        edit_name VARCHAR(256),
        UNIQUE (edit_name)
    );
""",

"Srs-Edit" : """
    --sql
    CREATE TABLE `Srs-Edit`
    (
        series_id VARCHAR(5),
        edit_id INTEGER,
        PRIMARY KEY (series_id, edit_id),
        FOREIGN KEY (series_id) REFERENCES Series(series_id),
        FOREIGN KEY (edit_id) REFERENCES Editors(edit_id)
    );
"""}

for table_name in tables :
    # print("creating table", table_name)
    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
    cursor.execute(tables[table_name])
    # print("table", table_name, "created")
db.commit()

if __name__ == "__main__" :
    db.close()