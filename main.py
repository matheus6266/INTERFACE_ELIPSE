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
        


#Operations

def Operation_Coast_Down():
    key = "Operations/Operation_Coast_Down"
    
    tag_list=[
        "Dados.apis.Operation_Coast_Down.coefPistaRolamento.t1",
        "Dados.apis.Operation_Coast_Down.coefPistaRolamento.t2",
        "Dados.apis.Operation_Coast_Down.coefPistaRolamento.t3",
        "Dados.apis.Operation_Coast_Down.coefLossCurve.t1",
        "Dados.apis.Operation_Coast_Down.coefLossCurve.t2",
        "Dados.apis.Operation_Coast_Down.coefLossCurve.t3",
        "Dados.apis.Operation_Coast_Down.massaAmostra"
    ]
    while 1:
        try:
            t=e3.read_tag("Dados.apis.Operation_Coast_Down.btn")
            if t==True:
                e3.write_tag(["Dados.apis.Operation_Coast_Down.btn","False"])
                dados_recebidos=e3.read_tag(tag_list)
                dados_enviar={
                    "coefPistaRolamento": [dados_recebidos[0],dados_recebidos[1],dados_recebidos[2]],
                    "massaAmostra": dados_recebidos[6],
                    "coefLossCurve": [dados_recebidos[3],dados_recebidos[4],dados_recebidos[5]]
                }
                c.post(key,dados_enviar)
        except:
            pass
        time.sleep(0.5)    

def Operation_Curve_Loss_Dynamic():

    key = "Operations/Operation_Curve_Loss_Dynamic"
    while 1:
        try:
            t=e3.read_tag("Dados.apis.Operation_Curve_Loss_Dynamic.btn")
            if t==True:
                e3.write_tag(["Dados.apis.Operation_Curve_Loss_Dynamic.btn","False"])
                resultado=c.get(key)
        except:
            pass
        time.sleep(0.5)    

def Operation_Curve_Loss_Static():

    key = "Operations/Operation_Curve_Loss_Static"
    while 1:
        try:
            t=e3.read_tag("Dados.apis.Operation_Curve_Loss_Static.btn")
            if t==True:
                e3.write_tag(["Dados.apis.Operation_Curve_Loss_Static.btn","False"])
                resultado=c.get(key)
        except:
            pass
        time.sleep(0.5)

#?
def Operation_Dina_Verification():
    pass

def Operation_FreeTest():
    key = "Operations/Operation_FreeTest"
    tag_list=[
        "Dados.apis.FreeTest.coefCoastDown.t1",
        "Dados.apis.FreeTest.coefCoastDown.t2",
        "Dados.apis.FreeTest.coefCoastDown.t3",
        "Dados.apis.FreeTest.coefLossCurve.t1",
        "Dados.apis.FreeTest.coefLossCurve.t2",
        "Dados.apis.FreeTest.coefLossCurve.t3"
    ]
    while 1:
        t=e3.read_tag("Dados.apis.FreeTest.iniciar")
        if t == True:            
            e3.write_tag(["Dados.apis.FreeTest.iniciar","False"])
            dados_recebidos=e3.read_tag(tag_list)
            dados_envia= {
                "coefDinaCoastDown": [dados_recebidos[0],dados_recebidos[1],dados_recebidos[2]],
                "coefLossCurve": [dados_recebidos[3],dados_recebidos[4],dados_recebidos[5]]
            }
            c.post(key, dados_envia)

def Operation_LoadCellCalibration():
    key="Operations/Operation_LoadCellCalibration"
    tag_list=[
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t1",
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t2",
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t3",
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t4",
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t5",
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t6",
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t7",
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t8",
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t9",
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.t10",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t1",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t2",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t3",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t4",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t5",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t6",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t7",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t8",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t9",
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.t10"
    ]
    while 1:
        try:  
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.btn")==True:
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.btn",False])
                dados_recebidos=e3.read_tag(tag_list)
                data={
                    "P1_P10":[dados_recebidos[0],dados_recebidos[1],dados_recebidos[2],dados_recebidos[3],dados_recebidos[4],dados_recebidos[5],dados_recebidos[6],dados_recebidos[7],dados_recebidos[8],dados_recebidos[9]],
                    "P11_P20":[dados_recebidos[10],dados_recebidos[11],dados_recebidos[12],dados_recebidos[13],dados_recebidos[14],dados_recebidos[15],dados_recebidos[16],dados_recebidos[17],dados_recebidos[18],dados_recebidos[19]]
                }
                c.post(key,data)
        except:
            pass

#?
def Operation_RoadTest():
    pass

def Operation_SamplePositioning():
    key = "Operations/Operation_SamplePositioning"
    while 1:
        try:
            t=e3.read_tag("Dados.apis.Operation_SamplePositioning.btn")
            if t==True:
                e3.write_tag(["Dados.apis.Operation_SamplePositioning.btn","False"])
                resultado=c.get(key)
        except:
            pass
        time.sleep(0.5)


def Operation_Warmup():
    key = "Operations/Operation_Warmup"
    tag_list=[
        "Dados.apis.Operation_Warmup.warmupVelocity.t1",
        "Dados.apis.Operation_Warmup.warmupVelocity.t2",
        "Dados.apis.Operation_Warmup.warmupVelocity.t3",
        "Dados.apis.Operation_Warmup.warmupVelocity.t4",
        "Dados.apis.Operation_Warmup.warmupVelocity.t5",
        "Dados.apis.Operation_Warmup.warmupTime.t1",
        "Dados.apis.Operation_Warmup.warmupTime.t2",
        "Dados.apis.Operation_Warmup.warmupTime.t3",
        "Dados.apis.Operation_Warmup.warmupTime.t4",
        "Dados.apis.Operation_Warmup.warmupTime.t5"
    ]
    while 1:
        try:  
            if e3.read_tag("Dados.apis.Operation_Warmup.btn")==True:
                e3.write_tag(["Dados.apis.Operation_Warmup.btn",False])
                dados_recebidos=e3.read_tag(tag_list)
                dados_enviar={
                    "warmupVelocity": [dados_recebidos[0],dados_recebidos[1],dados_recebidos[2],dados_recebidos[3],dados_recebidos[4]],
                    "warmupTime": [dados_recebidos[5],dados_recebidos[6],dados_recebidos[7],dados_recebidos[8],dados_recebidos[9]]
                }
                c.post(key,dados_enviar)
                e3.write_tag(["Dados.apis.Operation_Warmup.info","Enviado!"])
        except:
            pass




#Server Interface


def Interface_Curve_Loss_Static():
    while 1:
        try:
            if e3.read_tag("Dados.apis.Operation_Curve_Loss_Static.stop"):
                e3.write_tag(["Dados.apis.Operation_Curve_Loss_Static.stop","False"])
                c.get("Operations_Servers_Interface/Interface_Curve_Loss_Static?User_Stop=True")
        except:
            pass
        time.sleep(0.5)


def Interface_FreeTest():
    key =  "Operations_Servers_Interface/Interface_FreeTest"
    tag_list = [
        "Dados.FreeTest.coefCoastDown.t1",
        "Dados.FreeTest.coefCoastDown.t2",
        "Dados.FreeTest.coefCoastDown.t3",
        "Dados.FreeTest.coefLossCurve.t1",
        "Dados.FreeTest.coefLossCurve.t2",
        "Dados.FreeTest.coefLossCurve.t3", 
        "Dados.FreeTest.VelForce",
        "Dados.FreeTest.SetPointVel",
        "Dados.FreeTest.SetPointForce",
        "Dados.FreeTest.TimeInVel",
        "Dados.FreeTest.TimeInForce",
        "Dados.FreeTest.EnableForceCoastDown",
        "Dados.FreeTest.StartTest",
        "Dados.FreeTest.StopTest",
        "Dados.FreeTest.ZeraDistancia",
        "Dados.FreeTest.FreeTestType"
    ]
    while 1:
        try:
            b=e3.read_tag("Dados.FreeTest.atualiza")
            if b == True:
                e3.write_tag(["Dados.FreeTest.atualiza","False"])
                t=e3.read_tag(tag_list)
                post_ope_interface_free_teste = {
                    "coefCoastDown": [t[0],t[1],t[2]],
                    "coefLossCurve": [t[3],t[4],t[5]],
                    "VelForce": bool(t[6]),
                    "SetPointVel": t[7],
                    "SetPointForce": t[8],
                    "TimeInVel": t[9],
                    "TimeInForce": t[10],
                    "EnableForceCoastDown": bool(t[11]),
                    "StartTest": t[12],
                    "StopTest": t[13],
                    "ZeraDistancia": t[14],
                    "FreeTestType": t[15]
                }    
                c.post(key, post_ope_interface_free_teste)
        except:
            pass
        time.sleep(0.5)

def Interface_Input_LoadCell_Arrays():
    key="Operations_Servers_Interface/Interface_Input_LoadCell_Arrays"
    tag_list=[
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t1",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t2",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t3",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t4",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t5",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t6",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t7",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t8",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t9",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t10",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t11",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t12",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t13",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t14",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t15",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t16",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t17",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t18",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t19",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t20",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t21",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t1",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t2",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t3",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t4",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t5",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t6",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t7",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t8",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t9",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t10",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t11",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t12",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t13",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t14",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t15",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t16",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t17",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t18",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t19",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t20",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t21",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t1",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t2",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t3",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t4",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t5",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t6",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t7",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t8",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t9",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t10",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t11",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t12",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t13",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t14",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t15",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t16",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t17",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t18",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t19",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t20",
        "Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t21"
    ]   
    while 1:
        try:
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.envia"):
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.envia",False])
                dados_recebidos=e3.read_tag(tag_list)
                dados_enviar={
                    "Data_LoadCell_Calibrated": [dados_recebidos[0],dados_recebidos[1],dados_recebidos[2],dados_recebidos[3],dados_recebidos[4],dados_recebidos[5],dados_recebidos[6],dados_recebidos[7],dados_recebidos[8],dados_recebidos[9],dados_recebidos[10],dados_recebidos[11],dados_recebidos[12],dados_recebidos[13],dados_recebidos[14],dados_recebidos[15],dados_recebidos[16],dados_recebidos[17],dados_recebidos[18],dados_recebidos[19],dados_recebidos[20]],
                    "Data_LoadCell_Raw": [dados_recebidos[20],dados_recebidos[21],dados_recebidos[22],dados_recebidos[23],dados_recebidos[24],dados_recebidos[25],dados_recebidos[26],dados_recebidos[27],dados_recebidos[28],dados_recebidos[29],dados_recebidos[20],dados_recebidos[21],dados_recebidos[22],dados_recebidos[23],dados_recebidos[24],dados_recebidos[25],dados_recebidos[26],dados_recebidos[27],dados_recebidos[28],dados_recebidos[29],dados_recebidos[30]],
                    "Data_LoadCell_Uncertainties": [dados_recebidos[30],dados_recebidos[31],dados_recebidos[32],dados_recebidos[33],dados_recebidos[34],dados_recebidos[35],dados_recebidos[36],dados_recebidos[37],dados_recebidos[38],dados_recebidos[39],dados_recebidos[40],dados_recebidos[41],dados_recebidos[42],dados_recebidos[43],dados_recebidos[44],dados_recebidos[45],dados_recebidos[46],dados_recebidos[47],dados_recebidos[48],dados_recebidos[49],dados_recebidos[50]]
                }
                c.post(key,dados_enviar)
        except:
            pass

def Interface_LoadCellCalibration():
    key="Operations_Servers_Interface/Interface_LoadCellCalibration"
    tag_list=[
        ""
    ]
    while 1:
        try:
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.ok"):
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.ok","False"])
                dados_enviar={
                    "okButton": True,
                    "stopButton": False
                }
                c.post(key,dados_enviar)
                time.sleep(0.5)
                dados_enviar={
                    "okButton": False,
                    "stopButton": False
                }
                c.post(key,dados_enviar)
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.stop"):
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.stop","False"])
                dados_enviar={
                    "okButton": False,
                    "stopButton": True
                }
                c.post(key,dados_enviar)
                time.sleep(0.5)
                dados_enviar={
                    "okButton": False,
                    "stopButton": False
                }
                c.post(key,dados_enviar)
        except:
            pass
        time.sleep(0.5)


def Interface_Output_test():
    tag_list=[
        "man_auto_test",
        "vel_torq_test",
        "setpoint-vel",
        "setpoint_torq",
        "time_in_torq",
        "time_in_vel"
    ]
    while 1:
        try:
            if e3.read_tag("Dados.apis.Interface_Output_test.atualiza"):
                e3.write_tag(["Dados.apis.Interface_Output_test.atualiza","False"])
                dados_recebidos=e3.read_tag(tag_list)
                c.get("Operations_Servers_Interface/Interface_Output_test?man_auto_test={}&vel_torq_test={}&setpoint-vel={}&setpoint_torq={}&time_in_torq={}&time_in_vel={}".format(dados_recebidos[0],dados_recebidos[1],dados_recebidos[2],dados_recebidos[3],dados_recebidos[4],dados_recebidos[5]))
        except:
            pass
        time.sleep(0.5)

#?        
def Interface_Read_Datalog():
    pass

#?
def Interface_RoadTests():
    pass

#?
def Interface_RoadTests_Driver():
    pass

#?
def Interface_SamplePositioning():
    pass



def Interface_RoadTests_Driver():
    {'Distancia_percorrida': 0, 'Velocidade_Target_RoadTests': 0, 'Velocidade_Encoder_km_h': 0}
    key = "Operations_Servers_Interface/Interface_RoadTests_Driver"
    resultado=c.get(key)



async def wsocket():
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
t.append(Thread(target=Operation_Curve_Loss_Dynamic))


for th in t:
    th.start()
while 1:
    try:
        asyncio.get_event_loop().run_until_complete(wsocket())
    except:
        pass
for th in t:
    th.join()