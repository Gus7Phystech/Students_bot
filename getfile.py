from libraries import *

f = open('received\\1-kurs-osen-2020.xls',"wb")
ufr = requests.get('https://mipt.ru/upload/medialibrary/2e2/1-kurs-osen-2020.xls')
f.write(ufr.content)
f.close()
