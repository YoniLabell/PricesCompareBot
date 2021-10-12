
import requests
import json
import matplotlib

import matplotlib.pyplot as plt
import numpy as np


def createpng(items_text,uid):

    matplotlib.use("Agg")

    storlist=['osherad','yohananof','RamiLevi']

    items_list=items_text.split(',')


    items_dict={}

    for item in items_list:
        response=requests.get("http://yonilabell.pythonanywhere.com/getitembymame/"+item)
        price=json.loads(response.content)
        items_dict[item]=price



    def mysum(storname):

        sum=0
        for item in items_dict.values():

            if storname in item['storname'].keys():


                sum+=float(item['storname'][storname]['Price'])
            else:
                return 0
        return sum

    sums_list=[]
    for name in storlist:
        sum=mysum(name)
        sums_list.append(sum)




    x = np.array(storlist)
    y = np.array(sums_list)

    plt.bar(x,y)
    plt.savefig(uid+"graph.png")
    plt.close('all')

    return str(items_dict)


