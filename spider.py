import re

from urllib import request

class Spider():

    #类变量,来保存url
    url = 'https://www.panda.tv/cate/lol'
    '''
    标签 加上*是匹配0次或无限多次  加上问号匹配的是非贪婪模式
    如果不加问号为贪婪模式，它会导致无法精准匹配标识符内部内容
    加上括号()变成组，去除了外部标签
    '''
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<span class="video-number">([\s\S]*?)</span>'

    #私有方法
    def __fetch_content(self):

        #request对象下有个方法urloprn(),它来接收url
        r = request.urlopen(Spider.url)  

        #bytes
        htmls = r.read()
        htmls = str(htmls,encoding='utf-8')
        return htmls

    #抓包获取所需要的信息，进行正则匹配
    def __analysis(self,htmls):
        root_html = re.findall(Spider.root_pattern,htmls)

        #定义一个列表
        anchors = []
        for html in root_html:
            #内部循环，提取姓名和人数
            name = re.findall(Spider.name_pattern,html)
            number = re.findall(Spider.number_pattern,html)

            #将name和number拼成字典
            anchor = {'name':name,'number':number}
            anchors.append(anchor)
        return anchors

    #定义一个函数 ->数据精炼
    def __refine(self,anchors):
        l = lambda anchor: {
            'name':anchor['name'][0].strip(),
            'number':anchor['number'][0]
            }
        return map(l,anchors)

    #排序的函数 key接受一个参数
    def __sort(self,anchors):
        snchors = sorted(anchors,key=self.__sort_seed,reverse=True)
        return anchors

    #key定义一个比较,接收参数anchor（字典）
    def __sort_seed(self,anchor):
        r = re.findall('\d*',anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    #展现数据
    def __show(self,anchors):
        for rank in range(0,len(anchors)):
            print('rank ' + str(rank + 1)
            + '  : ' + anchors[rank]['name']
            + '    ' + anchors[rank]['number'])

    #调用私有方法,总控所有方法   主方法
    def go(self):

        ''' 
        1、获取数据  2、数据分析  3、精炼数据  4、业务处理(排序)  5、展示方法
        '''
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)

#实例化对象
spider = Spider() 
spider.go()