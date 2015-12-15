# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from sportingScrapper.items import TeamStat

class TeamStatsSpider(scrapy.Spider):

	name = "team-stats"
	allowed_domains = ['sportinglife.com']
	start_urls = (
        	'http://www.sportinglife.com/football/premier-league/results',
	)

	def __init__(self, name=None, **kwargs):
                super(TeamStatsSpider, self).__init__(name, **kwargs)
                self.items_buffer = {}
                self.base_url = "http://www.sportinglife.com"
                from scrapy.conf import settings
                settings.overrides['DOWNLOAD_TIMEOUT'] = 360


	def parse(self, response):

		self.logger.info('A response from %s just arrived!', response.url)
	
		for url in response.xpath("//section[@class='fr-gp'][1]//a[@class='ixxa']/@href").extract():
			print url
			_url = self.base_url + url.replace("match-commentary","match-stats")
			print _url
			yield Request( url= _url, callback=self.parse_details )


	def parse_details(self, response):
                print "Start scrapping Detailed Info...."
                try:
             
                        team1_stat = TeamStat()
                        team2_stat = TeamStat()

                        teams = response.xpath("//h4[@class='ls-match-team']/text()").extract()
                        
			team1_stat["team"] = teams[0]
			team2_stat["team"] = teams[1]

			urlParts = response.url.split("/")
			matchId = urlParts[6]
			team1_stat["matchId"] = matchId
                        team2_stat["matchId"] = matchId                        

			subDetails = response.xpath("//p[@class='ls-match-detsub']/text()").extract()
			matchDate = subDetails[0]
			team1_stat["matchDate"] = matchDate
                        team2_stat["matchDate"] = matchDate


			team1_stat["goals"] = response.xpath("//div[@id='ls-home-score']/text()").extract()[0]
			team2_stat["goals"] = response.xpath("//div[@id='ls-away-score']/text()").extract()[0]


			extra_stats = response.xpath("//ul[@class='s-con']")

			extra_stats1 = extra_stats[0].xpath(".//li")
			for extra_stat1 in extra_stats1:				
				statLabel = extra_stat1.xpath(".//strong[@class='lab']/text()").extract()[0]
				statValue = extra_stat1.xpath(".//strong[@class='val']/text()").extract()[0]
				self.logger.info('Lab %s value %s', statLabel,statValue)

				if statLabel=="Shots on target":
					team1_stat["shotsOnTarget"] = statValue
                                if statLabel=="Shots off target":
                                        team1_stat["shotsOffTarget"] = statValue
                                if statLabel=="Fouls won":
                                        team1_stat["foulsWon"] = statValue
                                if statLabel=="Fouls conceded":
                                        team1_stat["foulsConceded"] = statValue
                                if statLabel=="Yellow Cards":
                                        team1_stat["yellowCards"] = statValue
                                if statLabel=="Total passes":
                                        team1_stat["passes"] = statValue
                                if statLabel=="Accurate passes":
                                        team1_stat["accuratePasses"] = statValue
                                if statLabel=="Possession %":
                                        team1_stat["possesion"] = statValue
                                if statLabel=="Offside":
                                        team1_stat["offSide"] = statValue
                                if statLabel=="Corners won":
                                        team1_stat["corners"] = statValue


			extra_stats2 = extra_stats[1].xpath(".//li")
                        for extra_stat2 in extra_stats2:
                                statLabel = extra_stat2.xpath(".//strong[@class='lab']/text()").extract()[0]
                                statValue = extra_stat2.xpath(".//strong[@class='val']/text()").extract()[0]
                                self.logger.info('Lab %s value %s', statLabel,statValue)

                                if statLabel=="Shots on target":
                                        team2_stat["shotsOnTarget"] = statValue
                                if statLabel=="Shots off target":
                                        team2_stat["shotsOffTarget"] = statValue
                                if statLabel=="Fouls won":
                                        team2_stat["foulsWon"] = statValue
                                if statLabel=="Fouls conceded":
                                        team2_stat["foulsConceded"] = statValue
                                if statLabel=="Yellow Cards":
                                        team2_stat["yellowCards"] = statValue
                                if statLabel=="Total passes":
                                        team2_stat["passes"] = statValue
                                if statLabel=="Accurate passes":
                                        team2_stat["accuratePasses"] = statValue
                                if statLabel=="Possession %":
                                        team2_stat["possesion"] = statValue
                                if statLabel=="Offside":
                                        team2_stat["offSide"] = statValue
                                if statLabel=="Corners won":
                                        team2_stat["corners"] = statValue
			

			teams_stats = []
			teams_stats.append(team1_stat)
			teams_stats.append(team2_stat)
			
			for stat in teams_stats:
                       		yield stat


                except Exception as e:
                        self.logger.info('Parsing failed for URL %s', response.url)
                        raise
