# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http import FormRequest


class ProfileSpider(scrapy.Spider):
    name = 'profile'
    allowed_domains = ['http://example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile?_next=/places/default/index']

    def parse(self, response):
        yield dict(zip(response.css('label.readonly::text').re('(.+):'), response.css('td.w2p_fw::text').extract()))

    # 登录部分
    login_url = 'http://example.webscraping.com/places/default/user/login?_next=/places/default/index'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        yield FormRequest.from_response(response, callback=self.login2, formdata={'email': 'gjw199513@163.com', 'password': 'gjw605134015'})

    def login2(self, response):
        if response.url == self.login_url:
            raise scrapy.exceptions.CloseSpider('登录失败')

        yield from super().start_requests()