from sqlalchemy import create_engine
from sqlalchemy import sql

from BarBeerDrinker import config

engine = create_engine(config.database_uri)

def get_bars():
    with engine.connect() as con:
        rs = con.execute("SELECT * FROM bars;")
        return [dict(row) for row in rs]

def get_drinkers():
    with engine.connect() as con:
        rs = con.execute("SELECT * FROM barbeerdrinker.drinkerList;")
        return [dict(row) for row in rs]


def find_bar(name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT * FROM bars WHERE name = :name;"
        )

        rs = con.execute(query, name=name)
        result = rs.first()
        if result is None:
            return None
        return dict(result)

def filter_beers(max_price):
    with engine.connect() as con:
        query = sql.text(
            "SELECT * FROM sells WHERE price < :max_price;"
        )

        rs = con.execute(query, max_price=max_price)
        results = [dict(row) for row in rs]

        for r in results:
            r['price'] = float(r['price'])
        return results

'''
GIVEN A DRINKER NAME::
- Below are all Queries that are needed to get all the data
    for the Drinker page
1) Show his/her transactions ordered by time and grouped by different bars
2) Show Bar Graphs of beers s/he orders the most
3) Show Bar Graohs of his/her spending in different Bars, on different dates/weeks/months.
'''
# Given a drinker, show all his/her transactions ordered by time and grouped by different bars.
def drinker_data(drinker_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT ID, bar, totalAmount, trans_time, trans_date " \
            "FROM barbeerdrinker.transactions " \
            "WHERE drinker = :drinker_name " \
            "GROUP BY ID "
        )

        rs = con.execute(query, drinker_name=drinker_name)
        result = [dict(row) for row in rs]
        return result

# Show bar graphs of beers s/he orders the most.
# NEEDS TO BE IMPLEMENTED------------------------------
def top_beers_for_drinker(drinker_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT barbeerdrinker.transactions.item, COUNT(*) as c " \
            "FROM barbeerdrinker.transactions " \
            "WHERE drinker = :drinker_name AND EXISTS(SELECT name FROM barbeerdrinker.beers WHERE name = item) " \
            "GROUP BY barbeerdrinker.transactions.item " \
            "ORDER BY c DESC LIMIT 10"
        )

        rs = con.execute(query, drinker_name=drinker_name)
        result = [dict(row) for row in rs]
        return result

def drinker_distribution_week(drinker_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT count(week(trans_date)) BillsInWeek, week(trans_date) WeekNumberInYear, CONCAT(DATE_FORMAT(DATE_ADD(trans_date, INTERVAL(1-DAYOFWEEK(trans_date)) DAY),'%Y-%m-%e'), ' TO ', DATE_FORMAT(DATE_ADD(trans_date, INTERVAL(7-DAYOFWEEK(trans_date)) DAY),'%Y-%m-%e')) AS WeekDateRange "\
            "from barbeerdrinker.transactions " \
            "WHERE drinker = :drinker_name "\
            "group by WeekNumberInYear "\
            "order by BillsInWeek DESC "
        )
        
        rs = con.execute(query, drinker_name=drinker_name)
        result = [dict(row) for row in rs]
        return result

#3) Show Bar Graphs of his/her spending in different Bars, on different dates/weeks/months.
def spending_different_dates(drinker_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT trans_date, COUNT(totalAmount) as c " \
            "FROM barbeerdrinker.transactions " \
            "WHERE drinker = :drinker_name " \
            "GROUP BY ID "\
            "ORDER BY c DESC "\
            "LIMIT 10 "
        )

        rs = con.execute(query, drinker_name = drinker_name)
        result = [dict(row) for row in rs]
        return result

#BAR Page
# 1) for  top drinkers who are largest spenders, 
# 2) for beers which are most popular and 
# 3) for manufacturers who sell the most beers.
def popular_beer(bar_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT item, COUNT(*) as c " \
            "FROM barbeerdrinker.transactions " \
            "WHERE bar = :bar_name " \
            "GROUP BY barbeerdrinker.transactions.item " \
            "ORDER BY c DESC " \
            "LIMIT 10"
        )

        rs = con.execute(query, bar_name=bar_name)
        result = [dict(row) for row in rs]
        return result

def largest_spenders(bar_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT DISTINCT drinker, bar, SUM(totalAmount) as total " \
            "FROM barbeerdrinker.transactions " \
            "WHERE bar = :bar_name " \
            "GROUP BY drinker " \
            "ORDER BY total DESC " \
            "LIMIT 10 "
        )

        rs = con.execute(query, bar_name=bar_name)
        result = [dict(row) for row in rs]
        return result

def manf_most_beer(bar_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT topBeers.item, manf, topBeers.c " \
            "FROM barbeerdrinker.beers, (SELECT item, COUNT(*) as c FROM barbeerdrinker.transactions WHERE bar = :bar_name AND EXISTS(SELECT name FROM barbeerdrinker.beers WHERE item = name) GROUP BY barbeerdrinker.transactions.item ORDER BY c DESC LIMIT 10) as topBeers " \
            "WHERE name=topBeers.item " \
            "ORDER BY topBeers.c DESC"
        )

        rs = con.execute(query, bar_name=bar_name)
        result = [dict(row) for row in rs]
        return result


#Demonstrate time distribution of sales, show what are the busiest periods of the day and of the week. 
def time_distribution_for_bar_spending(beer_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT DISTINCT ID, trans_time " \
            "FROM barbeerdrinker.transactions " \
            "WHERE bar = :beer_name "\
            "ORDER BY trans_time ASC "
            )
            
        rs = con.execute(query, beer_name=beer_name)
        result = [dict(row) for row in rs]
        times = [li['trans_time'] for li in result]

        timeList = [{'time': '1:00 - 2:00', 'count': 0},
        {'time': '2:00 - 3:00', 'count': 0},
        {'time': '11:00 - 12:00', 'count': 0},
        {'time': '10:00 - 11:00', 'count': 0},
        {'time': '9:00 - 10:00', 'count': 0},
        {'time': '8:00 - 9:00', 'count': 0},
        {'time': '7:00 - 8:00', 'count': 0}]
        for time in times:
            if time >= '1:00' and time <= '2:00':
                for dic in timeList:
                    if dic['time'] == '1:00 - 2:00':
                        dic['count'] += 1
            elif time >= '2:00' and time <= '3:00':
                for dic in timeList:
                    if dic['time'] == '2:00 - 3:00':
                        dic['count'] += 1
            elif time >= '11:00' and time <= '12:00':
                for dic in timeList:
                    if dic['time'] == '11:00 - 12:00':
                        dic['count'] += 1
            elif time >= '10:00' and time <= '11:00':
                for dic in timeList:
                    if dic['time'] == '10:00 - 11:00':
                        dic['count'] += 1
            elif time >= '9:00' and time <= '10:00':
                for dic in timeList:
                    if dic['time'] == '9:00 - 10:00':
                        dic['count'] += 1
            elif time >= '8:00' and time <= '9:00':
                for dic in timeList:
                    if dic['time'] == '8:00 - 9:00':
                        dic['count'] += 1
            elif time >= '7:00' and time <= '8:00':
                for dic in timeList:
                    if dic['time'] == '7:00 - 8:00':
                        dic['count'] += 1

        print(timeList)

        return timeList

def distribution_by_week(bar_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT count(week(trans_date)) BillsInWeek, week(trans_date) WeekNumberInYear, CONCAT(DATE_FORMAT(DATE_ADD(trans_date, INTERVAL(1-DAYOFWEEK(trans_date)) DAY),'%Y-%m-%e'), ' TO ', DATE_FORMAT(DATE_ADD(trans_date, INTERVAL(7-DAYOFWEEK(trans_date)) DAY),'%Y-%m-%e')) AS WeekDateRange " \
            "from barbeerdrinker.transactions " \
            "WHERE bar = :bar_name " \
            "group by WeekNumberInYear " \
            "order by BillsInWeek DESC;"
        )

        rs = con.execute(query, bar_name=bar_name)
        result = [dict(row) for row in rs]
        return result

def post_bar_db(newbar_name, newbar_license, newbar_phone, newbar_city, newbar_addr,newbar_OpenTime, newbar_CloseTime):
    with engine.connect() as con:
        query = sql.text(
           "INSERT INTO bars (name, license, phone, city, addr, OpenTime, CloseTime) VALUES (:newbar_name, :newbar_license, :newbar_phone, :newbar_city, :newbar_addr, :newbar_OpenTime, :newbar_CloseTime)"
            #"INSERT INTO bars (name, license, phone, city, adrr, OpenTime, CloseTime) VALUES (%s, %s, %s, %s, %s, %s, %s)", (requestData["name"],requestData["license"],requestData["phone"],requestData["city"],requestData["addr"],requestData["OpenTime"],requestData["CloseTime"])
        )

        con.execute(query, newbar_name=newbar_name, newbar_license=newbar_license, newbar_phone=newbar_phone, newbar_city=newbar_city, newbar_addr=newbar_addr, newbar_OpenTime=newbar_OpenTime, newbar_CloseTime=newbar_CloseTime)
        return

def delete_bar_db(bar_name):
    with engine.connect() as con:
        query = sql.text(
            "DELETE FROM bars WHERE name = :bar_name"
        )

        con.execute(query, bar_name=bar_name)