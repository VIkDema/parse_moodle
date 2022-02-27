import json
from bs4 import BeautifulSoup
import re
import requests

data = {
    'username': '***',
    'password': '***',
    'url': 'https://vec.etu.ru/moodle/login/index.php',
    'urlMy': 'https://vec.etu.ru/moodle/my/',
    'toket_path': 'logintoken',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'protocol': 'https'
}

def start_parse(session):
    request = authorization(session)
    parse_student_objects(session, request)

def authorization(session): 
    #Хотел в дальнейшем вводить через put запросы
    data['username'] = input("Enter login:\n")
    data['password'] = input("Enter password:\n")

    request = session.get(data['url'], headers={
        'User-Agent': data['user_agent']
    })
    session.headers.update({'Referer': data['urlMy']})

    soup = BeautifulSoup(request.text, 'html.parser')
    token = parse_token(soup)

    post_request = session.post(data['url'], {
        'anchor': "",
        'username': data['username'],
        'password': data['password'],
        'rememberusername': 1,
        'logintoken': token,
    })
    return post_request

    

def parse_student_objects(session, request):
    soup = BeautifulSoup(request.text, 'html.parser')

    sesskey = parse_sesskey(soup)
    userid = parse_userid(soup)

    payload = [{
        "index": 0,
        "methodname": "core_course_get_recent_courses",
        "args": {
            "userid": userid,
            "limit": 10
        }
    }]

    ajax_request = session.post('https://vec.etu.ru/moodle/lib/ajax/service.php?sesskey='+str(sesskey)+'&info=core_course_get_recent_courses',
                                data=json.dumps(payload))
    print(ajax_request.text)
    '''
    [{"error":true,"exception":
    {"message":"Ваш сеанс, по-видимому, истек. Пожалуйста,войдите снова.", "errorcode":"invalidsesskey",
      "link":"https:\/\/vec.etu.ru\/moodle\/","moreinfourl":"https:\/\/docs.moodle.org\/311\/ru\/error\/moodle\/invalidsesskey"}}]
    
    '''

def parse_token(soup):
    token = soup.select("input[name=" + data['toket_path']+"]")[0]['value']
    return token

def parse_sesskey(soup):
    script = soup.select("script")[1]
    match = re.search('M.cfg = ({.*})', script.text)
    sesskey = re.search('"sesskey":"([^"]*)"', match.group(1))
    return sesskey

def parse_userid(soup):
    userid = soup.select("div[id='nav-notification-popover-container']")[0]['data-userid']
    return userid
