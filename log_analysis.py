#!/usr/bin/env python3
import psycopg2
import sys


# DB Connection functions
def connect():
    connection = psycopg2.connect("dbname=news")
    return connection, connection.cursor()


def disconnect(conn):
    conn.close()


def go_to_main_menu():
    u_input = raw_input("Press 'Enter key' to go back to main menu :")
    if u_input:
        return


# Functions for each input option
def op1_articles():
    conn, cur = connect()
    cur.execute("""
        select articles.title, count (*) as views
        from  articles,log
        where log.path = ('/article/' || articles.slug)
            and log.status = '200 OK'
        group by articles.title order by views desc limit 3;
    """)
    articles = cur.fetchall()
    for article in articles:
        print(article[0] + " ---- " + str(article[1]) + " views")
    disconnect(conn)
    go_to_main_menu()


def op2_authors():
    conn, cur = connect()
    cur.execute("""
        select authors.name, count (*) as views
        from  articles,log,authors
        where  log.path = ('/article/' || articles.slug)
            and articles.author=authors.id
            and log.status = '200 OK'
        group by authors.name
        order by views desc;
    """)
    authors = cur.fetchall()
    for author in authors:
        print(author[0] + " ---- " + str(author[1]) + " views")
    disconnect(conn)
    go_to_main_menu()


def op3_error_percent():
    conn, cur = connect()
    cur.execute("""
        select error.date,
            round((error.num :: numeric) * 100 / total_request.num,2)
        as error_percent
        from (select * from error) as error,
            (select * from total_request) as total_request
        where error.date = total_request.date
            and (error.num :: float / total_request.num) > 0.01
            order by error_percent;
    """)
    reports = cur.fetchall()
    for report in reports:
        print(report[0].strftime("%m-%d-%Y") + " ---- " + str(report[1]) + "%")
    disconnect(conn)
    go_to_main_menu()


if __name__ == '__main__':
    while 1:
        print("Log Analysis: ")
        print(""" Choose an option to pull a report.
            1. What are the most popular three articles of all time?
            2. Who are the most popular article authors of all time?
            3. On which days did more than 1% of requests lead to errors?
            4. Exit """)
        option = raw_input('Enter your option: ')
        try:
            option = int(option)
            if 5 > option > 0:
                if option == 1:
                    op1_articles()
                elif option == 2:
                    op2_authors()
                elif option == 3:
                    op3_error_percent()
                elif option == 4:
                    print("Exiting program ...")
                    break
            else:
                print("Invalid option")
        except:
            print("Invalid option")
    sys.exit()
