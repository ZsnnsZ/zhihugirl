#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
- author : "wq"
'''
import re
import os

import zhihu


exAvatarTag = re.compile(r'<img.*Avatar Avatar--l.*/>')
exAvatar = re.compile(r'(http.*?)_l\.jpg')
exPeople = re.compile(r'https://www\.zhihu\.com/people/([^"]*)')


def openUrl(url, isByte=False):
    rep = zhihu.session.get(url, headers=zhihu.headers)
    contents = rep.content
    if isByte:
        return contents
    else:
        return contents.decode('UTF-8')


def getPicUrl(contents):
    tag = exAvatarTag.search(contents)
    if tag is not None:
        s = tag.group()
        res = exAvatar.search(s)
        if res is not None:
            return res.group(1) + '.jpg'

    return None


def getPeopleUrl(contents):
    return exPeople.findall(contents)


def downLoadPic(url, picname):
    img = openUrl(url, isByte=True)
    with open("pic/" + picname + '.jpg', 'wb') as f:
        f.write(img)


def isFemale(contents):
    return contents.find('icon-profile-female') != -1


hasDownload = set(map(lambda x: x[0:-4], os.listdir("./pic")))
hasVisited = set()

if __name__ == '__main__':
    if zhihu.isLogin():
        print('您已经登录')
    else:
        account = input('请输入你的用户名\n>  ')
        secret = input("请输入你的密码\n>  ")
        zhihu.login(secret, account)

    waitQueue = ['guan-er-32-87', 'zhang-jing-88-76']
    picCount = 0

    while waitQueue and picCount < 1000:
        currentName = waitQueue.pop(0)
        if currentName not in hasVisited:
            currentUrl = 'https://www.zhihu.com/people/' + currentName + \
                         '/followees'
            pageData = openUrl(currentUrl)
            hasVisited.add(currentName)
            waitQueue.extend(getPeopleUrl(pageData))
            if isFemale(pageData):
                picUrl = getPicUrl(pageData)
                if picUrl and currentName not in hasDownload:
                    picCount = picCount + 1
                    downLoadPic(picUrl, currentName)
