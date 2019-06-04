import psycopg2
import json, requests, sys, time
import datetime

dictWeather = {14: 'Szczecin', 15: 'Koszalin', 16: 'Gdynia', 17: 'Olsztyn', 18: 'Suwałki',
               19: 'Opoczno', 20: 'Rzeszów', 21: 'Gorlice', 22: 'Kraków', 23: 'Bydgoszcz', 24: 'Poznań',
               25: 'Warszawa', 26: 'Białystok', 27: 'Lublin',
               28: 'Łódź', 29: 'Kielce', 30: 'Radom', 31: 'Zawiercie', 32: 'Katowice',
               33: 'Lublin', 34: 'Sanok', 35: 'Wrocław', 36: 'Legnica',
               37: 'Częstochowa', 38: 'Zakopane'}
conn = psycopg2.connect(dbname='p1448_weather', user='p1448_weather', password='Parasol41!', host='pgsql16.mydevil.net', port='5432')
cursor = conn.cursor()

for key, value in dictWeather.items():

    zapis = ""
    dateCheck = datetime.datetime.now()
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + value + "&APPID=436cbc1a223edeafa7efe19aa3525a25"

    response = requests.get(url)
    response.raise_for_status()

    weatherData = json.loads(response.text)
    # print(weatherData)
    w = weatherData['main']
    c = weatherData['coord']
    wind = weatherData['wind']
    try:
        rain = weatherData['rain']
    except:
        rain = ""
    try:
        snow = weatherData['snow']
    except:
        snow = ""
    zapis += str(dateCheck)[:19] + " " + value + " " + str(round((float(w.get('temp')) - 273.0), 2)) + "\n"
    # insert into weather(idmiasta, temperatura, cisnienie, wilgotnosc, wiatrpredkosc,wiatrkierunek,opadyrodzaj,opadyilosc)
    # values('3', '11.1', '333');
    # print(weatherData)

    if rain != "":
        opadyrodzaj = "deszcz"
        opadyIlosc = (rain.get('3h'))
        # print(opadyIlosc)
    if snow != "":
        opadyrodzaj = "śnieg"
        opadyIlosc = (snow.get('3h'))
        # print(opadyIlosc)
    if snow == "" and rain == "":
        opadyrodzaj = "brak"
        opadyIlosc = 0
    try:
        opadyIlosc = float(opadyIlosc)
    except:
        opadyIlosc = 0
    wiatrKat = wind.get('deg')
    try:
        wiatrKat = float(wiatrKat)
    except:
        wiatrKat = 0
    # insert into weather(idmiasta, temperatura, cisnienie, wilgotnosc, wiatrpredkosc,wiatrkierunek,opadyrodzaj,opadyilosc)
    zapytanie = "insert into weather(idmiasta, temperatura, cisnienie, wilgotnosc, wiatrpredkosc,wiatrkierunek,opadyrodzaj,opadyilosc) values ('"
    zapytanie += str(key) + "','"
    zapytanie += str(round((float(w.get('temp')) - 273.0), 2)) + "','"
    zapytanie += str(w.get('pressure')) + "','"
    zapytanie += str(w.get('humidity')) + "','"
    zapytanie += str(wind.get('speed')) + "','"
    zapytanie += str(wiatrKat) + "','"
    zapytanie += str(opadyrodzaj) + "','"
    zapytanie += str(opadyIlosc) + "')"

    #print(zapytanie)


#postgreSQL_select_Query = "select idmiasta, nazwamiasta from miasta;"
    postgreSQL_insert_Query = zapytanie
    cursor.execute(postgreSQL_insert_Query)
    conn.commit()
#cursor.execute(postgreSQL_select_Query)
#mobile_records = cursor.fetchall()
#print(mobile_records)