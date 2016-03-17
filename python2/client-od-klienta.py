#!/usr/bin/python
# -*- coding: UTF-8 -*-

import suds
import hashlib
from datetime import datetime
from suds.plugin import MessagePlugin
from suds.xsd.doctor import Import, ImportDoctor
from suds.client import Client
from suds.plugin import MessagePlugin

class LogPlugin(MessagePlugin):
  def sending(self, context):
    print(str(context.envelope))
  def received(self, context):
    print(str(context.reply))




path = 'F:/_PYTHON/'


url = 'http://xxx.iai-shop.com/edi/api-setproducts.php?wsdl'
username = "???"
password = "aaa"

hashpass = hashlib.sha1(password).hexdigest()
date = datetime.now().strftime('%Y%m%d')
key = hashlib.sha1(date + hashpass).hexdigest()

'''
url_tab = {'location': 'http://alfex.iai-shop.com/edi/api-setproducts.php', 'trace' : 1}
print url_tab
'''
imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
imp.filter.add('setProducts')  # tzw "namespace" nie zawsze jest w postaci URL, w tym przypadku to "target namespace" to "setProducts"
doctor = ImportDoctor(imp)
client = Client(url, doctor=doctor,plugins=[LogPlugin()])

request = {
    'authenticate' : {
        'system_key': key,
        'system_login': username
    },
    'params': {
        'settings' : {
            'modification_type' : 'edit'
        },
        'products' : {
            'id' : int(86938),
            'retail_price' : int(22.50),  # To zaokrągli do 22
            'sizes' : {
                'size_id' : 'uniw',
                'quantity' : {
                    'stocks' : {
                        'stock_id' : int(1),
                        'quantity' : int(10)
                    }
                }
            }
        }
    }
}

# print client  # to wyswietli informacje o calym schemacie komunikacji

response = client.service.setProducts(request)

#print response