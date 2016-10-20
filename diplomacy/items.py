# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Game(Item):
    game_id = Field()
    map_variant = Field()
    game_type = Field()
    stats = Field()
    public = Field()
    variants = Field()
    map_type = Field()
    orders_deadline = Field()
    retreat_deadline = Field()
    build_deadline = Field()
    country_choice = Field()
    BRITAIN = Field()
    EGYPT = Field()
    FRANCE = Field()
    ITALY = Field()
    GREECE = Field()
    GERMANY = Field()
    POLAND = Field()
    TURKEY = Field()
    USSR = Field()
    ROME = Field()
    CARTHAGE = Field()
    PERSIA = Field()
    ENGLAND = Field()
    AUSTRIA = Field()
    RUSSIA = Field()
    BRITAIN_won = Field()
    EGYPT_won = Field()
    FRANCE_won = Field()
    ITALY_won = Field()
    GREECE_won = Field()
    GERMANY_won = Field()
    POLAND_won = Field()
    TURKEY_won = Field()
    USSR_won = Field()
    ROME_won = Field()
    CARTHAGE_won = Field()
    PERSIA_won = Field()
    ENGLAND_won = Field()
    AUSTRIA_won = Field()
    RUSSIA_won = Field()
    start = Field()
    finish = Field()
    last_updated = Field()

class Order(Item):
    game_id = Field()
    country = Field()
    order = Field()
    status = Field()
    date = Field()

