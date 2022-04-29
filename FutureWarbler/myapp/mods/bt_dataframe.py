# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:32:46 2022

@author: Tiffany
"""



#futures代表要選哪個資料集
#longshort代表要選作多還是做空的predict結果
#longshort 0 代表作多 1 代表作空


def bt_dataframe(futures,longshort,algo):
    #如果是空
    if longshort ==0:
          name = "myapp\\mods\\algodata\\"+algo+"_bt_"+futures+"_long.csv"
          #file= pd.read_csv('data/rf_bt_mtx_short.csv')
            
    #如果是多
    else:
          name = "myapp\\mods\\algodata\\"+algo+"_bt_"+futures+"_short.csv"
           

    return name








                 

                 
    