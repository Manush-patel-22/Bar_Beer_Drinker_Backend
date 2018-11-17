from sqlalchemy import create_engine
from sqlalchemy import sql

from BarBeerDrinker import config

engine = create_engine(config.database_uri)

def get_bars():
    with engine.connect() as con:
        rs = con.execute("SELECT * FROM barbeerdrinker.bars;")
        return [dict(row) for row in rs]

def get_beers():
    with engine.connect() as con:
        rs = con.execute("SELECT * FROM barbeerdrinker.beers;")
        return [dict(row) for row in rs]

def find_bar(name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT * FROM barbeerdrinker.bars WHERE name = :name;"
        )

        rs = con.execute(query, name=name)
        result = rs.first()
        if result is None:
            return None
        return dict(result)

def find_beer(name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT * FROM barbeerdrinker.beers WHERE name = :name;"
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
        result = [dict(row) for row in rs]

        for r in result:
            r['price'] = float(r['price'])
        return result

'''
GIVEN A BEER NAME::
- Below are all Queries that are needed to get all the data
    for the beer page
1) Show bars where this beer sells the most
2) Show Drinkers who are the biggest consumers of this beer
3) Time distribution for when this beer sells the most
'''
# Given a beer - show bars where this beer sells the most (again only top),
def top_bars_for_beer(beer_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT barbeerdrinker.transactions.bar, COUNT(*) as c " \
            "FROM barbeerdrinker.transactions " \
            "WHERE item = :beer_name " \
            "GROUP BY barbeerdrinker.transactions.bar " \
            "ORDER BY c DESC " \
            "LIMIT 10"
        )

        rs = con.execute(query, beer_name=beer_name)
        result = [dict(row) for row in rs]
        return result

# show also drinkers who are the biggest consumers of this beer. 
def top_drinker_for_beer(beer_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT barbeerdrinker.transactions.drinker, COUNT(*) as c " \
            "FROM barbeerdrinker.transactions " \
            "WHERE item = :beer_name " \
            "GROUP BY barbeerdrinker.transactions.drinker " \
            "ORDER BY c DESC " \
            "LIMIT 10"
        )

        rs = con.execute(query, beer_name=beer_name)
        result = [dict(row) for row in rs]

        return result

# As well as time distribution of when this beer sells the most.
def time_distribution_for_beer(beer_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT item, trans_time " \
            "FROM barbeerdrinker.transactions " \
            "WHERE item = :beer_name " \
            "ORDER BY trans_time ASC" \
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

'''
GIVEN A DRINKER NAME::
- Below are all Queries that are needed to get all the data
    for the Drinker page
1) Show his/her transactions ordered by time and grouped by different bars
2) Show Bar Graphs of beers s/he orders the most
3) Show Bar Graphs of his/her spending in different Bars, on different dates/weeks/months.
'''
# Given a drinker, show all his/her transactions ordered by time and grouped by different bars.
def drinker_data(drinker_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT drinker, bar, time FROM barbeerdrinker.transactions " \
            "WHERE drinker = :drinker_name " \
            "GROUP BY drinker " \
            "ORDER BY time"
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


# Also, bar graph of his/her spending in different bars, on different dates/weeks/months.
# NEEDS TO BE IMPLEMENTED------------------------------


'''
GIVEN A BAR NAME::
- Below are all Queries that are needed to get all the data
    for the Bar page
1) Show top drinkers who are the largest spenders
2) Show beers which are the most popular
3) Show Manufacturers who sell the most beers
'''

# Given a Bar, Show Largest Spenders at the bar.
def largest_spenders(bar_name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT DISTINCT drinker, bar, SUM(totalAmount) as total " \
            "FROM barbeerdrinker.transactions " \
            "WHERE bar = :bar_name " \
            "GROUP BY drinker " \
            "ORDER BY total DESC " \
            "LIMIT 10"
        )

        rs = con.execute(query, drinker_name=drinker_name)
        result = [dict(row) for row in rs]
        return result

