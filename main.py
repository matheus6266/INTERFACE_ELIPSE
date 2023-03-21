from e3 import elipse
from threading import Thread
import requests
import json
import time
import asyncio
import websockets
requests.packages.urllib3.disable_warnings()

r_data=[
    ["Velocidade_kmh",99999],
    ["Forca_calibrada",999999],
    ["Distancia_Percorrida",999999],
    ["Operation_Status",999999],
    ["Operation_Codes",999999],
    ["User_msg","mortadela"],
    ["Ind_Pressao_Ar",""],
    ["Ind_Sistema_Pressao_Ar",""],
    ["Ind_Botao_Emegencia_Painel_H2",""],
    ["Ind_Botao_Emegencia_Painel_F1",""],
    ["Ind_Botao_Emergencia_CR",""],
    ["Ind_Falha_Seguranca",""],
    ["Ind_Tensao_Comando",""],
    ["Ind_Stop_Usuario",""],
    ["System_Failure_Geral_Ind",""],
    ["System_Failure_Inversor_Ind",""],
    ["System_Failure_Pneumatico_Ind",""],
    ["System_Failure_FC_Roletes_Ind",""],
    ["Ind_Disjuntor_Comando",""],
    ["Ind_Disjuntor_Aquecimento",""],
    ["Ind_Disjuntor_Ventilador",""],
    ["Ind_Falha_Inversor",""],
    ["Ind_Falha_Modos_Operacao_CC",""],
    ["Ind_Alerta_Sobreaquecimento_Motor_CA",""],
    ["Ind_Sobreaquecimento_Motor_CA",""],
    ["Failure_Rotacao_Maxima_Atingida",""],
    ["Failure_FC_Sup_Rol_Post_Esquerdo",""],
    ["Failure_FC_Sup_Rol_Post_Direito",""],
    ["Failure_FC_Sup_Rol_Ant_Esquerdo",""],
    ["Failure_FC_Sup_Rol_Ant_Direito",""],
    ["Failure_FC_Inf_Rol_Post_Esquerdo",""],
    ["Failure_FC_Inf_Rol_Post_Direito",""],
    ["Failure_FC_Inf_Rol_Ant_Esquerdo",""],
    ["Failure_FC_Inf_Rol_Ant_Direito",""],
    ["System_Reset",""],
    ["Rolo_Inputs",""]
]

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
            for i in range(0,len(dados_recebidos)):
                if dados_recebidos[i]==None:
                    dados_recebidos[i]=0
            dados_envia= {
                "coefDinaCoastDown": [float(dados_recebidos[0]),float(dados_recebidos[1]),float(dados_recebidos[2])],
                "coefLossCurve": [float(dados_recebidos[3]),float(dados_recebidos[4]),float(dados_recebidos[5])]
            }
            print(key)
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
                print("Botao")
                e3.write_tag(["Dados.apis.Operation_Warmup.btn",False])
                dados_recebidos=e3.read_tag(tag_list)
                dados_enviar={
                    "warmupVelocity": [int(dados_recebidos[0]),int(dados_recebidos[1]),int(dados_recebidos[2]),int(dados_recebidos[3]),int(dados_recebidos[4])],
                    "warmupTime": [int(dados_recebidos[5]),int(dados_recebidos[6]),int(dados_recebidos[7]),int(dados_recebidos[8]),int(dados_recebidos[9])]
                }
                c.post(key,dados_enviar)
        except Exception as e:
            print(e)
        time.sleep(0.5)




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
        "Dados.apis.FreeTest.coefCoastDown.t1",
        "Dados.apis.FreeTest.coefCoastDown.t2",
        "Dados.apis.FreeTest.coefCoastDown.t3",
        "Dados.apis.FreeTest.coefLossCurve.t1",
        "Dados.apis.FreeTest.coefLossCurve.t2",
        "Dados.apis.FreeTest.coefLossCurve.t3", 
        "Dados.apis.FreeTest.VelForce",
        "Dados.apis.FreeTest.SetPointVel",
        "Dados.apis.FreeTest.SetPointForce",
        "Dados.apis.FreeTest.TimeInVel",
        "Dados.apis.FreeTest.TimeInForce",
        "Dados.apis.FreeTest.EnableForceCoastDown",
        "Dados.apis.FreeTest.StartTest",
        "Dados.apis.FreeTest.StopTest",
        "Dados.apis.FreeTest.ZeraDistancia",
        "Dados.apis.FreeTest.FreeTestType"
    ]
    while 1:
        try:
            b=e3.read_tag("Dados.apis.FreeTest.atualiza")
            if b == True:
                e3.write_tag([["Dados.apis.FreeTest.atualiza","False"],["Dados.apis.FreeTest.StopTest","False"],["Dados.apis.FreeTest.ZeraDistancia","False"]])
                t=e3.read_tag(tag_list)
                for i in range(0,len(t)):
                    if t[i]==None:
                        t[i]=0
                print(t)
                post_ope_interface_free_teste = {
                    "coefCoastDown": [float(t[0]),float(t[1]),float(t[2])],
                    "coefLossCurve": [float(t[3]),float(t[4]),float(t[5])],
                    "VelForce": t[6]==True,
                    "SetPointVel": float(t[7]),
                    "SetPointForce": float(t[8]),
                    "TimeInVel": float(t[9]),
                    "TimeInForce": float(t[10]),
                    "EnableForceCoastDown": t[11]==True,
                    "StartTest": t[12]==True,
                    "StopTest": t[13]==True,
                    "ZeraDistancia": t[14]==True,
                    "FreeTestType": int(t[15])
                }
                print(post_ope_interface_free_teste)
                c.post(key, post_ope_interface_free_teste)
        except Exception as e:
            print(e)
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
    key="Operations_Servers_Interface/Interface_RoadTests"
    while 1:
        try:
            if e3.read_tag("Dados.apis.Operation_Warmup.atualiza")==True:
                e3.write_tag(["Dados.apis.Operation_Warmup.atualiza","False"])
                t=e3.read_tag("Dados.apis.Operation_Warmup.stop")
                post_ope_interface_free_teste = {
                    "TestStart": False,
                    "UserStop": t
                }    
                c.post(key, post_ope_interface_free_teste)
                time.sleep(0.5)
                post_ope_interface_free_teste = {
                    "TestStart": False,
                    "UserStop": False
                }    
                c.post(key, post_ope_interface_free_teste)
        except:
            pass
        time.sleep(0.5)

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
        time.sleep(5)
        i=0
        while 1:
            await websocket.send("{}".format(i))
            response = await websocket.recv()
            try:
                data=json.loads(response)
                r=[]
                for d in r_data:
                    if data[d[0]] != d[1]:
                        r.append(["Dados.apis.websocket.{}".format(d[0]),data[d[0]]])
                        d[1]=data[d[0]]
                if r!=[]:
                    e3.write_tag(r)
            except Exception as e:
                print("Falha:{}{}".format(e,d[0]))
            time.sleep(0.1)



e3=elipse()
c=crio("http://169.254.62.198:8001/DinaCON_WebService/")



t=[]
t.append(Thread(target=Operation_Warmup))
t.append(Thread(target=Interface_RoadTests))
t.append(Thread(target=Operation_SamplePositioning))
t.append(Thread(target=Interface_FreeTest))
t.append(Thread(target=Operation_FreeTest))



for th in t:
    th.start()
while 1:
    try:
        asyncio.get_event_loop().run_until_complete(wsocket())
    except:
        pass
for th in t:
    th.join()