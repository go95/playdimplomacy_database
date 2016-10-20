# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.http import Request, FormRequest
from diplomacy.items import Game, Order
from abc import ABCMeta, abstractmethod

import scrapy
import csv
import re
import time


class LoginSpider(Spider):
    """Inherit this class to login and implement parse_after_login"""

    __metaclass__ = ABCMeta
    name = 'login'
    start_urls = ['http://www.playdiplomacy.com/']

    def parse(self, response):
        if "You need to fill in orders" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            return self.parse_after_login(response)
        else:
            return [FormRequest.from_response(response,
                        formdata={'username': 'user', 'password': 'password'},
                        callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "You need to fill in orders" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            return self.parse_after_login(response)
        else:
            self.log("Login failed", level=log.ERROR)

    @abstractmethod
    def parse_after_login(self, response):
        raise NotImplementedError("Must override parse_after_login")


class GamesSpider(LoginSpider):
    """Scraps all the games from the search results in the search_urls list"""

    name = "scrap_games"
    search_urls = [
        ("rand", r"http://www.playdiplomacy.com/games.php?subpage=all_finished&game_title=&game_id=&with_usr=&with_usr_2=&stats-rank=1&stats-norank=1&type-regular=1&type-anonymous_countries=1&type-anonymous_players=1&type-gunboat=2&type-gunboat_shoutbox=3&variant-0=1&variant-1=1&variant-2=1&map_variant-0=1&map_variant-1=1&map_variant-2=1&map_variant-3=1&map_variant-4=1&countries-rand=1&draws-open=1&speed=&ambassador=no&grace=&NMR_protect=&shorthanded=no&fog=no&stuff_happens=no"),
        ("pref", r"http://www.playdiplomacy.com/games.php?subpage=all_finished&game_title=&game_id=&with_usr=&with_usr_2=&stats-rank=1&stats-norank=1&type-regular=1&type-anonymous_countries=1&type-anonymous_players=1&type-gunboat=2&type-gunboat_shoutbox=3&variant-0=1&variant-1=1&variant-2=1&map_variant-0=1&map_variant-1=1&map_variant-2=1&map_variant-3=1&map_variant-4=1&countries-pref=1&draws-open=1&speed=&ambassador=no&grace=&NMR_protect=&shorthanded=no&fog=no&stuff_happens=no"),
        ("self", r"http://www.playdiplomacy.com/games.php?subpage=all_finished&game_title=&game_id=&with_usr=&with_usr_2=&stats-rank=1&stats-norank=1&type-regular=1&type-anonymous_countries=1&type-anonymous_players=1&type-gunboat=2&type-gunboat_shoutbox=3&variant-0=1&variant-1=1&variant-2=1&map_variant-0=1&map_variant-1=1&map_variant-2=1&map_variant-3=1&map_variant-4=1&countries-sel=1&draws-open=1&speed=&ambassador=no&grace=&NMR_protect=&shorthanded=no&fog=no&stuff_happens=no")
    ]

    def parse_after_login(self, response):
        for country_choice, url in self.search_urls:
            meta = {"country_choice" : country_choice}
            yield Request(url, callback=self.parse_search_results, meta=meta)


    def parse_search_results(self, response):
        url = response.url
        npages_xpath = r'//*[@id="wrap"]/div[4]/text()'

        sel = Selector(response)
        npages_raw = sel.xpath(npages_xpath).extract()[0]
        m = re.findall(r'[0-9]+', npages_raw)
        npages = int(m[1])

        for i in xrange(npages+1):
            yield Request("".join([url, "&current_page=", str(i)]), callback=self.parse_search_page, meta=response.meta)

    def parse_search_page(self, response):
        games_table_xpath = r'//*[@id="games_list"]/tr'
        map_variant_xpath = r'td/table/tr/td[2]/ul[1]/li[1]/text()'
        game_type_xpath = r'td/table/tr/td[2]/ul[1]/li[2]/text()'
        stats_xpath = r'td/table/tr/td[2]/ul[1]/li[3]/text()'
        public_xpath = r'td/table/tr/td[2]/ul[1]/li[4]/text()'
        variants_xpath = r'td/table/tr/td[2]/ul[1]/li[5]/text()'
        map_xpath = r'td/table/tr/td[2]/ul[1]/li[6]/text()'
        orders_deadline_xpath = r'td/table/tr/td[2]/ul[2]/li[1]/text()'
        retreat_deadline_xpath = r'td/table/tr/td[2]/ul[2]/li[2]/text()'
        build_deadline_xpath = r'td/table/tr/td[2]/ul[2]/li[3]/text()'
        players_xpath = r'td/table/tr/td[3]/ul/li'
        start_xpath = r'td/table/tr/td[4]/p[1]/text()'
        finish_xpath = r'td/table/tr/td[4]/p[2]/text()'
        
        sel = Selector(response)
        for game_sel in sel.xpath(games_table_xpath):
            game = Game()
            id_raw = game_sel.xpath(r'td/h3/a/text()').extract()[0]
            game['last_updated'] = time.strftime('%X %x %Z')
            game['game_id'] = re.search(r'[0-9]+', id_raw).group()
            game['map_variant'] = re.search(r'(?<=: ).*$', game_sel.xpath(map_variant_xpath).extract()[0]).group()
            game['game_type'] = re.search(r'(?<=: ).*$', game_sel.xpath(game_type_xpath).extract()[0]).group()
            game['stats'] = re.search(r'(?<=: ).*$', game_sel.xpath(stats_xpath).extract()[0]).group()
            game['public'] = re.search(r'(?<=: ).*$', game_sel.xpath(public_xpath).extract()[0]).group()
            game['variants'] = re.search(r'(?<=: ).*$', game_sel.xpath(variants_xpath).extract()[0]).group()
            game['map_type'] = re.search(r'(?<=: ).*$', game_sel.xpath(map_xpath).extract()[0]).group()
            game['orders_deadline'] = re.search(r'(?<= every ).*$', game_sel.xpath(orders_deadline_xpath).extract()[0]).group()
            game['retreat_deadline'] = re.search(r'(?<= every ).*$', game_sel.xpath(retreat_deadline_xpath).extract()[0]).group()
            game['build_deadline'] = re.search(r'(?<= every ).*$', game_sel.xpath(build_deadline_xpath).extract()[0]).group()
            game['start'] = game_sel.xpath(start_xpath).extract()[0]
            game['finish'] = game_sel.xpath(finish_xpath).extract()[0]
            game['country_choice'] = response.meta['country_choice']
            for playersel in game_sel.xpath(players_xpath):
                country = playersel.xpath(r'img[1]/@title').extract()[0]
                if playersel.xpath(r'i').extract():
                    game[country] = "surrendered"
                else:
                    game[country] = playersel.xpath(r'text()').extract()[0]
                    if playersel.xpath(r'b').extract():
                        game["".join([country, "_won"])] = 1
            yield game

class OrdersSpider(LoginSpider):
    """
    Inherit and implement a generator orders_url_feeder.

    orders_url_feeder would be called every time a new url is needed
    Useful Constants:
        empty_subesq_pages -- number of subsequent pages, turned out to be empty
        orders_url -- pattern for an order url
    """

    __metaclass__ = ABCMeta
    name = 'scrap_orders'
    orders_url = r'http://www.playdiplomacy.com/game_history.php?game_id={}&gdate={}&phase={}'
    empty_subesq_pages = 0

    def games_feeder(self):
        with open('games.csv', 'rb') as games_csvfile:
            games_reader = csv.reader(games_csvfile)
            title = games_reader.next()
            ind_game_id = title.index("game_id")
            for row in games_reader:
                yield row[ind_game_id]
    
    def requests_feeder(self):
        for game_id in self.games_feeder():
            self.empty_subseq_pages = 0
            for url in self.orders_url_feeder(game_id):
                yield Request(url, meta={'game_id':game_id}, callback=self.parse_orders)

    def parse_after_login(self, response):
        self.requests = self.requests_feeder()
        yield self.requests.next()

    def parse_orders(self, response):
        if 'no orders' in response.body:
            self.empty_subseq_pages += 1
            yield self.requests.next()
        else:
            self.empty_subseq_pages = 0
            date_xpath = r'//table[@cellpadding=2]/tr[1]/td/b/text()'
            countries_list_xpath = r'//table[@cellpadding=2]/tr[2]/td/table/tr[1]//b/text()'
            orders_list_xpath = r'//table[@cellpadding=2]/tr[2]/td/table/tr[1]//ul'
            game_id = response.meta['game_id']
            sel = Selector(response)
            countries = sel.xpath(countries_list_xpath).extract()
            orders_htmls = sel.xpath(orders_list_xpath).extract()
            for country, orders_html in zip(countries, orders_htmls):
                orders_sel = Selector(text=orders_html)
                for order_sel in orders_sel.xpath('//li/text()'):
                    order_item = Order()
                    order_item['date'] = sel.xpath(date_xpath).extract()[0]
                    order_item['country'] = country
                    order_item['game_id'] = game_id
                    order_full_text = order_sel.extract()
                    print order_full_text
                    if order_full_text.strip() == "":
                        continue
                    order_text, order_status = order_full_text.split(r'->')
                    order_text = order_text.strip()
                    order_status = order_status.strip()
                    order_item['status'] = order_status
                    order_item['order'] = order_text
                    yield order_item
            yield self.requests.next()

    @abstractmethod
    def orders_url_feeder(self, game_id):
        raise NotImplementedError("Must override orders_url_feeder")


class StartingOrdersSpider(OrdersSpider):
    name = 'scrap_starting_orders'

    def orders_url_feeder(self, game_id):
        yield self.orders_url.format(game_id, '0', 'O')


class AllOrdersSpider(OrdersSpider):
    name = 'scrap_all_orders'

    def orders_url_feeder(self, game_id):
        turn = 0
        while self.empty_subseq_pages < 4:
            yield self.orders_url.format(game_id, str(turn), 'O')
            yield self.orders_url.format(game_id, str(turn), 'B')
            yield self.orders_url.format(game_id, str(turn), 'R')
            turn += 1
