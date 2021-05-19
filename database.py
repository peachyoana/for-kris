import sqlite3 

# YYYY-MM-DD@HH-MM : STATS PRIMARY KEY 


def setup_db():
        try: 
                conn = sqlite3.connect("database.db")
                conn.execute("PRAGMA foreign_keys = 1") 
                c = conn.cursor()

                c.execute("""
                CREATE TABLE 
                    User(
                        USER_ID INTEGER PRIMARY KEY, 
                        username text NOT NULL
                        )""")

                c.execute("""
                CREATE TABLE 
                    Texts(
                        TEXT_ID INTEGER PRIMARY KEY,  
                        stored_text text,  
                        text_genre text NOT NULL
                        )""")

                c.execute("""
                CREATE TABLE 
                    Stats(
                        time_of_attempt TEXT PRIMARY_KEY,
                        username TEXT,
                        attempt_time TEXT,
                        wpm real,
                        net_wpm real,
                        chpm real,
                        errors_rate real,
                        score INT, 
                        FOREIGN KEY (username) REFERENCES User (username)
                        )""")

                c.execute("""
                CREATE TABLE 
                    UsedTexts(
                        TEXT_ID INT, 
                        username text,

                        FOREIGN KEY (TEXT_ID) REFERENCES Texts (TEXT_ID),
                        FOREIGN KEY (username) REFERENCES User (username)
                        )""")


                conn.commit()
                conn.close()
        except sqlite3.OperationalError: 
                pass 


def add_one_stats(username, gross_wpm, net_wpm, chpm, error_rate, time_for_attempt, real_time, score):
    """ Take all the user statistics data and add it to the Stats entity in the database """

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    statement = """INSERT INTO Stats values (?, ?, ?, ?, ?, ?, ?, ?)"""

    c.execute(statement, (real_time, username, time_for_attempt, gross_wpm, net_wpm, chpm, error_rate, score))

    items = c.fetchall()
    print("The items inserted are:", items)

    conn.commit()
    conn.close()

def add_texts():
    """ Read a file of texts and genres and add them to the appropriate
        values in the Texts entity of the database """

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    filename = "texts.txt"

    items = []
    data = ()
    with open(filename, "r") as file:
        for line in file.readlines():
            item = line.strip("\n").split("|")
            data = (item[0], item[1])
            items.append(data)

    statement = """
                    INSERT INTO 
                                Texts(stored_text, text_genre) 
                    VALUES 
                                (?, ?)"""

    c.executemany(statement, (items))

    items = c.fetchall()

    conn.commit()
    conn.close()

def get_text(genre):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    statement = """
                SELECT 
                    stored_text 
                FROM 
                    Texts 
                WHERE 
                    text_genre = '{}' 
                ORDER BY
                    RANDOM() 
                LIMIT
                    1
                """
    c.execute(statement.format(genre))


    current_text = c.fetchall()

    print(current_text[0][0])    
    conn.commit()
    conn.close()

    return current_text[0][0]


def add_username(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    statement = """
                INSERT INTO 
                    User (username) 
                VALUES 
                    (?)
                """
    c.execute(statement, (username,))

    print("Username", username, "has been added.")

    conn.commit()
    conn.close()
    



def is_username(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    statement = """
                SELECT 
                    username 
                FROM 
                    User 
                WHERE 
                    username = '{}'
                """
    c.execute(statement.format(username))

    username_result = c.fetchone()

    conn.commit()
    conn.close()
    
    try: 
        if username_result is None: 
            return False 
        else: 
            return True
    except TypeError:
        return False 

def get_all_scores(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    statement = """
                SELECT
                    score
                FROM
                    Stats
                WHERE
                    username = '{}'
                """
    c.execute(statement.format(username))

    scores = c.fetchall() 

    conn.commit()
    conn.close()

    return scores 

def bubble(scores):
    indexing_length = len(scores) - 1
    sorted = False 

    while not sorted: 
        sorted = True
        for i in range(0, indexing_length):
            if scores[i] > scores[i+1]:
                sorted = False 
                scores[i], scores[i+1] = scores[i+1], scores[i]

    sorted_scores = []

    for i in range(len(scores)): 
        sorted_scores.append(scores[i][0])
    
    return sorted_scores 


def get_highest_score(username):
    try: 
        scores = get_all_scores(username)
        sorted_scores = bubble(scores)
        highest_score = sorted_scores.pop()
        return highest_score        
    except IndexError: 
        return " "



def get_latest_time(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    statement =     """ 
                    SELECT
                        time_of_attempt 
                    FROM
                        Stats
                    WHERE
                        username = '{}'
                    ORDER BY
                        time_of_attempt DESC   
                    """
    try: 
        c.execute(statement.format(username))

        result = c.fetchone() 
        print(result[0])

        conn.commit()
        conn.close()
        return result[0]
    except TypeError: 
        return " "

setup_db()
