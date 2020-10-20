import datetime 
import sqlite3
import pandas as pd


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn

def select_all_timer(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM times")

    #rows = cur.fetchall()

    #for row in rows:
        #print(row)

def begin(start, end):
    """get user to write start when they start work"""
    ans = input('Do you want to start or end your session? s/e: ')
    if ans == "s":
        start = datetime.datetime.now()
        print(start)
        ans = input("press e to end session: ")
    elif ans == "e":
        end = datetime.datetime.now()
        print(end)
        return start, end

def month_wage():
    next = input("Would you like to print monthly round up? y/n: ")
    if next == "y":
        print(pd.read_sql_query("SELECT * FROM times WHERE month = :month",  conn, params = dict(month=start.strftime("%B"))))

    else:
        return
        


if __name__ == '__main__':

    conn = create_connection(r"/Users/ceriseabelthompson/documents/code/timer/times.db")
    select_all_timer(conn)

    #initialise start and end
    start = datetime.datetime.now()
    end = datetime.datetime.now()

    #start recording time and end recording
    begin(start, end)
    

    # get values
    #month = (start.strftime("%B"))
    #year = (start.strftime("%Y"))
    #day = (start.strftime("%d"))
    #start_t = (start.strftime("%H:%M"))
    #end_t = (end.strftime("%H:%M"))

    #get cost and hours values
    hours_total = start - end
    seconds = (24*3600) - hours_total.seconds
    hours = (seconds/60)/60
    minutes = seconds%60
    cost = round((hours*15), 2)
    print (cost)
    
    #put into table
    #cur = conn.cursor()
    conn.execute("INSERT INTO times VALUES (:year, :month, :day, :start_t, :end_t, :hours, :minutes, :cost)",\
    dict(year=start.strftime("%Y"), month = start.strftime("%B"), day = start.strftime("%d"), start_t = start.strftime("%H:%M"),\
    end_t = end.strftime("%H:%M"), hours = hours, minutes = minutes, cost = cost))
    conn.commit()
    #cur.close()
    #ask for month's wages
    month_wage()

    conn.close()



