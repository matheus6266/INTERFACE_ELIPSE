from e3 import elipse
from threading import Thread
import requests
import json
import time
import asyncio
import websockets
requests.packages.urllib3.disable_warnings()

r_data=[["Velocidade_kmh",0],["Forca_calibrada",0],["RPM_encoder",0],["Forca_Raw",0]]

class crio:
    def __init__(self,url):
            self.url=url

    def post(self,endpoint,data):
        result=requests.post(self.url+"/"+endpoint,json=data,verify=False)
        return (result.text)

    def get(self,endpoint):
        result=requests.get(url=self.url+endpoint)
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


def LabView_Failure_status():
    key="LabVIEW_Server_Status/LabView_Failure_status"
    hb=1
    while 1:
        try:
            resultado=c.get(key)
            e3.write_tag([["Dados.LabView_Failure_status.System_Failure_Pneumatico",resultado["System_Failure_Pneumatico"]],["Dados.LabView_Failure_status.System_Failure_FC_Roletes",resultado["System_Failure_FC_Roletes"]],["Dados.LabView_Failure_status.System_Failure_Geral",resultado["System_Failure_Geral"]],["Dados.LabView_Failure_status.System_Failure_Inversor",resultado["System_Failure_Inversor"]],["Dados.LabView_Failure_status.System_Failure_List",resultado["System_Failure_List"]]])
            e3.write_tag(["Dados.LabView_Failure_status.hb",hb+1])
            if hb<99:
                hb=hb+1
            else:
                hb=1
        except:
            pass
        time.sleep(2)



def LabView_server_status():
    key="LabVIEW_Server_Status/LabView_server_status"
    hb=1
    while 1:
        try:
            resultado=c.get(key)
            data=[["Dados.LabView_server_status.UserMsgString",resultado["UserMsgString"]],
            ["Dados.LabView_server_status.Operation_Codes",resultado["Operation_Codes"]],
            ["Dados.LabView_server_status.System_Failure_List",resultado["System_Failure_List"]],
            ["Dados.LabView_server_status.Operation_Status",resultado["Operation_Status"]],
            ["Dados.LabView_server_status.Error_Status",resultado["Error_Status"]],
            ["Dados.LabView_server_status.System_Failure_Inversor",resultado["System_Failure_Inversor"]],
            ["Dados.LabView_server_status.Zero_RPM_Encoder",resultado["Zero_RPM_Encoder"]],
            ["Dados.LabView_server_status.System_Failure_Geral",resultado["System_Failure_Geral"]],
            ["Dados.LabView_server_status.System_Failure_Pneumatico",resultado["System_Failure_Pneumatico"]],
            ["Dados.LabView_server_status.System_Failure_FC_Roletes",resultado["System_Failure_FC_Roletes"]],
            ["Dados.LabView_server_status.hb",hb]]
            e3.write_tag(data)
            e3.write_tag(["Dados.LabView_Failure_status.hb",hb+1])
            if hb<99:
                hb=hb+1
            else:
                hb=1
        except:
            pass
        time.sleep(2)


def Operation_Curve_Loss_Dynamic():

    key = "Operations/Operation_Curve_Loss_Dynamic"
    while 1:
        try:
            t=e3.read_tag("Dados.Operation_Curve_Loss_Dynamic.iniciar")
            if t==True:
                e3.write_tag(["Dados.Operation_Curve_Loss_Dynamic.iniciar","False"])
                resultado=c.get(key)
        except:
            pass
        time.sleep(0.5)    

def Operation_Curve_Loss_Static():

    key = "Operations/Operation_Curve_Loss_Static"
    while 1:
        try:
            t=e3.read_tag("Dados.Operation_Curve_Loss_Static.iniciar")
            if t==True:
                e3.write_tag(["Dados.Operation_Curve_Loss_Static.iniciar","False"])
                resultado=c.get(key)
        except:
            pass
        time.sleep(0.5)

def Operation_SamplePositioning():

    key = "Operations/Operation_SamplePositioning"
    while 1:
        try:
            t=e3.read_tag("Dados.Operation_SamplePositioning.iniciar")
            if t==True:
                e3.write_tag(["Dados.Operation_SamplePositioning.iniciar","False"])
                print("start")
                resultado=c.get(key)
                print("end")
        except:
            pass
        time.sleep(0.5)

def Interface_Read_Datalog():

    key = "Operations_Servers_Interface/Interface_Read_Datalog"

    resultado=c.get(key)
    print(resultado)
    # O resultado é aquele vetor que usávamos para analisar os testes

def Interface_RoadTests_Driver():
    {'Distancia_percorrida': 0, 'Velocidade_Target_RoadTests': 0, 'Velocidade_Encoder_km_h': 0}
    key = "Operations_Servers_Interface/Interface_RoadTests_Driver"
    resultado=c.get(key)
    print(resultado)

def Operation_FreeTeste():
    t=e3.read_tag("Dados.TesteLivre.IniciarTeste")
    post_ope_free_teste = {
                            "coefDinaCoastDown": [140.92,0,0.04240],
                            "coefLossCurve": [-1.42657,-0.0214967,-0.000723819]
                            }
    key = "Operations/Operation_FreeTest"
    print(t)
    if t == True:
        c.post(key, post_ope_free_teste)


def Interface_FreeTest():
    key =  "Operations_Servers_Interface/Interface_FreeTest"
    tag_list = ["Dados.TesteLivre.IniciarTeste", "Dados.TesteLivre.ZeraTeste", "Dados.TesteLivre.FinalizarTeste",
                 "Dados.TesteLivre.SetPointForca","Dados.TesteLivre.SetPointVeloc", "Dados.TesteLivre.TipoTeste" ]
    
    while 1:
        try:
            t=e3.read_tag(tag_list)
            post_ope_interface_free_teste = {
                            "coefCoastDown": [140.92,0,0.04240],
                            "coefLossCurve": [-1.42657,-0.0214967,-0.000723819],
                            "VelForce": False,
                            "SetPointVel": t[4],
                            "SetPointForce": t[3],
                            "TimeInVel": 0.00,
                            "TimeInForce": 0.00,
                            "EnableForceCoastDown": False,
                            "StartTest": t[0],
                            "StopTest": t[2],
                            "ZeraDistancia": t[1],
                            "FreeTestType": t[5]
                                }
            if t[2] == True:
                e3.write_tag(["Dados.TesteLivre.FinalizarTeste","False"])
                post_ope_interface_free_teste = {
                            "coefCoastDown": [140.92,0,0.04240],
                            "coefLossCurve": [-1.42657,-0.0214967,-0.000723819],
                            "VelForce": False,
                            "SetPointVel": 0,
                            "SetPointForce": 0,
                            "TimeInVel": 0.00,
                            "TimeInForce": 0.00,
                            "EnableForceCoastDown": False,
                            "StartTest": 0,
                            "StopTest": True,
                            "ZeraDistancia": 0,
                            "FreeTestType": 0
                                }
            c.post(key, post_ope_interface_free_teste)
        except:
            pass
        time.sleep(0.5)

    
    print(e3.read_tag(tag_list))


async def test():
    async with websockets.connect('ws://169.254.62.198:6123') as websocket:
        i=0
        while 1:
            await websocket.send("{}".format(i))
            response = await websocket.recv()
            print(response)
            try:
                data=json.loads(response)
                r=[]
                for d in r_data:
                    if data[d[0]] != d[1]:
                        r.append(["Dados.websocket.{}".format(d[0]),data[d[0]]])
                        d[1]=data[d[0]]
                e3.write_tag(r)
            except:
                pass
            time.sleep(0.1)



e3=elipse()
c=crio("http://169.254.62.198:8001/DinaCON_WebService/")


Interface_FreeTest()

t=[]
t.append(Thread(target=LabView_Failure_status))
t.append(Thread(target=LabView_server_status))
t.append(Thread(target=Operation_Curve_Loss_Dynamic))
t.append(Thread(target=Operation_Curve_Loss_Static))
t.append(Thread(target=Operation_SamplePositioning))
t.append(Thread(target=Operation_FreeTeste))
t.append(Thread(target=Interface_FreeTest))

for th in t:
    th.start()
while 1:
    try:
        asyncio.get_event_loop().run_until_complete(test())
    except:
        pass
for th in t:
    th.join()







