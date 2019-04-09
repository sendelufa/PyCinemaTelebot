# Copyright 2018 Shibkov Konstantin <sendel@sendel.ru>
# All rights reserved. MIT License.
# Parse HTML to XML cinema list

# coding: utf8
import bs4, requests, datetime, time, os, re

# url = 'https://oc.sendel.ru/1'
log_date = time.strftime("%d.%m.%Y", time.localtime())
url = 'https://rb7.ru/afisha/movie-shows?date=' + log_date
xml_file_party = os.path.dirname(os.path.abspath(__file__)) + '/main_rb7.xml'
print(os.path.dirname(os.path.abspath(__file__)))
sessions = []  # [] - список, {} - словарь
cinema = []
films = []


def parse_cinema_info(url):
    l = {}
    rq = requests.get(url).text
    html = bs4.BeautifulSoup(rq, "lxml").select('.data .address')
    logo_cinema = bs4.BeautifulSoup(rq, "lxml").select('.cinema_page .cinema .poster img')
    # print(logo_cinema[0].attrs['src'], type(logo_cinema[0]))
    l['adress'] = re.search(r".*</span>\n(.+?)\n</div>", str(html)).group(1)
    if len(logo_cinema) > 0:
        l['img_url'] = 'https://rb7.ru' + logo_cinema[0].attrs['src']
    else:
        l['img_url'] = 'none'
    print(l)
    return l


html_p = bs4.BeautifulSoup(requests.get(url).text, "lxml")

p = html_p.select('.date_navigation .active .date')
date_fromxml = p[0].getText().strip().split('.')  # дата текущего расписания
sessions_date = datetime.datetime(int(date_fromxml[2]), int(date_fromxml[1]), int(date_fromxml[0]), 0, 0)

p = html_p.find('table', class_='afisha-schedule')

session = []  # список
for block in p.find_all('tr', {'class': ['odd', 'even']}):
    for td in block.find_all('td'):
        session.append(td.getText(strip=True))

        # Получаем ссылку для парсинга инфо о фильме
        chck_film_info = re.match(r"^<td class=\"film\">\n<a href=\"\/afisha\/movies/(\d+?)\">.+\n</td>$", str(td))
        if chck_film_info:
            session.append("https://rb7.ru/afisha/movies/" + chck_film_info.group(1))

        # Получаем ссылку для парсинга инфо о кинотеатре
        chck_cinema_info = re.match(r"^<td class=\"theatre\">\n<a href=\"\/afisha\/cinemas/(\d+?)\">.+\n</td>$",
                                    str(td))
        if chck_cinema_info:
            session.append("https://rb7.ru/afisha/cinemas/" + chck_cinema_info.group(1))

    sessions.append(session.copy())

    session.clear()

# print(sessions)
# формируем список кинотеатров и фильмов
xml_films = xml_cinema = ''
cinema_count = 0
film_count = 0
for item in sessions:
    if item[3] not in cinema:  # Получаем список кинотеатров
        cinema.append(item[3])
        cinema_info_tuple = parse_cinema_info(item[4])
        xml_cinema += "\n\t\t<cinema_item id='" + str(cinema_count) + "' url='" + item[4] + "' adress='" + \
                      cinema_info_tuple['adress'] + "' logo='" + cinema_info_tuple['img_url'] + "'>" + item[3] + "</cinema_item>"
        cinema_count += 1
    if item[1] not in films:  # Получаем список фильмов
        films.append(item[1])
        xml_films += "\n\t\t<film_item id='" + str(film_count) + "' url='" + item[2] + "'>" + item[1] + "</film_item>"
        film_count += 1

#  films.sort()  # сортируем список фильмов по алфавиту
#  cinema.sort()  # сортируем список кинотеатров по алфавиту

xml_seansi_list = ''
for index, item in enumerate(sessions, 1):
    time_session = item[0].split(':')
    today_day = datetime.datetime(int(date_fromxml[2]), int(date_fromxml[1]), int(date_fromxml[0]), \
                                  int(time_session[0]), int(time_session[1]))
    is_tomorrow = 0
    if int(time_session[0]) < 6:  # 6 часов утра - разделение киносеансов на сегодня и завтра
        today_day = today_day + datetime.timedelta(days=1)
        is_tomorrow = 1
    cinema_index = cinema.index(item[3])  # поиск индекса кинотеатра по названию
    film_index = films.index(item[1])  # поиск индекса кинотеатра по названию
    xml_seansi_list += "\t\t<seans_item id='%s' film='%s' film_id='%s' cinema='%s' cinema_id='%s' hall='%s' " \
                       "datetime='%s' cost='%s' hour='%s' minutes='%s' timestamp='%s' is_tomorrow='%s'/\n" % (
    str(index), item[1], film_index, item[3], cinema_index, item[6], item[0], item[5], time_session[0], time_session[1],
    str(time.mktime(today_day.timetuple())), str(is_tomorrow))

s = str(sessions_date.strftime("%d.%m.%Y"))
xml_seansi_list = "<?xml version='1.0' encoding='UTF-8'?>\n<main>\n\t<date>%s</date>\n\t<cinema>%s\n\t</cinema>\n\t" \
                  "<films>%s\n\t</films>\n\t<sessions>\n%s\t</sessions>\n</main>" % (
s, xml_cinema, xml_films, xml_seansi_list)
print(sessions_date)

# Запись XML файла
try:
    file = open(xml_file_party, "w")
    file.write(xml_seansi_list)
    file.close()
except PermissionError:
    print('ошибка доступа к файлу')
    exit(0)