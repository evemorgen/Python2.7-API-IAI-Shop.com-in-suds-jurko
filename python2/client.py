#!/usr/bin/env python
# -*- coding: utf-8 -*-

from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor
import hashlib
import datetime
import pprint
from suds.plugin import MessagePlugin

class LogPlugin(MessagePlugin):
  def sending(self, context):
    print(str(context.envelope))
  def received(self, context):
    print(str(context.reply))




SHOP_NAME = "xxx"
PANEL_LOGIN = "???"
PANEL_PASS = "aaa"

url = "http://" + SHOP_NAME + ".iai-shop.com/edi/api-setproducts.php?wsdl"

imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
imp.filter.add("setProducts")
client = Client(url,doctor=ImportDoctor(imp),plugins=[LogPlugin()])

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
)

client.service.setProducts(req)