#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, bs4, mysql.connector

res = requests.get('https://www.bleague.jp/schedule/?tab=1&year=2018&event=2&club=&setuFrom=1&setuTo=36')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, "html.parser")

game_lists = soup.findAll("ul", {"class":"game_list"})

conn = mysql.connector.connect(
    user='root', password='root',
    host='127.0.0.1',
    database='sports_schedules',
    charset='utf8'
)

cur = conn.cursor()

for game_list in game_lists:
    games = game_list.findAll("div", {"class":"gamedata_left"})

    for game in games:
        print "---------------------------------------------------------"
        print game.find("span", class_="date").string
        print game.find("span", class_="week").string
        print game.find("span", class_="time").string
        home_team = unicode(game.findAll("span", {"class":"team_name"})[0].string)
        visitor_team = unicode(game.findAll("span", {"class":"team_name"})[1].string)
        print game.find("div", class_="arena").text.strip()

        sql = "insert into `bleague` (`home_team`, `visotor_team`) values (%s, %s)"
        val = (home_team, visitor_team)

        cur.execute(sql, val)

conn.commit()
cur.close
conn.close
