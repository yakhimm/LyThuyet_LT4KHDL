import scrapy

class collect_player_info(scrapy.Spider):
    name='Get_Data'

    def __init__(self):
        self.count = 0
        self.page_count = 2
        self.num_page = 55 #Num of page need to get data
    def start_requests(self):
        urls = ['https://www.topcv.vn/viec-lam-it?page=1']
        # YOUR CODE HERE
        yield scrapy.Request(urls[0], callback=self.parse)

    def parse(self, response):
        for link in response.css('div.lists h3.title  a::attr(href)'):
            self.count +=1
            yield response.follow(link.get(), callback = self.parse_info)
        if self.page_count < self.num_page:
            next_page_url = 'https://www.topcv.vn/viec-lam-it?page=' + str(self.page_count)
            self.page_count += 1
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_info(self, response):
        info = response.css('div.box-main div.box-item span::text').getall()
        title = response.css('h1.job-title a::text').get()
        if title == None:
            title = response.css('h1.job-title::text').get()
        jobdata = response.css('div.job-data div.content-tab  p::text').getall()
        if jobdata == []:
            jobdata = response.css('div.job-data div.content-tab li::text').getall()
        # DiaChi = response.css('div.box-address div::text').getall()[1]
        # DiaChi = DiaChi[DiaChi.index('-')+1:DiaChi.index(':')]

        a = self.count
        yield {
            'Title': title, 
            'Company': response.css('div.company-title a::text').get(), 
            'DeadlineHoSo': response.css('div.job-deadline::text').getall()[1], 
            'Salary': info[0], 
            'Quantity':  info[1], 
            'Hthuc': info[2], 
            'CapBac': info[3],
            'GioiTinh': info[4],
            'KinhNghiem': info[5],
            'DiaChi': response.css('div.area  a::text').getall(),
            'Skill': response.css('div.skill  a::text').getall(),
            'JobData': jobdata,
            }
     