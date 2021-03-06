import time
import urllib
import json
import httplib
import os

from datetime import datetime
from liblabiot import opencfg

import base64
import urllib2
import types

borneras_aire_2d = ["9031", "9033", "9035"]
borneras_tomas_2d = ["9034", "9051", "9052", "9053", "9054", "9055", "9056"]
borneras_luz_2d = ["9021", "9022", "9023"]

API_LESS = "http://52.10.233.24/v1/circuits/{0}/latest"

cfg = opencfg('labiot.cfg')
listendpoints = opencfg('listpaths.cfg')


def transform(array):

    dic = {}
    for key in range(len(array)):
        dic.update({array[key]: 0})
    return dic


def GET(url):

    # hace peticion a api en amazon, y api clima
    result = []
    try:
        response = urllib.urlopen(url)
    except:
        print "failed host {0}".format(url)
        return 0
    else:
        if response.code == 200:
            result = dict(json.load(response))
            # print result
            if result.has_key('data'):
                if result['data'][0]['proc']:
                    return result['data'][0]['proc']
            else:
                return 0
        elif response.code == 500:
            return 0
        else:
            return 0

def POST(sensor, proc={}):
    
    #print proc
    username = cfg.username
    password = cfg.password
    url = cfg.urlname
    datos = listendpoints.datos
    urlpath = url+datos[1]

    # _id
    # proc['irms'], proc['vrms'], proc['power']

    query_args = urllib.urlencode({
        "id": sensor,
        "datatype1" : "vrms",
        "data1": proc['vrms'],
        "datatype2" : "irms",
        "data2": proc['irms'],
        "datatype2" : "power",
        "data2": proc['power'],
    })

    try:
        request = urllib2.Request(urlpath)
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_data(query_args)
        request.add_header("Authorization", "Basic %s" % base64string)
        result = json.loads(urllib2.urlopen(request).read())
        print result
    except:
       return types.NoneType


def __getpost(sensor, borneras):
    

    for _id in borneras.keys():
        proc = GET(API_LESS.format(_id))
        #print proc
        if type(proc) != types.NoneType:
            borneras_tomas[_id] = proc
            if proc:
                POST(sensor, proc)
            else:
                print "sin datos"
        else:
            proc = borneras_tomas[_id]
            if proc:
                POST(sensor, proc)
            else:
                print "sin datos"
        time.sleep(10)

borneras_aire = transform(borneras_aire_2d)
borneras_tomas = transform(borneras_tomas_2d)
borneras_luz = transform(borneras_luz_2d)

if __name__ == '__main__':
    


    while True:

        __getpost("6", borneras_tomas) # id_sensor = 6, datatype  = (vrms, irms, power)
        __getpost("7", borneras_aire) # id_sensor = 7, datatype  = (vrms, irms, power)
        __getpost("8", borneras_luz) # id_sensor = 8, datatype  = (vrms, irms, power)