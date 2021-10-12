import requests
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import usersDB

RamiLevi='רמי לוי'
osherad='אושר עד'
yohananof='יוחננוף'


def get_graph(items,uid):


    stores=usersDB.get_stores(uid)

    items=items.split(',')


    if (not stores) or (not items):
        return

    def get_sum(store,items):

        _sum=0

        for item in items:
            try:
                _sum+=float(json.loads(requests.get("https://yonilabell.pythonanywhere.com/getp/"+str(store)+"/"+item).content)["price"])
            except:
                return 0
        return _sum

    sums=[get_sum(store,items) for store in stores]

    def store_name(store):
        astor=requests.get("https://yonilabell.pythonanywhere.com/getstore/"+str(store))
        j=json.loads(astor.content)
        snm=str(j['0']).split('\n')[0].replace(':','')
        r=str(store).split('/')[0].replace("osherad",osherad).replace("RamiLevi",RamiLevi).replace("yohananof",yohananof)+' '+snm
        return r[::-1]

    stores_name=[store_name(n) for n in stores]


    matplotlib.use("Agg")
    x = np.array(stores_name)
    y = np.array(sums)

    plt.bar(x,y)
    plt.savefig(uid+"graph.png")
    plt.close('all')







