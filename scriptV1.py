import re
import requests
import wget
from urllib.request import urlopen
from wsgiref import headers
from bs4 import BeautifulSoup

# -> url de prueba https://realpython.com/beautiful-soup-web-scraper-python/
# -> url target  https://www.idealista.com/inmueble/99306274/
# -> url target  https://www.idealista.com/inmueble/97659036/
# -> url target  https://www.idealista.com/inmueble/99045533/
# -> url target  https://www.idealista.com/inmueble/97053579/
# -> url target  https://www.idealista.com/inmueble/95217863/
# https://www.idealista.com/inmueble/99306274/foto/2/
def descargar_pagina_y_formatear_html(URL, headers):
    page = requests.get(URL, headers=headers)
    web_complet = BeautifulSoup(page.content, 'html.parser')
    results = web_complet.find_all('script')
    print(results)
    return results

def encontrar_etiqueta(results):
    for element in results:
        element = str(element)
        if re.findall('fullScreenGalleryPics', element):
            element_find = element
            f = open('idealista.txt','w')
            f.write(element)
            f.close()

def preparar_la_pagina_web():
    #URL = "https://www.idealista.com/inmueble/99164272"
    URL = input("Introduce la página web ")
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "es-ES,es;q=0.9",
        "cache-control": "max-age=0",
        "referer": "https://www.idealista.com/venta-viviendas/valencia/l-horta-nord/con-chalets/pagina-2.htm",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "Android",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
    }
    descargamos_web = descargar_pagina_y_formatear_html(URL, headers)
    encontramos_etiqueta = encontrar_etiqueta(descargamos_web)
    
preparar_la_pagina_web()


with open('idealista.txt') as archivo:
    while (line := archivo.readlines()):
        f = open('fotos_bruto.txt','w')
        f.write(line[115])
        f.close()

with open('fotos_bruto.txt') as f:
    lines = f.readlines()
    result_split = lines[0].split(',')
lista_url = []

for element in result_split:
    if "WEB_DETAIL" in element:
        lista_url.append(element[18:])
        
for url_photo in lista_url:
    if 'https' in url_photo:
        wget.download(url_photo, 'd:/devcode/Scrapy-Idealista/fotos/99164272')
        print("Descargando en la carpeta fotos la url ", url_photo)
    
