from e3 import elipse
from threading import Thread
import requests
import json
import time
import asyncio
import websockets
import PySimpleGUI as sg
import time

requests.packages.urllib3.disable_warnings()

send_calibration=False

r_data=[
    ["Velocidade_kmh",99999],
    ["Forca_calibrada",999999],
    ["Distancia_Percorrida",999999],
    ["Operation_Status",999999],
    ["Operation_Codes",999999],
    ["User_msg","mortadela"],
    ["Falhas",""],
    ["Rolo_Inputs",""],
    ["Calibration_Stage",""],
    ["Distancia_Durabilidade",""],
    ["Velocidade_Durabilidade",""],
    ["Controle_Remoto",""]
]

time_screen_diagnostics = 0
time_Operation_Warmup = 0
time_Interface_RoadTests = 0
time_Operation_SamplePositioning = 0
time_Interface_SamplePositioning = 0
time_Interface_FreeTest = 0
time_Operation_FreeTest = 0
time_Operation_LoadCellCalibration = 0
time_Interface_Input_LoadCell_Arrays = 0
time_Interface_LoadCellCalibration = 0
time_Interface_Open_Alcapao_PL = 0
time_Operation_Coast_Down = 0
time_Operation_Coast_Down_R2 = 0
time_Operation_RoadTest = 0
time_Operation_Curve_Loss_Static = 0
time_Interface_Curve_Loss_Static = 0
time_Operation_Durab_Teste = 0
time_web_socket = 0

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
    global time_Operation_Coast_Down
    key = "Operations/Operation_Coast_Down"
    
    tag_list=[
        "Dados.amostraselecionada.cApista",
        "Dados.amostraselecionada.cBpista",
        "Dados.amostraselecionada.cCpista",
        "Dados.apis.Operation_Curve_Loss_Static.f0",
        "Dados.apis.Operation_Curve_Loss_Static.f1",
        "Dados.apis.Operation_Curve_Loss_Static.f2",
        "Dados.amostraselecionada.massa"
    ]
    while 1:
        start_time = time.time()
        try:
            t=e3.read_tag("Dados.apis.Operation_Coast_Down.btn")
            if t==True:
                e3.write_tag(["Dados.apis.Operation_Coast_Down.btn","False"])
                dados_recebidos=e3.read_tag(tag_list)                
                for r in range(0,len(dados_recebidos)):
                    if dados_recebidos[r]=='':
                        dados_recebidos[r]=0
                dados_enviar={
                    "coefPistaRolamento": [float(str(dados_recebidos[0]).replace(",",".")),float(str(dados_recebidos[1]).replace(",",".")),float(str(dados_recebidos[2]).replace(",","."))],
                    "massaAmostra": float(str(dados_recebidos[6]).replace(",",".")),
                    "coefLossCurve": [float(str(dados_recebidos[3]).replace(",",".")),float(str(dados_recebidos[4]).replace(",",".")),float(str(dados_recebidos[5]).replace(",","."))]
                }
                r=c.post(key,dados_enviar)
                r=json.loads(r)
                e3.write_tag([
                    ["Dados.amostraselecionada.cAcalculado",r["coefPistaDina_Calc"][0]],
                    ["Dados.amostraselecionada.cBcalculado",r["coefPistaDina_Calc"][1]],
                    ["Dados.amostraselecionada.cCcalculado",r["coefPistaDina_Calc"][2]]]
                )
        except Exception as e:
            print(e)
        time.sleep(0.5)
        time_Operation_Coast_Down = time.time() - start_time
        

def Operation_Coast_Down_R2():
    global time_Operation_Coast_Down_R2
    key = "Operations/Operation_Coast_Down_R02"
    
    tag_list=[
        "Dados.amostraselecionada.cApista",
        "Dados.amostraselecionada.cBpista",
        "Dados.amostraselecionada.cCpista",
        "Dados.apis.Operation_Curve_Loss_Static.f0",
        "Dados.apis.Operation_Curve_Loss_Static.f1",
        "Dados.apis.Operation_Curve_Loss_Static.f2",
        "Dados.amostraselecionada.massa"
    ]
    while 1:
        start_time = time.time()
        try:
            t=e3.read_tag("Dados.apis.Operation_Coast_Down.btn")
            if t==True:
                e3.write_tag(["Dados.apis.Operation_Coast_Down.btn","False"])
                dados_recebidos=e3.read_tag(tag_list)                
                for r in range(0,len(dados_recebidos)):
                    if dados_recebidos[r]=='':
                        dados_recebidos[r]=0
                dados_enviar={
                    "coefPistaRolamento": [float(str(dados_recebidos[0]).replace(",",".")),float(str(dados_recebidos[1]).replace(",",".")),float(str(dados_recebidos[2]).replace(",","."))],
                    "massaAmostra": float(str(dados_recebidos[6]).replace(",",".")),
                    "coefLossCurve": [float(str(dados_recebidos[3]).replace(",",".")),float(str(dados_recebidos[4]).replace(",",".")),float(str(dados_recebidos[5]).replace(",","."))]
                }
                r=c.post(key,dados_enviar)
                r=json.loads(r)
                e3.write_tag([
                    ["Dados.amostraselecionada.cAcalculado",r["coefPistaDina_Calc"][0]],
                    ["Dados.amostraselecionada.cBcalculado",r["coefPistaDina_Calc"][1]],
                    ["Dados.amostraselecionada.cCcalculado",r["coefPistaDina_Calc"][2]]]
                )
        except Exception as e:
            print(e)
        time.sleep(0.5)
        time_Operation_Coast_Down_R2 = time.time() - start_time    

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
    global time_Operation_Curve_Loss_Static
    key = "Operations/Operation_Curve_Loss_Static"
    while 1:
        start_time = time.time()
        try:
            t=e3.read_tag("Dados.apis.Operation_Curve_Loss_Static.btn")
            if t==True:
                e3.write_tag([["Dados.apis.Operation_Curve_Loss_Static.btn","False"],["Dados.apis.Operation_Curve_Loss_Static.f0","0"],["Dados.apis.Operation_Curve_Loss_Static.f1","0"],["Dados.apis.Operation_Curve_Loss_Static.f2","0"]])
                r=json.loads(str(c.get(key)).replace("'","\""))
                #r=json.loads(str("{'Array_Force_mean': [2.131791696848824, -36.75591981634028, -43.05322457675331, -47.09736131761025, -50.66178686313542, -53.94787085430391, -56.51531263216908, -60.27087413576736, -62.13168844806643, -64.83289104546871, -67.60879266438118, -71.54806258712011, -73.49645260316589, 0], 'Polynomial Coefficients': [-31.7576920234575, -0.4464380439978495, 0.0009325935555171616]}").replace("'","\""))
                dados = [
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo1", r["Array_Force_mean"][0]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo2", r["Array_Force_mean"][1]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo3", r["Array_Force_mean"][2]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo4", r["Array_Force_mean"][3]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo5", r["Array_Force_mean"][4]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo6", r["Array_Force_mean"][5]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo7", r["Array_Force_mean"][6]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo8", r["Array_Force_mean"][7]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo9", r["Array_Force_mean"][8]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo10",r["Array_Force_mean"][9]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo11",r["Array_Force_mean"][10]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo12",r["Array_Force_mean"][11]],
                    ["Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo13", r["Array_Force_mean"][12]],
                    ["Dados.apis.Operation_Curve_Loss_Static.f0", r['Polynomial Coefficients'][0]],
                    ["Dados.apis.Operation_Curve_Loss_Static.f1", r['Polynomial Coefficients'][1]],
                    ["Dados.apis.Operation_Curve_Loss_Static.f2", r['Polynomial Coefficients'][2]] 
                    ]
                e3.write_tag(dados)
        except Exception as e:
            print(e)
        time.sleep(0.5)
        time_Operation_Curve_Loss_Static = time.time() - start_time 

#?
def Operation_Dina_Verification():
    pass

def Operation_FreeTest():
    global time_Operation_FreeTest
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
        start_time = time.time()
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
            c.post(key, dados_envia)
            time_Operation_FreeTest = time.time() - start_time 

def Operation_LoadCellCalibration():
    global time_Operation_LoadCellCalibration
    key="Operations/Operation_LoadCellCalibration"
    tag_list=[
        "Dados.apis.Operation_LoadCellCalibration.P1_P10.h1",
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
        "Dados.apis.Operation_LoadCellCalibration.P11_P20.h1",
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
        start_time = time.time()
        try:
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.btn")==True:
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.btn",False])
                dados_recebidos=e3.read_tag(tag_list)
                for i in range(0,len(dados_recebidos)):
                    if dados_recebidos[i]==None:
                        dados_recebidos[i]=0
                data={
                    "P1_P10":[float(dados_recebidos[0]),float(dados_recebidos[1]),float(dados_recebidos[2]),float(dados_recebidos[3]),float(dados_recebidos[4]),float(dados_recebidos[5]),float(dados_recebidos[6]),float(dados_recebidos[7]),float(dados_recebidos[8]),float(dados_recebidos[9]),float(dados_recebidos[10])],
                    "P11_P20":[float(dados_recebidos[11]),float(dados_recebidos[12]),float(dados_recebidos[13]),float(dados_recebidos[14]),float(dados_recebidos[15]),float(dados_recebidos[16]),float(dados_recebidos[17]),float(dados_recebidos[18]),float(dados_recebidos[19]),float(dados_recebidos[20]),float(dados_recebidos[21])]
                }
                result=json.loads(c.post(key,data))           
                dados=[
                    ["Dados.apis.Operation_LoadCellCalibration.Data_loadCell_Calibrated.t1",result["Medicao final"][0]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t2",result["Medicao final"][1]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t3",result["Medicao final"][2]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t4",result["Medicao final"][3]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t5",result["Medicao final"][4]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t6",result["Medicao final"][5]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t7",result["Medicao final"][6]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t8",result["Medicao final"][7]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t9",result["Medicao final"][8]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t10",result["Medicao final"][9]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t11",result["Medicao final"][10]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t12",result["Medicao final"][11]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t13",result["Medicao final"][12]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t14",result["Medicao final"][13]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t15",result["Medicao final"][14]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t16",result["Medicao final"][15]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t17",result["Medicao final"][16]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t18",result["Medicao final"][17]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t19",result["Medicao final"][18]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t20",result["Medicao final"][19]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Calibrated.t21",result["Medicao final"][20]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t1",result["Sequencia Forca "][0]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t2",result["Sequencia Forca "][1]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t3",result["Sequencia Forca "][2]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t4",result["Sequencia Forca "][3]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t5",result["Sequencia Forca "][4]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t6",result["Sequencia Forca "][5]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t7",result["Sequencia Forca "][6]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t8",result["Sequencia Forca "][7]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t9",result["Sequencia Forca "][8]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t10",result["Sequencia Forca "][9]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t11",result["Sequencia Forca "][10]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t12",result["Sequencia Forca "][11]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t13",result["Sequencia Forca "][12]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t14",result["Sequencia Forca "][13]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t15",result["Sequencia Forca "][14]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t16",result["Sequencia Forca "][15]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t17",result["Sequencia Forca "][16]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t18",result["Sequencia Forca "][17]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t19",result["Sequencia Forca "][18]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t20",result["Sequencia Forca "][19]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Raw.t21",result["Sequencia Forca "][20]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t1",result["Incerteza abs final"][0]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t2",result["Incerteza abs final"][1]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t3",result["Incerteza abs final"][2]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t4",result["Incerteza abs final"][3]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t5",result["Incerteza abs final"][4]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t6",result["Incerteza abs final"][5]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t7",result["Incerteza abs final"][6]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t8",result["Incerteza abs final"][7]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t9",result["Incerteza abs final"][8]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t10",result["Incerteza abs final"][9]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t11",result["Incerteza abs final"][10]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t12",result["Incerteza abs final"][11]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t13",result["Incerteza abs final"][12]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t14",result["Incerteza abs final"][13]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t15",result["Incerteza abs final"][14]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t16",result["Incerteza abs final"][15]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t17",result["Incerteza abs final"][16]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t18",result["Incerteza abs final"][17]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t19",result["Incerteza abs final"][18]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t20",result["Incerteza abs final"][19]],
                    ["Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_Uncertainties.t21",result["Incerteza abs final"][20]],
                    ["Dados.apis.Operation_LoadCellCalibration.concluido","True"]
                ]
                e3.write_tag(dados)
        except Exception as e:
            print(e)
        time.sleep(0.5)
        time_Operation_LoadCellCalibration = time.time() - start_time 

#?
def Operation_RoadTest():
    global time_Operation_RoadTest
    key="Operations/Operation_RoadTests"
    tag_list=[
        "Dados.amostraselecionada.cAcalculado",
        "Dados.amostraselecionada.cBcalculado",
        "Dados.amostraselecionada.cCcalculado",
        "Dados.amostraselecionada.massa",
        "Dados.apis.Operation_Curve_Loss_Static.f0",
        "Dados.apis.Operation_Curve_Loss_Static.f1",
        "Dados.apis.Operation_Curve_Loss_Static.f2"
    ]
    while 1:
        start_time = time.time()
        t=e3.read_tag("Dados.apis.RoadTest.btn")
        if t == True:
            e3.write_tag(["Dados.apis.RoadTest.btn","False"])

            dados_recebidos=e3.read_tag(tag_list)
            for i in range(0,len(dados_recebidos)):
                if dados_recebidos[i]==None:
                    dados_recebidos[i]=0
            dados_envia= {
                "coefDinaCoastDown": [float(dados_recebidos[0]),float(dados_recebidos[1]),float(dados_recebidos[2])],
                "massaAmostra": float(dados_recebidos[3]),
                "coefLossCurve": [float(dados_recebidos[4]),float(dados_recebidos[5]),float(dados_recebidos[6])],
                "DurabDist": [0.0,0.0],
                "DurabVel": [1,1],
                "TypeTest": True,
                "RoadVelArray": [0 for a in range(0,60*60*24)]
            }
            c.post(key, dados_envia)
    time.sleep(0.5)
    time_Operation_RoadTest = time.time() - start_time

def Operation_Durab_Teste():
    global time_Operation_Durab_Teste
    key="Operations/Operation_RoadTests"
    tag_list=[
        "Dados.amostraselecionada.cAcalculado",
        "Dados.amostraselecionada.cBcalculado",
        "Dados.amostraselecionada.cCcalculado",
        "Dados.amostraselecionada.massa",
        "Dados.Curvadeperda.f0",
        "Dados.Curvadeperda.f1",
        "Dados.Curvadeperda.f2",
        "Dados.apis.Operation_Durab_Teste.Velocidades.vel1",
        "Dados.apis.Operation_Durab_Teste.Velocidades.vel2",
        "Dados.apis.Operation_Durab_Teste.Velocidades.vel3",
        "Dados.apis.Operation_Durab_Teste.Velocidades.vel4",
        "Dados.apis.Operation_Durab_Teste.Velocidades.vel5",
        "Dados.apis.Operation_Durab_Teste.Velocidades.vel6",
        "Dados.apis.Operation_Durab_Teste.Distancias.Dist1",
        "Dados.apis.Operation_Durab_Teste.Distancias.Dist2",
        "Dados.apis.Operation_Durab_Teste.Distancias.Dist3",
        "Dados.apis.Operation_Durab_Teste.Distancias.Dist4",
        "Dados.apis.Operation_Durab_Teste.Distancias.Dist5",
        "Dados.apis.Operation_Durab_Teste.Distancias.Dist6"
    ]
    while 1:
        start_time = time.time()
        t=e3.read_tag("Dados.apis.Operation_Durab_Teste.btn")
        if t == True:
            e3.write_tag(["Dados.apis.Operation_Durab_Teste.btn","False"])

            dados_recebidos=e3.read_tag(tag_list)
            for i in range(0,len(dados_recebidos)):
                if dados_recebidos[i]==None:
                    dados_recebidos[i]=0
            dados_envia= {
                "coefDinaCoastDown": [float(dados_recebidos[0]),float(dados_recebidos[1]),float(dados_recebidos[2])],
                "massaAmostra": float(dados_recebidos[3]),
                "coefLossCurve": [float(dados_recebidos[4]),float(dados_recebidos[5]),float(dados_recebidos[6])],
                "DurabDist": [float(dados_recebidos[13]),float(dados_recebidos[14]),float(dados_recebidos[15]),
                             float(dados_recebidos[16]),float(dados_recebidos[17]),float(dados_recebidos[18])],
                "DurabVel": [float(dados_recebidos[7]),float(dados_recebidos[8]),float(dados_recebidos[9]),
                             float(dados_recebidos[10]),float(dados_recebidos[11]),float(dados_recebidos[12])],
                "TypeTest": False,
                "RoadVelArray": [0 for a in range(0,60*60*24)],

            }
            c.post(key, dados_envia)
    time.sleep(0.5)
    time_Operation_Durab_Teste = time.time() - start_time

def Operation_SamplePositioning():
    global time_Operation_SamplePositioning
    key = "Operations/Operation_SamplePositioning"
    while 1:
        start_time = time.time()
        try:
            t=e3.read_tag("Dados.apis.Operation_SamplePositioning.btn")
            if t==True:
                e3.write_tag(["Dados.apis.Operation_SamplePositioning.btn","False"])
                resultado=c.get(key)
        except:
            pass
        time.sleep(0.5)
        time_Operation_SamplePositioning = time.time() - start_time


def Operation_Warmup():
    global time_Operation_Warmup
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
        start_time = time.time()
        try:  
            if e3.read_tag("Dados.apis.Operation_Warmup.btn")==True:
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
        time_Operation_Warmup = time.time() - start_time


#Server Interface


def Interface_Curve_Loss_Static():
    global time_Interface_Curve_Loss_Static
    while 1:
        start_time = time.time()
        try:
            if e3.read_tag("Dados.apis.Operation_Curve_Loss_Static.stop")==True:
                e3.write_tag(["Dados.apis.Operation_Curve_Loss_Static.stop","False"])
                c.get("Operations_Servers_Interface/Interface_Curve_Loss_Static?User_Stop=1")
                time.sleep(0.5)
                c.get("Operations_Servers_Interface/Interface_Curve_Loss_Static?User_Stop=0")
            if e3.read_tag("Dados.apis.reset")==True:
                e3.write_tag(["Dados.apis.reset","False"])
                c.get("Operations_Servers_Interface/Interface_Reset_Supervisorio?Reset_Supervisorio=1")
                time.sleep(4)
                c.get("Operations_Servers_Interface/Interface_Reset_Supervisorio?Reset_Supervisorio=0")
        except Exception as e:
            print(e)
        time.sleep(0.5)
        time_Interface_Curve_Loss_Static = time.time() - start_time


def Interface_FreeTest():
    global time_Interface_FreeTest
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
        start_time = time.time()
        try:
            b=e3.read_tag("Dados.apis.FreeTest.atualiza")
            if b == True:
                #e3.write_tag([["Dados.apis.FreeTest.atualiza","False"],["Dados.apis.FreeTest.StopTest","False"],["Dados.apis.FreeTest.ZeraDistancia","False"]])
                t=e3.read_tag(tag_list)
                for i in range(0,len(t)):
                    if t[i]==None:
                        t[i]=0
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
                e3.write_tag([["Dados.apis.FreeTest.atualiza","False"],["Dados.apis.FreeTest.StopTest","False"],["Dados.apis.FreeTest.ZeraDistancia","False"]])
                c.post(key, post_ope_interface_free_teste)
                time.sleep(0.5)
                if t[14]==True:
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
                        "ZeraDistancia": False,
                        "FreeTestType": int(t[15])
                    }
                    c.post(key, post_ope_interface_free_teste)
        except Exception as e:
            print(e)
        time.sleep(0.5)
        time_Interface_FreeTest = time.time() - start_time

def Interface_Input_LoadCell_Arrays():
    global time_Interface_Input_LoadCell_Arrays
    key="Operations_Servers_Interface/Interface_Input_LoadCell_Arrays"
    tag_list=[
        "Dados.apis.Operation_LoadCellCalibration.Data_loadCell_Calibrated.t1",
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
        start_time = time.time()
        try:
            global send_calibration
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.envia_calibracao") or send_calibration==True:
                send_calibration=False
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.envia_calibracao",False])
                dados_recebidos=e3.read_tag(tag_list)
                dados_enviar={
                    "Data_LoadCell_Calibrated": [float(dados_recebidos[0]),float(dados_recebidos[1]),float(dados_recebidos[2]),float(dados_recebidos[3]),float(dados_recebidos[4]),float(dados_recebidos[5]),float(dados_recebidos[6]),float(dados_recebidos[7]),float(dados_recebidos[8]),float(dados_recebidos[9]),float(dados_recebidos[10]),float(dados_recebidos[11]),float(dados_recebidos[12]),float(dados_recebidos[13]),float(dados_recebidos[14]),float(dados_recebidos[15]),float(dados_recebidos[16]),float(dados_recebidos[17]),float(dados_recebidos[18]),float(dados_recebidos[19]),float(dados_recebidos[20])],
                    "Data_LoadCell_Raw": [float(dados_recebidos[21]),float(dados_recebidos[22]),float(dados_recebidos[23]),float(dados_recebidos[24]),float(dados_recebidos[25]),float(dados_recebidos[26]),float(dados_recebidos[27]),float(dados_recebidos[28]),float(dados_recebidos[29]),float(dados_recebidos[30]),float(dados_recebidos[31]),float(dados_recebidos[32]),float(dados_recebidos[33]),float(dados_recebidos[34]),float(dados_recebidos[35]),float(dados_recebidos[36]),float(dados_recebidos[37]),float(dados_recebidos[38]),float(dados_recebidos[39]),float(dados_recebidos[40]),float(dados_recebidos[41])],
                    "Data_LoadCell_Uncertainties": [float(dados_recebidos[42]),float(dados_recebidos[43]),float(dados_recebidos[44]),float(dados_recebidos[45]),float(dados_recebidos[46]),float(dados_recebidos[47]),float(dados_recebidos[48]),float(dados_recebidos[49]),float(dados_recebidos[50]),float(dados_recebidos[51]),float(dados_recebidos[52]),float(dados_recebidos[53]),float(dados_recebidos[54]),float(dados_recebidos[55]),float(dados_recebidos[56]),float(dados_recebidos[57]),float(dados_recebidos[58]),float(dados_recebidos[59]),float(dados_recebidos[60]),float(dados_recebidos[61]),float(dados_recebidos[62])]
                }
                c.post(key,dados_enviar)
        except:
            pass
        time_Interface_Input_LoadCell_Arrays = time.time() - start_time

def Interface_LoadCellCalibration():
    global time_Interface_LoadCellCalibration
    key="Operations_Servers_Interface/Interface_LoadCellCalibration"
    while 1:
        start_time = time.time()
        try:
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.atualiza"):
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.atualiza","False"])
                if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.ok")==True:
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
                if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.stop")==True:
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
        time_Interface_LoadCellCalibration = time.time() - start_time


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
    global time_Interface_RoadTests
    key="Operations_Servers_Interface/Interface_RoadTests"
    while 1:
        start_time = time.time()
        try:
            if e3.read_tag("Dados.apis.Operation_Durab_Teste.start")==True:
                e3.write_tag(["Dados.apis.Operation_Durab_Teste.start","False"])
                post_ope_interface_free_teste = {
                    "TestStart": True,
                    "UserStop": False,
                    "TestEnd": False
                }    
                c.post(key, post_ope_interface_free_teste)
                time.sleep(0.5)
            if e3.read_tag("Dados.apis.Operation_Warmup.atualiza")==True:
                e3.write_tag(["Dados.apis.Operation_Warmup.atualiza","False"])
                t=e3.read_tag("Dados.apis.Operation_Warmup.stop")
                post_ope_interface_free_teste = {
                    "TestStart": False,
                    "UserStop": t,
                    "TestEnd": False
                }    
                c.post(key, post_ope_interface_free_teste)
                time.sleep(0.5)
                post_ope_interface_free_teste = {
                    "TestStart": False,
                    "UserStop": False,
                    "TestEnd": False
                }    
                c.post(key, post_ope_interface_free_teste)
            if e3.read_tag("Dados.apis.RoadTest.end")==True:
                e3.write_tag(["Dados.apis.RoadTest.end","False"])
                post_ope_interface_free_teste = {
                    "TestStart": False,
                    "UserStop": False,
                    "TestEnd": True
                }    
                c.post(key, post_ope_interface_free_teste)
                time.sleep(0.5)
                post_ope_interface_free_teste = {
                    "TestStart": False,
                    "UserStop": False,
                    "TestEnd": False
                }    
                c.post(key, post_ope_interface_free_teste)
        except:
            pass
        time.sleep(0.5)
        time_Interface_RoadTests = time.time() - start_time
#?
def Interface_RoadTests_Driver():
    pass

#?
def Interface_SamplePositioning():
    global time_Interface_SamplePositioning
    while 1:
        start_time = time.time()
        try:
            if e3.read_tag("Dados.apis.Operation_SamplePositioning.stop"):
                e3.write_tag(["Dados.apis.Operation_SamplePositioning.stop","False"])
                c.get("Operations_Servers_Interface/Interface_SamplePositioning?Stop_Supervisorio={}".format("True"))
        except:
            pass
        time.sleep(0.5)
        time_Interface_SamplePositioning = time.time() - start_time


def Interface_RoadTests_Driver():
    {'Distancia_percorrida': 0, 'Velocidade_Target_RoadTests': 0, 'Velocidade_Encoder_km_h': 0}
    key = "Operations_Servers_Interface/Interface_RoadTests_Driver"
    resultado=c.get(key)



def Interface_Open_Alcapao_PL():
    global time_Interface_Open_Alcapao_PL
    key = "Operations_Servers_Interface/Interface_Open_Alcapao_PL"
    while 1:
        start_time = time.time()
        try:
            if e3.read_tag("Dados.apis.Operation_Open_Alcapao_PL.atualiza")==True:
                e3.write_tag(["Dados.apis.Operation_Open_Alcapao_PL.atualiza","False"])
                al=e3.read_tag("Dados.apis.Operation_Open_Alcapao_PL.alcapao")
                if al!=True:
                    al=False
                pl=e3.read_tag("Dados.apis.Operation_Open_Alcapao_PL.pl")
                if pl!=True:
                    pl=False
                dados = {
                    "Alcapao": al,
                    "PL": pl
                }
                c.post(key, dados)
        except:
            pass
        time.sleep(0.5)
        time_Interface_Open_Alcapao_PL = time.time() - start_time
    


async def wsocket():
    global time_web_socket
    while 1:
        start_time = time.time()
        try:
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
                            if d[0] == "Forca_calibrada" and d[1]==0:
                                if d[1]==0:
                                    global send_calibration
                                    send_calibration=True
                            if 1:
                                r.append(["Dados.apis.websocket.{}".format(d[0]),data[d[0]]])
                                d[1]=data[d[0]]
                        if r!=[]:
                            e3.write_tag(r)
                        e3.write_tag(["Dados.apis.heartbeat",1],True)
                    except Exception as e:
                        print("Falha:{}{}".format(e,d[0]))
                    time.sleep(0.1)
        except:
            pass
        time.sleep(10)
        time_web_socket = time.time() - start_time

def screen_diagnostics():

    trigger = 30
    size = (940, 300)

    frame_layout_1 = [
                        [sg.Text("Status Operação: Checagem", background_color="#344E61")],
                        [sg.Text("Status Operação: Interface Checagem", background_color="#344E61")],
                        [sg.Text("Status Operação: Warm Up", background_color="#344E61")],
                        [sg.Text("Status Operação: Curva de Perda", background_color="#344E61")],
                        [sg.Text("Status Operação: Interface Curva de Perda", background_color="#344E61")],
                        [sg.Text("Status Operação: Posicionamento da Amostra", background_color="#344E61")],
                        [sg.Text("Status Operação: Interface Posicionamento da Amostra", background_color="#344E61")],
                        [sg.Text("Status Operação: Coast Down", background_color="#344E61")],
                        [sg.Text("Status Operação: Teste Livre", background_color="#344E61")],
                        [sg.Text("Status Operação: Interface Teste Livre", background_color="#344E61")],
                        [sg.Text("Status Operação: Teste de Durabilidade", background_color="#344E61")],
                        [sg.Text("Status Operação: Teste de Pista", background_color="#344E61")],
                        [sg.Text("Status Operação: Interface Teste de Pista", background_color="#344E61")]
                        ]

    frame_layout_2 = [
                        [sg.Text("Tempo de Execução:", key = "-TIME_OPERATION_CHECAGEM-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_INTERFACE_CHECAGEM-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_OPERATION_WARMUP-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_OPERATION_CURVA_PERDA-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_INTERFACE_CURVA_PERDA-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_POSICIONAMENTO_DA_AMOSTRA-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_INTERFACE_POSICIONAMENTO_AMOSTRA-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_COAST_DOWN-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "TIME_TESTE_LIVRE-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_INTERFACE_TESTE_LIVRE-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "TIME_DURABILIDADE", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_PISTA-", background_color="#344E61")],
                         [sg.Text("Tempo de Execução:", key = "-TIME_INTERFACE_PISTA-", background_color="#344E61")]
                    ]
    
    frame_layout_3 = [
        [sg.Text("Good", key = "-STATUS_OPERATION_CHECAGEM-")],
        [sg.Text("Good", key = "-STATUS_INTERFACE_CHECAGEM-")],
        [sg.Text("Good", key = "-STATUS_OPERATION_WARMUP-")],
        [sg.Text("Good", key = "-STATUS_OPERATION_CURVA_PERDA-")],
        [sg.Text("Good", key = "-STATUS_INTERFACE_CURVA_PERDA-")],
        [sg.Text("Good", key = "-STATUS_POSICIONAMENTO_DA_AMOSTRA-")],
        [sg.Text("Good", key = "-STATUS_INTERFACE_POSICIONAMENTO_AMOSTRA-")],
        [sg.Text("Good", key = "-STATUS_COAST_DOWN-")],
        [sg.Text("Good", key = "-STATUS_TESTE_LIVRE-")],
        [sg.Text("Good", key = "-STATUS_INTERFACE_TESTE_LIVRE-")],
        [sg.Text("Good", key = "-STATUS_DURABILIDADE-")],
        [sg.Text("Good", key = "-STATUS_PISTA-")],
        [sg.Text("Good", key = "-STATUS_INTERFACE_PISTA-")]
    ]

    layout = [
        [sg.Frame("Canal de Comunicação", frame_layout_1, font="Helvetica 12", title_color="white", background_color="#344E61",
                  expand_x=True, expand_y=True),
        sg.Frame("Tempo de Execução (segundos)", frame_layout_2, font="Helvetica 12", title_color="white", background_color="#344E61",
                  expand_x=True, expand_y=True),
        sg.Frame("Status do Canal", frame_layout_3, font="Helvetica 12", title_color="white", background_color="#344E61",
                  expand_x=True, expand_y=True)]
        
    ]

    window = sg.Window('Diagnóistico da Comunicação Labview', layout, size=size,
                        background_color="#344E61", enable_close_attempted_event=False)
    
    while True:
        event, values = window.read(timeout=10)

        if event == sg.WIN_CLOSED :
            break

        window["-TIME_OPERATION_CHECAGEM-"].update(f"Tempo de Execução: {round(time_Operation_LoadCellCalibration,5)}")
        window["-TIME_INTERFACE_CHECAGEM-"].update(f"Tempo de Execução: {round(time_Interface_LoadCellCalibration, 5)}")
        window["-TIME_OPERATION_WARMUP-"].update(f"Tempo de Execução: {round(time_Operation_Warmup, 5)}")
        window["-TIME_OPERATION_CURVA_PERDA-"].update(f"Tempo de Execução: {round(time_Operation_Curve_Loss_Static, 5)}")
        window["-TIME_INTERFACE_CURVA_PERDA-"].update(f"Tempo de Execução: {round(time_Operation_Curve_Loss_Static, 5)}")
        window["-TIME_POSICIONAMENTO_DA_AMOSTRA-"].update(f"Tempo de Execução: {round(time_Operation_SamplePositioning, 5)}")
        window["-TIME_INTERFACE_POSICIONAMENTO_AMOSTRA-"].update(f"Tempo de Execução: {round(time_Interface_SamplePositioning, 5)}")
        window["-TIME_COAST_DOWN-"].update(f"Tempo de Execução: {round(time_Operation_Coast_Down, 5)}")
        window["TIME_TESTE_LIVRE-"].update(f"Tempo de Execução: {round(time_Operation_FreeTest, 5)}")
        window["-TIME_INTERFACE_TESTE_LIVRE-"].update(f"Tempo de Execução: {round(time_Interface_FreeTest, 5)}")
        window["TIME_DURABILIDADE"].update(f"Tempo de Execução: {round(time_Operation_Durab_Teste, 5)}")
        window["-TIME_PISTA-"].update(f"Tempo de Execução: {round(time_Operation_RoadTest, 5)}")
        window["-TIME_INTERFACE_PISTA-"].update(f"Tempo de Execução: {round(time_Operation_RoadTest, 5)}")


        if time_Operation_LoadCellCalibration > trigger:
            window["-STATUS_OPERATION_CHECAGEM-"].update("Bad", background_color="red")
        else:
            window["-STATUS_OPERATION_CHECAGEM-"].update(background_color="green")
        if time_Interface_LoadCellCalibration > trigger:
            window["-STATUS_INTERFACE_CHECAGEM-"].update("Bad", background_color="red")
        else:
            window["-STATUS_INTERFACE_CHECAGEM-"].update(background_color="green")
        if time_Operation_Warmup > trigger:
            window["-STATUS_OPERATION_WARMUP-"].update("Bad", background_color="red")
        else:
            window["-STATUS_OPERATION_WARMUP-"].update(background_color="green")
        if time_Operation_Curve_Loss_Static > trigger:
            window["-STATUS_OPERATION_CURVA_PERDA-"].update("Bad", background_color="red")
        else:
            window["-STATUS_OPERATION_CURVA_PERDA-"].update(background_color="green")
        if time_Interface_Curve_Loss_Static > trigger:
            window["-STATUS_INTERFACE_CURVA_PERDA-"].update("Bad", background_color="red")
        else:
            window["-STATUS_INTERFACE_CURVA_PERDA-"].update(background_color="green")
        if time_Operation_SamplePositioning > trigger:
            window["-STATUS_POSICIONAMENTO_DA_AMOSTRA-"].update("Bad", background_color="red")
        else:
            window["-STATUS_POSICIONAMENTO_DA_AMOSTRA-"].update(background_color="green")
        if time_Interface_SamplePositioning > trigger:
            window["-STATUS_INTERFACE_POSICIONAMENTO_AMOSTRA-"].update("Bad", background_color="red")
        else:
            window["-STATUS_INTERFACE_POSICIONAMENTO_AMOSTRA-"].update(background_color="green")
        if time_Operation_Coast_Down > trigger:
            window["-STATUS_COAST_DOWN-"].update("Bad", background_color="red")
        else:
            window["-STATUS_COAST_DOWN-"].update(background_color="green")
        if time_Operation_FreeTest > trigger:
            window["-STATUS_TESTE_LIVRE-"].update("Bad", background_color="red")
        else:
            window["-STATUS_TESTE_LIVRE-"].update(background_color="green")
        if time_Interface_FreeTest > trigger:
            window["-STATUS_INTERFACE_TESTE_LIVRE-"].update("Bad", background_color="red")
        else:
            window["-STATUS_INTERFACE_TESTE_LIVRE-"].update(background_color="green")
        if time_Operation_Durab_Teste > trigger:
            window["-STATUS_DURABILIDADE-"].update("Bad", background_color="red")
        else:
            window["-STATUS_DURABILIDADE-"].update(background_color="green")
        if time_Operation_RoadTest > trigger:
            window["-STATUS_PISTA-"].update("Bad", background_color="red")
        else:
            window["-STATUS_PISTA-"].update(background_color="green")
        if time_Interface_RoadTests > trigger:
            window["-STATUS_INTERFACE_PISTA-"].update("Bad", background_color="red")
        else:
            window["-STATUS_INTERFACE_PISTA-"].update(background_color="green")
        
        


e3=elipse()
c=crio("http://169.254.62.198:8001/DinaCON_WebService/")

t=[]
t.append(Thread(target=Operation_Warmup))
t.append(Thread(target=Interface_RoadTests))
t.append(Thread(target=Operation_SamplePositioning))
t.append(Thread(target=Interface_SamplePositioning))
t.append(Thread(target=Interface_FreeTest))
t.append(Thread(target=Operation_FreeTest))
t.append(Thread(target=Operation_LoadCellCalibration))
t.append(Thread(target=Interface_Input_LoadCell_Arrays))
t.append(Thread(target=Interface_LoadCellCalibration))
t.append(Thread(target=Interface_Open_Alcapao_PL))
t.append(Thread(target=Operation_Coast_Down))
#t.append(Thread(target=Operation_Coast_Down_R2))
t.append(Thread(target=Operation_RoadTest))
t.append(Thread(target=Operation_Curve_Loss_Static))
t.append(Thread(target=Interface_Curve_Loss_Static))
t.append(Thread(target=Operation_Durab_Teste))
t.append(Thread(target=screen_diagnostics))


for th in t:
    th.start()



async def echo(websocket):
    async for message in websocket:
        try:
            await websocket.send("{\"Velocidade_kmh\":"+str(r_data[0][1])+",\"start\":"+str((int(r_data[11][1])&4)==4).lower()+",\"stop\":"+str((int(r_data[11][1])&8)==8).lower()+",\"end\":"+str((int(r_data[11][1])&2)==2).lower()+"}")
            mess=json.loads(message)
            try:
                e3.write_tag(["Dados.apis.websocket.acertos",mess["acertos"]])
            except:
                pass
            try:
                e3.write_tag(["Dados.apis.websocket.progresso",mess["progresso"]])
            except:
                pass
            try:
                if mess["testend"]:
                    post_ope_interface_free_teste = {
                        "TestStart": False,
                        "UserStop": False,
                        "TestEnd": True
                    }    
                    c.post("Operations_Servers_Interface/Interface_RoadTests", post_ope_interface_free_teste)
                    time.sleep(0.5)
                    post_ope_interface_free_teste = {
                        "TestStart": False,
                        "UserStop": False,
                        "TestEnd": False
                    }    
                    c.post("Operations_Servers_Interface/Interface_RoadTests", post_ope_interface_free_teste)
            except:
                pass
        except Exception as e:
            print(e)

async def ma():
    async with websockets.serve(echo, "169.254.62.180", 8765):
        await asyncio.Future()  # run forever


ma=asyncio.ensure_future(ma())
ws=asyncio.ensure_future(wsocket())

loop=asyncio.get_event_loop()
loop.run_forever()

#while 1:
#    try:
#        asyncio.get_event_loop().run_until_complete(wsocket())
#    except:
#        pass

#for th in t:
    #th.join()