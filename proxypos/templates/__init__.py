import os
from os.path import expanduser
import sys
import json

import re
import commands

from test import test_rec

mapping = {"order_name":lambda r: r['name'],
           "total_tax": lambda r: r['total_tax'],
           "shop_name": lambda r: r['shop']['name'],
           "company_name": lambda r: r['company']['name'],
           "company_website": lambda r: r['company']['website'],
           "company_phone": lambda r: r['company']['phone'],
           "company_email": lambda r: r['company']['email'],
           "company_address":lambda r: r['company']['contact_address'],
           "company_vat": lambda r: r['company']['vat'],
           "company_registry": lambda r: r['company']['company_registry'],
           "orderlines": lambda r: r['orderlines'],
           "cashier": lambda r: r['cashier'],
           "client": lambda r: r['client'],
           "currency": lambda r: r['currency'],
           "total_discount": lambda r: r['total_discount'],
           "invoice_id": lambda r: r['invoice_id'],
           "date": lambda r: r['date'],
           "total_paid": lambda r: r['total_paid'],
           "payment_amount": lambda r: r['paymentlines'][0]['amount'],
           "payment_journal": lambda r: r['paymentlines'][0]['journal'],
           "total_with_tax": lambda r: r["total_with_tax"],
           "subtotal": lambda r: r['subtotal'],
           "change": lambda r: r['change'],
          }

def find_templates(path):
    try:
        return [f[:-4] for f in os.listdir(path)
               if f.endswith('.tmp')]
    except OSError:
        return []

def html_template(template_name,base_path,receipt):
    temporal_path = os.path.join(expanduser("~"),".proxypos/tmp")
    config = json.loads(open(os.path.join(base_path,template_name+".tmp")).read())
    template_path = os.path.join(base_path,config['path'])
    css = os.path.join(template_path,config['files']['css']).decode("utf-8")
    html = os.path.join(template_path,config['files']['template']).decode("utf-8")
    query = 'esc="(.*)"'
    query = '<t\s* esc="(.*)"\s*\/>'
    template_buffer = open(html,"rb").read()
    requested_values = re.findall(query,template_buffer)
    for requested_value in requested_values:
        query = '<t\s* esc="'+requested_value+'"\s*\/>'
        value = mapping[requested_value](receipt)
        if value == False:
            value = "False"
        template_buffer = re.sub(query,value,template_buffer)
    filename = os.path.join(temporal_path,"ticket.html")
    try:
        f = open(filename,"wb")
        f.write(template_buffer)
        f.close()
        files = commands.wkhtmltoimage(filename,css,config["width"].decode("utf-8"))
    except OSError:
        print "Error: Cannot write to ticket.html"

    

def text_template(template_name,receipt):
    pass

template_types = {'image': html_template,
                  'text': text_template,
                 }

def get_templates(path,types=['image','text'],full=False):
    _templates = {}
    for tmp in find_templates(path):
        f = open(path+"/"+tmp+".tmp","rb").read()
        template_conf = json.loads(f)
        if template_conf['type'] in types:
            template_name = template_conf['name']
            template_type = template_conf['type']
            if full:
                _templates[tmp] = template_conf
            else:
                _templates[tmp] = (template_type.lower(),path,template_name)

    return _templates

def gen_receipt(template_name,receipt,paths):
    templates = {}
    for path in paths:
        templates.update(get_templates(path))
    if template_name in list(templates):
        template_type,base_path,_ = templates[template_name]
        template_types[template_type](template_name,base_path,receipt)

if __name__ == "__main__":
    paths = [os.path.dirname(os.path.abspath(__file__)),]
    get_templates(os.path.dirname(os.path.abspath(__file__)))
    gen_receipt('default',test_rec,paths)
