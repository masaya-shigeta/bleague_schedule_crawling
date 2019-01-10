#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, bs4, mysql.connector, datetime

res = requests.get('https://www.bleague.jp/schedule/?tab=1&year=2018&event=2&club=&setuFrom=1&setuTo=36')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, "html.parser")

game_lists = soup.findAll("ul", {"class":"game_list"})

conn = mysql.connector.connect(
    user='root',
    password='root',
    host='127.0.0.1',
    database='sports_schedules',
    charset='utf8',
)

cur = conn.cursor()

for game_list in game_lists:
    games = game_list.findAll("div", {"class":"gamedata_left"})

    for game in games:
        month = int(game.find("span", class_="date").string.split('.', 1)[0])
        day = int(game.find("span", class_="date").string.split('.', 1)[1])
        hour = int(game.find("span", class_="time").string.split(' ', 1)[0].split(':', 1)[0])
        minute = int(game.find("span", class_="time").string.split(' ', 1)[0].split(':', 1)[1])

        if month <= 4:
            year = 2019
        else:
            year = 2018

        league_type = 1
        game_date = datetime.datetime(year, month, day, hour, minute)
        home_team = game.findAll("span", {"class":"team_name"})[0].string.decode('utf-8')
        visitor_team = game.findAll("span", {"class":"team_name"})[1].string.decode('utf-8')
        place =  game.find("div", class_="arena").text.strip().decode('utf-8')

        sql = "insert into `bleague` (`league_type`, `game_date`, `place`, `home_team`, `visotor_team`) values (%s, %s, %s, %s, %s)"
        val = (league_type, game_date, place, home_team, visitor_team)

        cur.execute(sql, val)

conn.commit()
cur.close
conn.close
