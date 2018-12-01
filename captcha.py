#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import requests
from requests_html import HTMLSession
from urllib.parse import urljoin
import pytesseract


# TODO fill your own url and pattern
login_url = 'LOGIN_URL' # http://bbs.baidu.com/login etc.
base_url = 'BASE_URL' # http://bbs.baidu.com etc.
csrf_pattern = '#CSRF_TAG_ID_OR_PATTERN' # [name=csrf_token] etc.
captcha_pattern = '#YOUR_CAPTCHA_TAG_ID_OR_PATTERN' # #captcha_img etc.
post_csrf_pattern = '#CSRF_TAG_ID_OR_PATTERN' # [name=csrf_token] etc.
post_captcha_pattern = '#YOUR_CAPTCHA_TAG_ID_OR_PATTERN' # #captcha_img etc.
username = 'USRNAME'
password = 'PASSWORD'
post_url = 'POST_URL_TO_WHICH_YOU_WANT_TO_COMMENT_ON' # xx/posts/?id=100 etc.
comment_content = 'YOUR_COMMENT'

def get_captcha(session, url):
    captcha_r = session.get(url, stream=True)
    if captcha_r.status_code == 200:
        path = 'imgs/temp/'+url.split('=')[1]+'.png'
        with open(path, 'wb') as f:
            for chunk in captcha_r:
                f.write(chunk)

        # please config and tune tesseract to fit your own situation if
        # correct rate is too low
        guess = pytesseract.image_to_string(path, lang='eng', config='-psm 6 bazaar')
        print("guess of {} is {}".format(path, guess))
        return guess
    return ''


def login():
    session = HTMLSession()
    r = session.get(login_url)
    csrf = r.html.find(csrf_pattern, first=True).attrs['value']
    captcha_tag = r.html.find(captcha_pattern, first=True)
    captcha_url = urljoin(base_url, captcha_tag.attrs['src'])
    captcha = get_captcha(session, captcha_url)

    # TODO get your own login form through firebug or charles
    data = {
        '_csrf': csrf,
        'username': username,
        'password': password,
        'captcha_code': captcha,
        'rememberMe': 1
    }

    headers = {
        'Referer': login_url
    }

    login_res = session.post(login_url, data=data, headers=headers)
    print(login_res.status_code)
    # TODO find a way to juedge whether login succeed or failed.
    # in my case it shows logout button after login
    login_check = bool(len(login_res.html.find('a[href="/site/logout"]')))
    print(login_check)
    print(login_res.request.body)
    # print(login_res.text)
    print('########################')
    ok = bool(login_res.ok and login_check)
    return ok, session


def get_score(session):
    r = session.get(post_url)

    captcha_tag = r.html.find(post_captcha_pattern, first=True)
    captcha_url = urljoin(base_url, captcha_tag.attrs['src'])
    captcha = get_captcha(session, captcha_url)
    csrf = r.html.find(post_csrf_pattern, first=True).attrs['value']

    # TODO fill your comment form
    data = {
        'csrf': csrf,
        'content': comment_content,
        'code': captcha,
    }

    headers = {
        'Referer': post_url
    }

    res = session.post(post_url, data=data, headers=headers)
    print(res.ok)


def main():
    max_try = 100
    session = None
    login_success = False

    for i in range(max_try):
        login_success, session = login()
        print('login fail {}'.format(i))
        if login_success:
            break

    if not login_success:
        print('max_try exceed, please tune your OCR')

    max_score = 1000

    for i in range(max_score):
        get_score(session)
        if not i % 100:
            print("score added i")


if __name__ == "__main__":
    main()
