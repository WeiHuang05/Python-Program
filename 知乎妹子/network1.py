from urllib.parse import urlsplit
from os.path import basename
import urllib.request
import re
import requests
import os
import json
import urllib


def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        print (u'新建了名字叫做',path,u'的文件夹')
        os.makedirs(path)
        return True
    else:
        print (u'名为',path,u'的文件夹已经创建成功')
        return False


def downloadImage(id ,path):    
    number = 0
    offset = 0
    while offset < 1000:

        get_url = 'https://www.zhihu.com/api/v4/questions/'+id+'/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset='+str(offset)+'&sort_by=default'

        header = {
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
            'Host': "www.zhihu.com",
        }

        r = requests.get(get_url, verify=False, headers=header)
        content = r.content.decode("utf-8")
        txt = json.loads(content)
        
        if txt.get("paging").get("is_end"):
            print ("爬取完毕！")
            break
        offset += 20
        
        imgUrls = re.findall(r'data-original="([^"]+)"', str(txt))
        imgUrls = list(set(imgUrls))
        
        for imgUrl in imgUrls:
            try:
                splitPath = imgUrl.split('.')
                fTail = splitPath.pop()
                print(fTail)
                if len(fTail) > 3 :
                    fTail = 'jpg'
                fileName = path +"/" + str(number) + "."+fTail
                
                img_data = urllib.request.urlopen(imgUrl).read()
                
                output = open(fileName, 'wb')
                output.write(img_data)
                print (u'正在保存的一张图片为',fileName)
                output.close()
            except urllib.request.URLError as e:
                print (e.reason)
            number += 1
 
 
if __name__ == '__main__':
    path = u'/home/zhihuimage'
    mkdir(path) #创建本地文件夹
    downloadImage("266808424",path)