import psycopg2
import requests, json, time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conn = psycopg2.connect(dbname='p1448_weather', user='p1448_weather', password='Parasol41!', host='pgsql16.mydevil.net', port='5432')
cursor = conn.cursor()
"""

curl -X GET \
    --header 'Accept: application/json' \
    --header 'apikey: D6Gb0ynGdj9sanzlfIOsn3aUPEQP0xR5' \
    'https://airapi.airly.eu/v2/measurements/point?lat=50.062006&lng=19.940984'
"""
'https://airapi.airly.eu/v2/installations/nearest?lat=50.062006&lng=19.940984&maxDistanceKM=5&maxResults=3'
headers = {'apikey': 'D6Gb0ynGdj9sanzlfIOsn3aUPEQP0xR5', 'Accept': 'application/json'}
stations = [49, 2122, 2100, 126, 2134, 7588, 2836, 3476, 82, 6617, 2526, 2548, 2559, 2237, 2442, 7799, 7798, 2671,
            7491, 7476, 2086, 6936, 849, 6901, 8077, 58, 7394, 9, 2336, 10, 6955, 7468, 1062, 658, 337, 956, 32, 2234,
            2119, 12, 7026, 6994, 14, 7561, 2318, 2264, 7796, 88, 24, 6366, 6440, 2718, 3520, 6091, 700, 2249, 749, 2542,
            2512, 7972, 1127, 822, 6947, 2167, 860, 107, 2121, 2418, 2393, 7067, 67, 5627]
#stations = [12]

for id in stations:

    req = "https://airapi.airly.eu/v2/measurements/installation?installationId=" +str(id)
    r = requests.get(req, headers=headers, verify=False)
    r.raise_for_status()
    smogData = json.loads(r.text)
    current = smogData['current']
    values = (current.get('values'))
    time.sleep(1)

    zapytanie = "insert into pomiary(idstacji,wilgotnosc,cisnienie,temperatura,pm1,pm10,pm25) values ('"
    zapytanie += str(id) + "',"
    wilgotnosc = "null"
    cisnienie = "null"
    temperatura = "null"
    pm1 = "null"
    pm10 = "null"
    pm25 = "null"
    #HUMIDITY', 'PRESSURE', 'PM1', 'PM10', 'TEMPERATURE', 'PM25'
    for value in values:
        fieldName = (value.get('name'))
        fieldValue =(value.get('value'))
        if fieldName == "HUMIDITY":
            wilgotnosc = fieldValue
        if fieldName == "PRESSURE":
            cisnienie = fieldValue
        if fieldName == "TEMPERATURE":
            temperatura = fieldValue
        if fieldName == "PM1":
            pm1 = fieldValue
        if fieldName == "PM10":
            pm10 = fieldValue
        if fieldName == "PM25":
            pm25 = fieldValue


    zapytanie +=str(wilgotnosc)
    zapytanie += ","
    zapytanie +=str(cisnienie)
    zapytanie += ","
    zapytanie +=str(temperatura)
    zapytanie += ","
    zapytanie +=str(pm1)
    zapytanie += ","
    zapytanie +=str(pm10)
    zapytanie += ","
    zapytanie +=str(pm25)
    zapytanie += ");"

    postgreSQL_insert_Query = zapytanie
    cursor.execute(postgreSQL_insert_Query)
    conn.commit()
"""

{'fromDateTime': '2019-05-04T22:41:15.172Z', 
'tillDateTime': '2019-05-04T23:41:15.172Z', 
'values': [{'name': 'PM1', 'value': 12.46}, 
            {'name': 'PM25', 'value': 17.69}, 
            {'name': 'PM10', 'value': 32.47}, 
            {'name': 'PRESSURE', 'value': 1005.82}, 
            {'name': 'HUMIDITY', 'value': 80.4}, 
            {'name': 'TEMPERATURE', 'value': 10.6}], 
            
'indexes': [{'name': 'AIRLY_CAQI', 
            'value': 32.47, 
            'level': 'LOW', 
            'description': 'Air is quite good.', 
            'advice': 'Enjoy the clean air.', 
            'color': '#D1CF1E'}], 
            
'standards': [{'name': 'WHO', 
            'pollutant': 'PM25', 
            'limit': 25.0, 
            'percent': 70.76}, 
            {'name': 'WHO', 
            'pollutant': 'PM10', 
            'limit': 50.0, 'percent': 64.93}]}















{'current': {
    'fromDateTime': '2019-05-04T20:05:11.471Z',
    'tillDateTime': '2019-05-04T21:05:11.471Z',
    'values': [{'name': 'PM1', 'value': 11.61},
               {'name': 'PM25', 'value': 16.82},
               {'name': 'PM10', 'value': 30.56},
               {'name': 'PRESSURE', 'value': 1004.56},
               {'name': 'HUMIDITY', 'value': 73.04},
               {'name': 'TEMPERATURE', 'value': 12.67}],
    'indexes': [{'name': 'AIRLY_CAQI',
                 'value': 30.56,
                 'level': 'LOW',
                 'description': 'Air is quite good.',
                 'advice': 'Leave the mask at home today!',
                 'color': '#D1CF1E'}],
    'standards': [{'name': 'WHO',
                   'pollutant': 'PM25',
                   'limit': 25.0, 'percent': 67.29},
                  {'name': 'WHO',
                   'pollutant': 'PM10',
                   'limit': 50.0, 'percent': 61.12}]},
    'history': [{'fromDateTime': '2019-05-03T21:00:00.000Z',
                 'tillDateTime': '2019-05-03T22:00:00.000Z',
                 'values': [{'name': 'PM1', 'value': 16.73},
                            {'name': 'PM25', 'value': 24.9},
                            {'name': 'PM10', 'value': 48.7},
                            {'name': 'PRESSURE', 'value': 1009.68},
                            {'name': 'HUMIDITY', 'value': 85.18},
                            {'name': 'TEMPERATURE', 'value': 8.54}],
                 'indexes': [{'name': 'AIRLY_CAQI', 'value': 48.7,
                              'level': 'LOW',
                              'description': 'Air is quite good.',
                              'advice': "It's a good time to use those rollerskates today!",
                              'color': '#D1CF1E'}],
                 'standards': [{'name': 'WHO',
                                'pollutant': 'PM25',
                                'limit': 25.0,
                                'percent': 99.61},
                               {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 97.41}]},
                                {'fromDateTime': '2019-05-03T22:00:00.000Z',
                                 'tillDateTime': '2019-05-03T23:00:00.000Z',
                                 'values': [{'name': 'PM1', 'value': 16.71},
                                {'name': 'PM25', 'value': 24.73},
                                {'name': 'PM10', 'value': 48.5},
                                {'name': 'PRESSURE', 'value': 1009.74},
                                {'name': 'HUMIDITY', 'value': 86.5},
                                {'name': 'TEMPERATURE', 'value': 8.3}],
                                 'indexes': [{'name': 'AIRLY_CAQI', 'value': 48.5, 'level': 'LOW',
                                              'description': 'Air is quite good.',
                                              'advice': 'Take a deep breath. Today, you can. ;)',
                                              'color': '#D1CF1E'}],
                                 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 98.93},
                                               {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 97.0}]},
                {'fromDateTime': '2019-05-03T23:00:00.000Z', 'tillDateTime': '2019-05-04T00:00:00.000Z',
                 'values': [{'name': 'PM1', 'value': 17.16}, {'name': 'PM25', 'value': 25.66}, {'name': 'PM10', 'value': 49.84}, {'name': 'PRESSURE', 'value': 1009.47}, {'name': 'HUMIDITY', 'value': 86.5}, {'name': 'TEMPERATURE', 'value': 8.28}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 49.84, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Take a breath!', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 102.64}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 99.67}]}, {'fromDateTime': '2019-05-04T00:00:00.000Z', 'tillDateTime': '2019-05-04T01:00:00.000Z', 'values': [{'name': 'PM1', 'value': 16.28}, {'name': 'PM25', 'value': 24.06}, {'name': 'PM10', 'value': 47.23}, {'name': 'PRESSURE', 'value': 1009.04}, {'name': 'HUMIDITY', 'value': 87.23}, {'name': 'TEMPERATURE', 'value': 7.94}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 47.23, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Enjoy the clean air.', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 96.24}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 94.46}]}, {'fromDateTime': '2019-05-04T01:00:00.000Z', 'tillDateTime': '2019-05-04T02:00:00.000Z', 'values': [{'name': 'PM1', 'value': 17.51}, {'name': 'PM25', 'value': 26.44}, {'name': 'PM10', 'value': 51.84}, {'name': 'PRESSURE', 'value': 1008.84}, {'name': 'HUMIDITY', 'value': 85.81}, {'name': 'TEMPERATURE', 'value': 7.61}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 51.15, 'level': 'MEDIUM', 'description': "Well... It's been better.", 'advice': 'Protect your lungs!', 'color': '#EFBB0F'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 105.77}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 103.68}]}, {'fromDateTime': '2019-05-04T02:00:00.000Z', 'tillDateTime': '2019-05-04T03:00:00.000Z', 'values': [{'name': 'PM1', 'value': 18.57}, {'name': 'PM25', 'value': 28.35}, {'name': 'PM10', 'value': 55.07}, {'name': 'PRESSURE', 'value': 1008.76}, {'name': 'HUMIDITY', 'value': 89.35}, {'name': 'TEMPERATURE', 'value': 6.13}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 53.17, 'level': 'MEDIUM', 'description': "Well... It's been better.", 'advice': 'Protect your lungs!', 'color': '#EFBB0F'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 113.41}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 110.14}]}, {'fromDateTime': '2019-05-04T03:00:00.000Z', 'tillDateTime': '2019-05-04T04:00:00.000Z', 'values': [{'name': 'PM1', 'value': 19.59}, {'name': 'PM25', 'value': 30.12}, {'name': 'PM10', 'value': 58.24}, {'name': 'PRESSURE', 'value': 1008.75}, {'name': 'HUMIDITY', 'value': 90.22}, {'name': 'TEMPERATURE', 'value': 6.84}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 55.15, 'level': 'MEDIUM', 'description': "Well... It's been better.", 'advice': 'The air is slightly polluted.', 'color': '#EFBB0F'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 120.48}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 116.48}]}, {'fromDateTime': '2019-05-04T04:00:00.000Z', 'tillDateTime': '2019-05-04T05:00:00.000Z', 'values': [{'name': 'PM1', 'value': 17.76}, {'name': 'PM25', 'value': 26.82}, {'name': 'PM10', 'value': 52.09}, {'name': 'PRESSURE', 'value': 1008.84}, {'name': 'HUMIDITY', 'value': 90.25}, {'name': 'TEMPERATURE', 'value': 6.45}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 51.31, 'level': 'MEDIUM', 'description': "Well... It's been better.", 'advice': 'Protect your lungs!', 'color': '#EFBB0F'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 107.29}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 104.18}]}, {'fromDateTime': '2019-05-04T05:00:00.000Z', 'tillDateTime': '2019-05-04T06:00:00.000Z', 'values': [{'name': 'PM1', 'value': 16.42}, {'name': 'PM25', 'value': 24.45}, {'name': 'PM10', 'value': 47.98}, {'name': 'PRESSURE', 'value': 1008.92}, {'name': 'HUMIDITY', 'value': 90.25}, {'name': 'TEMPERATURE', 'value': 7.52}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 47.98, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'The air quality is good today!', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 97.82}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 95.97}]}, {'fromDateTime': '2019-05-04T06:00:00.000Z', 'tillDateTime': '2019-05-04T07:00:00.000Z', 'values': [{'name': 'PM1', 'value': 13.12}, {'name': 'PM25', 'value': 19.14}, {'name': 'PM10', 'value': 37.23}, {'name': 'PRESSURE', 'value': 1009.06}, {'name': 'HUMIDITY', 'value': 87.37}, {'name': 'TEMPERATURE', 'value': 10.66}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 37.23, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'The air quality is good today!', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 76.57}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 74.46}]}, {'fromDateTime': '2019-05-04T07:00:00.000Z', 'tillDateTime': '2019-05-04T08:00:00.000Z', 'values': [{'name': 'PM1', 'value': 10.18}, {'name': 'PM25', 'value': 14.75}, {'name': 'PM10', 'value': 27.13}, {'name': 'PRESSURE', 'value': 1008.91}, {'name': 'HUMIDITY', 'value': 84.96}, {'name': 'TEMPERATURE', 'value': 13.33}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 27.13, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Leave the mask at home today!', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 58.98}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 54.27}]}, {'fromDateTime': '2019-05-04T08:00:00.000Z', 'tillDateTime': '2019-05-04T09:00:00.000Z', 'values': [{'name': 'PM1', 'value': 8.13}, {'name': 'PM25', 'value': 11.88}, {'name': 'PM10', 'value': 21.7}, {'name': 'PRESSURE', 'value': 1008.06}, {'name': 'HUMIDITY', 'value': 70.85}, {'name': 'TEMPERATURE', 'value': 11.53}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 21.7, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Breathe as much as you can!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 47.5}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 43.39}]}, {'fromDateTime': '2019-05-04T09:00:00.000Z', 'tillDateTime': '2019-05-04T10:00:00.000Z', 'values': [{'name': 'PM1', 'value': 5.71}, {'name': 'PM25', 'value': 8.13}, {'name': 'PM10', 'value': 14.77}, {'name': 'PRESSURE', 'value': 1007.38}, {'name': 'HUMIDITY', 'value': 60.82}, {'name': 'TEMPERATURE', 'value': 12.31}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 14.77, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Feel free to run, walk, dance and let the air outside in today!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 32.53}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 29.54}]}, {'fromDateTime': '2019-05-04T10:00:00.000Z', 'tillDateTime': '2019-05-04T11:00:00.000Z', 'values': [{'name': 'PM1', 'value': 5.5}, {'name': 'PM25', 'value': 7.75}, {'name': 'PM10', 'value': 13.88}, {'name': 'PRESSURE', 'value': 1006.68}, {'name': 'HUMIDITY', 'value': 55.49}, {'name': 'TEMPERATURE', 'value': 13.01}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 13.88, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Perfect air for exercising! Go for it!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 31.01}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 27.76}]}, {'fromDateTime': '2019-05-04T11:00:00.000Z', 'tillDateTime': '2019-05-04T12:00:00.000Z', 'values': [{'name': 'PM1', 'value': 5.25}, {'name': 'PM25', 'value': 7.39}, {'name': 'PM10', 'value': 13.16}, {'name': 'PRESSURE', 'value': 1006.0}, {'name': 'HUMIDITY', 'value': 50.21}, {'name': 'TEMPERATURE', 'value': 14.27}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 13.16, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Great air!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 29.56}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 26.31}]}, {'fromDateTime': '2019-05-04T12:00:00.000Z', 'tillDateTime': '2019-05-04T13:00:00.000Z', 'values': [{'name': 'PM1', 'value': 5.44}, {'name': 'PM25', 'value': 7.67}, {'name': 'PM10', 'value': 14.04}, {'name': 'PRESSURE', 'value': 1005.46}, {'name': 'HUMIDITY', 'value': 48.43}, {'name': 'TEMPERATURE', 'value': 14.5}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 14.04, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Feel free to run, walk, dance and let the air outside in today!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 30.69}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 28.08}]}, {'fromDateTime': '2019-05-04T13:00:00.000Z', 'tillDateTime': '2019-05-04T14:00:00.000Z', 'values': [{'name': 'PM1', 'value': 6.47}, {'name': 'PM25', 'value': 9.0}, {'name': 'PM10', 'value': 16.43}, {'name': 'PRESSURE', 'value': 1004.87}, {'name': 'HUMIDITY', 'value': 48.04}, {'name': 'TEMPERATURE', 'value': 14.82}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 16.43, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Green, green, green!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 36.02}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 32.86}]}, {'fromDateTime': '2019-05-04T14:00:00.000Z', 'tillDateTime': '2019-05-04T15:00:00.000Z', 'values': [{'name': 'PM1', 'value': 5.49}, {'name': 'PM25', 'value': 7.87}, {'name': 'PM10', 'value': 14.18}, {'name': 'PRESSURE', 'value': 1004.36}, {'name': 'HUMIDITY', 'value': 50.42}, {'name': 'TEMPERATURE', 'value': 14.8}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 14.18, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Breathe to fill your lungs!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 31.5}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 28.36}]}, {'fromDateTime': '2019-05-04T15:00:00.000Z', 'tillDateTime': '2019-05-04T16:00:00.000Z', 'values': [{'name': 'PM1', 'value': 4.31}, {'name': 'PM25', 'value': 6.56}, {'name': 'PM10', 'value': 11.79}, {'name': 'PRESSURE', 'value': 1004.01}, {'name': 'HUMIDITY', 'value': 52.63}, {'name': 'TEMPERATURE', 'value': 14.88}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 11.79, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Feel free to run, walk, dance and let the air outside in today!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 26.24}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 23.59}]}, {'fromDateTime': '2019-05-04T16:00:00.000Z', 'tillDateTime': '2019-05-04T17:00:00.000Z', 'values': [{'name': 'PM1', 'value': 4.63}, {'name': 'PM25', 'value': 6.8}, {'name': 'PM10', 'value': 12.29}, {'name': 'PRESSURE', 'value': 1003.81}, {'name': 'HUMIDITY', 'value': 58.03}, {'name': 'TEMPERATURE', 'value': 14.62}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 12.29, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Feel free to run, walk, dance and let the air outside in today!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 27.18}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 24.58}]}, {'fromDateTime': '2019-05-04T17:00:00.000Z', 'tillDateTime': '2019-05-04T18:00:00.000Z', 'values': [{'name': 'PM1', 'value': 4.6}, {'name': 'PM25', 'value': 6.95}, {'name': 'PM10', 'value': 12.29}, {'name': 'PRESSURE', 'value': 1003.78}, {'name': 'HUMIDITY', 'value': 55.39}, {'name': 'TEMPERATURE', 'value': 14.07}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 12.29, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Zero dust - zero worries!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 27.8}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 24.59}]}, {'fromDateTime': '2019-05-04T18:00:00.000Z', 'tillDateTime': '2019-05-04T19:00:00.000Z', 'values': [{'name': 'PM1', 'value': 6.03}, {'name': 'PM25', 'value': 8.85}, {'name': 'PM10', 'value': 15.78}, {'name': 'PRESSURE', 'value': 1003.98}, {'name': 'HUMIDITY', 'value': 62.43}, {'name': 'TEMPERATURE', 'value': 13.14}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 15.78, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Breathe to fill your lungs!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 35.39}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 31.55}]}, {'fromDateTime': '2019-05-04T19:00:00.000Z', 'tillDateTime': '2019-05-04T20:00:00.000Z', 'values': [{'name': 'PM1', 'value': 9.74}, {'name': 'PM25', 'value': 13.96}, {'name': 'PM10', 'value': 25.84}, {'name': 'PRESSURE', 'value': 1004.13}, {'name': 'HUMIDITY', 'value': 64.9}, {'name': 'TEMPERATURE', 'value': 13.35}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 25.84, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Time for a walk with friends or activities with your family - because the air is clean!', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 55.84}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 51.67}]}, {'fromDateTime': '2019-05-04T20:00:00.000Z', 'tillDateTime': '2019-05-04T21:00:00.000Z', 'values': [{'name': 'PM1', 'value': 11.6}, {'name': 'PM25', 'value': 16.79}, {'name': 'PM10', 'value': 30.51}, {'name': 'PRESSURE', 'value': 1004.52}, {'name': 'HUMIDITY', 'value': 72.77}, {'name': 'TEMPERATURE', 'value': 12.72}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 30.51, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'You can go out and enjoy nature without worries.', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 67.15}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 61.01}]}], 'forecast': [{'fromDateTime': '2019-05-04T21:00:00.000Z', 'tillDateTime': '2019-05-04T22:00:00.000Z', 'values': [{'name': 'PM25', 'value': 18.37}, {'name': 'PM10', 'value': 31.61}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 31.61, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Take a deep breath. Today, you can. ;)', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 73.49}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 63.22}]}, {'fromDateTime': '2019-05-04T22:00:00.000Z', 'tillDateTime': '2019-05-04T23:00:00.000Z', 'values': [{'name': 'PM25', 'value': 21.08}, {'name': 'PM10', 'value': 35.37}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 35.37, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'How about going for a walk?', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 84.33}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 70.74}]}, {'fromDateTime': '2019-05-04T23:00:00.000Z', 'tillDateTime': '2019-05-05T00:00:00.000Z', 'values': [{'name': 'PM25', 'value': 22.91}, {'name': 'PM10', 'value': 37.77}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 38.18, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Enjoy the clean air.', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 91.64}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 75.54}]}, {'fromDateTime': '2019-05-05T00:00:00.000Z', 'tillDateTime': '2019-05-05T01:00:00.000Z', 'values': [{'name': 'PM25', 'value': 22.99}, {'name': 'PM10', 'value': 37.81}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 38.32, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'You can go out and enjoy nature without worries.', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 91.96}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 75.61}]}, {'fromDateTime': '2019-05-05T01:00:00.000Z', 'tillDateTime': '2019-05-05T02:00:00.000Z', 'values': [{'name': 'PM25', 'value': 21.88}, {'name': 'PM10', 'value': 36.37}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 36.47, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Enjoy the clean air.', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 87.52}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 72.74}]}, {'fromDateTime': '2019-05-05T02:00:00.000Z', 'tillDateTime': '2019-05-05T03:00:00.000Z', 'values': [{'name': 'PM25', 'value': 19.75}, {'name': 'PM10', 'value': 33.46}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 33.46, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'The air quality is good today!', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 79.0}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 66.93}]}, {'fromDateTime': '2019-05-05T03:00:00.000Z', 'tillDateTime': '2019-05-05T04:00:00.000Z', 'values': [{'name': 'PM25', 'value': 17.7}, {'name': 'PM10', 'value': 30.71}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 30.71, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Great air for a walk to the park!', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 70.82}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 61.43}]}, {'fromDateTime': '2019-05-05T04:00:00.000Z', 'tillDateTime': '2019-05-05T05:00:00.000Z', 'values': [{'name': 'PM25', 'value': 15.6}, {'name': 'PM10', 'value': 27.73}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 27.73, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Take a breath!', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 62.42}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 55.47}]}, {'fromDateTime': '2019-05-05T05:00:00.000Z', 'tillDateTime': '2019-05-05T06:00:00.000Z', 'values': [{'name': 'PM25', 'value': 13.9}, {'name': 'PM10', 'value': 25.07}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 25.07, 'level': 'LOW', 'description': 'Air is quite good.', 'advice': 'Enjoy the clean air.', 'color': '#D1CF1E'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 55.58}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 50.14}]}, {'fromDateTime': '2019-05-05T06:00:00.000Z', 'tillDateTime': '2019-05-05T07:00:00.000Z', 'values': [{'name': 'PM25', 'value': 12.42}, {'name': 'PM10', 'value': 22.47}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 22.47, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Great air!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 49.7}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 44.94}]}, {'fromDateTime': '2019-05-05T07:00:00.000Z', 'tillDateTime': '2019-05-05T08:00:00.000Z', 'values': [{'name': 'PM25', 'value': 11.34}, {'name': 'PM10', 'value': 20.56}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 20.56, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Feel free to run, walk, dance and let the air outside in today!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 45.38}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 41.12}]}, {'fromDateTime': '2019-05-05T08:00:00.000Z', 'tillDateTime': '2019-05-05T09:00:00.000Z', 'values': [{'name': 'PM25', 'value': 10.52}, {'name': 'PM10', 'value': 19.14}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 19.14, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': "It couldn't be better ;)", 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 42.1}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 38.28}]}, {'fromDateTime': '2019-05-05T09:00:00.000Z', 'tillDateTime': '2019-05-05T10:00:00.000Z', 'values': [{'name': 'PM25', 'value': 9.9}, {'name': 'PM10', 'value': 18.36}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 18.36, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Green equals clean!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 39.62}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 36.72}]}, {'fromDateTime': '2019-05-05T10:00:00.000Z', 'tillDateTime': '2019-05-05T11:00:00.000Z', 'values': [{'name': 'PM25', 'value': 9.06}, {'name': 'PM10', 'value': 17.42}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 17.42, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': "It couldn't be better ;)", 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 36.25}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 34.84}]}, {'fromDateTime': '2019-05-05T11:00:00.000Z', 'tillDateTime': '2019-05-05T12:00:00.000Z', 'values': [{'name': 'PM25', 'value': 8.21}, {'name': 'PM10', 'value': 16.5}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 16.5, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Green, green, green!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 32.83}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 32.99}]}, {'fromDateTime': '2019-05-05T12:00:00.000Z', 'tillDateTime': '2019-05-05T13:00:00.000Z', 'values': [{'name': 'PM25', 'value': 7.2}, {'name': 'PM10', 'value': 15.36}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 15.36, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Feel free to run, walk, dance and let the air outside in today!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 28.8}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 30.71}]}, {'fromDateTime': '2019-05-05T13:00:00.000Z', 'tillDateTime': '2019-05-05T14:00:00.000Z', 'values': [{'name': 'PM25', 'value': 6.38}, {'name': 'PM10', 'value': 14.45}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 14.45, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Breathe as much as you can!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 25.52}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 28.89}]}, {'fromDateTime': '2019-05-05T14:00:00.000Z', 'tillDateTime': '2019-05-05T15:00:00.000Z', 'values': [{'name': 'PM25', 'value': 5.55}, {'name': 'PM10', 'value': 13.55}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 13.55, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Breathe deep! The air is clean!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 22.2}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 27.11}]}, {'fromDateTime': '2019-05-05T15:00:00.000Z', 'tillDateTime': '2019-05-05T16:00:00.000Z', 'values': [{'name': 'PM25', 'value': 5.15}, {'name': 'PM10', 'value': 13.5}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 13.5, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Breathe to fill your lungs!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 20.61}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 27.01}]}, {'fromDateTime': '2019-05-05T16:00:00.000Z', 'tillDateTime': '2019-05-05T17:00:00.000Z', 'values': [{'name': 'PM25', 'value': 5.19}, {'name': 'PM10', 'value': 13.99}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 13.99, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'The air is grand today. ;)', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 20.78}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 27.98}]}, {'fromDateTime': '2019-05-05T17:00:00.000Z', 'tillDateTime': '2019-05-05T18:00:00.000Z', 'values': [{'name': 'PM25', 'value': 6.24}, {'name': 'PM10', 'value': 15.56}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 15.56, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'The air is grand today. ;)', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 24.96}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 31.13}]}, {'fromDateTime': '2019-05-05T18:00:00.000Z', 'tillDateTime': '2019-05-05T19:00:00.000Z', 'values': [{'name': 'PM25', 'value': 7.8}, {'name': 'PM10', 'value': 17.78}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 17.78, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'The air is grand today. ;)', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 31.19}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 35.56}]}, {'fromDateTime': '2019-05-05T19:00:00.000Z', 'tillDateTime': '2019-05-05T20:00:00.000Z', 'values': [{'name': 'PM25', 'value': 9.79}, {'name': 'PM10', 'value': 20.47}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 20.47, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': 'Zero dust - zero worries!', 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 39.15}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 40.95}]}, {'fromDateTime': '2019-05-05T20:00:00.000Z', 'tillDateTime': '2019-05-05T21:00:00.000Z', 'values': [{'name': 'PM25', 'value': 11.7}, {'name': 'PM10', 'value': 23.27}], 'indexes': [{'name': 'AIRLY_CAQI', 'value': 23.27, 'level': 'VERY_LOW', 'description': 'Great air here today!', 'advice': "It couldn't be better ;)", 'color': '#6BC926'}], 'standards': [{'name': 'WHO', 'pollutant': 'PM25', 'limit': 25.0, 'percent': 46.81}, {'name': 'WHO', 'pollutant': 'PM10', 'limit': 50.0, 'percent': 46.55}]}]}
"""