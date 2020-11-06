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


def begin():
    """get user to write start when they start work"""
    ans = input('Do you want to start or end your session? s/e: ')
    if ans == "s":
        start = datetime.datetime.now()
        print(start)
        ans_b = input("press e to end session: ")
        if ans_b == "e":
            end = datetime.datetime.now()
            print(end)
            return start, end
        else:
            return None, None

def month_wage():
    next = input("Would you like to print monthly round up? y/n: ")
    if next == "y":
        which_month = input("Would you like to see this month's wages? y/n: ")
        if which_month == "y":
            print(pd.read_sql_query("SELECT * FROM times WHERE month = :month ORDER BY day",  conn, params = dict(month=today.strftime("%B"))))
            print("Total:")
            print(pd.read_sql_query("SELECT SUM(cost)  FROM times WHERE month = :month ORDER BY day",  conn, params = dict(month=today.strftime("%B"))))
        elif which_month == "n":
            which_month = input("Please the month you wish to see: ")
            print(pd.read_sql_query("SELECT * FROM times WHERE month = :month ORDER BY day",  conn, params = (which_month,)))
            print("Total:")
            print(pd.read_sql_query("SELECT SUM(cost)  FROM times WHERE month = :month ORDER BY day",  conn, params = (which_month,)))
        else: 
            print("please try again")
            month_wage()
    else:
        return

def create_cost():
    #get cost and hours values
    hours_total = end - start
    minutes = hours_total.seconds//60
    hours = (minutes)//60
    cost_time = (5 * (round(minutes/5))/60)
    cost = round((cost_time*15), 2)
    print("In this session you worked for {} hours and {} minutes, earning £{}".format(hours, (minutes%60), cost))
   
    #put into table
    conn.execute("INSERT INTO times VALUES (:year, :month, :day, :start_t, :end_t, :hours, :minutes, :cost)",\
    dict(year=start.strftime("%Y"), month = start.strftime("%B"), day = start.strftime("%d"), start_t = start.strftime("%H:%M"),\
    end_t = end.strftime("%H:%M"), hours = hours, minutes = minutes, cost = cost))
    conn.commit()

    return (hours, minutes, cost)

    
def opener():
    q = input("Would you like to start timer or see monthly invoice? press t / i to continue: ")
    if q == 't':
        #start recording time and end recording
        start, end = begin()
        hours, minutes, cost = create_cost()
    elif q == 'i':
        #ask for month's wages
        month_wage()
    else:
        print("please try again")
        opener()

    



if __name__ == '__main__':

    conn = create_connection(r"/Users/ceriseabelthompson/documents/code/timer/times.db")
    select_all_timer(conn)
    today = datetime.datetime.now()

    q = input("Would you like to start timer or see monthly invoice? press t / i to continue: ")
    if q == 't':
        #start recording time and end recording
        start, end = begin()
        hours, minutes, cost = create_cost()
    elif q == 'i':
        #ask for month's wages
        month_wage()
    

    conn.close()



