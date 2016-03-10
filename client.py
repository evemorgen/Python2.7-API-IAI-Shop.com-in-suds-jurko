#!/usr/bin/env python
# -*- coding: utf-8 -*-

from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor
import hashlib
import datetime
import pprint





SHOP_NAME = "???"
PANEL_LOGIN = "login"
PANEL_PASS = "password"

url = "http://" + SHOP_NAME + ".iai-shop.com/edi/api-setproducts.php?wsdl"

imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
imp.filter.add("setProducts")
client = Client(url,doctor=ImportDoctor(imp))

#print client




req = {}
req['authenticate'] = {}
#dane do uwierzytelnienia
req['authenticate']['system_key'] = hashlib.sha1(datetime.datetime.now().strftime("%Y%m%d") + hashlib.sha1(PANEL_PASS).hexdigest()).hexdigest()
req['authenticate']['system_login'] = PANEL_LOGIN
#tablica parametrów (w pythonie słownik)
req['params'] = {}
#tablica ustawien konfiguracyjnych wywolania bramki
req['params']['settings'] = {}
req['params']['settings']['modification_type'] = 'edit';
#tablica produktow do edycji
req['params']['products'] = (
    {
        'id': 1175014091, #identyfikator produktu (nalezy podac wlasciwy dla jednego z prdodktow z wlasneogo panelu)
        'retail_price': 22.50, #cena detaliczna brutto
        #tablica danych rozmiarowych
        'sizes': (
            {
                'size_id': 'uniw',  #identyfikator rozmiaru
                #tablica stanow magazynowych (ilosci produktu)
                'quantity': {
                    #tablica magazynow
                    'stocks': (
                        {
                            'stock_id': 1,      #id magazynu
                            'quantity': 10      #nowy stan magazynowy (ilosc)
                        },
                        {
                            'stock_id': 2,      #id magazynu
                            'quantity_add': 5   #dodanie do aktualnej ilości 5 sztuk (powiększenie stanu magazynowego)
                        }
                    )
                }
            },
        )
    },

    # edycja danych produktu identyfikowanego tylko po kodzie
    # zewnetrznego systemu - przydatna w przypadku gdy nieznaze
    # jest id produktu oraz id rozmiaru
    {
        'product_sizecode': 'ABCD', #kod zewnetrznego systemu
        'note': "produkt edytowany przez api w Pythonie :)", #adnotacja
        #nazwa produktu
        'name': {
            #tablica jezykow, w ktorych podana jest nazwa
            'languages': (
                {
                    'language_id': "pol",       #identyfikator jezyka
                    'value': 'nazwa produktu'   #nazwa
                },
            )
        },
        #opis krotki produktu
        'description': {
            #tablica jezykow, w ktorych podany jest opis krotki
            'languages': (
                {
                    'language_id': 'pol',       #identyfikator jezyka
                    'value': 'przykladowy opis' #opis krotki
                },
            )
        },
        #opis dlugi produktu
        'long_description': {
            #tablica jezykow, w ktorych podany jest opis krotki
            'languages': (
                {
                    'language_id': 'pol',       #identyfikator jezyka
                    'value': 'przykladowy opis' #opis dlugi
                },
            )
        },
        #tablica elementow zaleznych od kodu zewnetrznego systemu
        'product_sizecode_data': {
            'retail_price': 86.99,          #cena detaliczna brutto
            'wholesale_price': 70,          #cena hurtowa brutto
            #tablica stanow magazynowych (ilosci produktu)
            'quantity': {
                #tablica magazynow
                'stocks': (
                    {
                        'stock_id': 1,      #id magazynu
                        'quantity': 25      #nowy stan magazynowy (ilosc)
                    },
                    {
                        'stock_id': 2,      #id magazynu
                        'quantity_add': 5   #dodanie do aktualnej ilości 5 sztuk (powiększenie stanu magazynowego)
                    }
                )
            }
        }

    }
)

client.service.setProducts(req)
print client.last_sent()