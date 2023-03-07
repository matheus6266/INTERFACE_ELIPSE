from e3 import elipse
from threading import Thread
import requests
import json
import time
requests.packages.urllib3.disable_warnings()

#Ler json
json_file=open('dina/data.json')
json_data=json.load(json_file)
json_file.close()

class crio:
    def __init__(self,url):
            self.url=url

    def post(self,endpoint,data):
        result=requests.post(self.url+"/"+endpoint,json=data,verify=False)
        return (result.text)

    def get(self,endpoint):
        result=requests.get(url=endpoint)
        return json.loads(result.text)
        

def processa_api(key):
    endp=key
    method=json_data[key]["method"]
    payload=json_data[key]["payload"]
    response=json_data[key]["response"]
    if method=="post":
        p={}
        for q in json_data[key]["payload"]:
            if json_data[key]["payload"][q]["format"]=="int":
                p[q]=int(e3.read_tag(json_data[key]["payload"][q]["tag"]))
            elif json_data[key]["payload"][q]["format"]=="float":
                print("aqui mesmo")
                p[q]=float(e3.read_tag(json_data[key]["payload"][q]["tag"]))
            elif json_data[key]["payload"][q]["format"]=="str":
                p[q]=str(e3.read_tag(json_data[key]["payload"][q]["tag"]))
        print(p)
        print(endp)
        r=c.post(endp,p)
        print(r)
        resposta=json.loads(c.post(endp,p))
        print("fez")
        print(resposta)
        for q in json_data[key]["response"]:
            response[q]
            e3.write_tag([response[q],resposta[q]])
    response=[]



def Operation_LoadCellCalibration():
    while 1:
        try:  
            key="Operation_LoadCellCalibration"
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.btn_envia")==True:
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.btn_envia",False])
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.info","Iniciando envio."])
                endp=key
                p=[]
                for i in range(1,21):
                    p.append("Dados.apis.Operation_LoadCellCalibration.P{}".format(i))
                r=e3.read_tag(p)
                if None in r:
                    e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.info","Falha no envio!"])
                    return
                else:
                    data={
                        "P1_P10":[r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9]],
                        "P11_P20":[r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18],r[19]]
                    }
                    c.post(endp,data)
                    e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.info","Enviado!"])
        except:
            pass

def Operation_Warmup():
    while 1:
        try:  
            key="Operation_Warmup"
            if e3.read_tag("Dados.apis.Operation_Warmup.btn_envia")==True:
                e3.write_tag(["Dados.apis.Operation_Warmup.btn_envia",False])
                e3.write_tag(["Dados.apis.Operation_Warmup.info","Iniciando envio."])
                endp=key
                data={
                    "warmupVelocity":[50,80,100,120,0],
                    "P11_P20":[15,15,15,15,5]
                }
                c.post(endp,data)
                e3.write_tag(["Dados.apis.Operation_Warmup.info","Enviado!"])
        except:
            pass



def endpoint1():
    while 1:
        try:
            t=e3.read_tag("Dados.apis.endpoint1.btn_atualiza")
            if t==True:
                e3.write_tag(["Dados.apis.endpoint1.btn_atualiza","False"])
                processa_api("operationloadcell")       
        except Exception as e:
            print(e)


def endpoint2():
    while 1:
        try:
            #t=e3.read_tag("Dados.apis.endpoint1.btn_calibrar")
            #if t==True:
            if 1:
                #e3.write_tag(["Dados.apis.endpoint1.btn_calibrar","False"])
                processa_api("Operation_LoadCellCalibration")       
        except Exception as e:
            print(e)
        time.sleep(2)

e3=elipse()

#be=e3.read_tag("Dados.Interface1.Btn_Enviar")

#print(be)

c=crio("http://127.0.0.1:8000")

Operation_LoadCellCalibration()


t1=Thread(target=Operation_LoadCellCalibration)



t1.start()



t1.join()


print("acabou")

#x=c.post("items/",{"ss":3})
#print(x)
#data_example={
#    "id":0,
#    "jsonrpc":"2.0",
#    "method":"PlcProgram.Read",
#    "params":{
#        "var":"\""+1+"\"."+2
#    }
#}

#"operationloadcell2":{
#        "method":"post",
#        "payload":{
#            "data1":"Dados.apis.endpoint1.info1",
#            "data2":"Dados.apis.endpoint1.info2"
#        },
#        "response":{
#        }
#    }