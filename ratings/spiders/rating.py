# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ratings.items import RatingsItem


class RatingSpider(scrapy.Spider):
    name = 'rating'
    start_urls = [
        'http://www.themoviedb.org/tv/1668-friends/season/1?language=en-US/']

    def parse(self, response):
        rate = (response.xpath(
            ".//div[@class='rating_wrapper']/div/div/text()[position()=2]").getall())

        def rem(x): return x.strip()
        rate = map(rem, rate)
        rate = iter(rate)
        for info in response.xpath("//div[@class='image']"):
            yield {
                'season': info.xpath("./a/@season").get(),
                'episode': info.xpath(".//a/@episode").get(),
                'title': (info.xpath(".//a/@title").get()).split(sep='-')[1],
                'rating': next(rate)
            }

            next_page = response.xpath("//span[@class='next']/a/@href").get()
            if next_page is not True:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
