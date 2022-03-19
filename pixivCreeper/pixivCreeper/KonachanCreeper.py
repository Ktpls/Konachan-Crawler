
from django.http import HttpResponse
from django.shortcuts import render_to_response
from pip._vendor.requests import session
from lxml import etree
import json
import subprocess

#服务器的工作只有返回页面，爬取图片链接，返回查找tag的url
#显示、下载等都放在html中了
#后来新添了idm下载
def page(request):
    return render_to_response('KonachanCreeper.html')

def loadKonachan(page,tag):
    session_requests = session()
    result = session_requests.get('https://konachan.com/post?page='+page+(('&tags='+tag)if(tag!='')else''))
    session_requests.close()
    selector = etree.HTML(result.text)
    large = selector.xpath('//*[@id="post-list-posts"]/li/a/@href')#这里假定这两个是按序号对应的
    preview=selector.xpath('//*[@id="post-list-posts"]/li/div/a/img/@src')#这两个匹配可无修移植到yande.re的爬取上
    lst=[{'large':large[i],'preview':preview[i]} for i in range(len(large))]
    return json.dumps(lst)
    
def loadYandere(page,tag):
    session_requests = session()
    result = session_requests.get('https://yande.re/post?page='+page+(('&tags='+tag)if(tag!='')else''))
    session_requests.close()
    selector = etree.HTML(result.text)
    large = selector.xpath('//*[@id="post-list-posts"]/li/a/@href')#这里假定这两个是按序号对应的
    preview=selector.xpath('//*[@id="post-list-posts"]/li/div/a/img/@src')#这两个匹配可无修移植到yande.re的爬取上
    lst=[{'large':large[i],'preview':preview[i]} for i in range(len(large))]
    return json.dumps(lst)
    #这是从loadKonachan中复制过来的，只改了网址

def more(request):
    switcher = {
        'Konachan': loadKonachan,#记得同步html中select的值和searchTag中的值
        'Yandere': loadYandere
    }
    loader= switcher.get(request.GET['site'], "nothing")
    if loader!='nothing':
        return HttpResponse(loader(request.GET['page'],request.GET['tag']))

def searchTagOnKonachan(tag):
    return 'https://konachan.com/tag?name='+tag

def searchTagOnYandere(tag):
    return 'https://yande.re/tag?name='+tag

def searchTag(request):
    switcher = {
        'Konachan': searchTagOnKonachan,#记得同步html中select的值和more中的值
        'Yandere': searchTagOnYandere
    }
    searcher= switcher.get(request.GET['site'], "nothing")
    if searcher!='nothing':
        return HttpResponse(searcher(request.GET['tag']))

def CallIDM(url,path,file):
    IDM_PATH='"D:/Program Files (x86)/Internet Download Manager/IDMan.exe"'
    subprocess.Popen('{0} /d "{1}" /p "{2}" /f "{3}"'.format(IDM_PATH, url, path, file))

def DownloadByIDM(request):
    DOWNLOAD_PATH='D:/File/download'
    CallIDM(request.GET['url'],DOWNLOAD_PATH,'')
    return HttpResponse('')