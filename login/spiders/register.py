# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest


class RegisterSpider(scrapy.Spider):
    name = 'register'
    allowed_domains = ['example.webscraping.com']
    # start_urls = ['http://example.webscraping.com/']
    register_url = 'http://example.webscraping.com/places/default/user/register'
    logout_url = 'http://example.webscraping.com/places/default/user/logout?_next=/places/default/index'

    i = 7060
    n = 1

    # 起始url
    def start_requests(self):
        yield scrapy.Request(self.register_url, dont_filter=True)

    # 进入注册页面输入信息
    def parse(self, response):
        # 获取页面的name
        keys = response.xpath('//form//table//input/@name').extract()

        # 注册信息值
        values = [
            'gjw1',
            'gjw1',
            'gjw11%s@163.com' % self.i,
            '123456',
            '123456',
            self._get_recaptcha(response)
        ]
        # 将上述二者组成字典
        form = dict(zip(keys, values))
        # 将字典信息传入
        yield FormRequest.from_response(response, formdata=form, dont_filter=True, callback=self.check, meta={'_form': form})

    # 检查注册是否成功
    def check(self, response):
        from scrapy.utils.response import open_in_browser
        if 'Logged in' in response.text:
            print('注册成功')
            self.i += 1
            self.n -= 1
            yield response.meta['_form']
        else:
            print('注册失败')
            open_in_browser(response)

        if self.n > 0:
            yield scrapy.Request(self.logout_url, dont_filter=True,
                                 callback=lambda _: self.start_requests())

        # yield from self.start_requests()

    # 获取图片
    def _get_img(self, response):
        import base64

        data = response.css('div#recaptcha img::attr(src)').extract_first()
        b64_img = data[22:].encode(response.encoding)
        img = base64.b64decode(b64_img)

        return img

    # 验证码提交（联众答题）
    def _get_recaptcha(self, response):
        import requests
        from io import BytesIO
        img = self._get_img(response)

        post_url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"

        data = {
            'user_name': 'gjw199513',
            'user_pw': 'Gjw18647373096.'
        }

        files = {
            'upload': BytesIO(img)
        }

        r = requests.post(post_url, data=data, files=files)
        res = r.json()

        if res['result']:
            print(res['data']['val'])
            return res['data']['val'].lower()
        return ''