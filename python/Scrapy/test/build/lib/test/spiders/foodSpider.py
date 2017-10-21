import scrapy

class foodSpider(scrapy.Spider):
    name = "allrecipes"
    allowed_domains = ["allrecipes.com"]

    with open("users.txt") as f:
        content = f.readlines()
        start_urls = [x.strip() for x in content] 

    def parse(self, response):
        filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response)
        with open(filename, "w") as f:
            f.write(response.text)