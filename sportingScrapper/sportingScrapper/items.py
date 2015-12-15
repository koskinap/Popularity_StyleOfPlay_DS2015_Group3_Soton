# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeamStat(scrapy.Item):
	# define the fields for your item here like:
	team = scrapy.Field()
	matchId = scrapy.Field()	
	matchDate = scrapy.Field()
	goals = scrapy.Field()
	shotsOnTarget = scrapy.Field()
	shotsOffTarget = scrapy.Field()
	foulsWon = scrapy.Field()
	foulsConceded = scrapy.Field()
	yellowCards = scrapy.Field()
	passes = scrapy.Field()
	accuratePasses = scrapy.Field()
	possesion = scrapy.Field()
	offSide = scrapy.Field()
	corners = scrapy.Field()

	pass
