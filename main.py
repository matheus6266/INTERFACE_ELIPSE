from e3 import elipse
from threading import Thread
import threading
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
    ["Falhas",""],
    ["Rolo_Inputs",""],
    ["Calibration_Stage",""],
    ["Distancia_Durabilidade",""],
    ["Velocidade_Durabilidade",""]
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
        
def str_to_float(value):
    return float(str(value).replace(",", "."))

def api_call(key, value):
    return json.loads(c.post(key, value))

#Operations

def Operation_Coast_Down():                                                                     # Revisado
    key = "Operations/Operation_Coast_Down" # Chave para a API
    
    # Lista de tags para coletar dados
    tag_list=[
        "Dados.amostraselecionada.cApista",
        "Dados.amostraselecionada.cBpista",
        "Dados.amostraselecionada.cCpista",
        "Dados.apis.Operation_Curve_Loss_Static.f0",
        "Dados.apis.Operation_Curve_Loss_Static.f1",
        "Dados.apis.Operation_Curve_Loss_Static.f2",
        "Dados.amostraselecionada.massa"
    ]
    # Dicionário para armazenar os dados que serão enviados
    dados_enviar = {
        "coefPistaRolamento": [0.0, 0.0, 0.0],
        "massaAmostra": [0.0],
        "coefLossCurve": [0.0, 0.0, 0.0]
    }
    # Loop infinito para realizar a operação Coast Down
    while True:
        try:
            # Verifica se o botão foi pressionado
            t=e3.read_tag("Dados.apis.Operation_Coast_Down.btn")
            if t:
                # Reseta o valor do botão
                e3.write_tag(["Dados.apis.Operation_Coast_Down.btn","False"])
                # Lê os dados das tags
                dados_recebidos=e3.read_tag(tag_list)
                # Processa os dados recebidos e atualiza o dicionário 'dados_enviar'
                dados_enviar["coefPistaRolamento"] = [str_to_float(dados_recebidos[i]) for i in range(3)]
                dados_enviar["massaAmostra"] = str_to_float(dados_recebidos[6])
                dados_enviar["coefLossCurve"] = [str_to_float(dados_recebidos[i]) for i in range(3, 6)]
                # Realiza chamada da API com os dados enviados e armazena a resposta
                r= api_call(key=key, value=dados_enviar)
                # Escreve os valores calculados no Elipse
                e3.write_tag([
                    ["Dados.amostraselecionada.cAcalculado",r["coefPistaDina_Calc"][0]],
                    ["Dados.amostraselecionada.cBcalculado",r["coefPistaDina_Calc"][1]],
                    ["Dados.amostraselecionada.cCcalculado",r["coefPistaDina_Calc"][2]]]
                )
        except Exception as e:
            # Exibe a mensagem de erro em caso de falha na operação Coast Down
            print("Erro na Operation_Coast_Down: {}".format(e))   

# Função para realizar a operação Curve Loss Dynamic
def Operation_Curve_Loss_Dynamic():                                                              # Revisado

    key = "Operations/Operation_Curve_Loss_Dynamic" # Chave para a API
    # Loop infinito para executar a operação Curve Loss Dynamic
    while True:
        try:
            # Verifica se o botão foi pressionado
            t=e3.read_tag("Dados.apis.Operation_Curve_Loss_Dynamic.btn")
            if t:
                # Reseta o valor do botão
                e3.write_tag(["Dados.apis.Operation_Curve_Loss_Dynamic.btn","False"])
                # Realiza chamada da API e armazena o resultado
                resultado=c.get(key)
        except Exception as e:
            # Exibe a mensagem de erro em caso de falha na operação Curve Loss Dynamic
            print("Erro na Operation_Curve_Loss_Dynamic: {}".format(e))
        time.sleep(0.5)    

# Função para realizar a operação Curve Loss Static
def Operation_Curve_Loss_Static():                                                               # Revisado
    key = "Operations/Operation_Curve_Loss_Static" # Chave para a API
    while True:
        try:
            # Verifica se o botão foi pressionado
            t=e3.read_tag("Dados.apis.Operation_Curve_Loss_Static.btn")
            if t:
                # Reseta o valor do botão e zera os coeficientes
                e3.write_tag([["Dados.apis.Operation_Curve_Loss_Static.btn","False"],
                              ["Dados.apis.Operation_Curve_Loss_Static.f0","0"],
                              ["Dados.apis.Operation_Curve_Loss_Static.f1","0"],
                              ["Dados.apis.Operation_Curve_Loss_Static.f2","0"]])
                 # Realiza chamada da API e converte a resposta para um dicionário
                r=json.loads(str(c.get(key)).replace("'","\""))
                 # Monta a lista de dados com as médias dos intervalos e os coeficientes polinomiais
                dados = [[f"Dados.apis.Operation_Curve_Loss_Static.Media_Forcas.Media_Intervalo{i+1}", r["Array_Force_mean"][i]]
                         for i in range(13)]
                dados += [["Dados.apis.Operation_Curve_Loss_Static.f0", r['Polynomial Coefficients'][0]],
                          ["Dados.apis.Operation_Curve_Loss_Static.f1", r['Polynomial Coefficients'][1]],
                          ["Dados.apis.Operation_Curve_Loss_Static.f2", r['Polynomial Coefficients'][2]]]
                # Escreve os dados no Elipse
                e3.write_tag(dados)
        except Exception as e:
            print("Erro na Operation_Curve_Loss_Static: {}".format(e))

#?
def Operation_Dina_Verification():
    pass

# Função Operation_FreeTest
def Operation_FreeTest():                                                                         # Revisado
    # Define a chave para a operação
    key = "Operations/Operation_FreeTest"
    # Cria a lista de tags usando list comprehensions
    tag_list = [f"Dados.apis.FreeTest.coefCoastDown.t{i+1}" for i in range(3)]
    tag_list += [f"Dados.apis.FreeTest.coefLossCurve.t{i+1}" for i in range(3)]
     # Inicializa um dicionário com os coeficientes a serem enviados
    dados_envia = {
        "coefDinaCoastDown": [0.0, 0.0, 0.0],
        "coefLossCurve": [0.0, 0.0, 0.0]
    }
    # Loop infinito
    while True:
        try:
            # Lê o valor da tag "Dados.apis.FreeTest.iniciar"
            t=e3.read_tag("Dados.apis.FreeTest.iniciar")
            if t:
                 # Escreve "False" na tag "Dados.apis.FreeTest.iniciar"            
                e3.write_tag(["Dados.apis.FreeTest.iniciar","False"])
                # Lê os valores das tags na lista tag_list
                dados_recebidos=e3.read_tag(tag_list)
                # Substitui os valores None por 0 na lista dados_recebidos
                dados_recebidos = [0 if dado is None else dado for dado in dados_recebidos]
                # Atualiza o dicionário dados_envia com os valores convertidos para float
                dados_envia["coefDinaCoastDown"] = [float(dados_recebidos[i]) for i in range(3)],
                dados_envia["coefLossCurve"] = [float(dados_recebidos[i]) for i in range(3, 6)]
                # Envia os dados para o servidor usando a chave
                c.post(key, dados_envia)
        except Exception as e:
            # Imprime a mensagem de erro em caso de exceção
            print("Erro na Operation_FreeTest: {}".format(e))

def Operation_LoadCellCalibration():
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

#?
def Operation_RoadTest():
    key="Operations/Operation_RoadTests"
    tag_list=[
        "Dados.amostraselecionada.cAcalculado",
        "Dados.amostraselecionada.cBcalculado",
        "Dados.amostraselecionada.cCcalculado",
        "Dados.amostraselecionada.massa",
        "Dados.Curvadeperda.f0",
        "Dados.Curvadeperda.f1",
        "Dados.Curvadeperda.f2",
    ]
    while 1:
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
                "RoadVelArray": [0,0]
            }
            c.post(key, dados_envia)
    time.sleep(0.5)

def Operation_Durab_Teste():
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
                "RoadVelArray": [0,0],

            }
            c.post(key, dados_envia)
    time.sleep(0.5)

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

def Interface_Input_LoadCell_Arrays():
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
        try:
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.envia_calibracao"):
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

def Interface_LoadCellCalibration():
    key="Operations_Servers_Interface/Interface_LoadCellCalibration"
    while 1:
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
            if e3.read_tag("Dados.apis.Operation_Durab_Teste.start")==True:
                e3.write_tag(["Dados.apis.Operation_Durab_Teste.start","False"])
                post_ope_interface_free_teste = {
                    "TestStart": True,
                    "UserStop": False
                }    
                c.post(key, post_ope_interface_free_teste)
                time.sleep(0.5)
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
    while 1:
        try:
            if e3.read_tag("Dados.apis.Operation_SamplePositioning.stop"):
                e3.write_tag(["Dados.apis.Operation_SamplePositioning.stop","False"])
                c.get("Operations_Servers_Interface/Interface_SamplePositioning?Stop_Supervisorio={}".format("True"))
        except:
            pass
        time.sleep(0.5)


def Interface_RoadTests_Driver():
    {'Distancia_percorrida': 0, 'Velocidade_Target_RoadTests': 0, 'Velocidade_Encoder_km_h': 0}
    key = "Operations_Servers_Interface/Interface_RoadTests_Driver"
    resultado=c.get(key)



def Interface_Open_Alcapao_PL():
    key = "Operations_Servers_Interface/Interface_Open_Alcapao_PL"
    while 1:
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
                e3.write_tag(["Dados.apis.heartbeat",1])
            except Exception as e:
                print("Falha:{}{}".format(e,d[0]))
            time.sleep(0.1)
            



e3=elipse()
c=crio("http://169.254.62.198:8001/DinaCON_WebService/")

t=[]
t.append(threading.Timer(0.5, Operation_Coast_Down))
t.append(Thread(target=Interface_RoadTests))
t.append(Thread(target=Operation_SamplePositioning))
t.append(Thread(target=Interface_SamplePositioning))
t.append(Thread(target=Interface_FreeTest))
t.append(threading.Timer(0.5, Operation_FreeTest))
t.append(Thread(target=Operation_LoadCellCalibration))
t.append(Thread(target=Interface_Input_LoadCell_Arrays))
t.append(Thread(target=Interface_LoadCellCalibration))
t.append(Thread(target=Interface_Open_Alcapao_PL))
t.append(Thread(target=Operation_Coast_Down))
t.append(Thread(target=Operation_RoadTest))
t.append(threading.Timer(0.5, Operation_Curve_Loss_Static))
t.append(Thread(target=Interface_Curve_Loss_Static))
t.append(Thread(target=Operation_Durab_Teste))


for th in t:
    th.start()
while 1:
    try:
        asyncio.get_event_loop().run_until_complete(wsocket())
    except:
        pass
for th in t:
    th.join()