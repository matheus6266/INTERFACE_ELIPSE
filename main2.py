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
        "coefPistaRolamento": [0.0]*3,
        "massaAmostra": [0.0],
        "coefLossCurve": [0.0]*3
    }
    # Loop infinito para realizar a operação Coast Down
    while True:
        try:
            if e3.read_tag("Dados.apis.Operation_Coast_Down.btn"):
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
            if e3.read_tag("Dados.apis.Operation_Curve_Loss_Dynamic.btn"):
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
            if e3.read_tag("Dados.apis.Operation_Curve_Loss_Static.btn"):
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
            if e3.read_tag("Dados.apis.FreeTest.iniciar"):
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

def Operation_LoadCellCalibration():                                                                    # Revisado
    # Define a chave para a operação
    key="Operations/Operation_LoadCellCalibration"
    # Define a lista de tags a serem lidas
    tag_list = ["Dados.apis.Operation_LoadCellCalibration.P1_P10.h1"]
    tag_list += [f"Dados.apis.Operation_LoadCellCalibration.P1_P10.t{i+1}" for i in range(11)]
    tag_list += ["Dados.apis.Operation_LoadCellCalibration.P11_P20.h1"]
    tag_list += [f"Dados.apis.Operation_LoadCellCalibration.P11_P20.t{i+1}" for i in range(11)]
    # Define o dicionário de dados a serem enviados para o servidor
    data = {"P1_P10": [0.0]*11, "P11_P20": [0.0]*11}
    # Loop infinito da operação
    while True:
        try:
            # Se o botão de start foi pressionado 
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.btn"):
                # Escreve False na tag do botão para evitar que a operação seja executada novamente
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.btn",False])
                # Lê as tags definidas na lista tag_list
                dados_recebidos=e3.read_tag(tag_list)
                # Substitui valores None por 0
                dados_recebidos = [0 if dados is None else dados for dados in dados_recebidos]
                # Armazena os valores lidos no dicionário data
                data["P1_P10"] = [dados_recebidos[i] for i in range(11)]
                data["P11_P20"] = [dados_recebidos[i] for i in range(11, 22)]
                # Envia os dados para o servidor utilizando a chave key
                result=json.loads(c.post(key,data))
                # Define as listas de sufixos e prefixos das chaves a serem escritas           
                keys_suffixes = ["Medicao final", "Sequencia Forca ", "Incerteza abs final"]
                keys_prefixes = ["Data_LoadCell_Calibrated", "Data_LoadCell_Raw", "Data_LoadCell_Uncertainties"]
                # Define a lista de dados a serem escritos
                dados = []
                # Percorre as listas de sufixos e prefixos para criar as chaves e os valores correspondentes
                for i in range(3):
                    for j in range(21):
                        key = f"Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_{keys_prefixes[i]}.t{j+1}"
                        value = result[keys_suffixes[j]][i]
                        dados.append([key, value])
                # Adiciona a tag "concluido" com valor True na lista de dados a serem escritos
                dados.append(["Dados.apis.Operation_LoadCellCalibration.concluido", "True"])
                # Escreve as tags com os valores correspondentes
                e3.write_tag(dados)
        # Em caso de exceção, imprime o erro
        except Exception as e:
            print("Erro na Operation_LoadCellCalibration: {}".format(e))

#?
def Operation_RoadTest():                                                                                   # Revisado
    # Chave para a API de operações de teste de estrada
    key="Operations/Operation_RoadTests"
    # Lista de tags para obter informações relacionadas ao teste de estrada
    tag_list=[
        "Dados.amostraselecionada.cAcalculado",
        "Dados.amostraselecionada.cBcalculado",
        "Dados.amostraselecionada.cCcalculado",
        "Dados.amostraselecionada.massa",
        "Dados.Curvadeperda.f0",
        "Dados.Curvadeperda.f1",
        "Dados.Curvadeperda.f2",
    ]
    # Dicionário com informações a serem enviadas à API
    dados_envia = {"coefDinaCoastDown": [0.0]*3, "massaAmostra": [0.0], "coefLossCurve": [0.0]*3,
                    "DurabDist": [0.0]*2, "DurabVel": [1]*2, "TypeTest": True, "RoadVelArray": [0]*2}
    # Loop infinito para executar o teste de estrada
    while True:
        try:
            if e3.read_tag("Dados.apis.RoadTest.btn"):
                # Reseta o estado do botão de teste de estrada
                e3.write_tag(["Dados.apis.RoadTest.btn","False"])
                # Lê os dados das tags especificadas
                dados_recebidos=e3.read_tag(tag_list)
                # Substitui os valores None por 0
                dados_recebidos = [0 if dados is None else dados for dados in dados_recebidos]
                # Atualiza o dicionário de dados a serem enviados com os dados recebidos
                dados_envia["coefDinaCoastDown"] = [dados_recebidos[i] for i in range(3)]
                dados_envia["massaAmostra"] = dados_recebidos[3]
                dados_envia["coefLossCurve"] = [dados_recebidos[i] for i in range(4, 7)]
                # Envia os dados para a API
                c.post(key, dados_envia)
        except Exception as e:
            # Imprime qualquer erro ocorrido durante a execução da função
            print("Erro na Operation_RoadTest: {}".format(e))

def Operation_Durab_Teste():                                                                              # Revisado
    # Chave para a API de operações de teste de durabilidade
    key="Operations/Operation_RoadTests"
    # Lista de tags para obter informações relacionadas ao teste de durabilidade
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
    # Dicionário com informações a serem enviadas à API
    dados_envia = {"coefDinaCoastDown": [0.0]*3, "massaAmostra": [0.0], "coefLossCurve": [0.0]*3,
                   "DurabDist": [0.0]*6, "DurabVel": [0.0]*6, "TypeTest": False, "RoadVelArray": [0]*2}
    # Loop infinito para executar o teste de durabilidade
    while True:
        try:
            # Verifica se o botão de teste de durabilidade foi acionado
            if e3.read_tag("Dados.apis.Operation_Durab_Teste.btn"):
                # Reseta o estado do botão de teste de durabilidade
                e3.write_tag(["Dados.apis.Operation_Durab_Teste.btn","False"])
                # Lê os dados das tags especificadas
                dados_recebidos=e3.read_tag(tag_list)
                # Substitui os valores None por 0
                dados_recebidos = [0 if dados is None else dados for dados in dados_recebidos]
                # Atualiza o dicionário de dados a serem enviados com os dados recebidos
                dados_envia["coefDinaCoastDown"] = [dados_recebidos[i] for i in range(3)]
                dados_envia["massaAmostra"] = dados_recebidos[3]
                dados_envia["coefLossCurve"] = [dados_recebidos[i] for i in range(4, 7)]
                dados_envia["DurabDist"] = [dados_recebidos[i] for i in range(13, 19)]
                dados_envia["DurabVel"] = [dados_recebidos[i] for i in range(7, 13)]
                # Envia os dados para a API
                c.post(key, dados_envia)
        except Exception as e:
             # Imprime qualquer erro ocorrido durante a execução da função
            print("Erro na Operation_Durab_Teste: {}".format(e))

def Operation_SamplePositioning():                                                                          # Revisado
    # Chave para a API de operações de posicionamento da amostra
    key = "Operations/Operation_SamplePositioning"
    # Loop infinito para verificar o botão de posicionamento da amostra
    while True:
        try:
            if e3.read_tag("Dados.apis.Operation_SamplePositioning.btn"):
                # Reseta o estado do botão de posicionamento da amostra
                e3.write_tag(["Dados.apis.Operation_SamplePositioning.btn","False"])
                # Obtém o resultado da operação de posicionamento da amostra a partir da API
                resultado=c.get(key)
        except Exception as e:
            # Imprime qualquer erro ocorrido durante a execução da função
            print("Erro na Operation_SamplePositioning: {}".format(e))


def Operation_Warmup():                                                                                 # Revisado
    # Chave para a API de operações de aquecimento
    key = "Operations/Operation_Warmup"
    # Lista de tags para obter informações relacionadas ao aquecimento
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
    # Dicionário com informações a serem enviadas à API
    dados_enviar ={"warmupVelocity": [0.0]*5, "warmupTime": [0.0]*5}
    # Loop infinito para executar o aquecimento
    while True:
        try:
            if e3.read_tag("Dados.apis.Operation_Warmup.btn"):
                # Reseta o estado do botão de aquecimento
                e3.write_tag(["Dados.apis.Operation_Warmup.btn",False])
                # Lê os dados das tags especificadas
                dados_recebidos=e3.read_tag(tag_list)
                 # Atualiza o dicionário de dados a serem enviados com os dados recebidos
                dados_enviar["warmupVelocity"] = [dados_recebidos[i] for i in range(5)]
                dados_enviar["warmupTime"] = [dados_recebidos[i] for i in range(5, 10)]
                # Envia os dados para a API
                c.post(key,dados_enviar)
        except Exception as e:
            # Imprime qualquer erro ocorrido durante a execução da função
            print("Erro na Operation_Warmup: {}".format(e))




#Server Interface


def Interface_Curve_Loss_Static():                                                              # Revisado
    # Loop infinito para executar a curva de perda estática
    while True:
        try:
            # Verifica se o botão de parada da curva de perda estática foi acionado
            if e3.read_tag("Dados.apis.Operation_Curve_Loss_Static.stop"):
                e3.write_tag(["Dados.apis.Operation_Curve_Loss_Static.stop","False"])
                c.get("Operations_Servers_Interface/Interface_Curve_Loss_Static?User_Stop=True")
        except Exception as e:
            # Imprime qualquer erro ocorrido durante a execução da função
            print("Erro na Operation_Warmup: {}".format(e))

def Interface_FreeTest():
    # Define uma chave para a API
    key =  "Operations_Servers_Interface/Interface_FreeTest"
    # Lista de tags usadas para a leitura dos dados
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
    # Dicionário com os valores iniciais dos dados a serem enviados
    dados_enviar = {"coefCoastDown": [0.0]*3, "coefLossCurve": [0.0]*3, "VelForce": False, "SetPointVel": 0.0,
                                     "SetPointForce": 0.0, "TimeInVel": 0.0, "TimeInForce": 0.0, "EnableForceCoastDown": False,
                                     "StartTest": False, "StopTest": False, "ZeraDistancia": False, "FreeTestType": 0}
    # Loop infinito
    while True:
        try:
            # Verifica se é necessário atualizar os dados
            if e3.read_tag("Dados.apis.FreeTest.atualiza"):
                # Lê os dados das tags especificadas na lista 'tag_list'
                dados_recebidos=e3.read_tag(tag_list)
                # Substitui os valores None por 0 na lista 'dados_recebidos'
                dados_recebidos = [0 if dados is None else dados for dados in dados_recebidos]
                 # Atualiza os valores do dicionário 'dados_enviar' com base nos dados recebidos
                dados_enviar["coefCoastDown"] = [dados_recebidos[i] for i in range(3)]
                dados_enviar["coefLossCurve"] = [dados_recebidos[i] for i in range(3, 6)]
                dados_enviar["VelForce"] = dados_recebidos[6]==True,
                dados_enviar["SetPointVel"] = float(dados_recebidos[7]),
                dados_enviar["SetPointForce"] = float(dados_recebidos[8]),
                dados_enviar["TimeInVel"] = float(dados_recebidos[9]),
                dados_enviar["TimeInForce"] = float(dados_recebidos[10]),
                dados_enviar["EnableForceCoastDown"] = dados_recebidos[11]==True,
                dados_enviar["StartTest"] = dados_recebidos[12]==True,
                dados_enviar["StopTest"] = dados_recebidos[13]==True,
                dados_enviar["ZeraDistancia"] = dados_recebidos[14]==True,
                dados_enviar["FreeTestType"] = int(dados_recebidos[15])
                # Define as tags para serem escritas como Falso
                e3.write_tag([["Dados.apis.FreeTest.atualiza","False"],["Dados.apis.FreeTest.StopTest","False"],["Dados.apis.FreeTest.ZeraDistancia","False"]])
                # Envia os dados atualizados para a API
                c.post(key, dados_enviar)
                # Aguarda meio segundo
                time.sleep(0.5)
                # Verifica se a tag 'ZeraDistancia' está como Verdadeira
                if dados_recebidos[14]==True:
                    dados_enviar["coefCoastDown"] = [dados_recebidos[i] for i in range(3)]
                    dados_enviar["coefLossCurve"] = [dados_recebidos[i] for i in range(3, 6)]
                    dados_enviar["VelForce"] = dados_recebidos[6]==True,
                    dados_enviar["SetPointVel"] = float(dados_recebidos[7]),
                    dados_enviar["SetPointForce"] = float(dados_recebidos[8]),
                    dados_enviar["TimeInVel"] = float(dados_recebidos[9]),
                    dados_enviar["TimeInForce"] = float(dados_recebidos[10]),
                    dados_enviar["EnableForceCoastDown"] = dados_recebidos[11]==True,
                    dados_enviar["StartTest"] = dados_recebidos[12]==True,
                    dados_enviar["StopTest"] = dados_recebidos[13]==True,
                    dados_enviar["ZeraDistancia"] = False,
                    dados_enviar["FreeTestType"] = int(dados_recebidos[15])
                    # Envia os dados atualizados para a API
                    c.post(key, dados_enviar)
        except Exception as e:
            print("Erro na Interface_FreeTest: {}".format(e))


def Interface_Input_LoadCell_Arrays():
    # Define uma chave para a API
    key="Operations_Servers_Interface/Interface_Input_LoadCell_Arrays"
    # Prefixos das chaves usadas para a leitura dos dados
    keys_prefixes = ["Data_LoadCell_Calibrated", "Data_LoadCell_Raw", "Data_LoadCell_Uncertainties"]
    # Lista de tags vazia e dicionário com os valores iniciais dos dados a serem enviados
    tag_list = []
    dados_enviar = {"Data_LoadCell_Calibrated": [0.0]*21,
                    "Data_LoadCell_Raw":[0.0]*21,
                    "Data_LoadCell_Uncertainties": [0.0]*21}
    # Popula a lista de tags com base nos prefixos e nos índices
    for i in range(3):
        for j in range(21):
            key = f"Dados.apis.Operation_LoadCellCalibration.Data_LoadCell_{keys_prefixes[i]}.t{j+1}"
            tag_list.append(key)
    # Loop infinito   
    while True:
        try:
            # Verifica se é necessário enviar os dados de calibração
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.envia_calibracao"):
                # Define a tag 'envia_calibracao' como Falso
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.envia_calibracao",False])
                # Lê os dados das tags especificadas na lista 'tag_list'
                dados_recebidos=e3.read_tag(tag_list)
                # Atualiza os valores do dicionário 'dados_enviar' com base nos dados recebidos
                dados_enviar["Data_LoadCell_Calibrated"] = [dados_recebidos[i] for i in range(21)]
                dados_enviar["Data_LoadCell_Raw"] = [dados_recebidos[i] for i in range(21, 42)]
                dados_enviar["Data_LoadCell_Uncertainties"] = [dados_recebidos[i] for i in range(42, 63)]
                # Envia os dados atualizados para a API
                c.post(key,dados_enviar)
        # Exibe a exceção e a mensagem de erro, caso ocorra
        except Exception as e:
            print("Erro na Interface_Input_LoadCell_Arrays: {}".format(e))

def Interface_LoadCellCalibration():
    # Define uma chave para a API
    key="Operations_Servers_Interface/Interface_LoadCellCalibration"
    # Dicionário com os valores iniciais dos botões a serem enviados
    dados_enviar = {"okButton": False, "stopButton": False}
    while True:
        try:
            # Verifica se a tag 'atualiza' está ativada
            if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.atualiza"):
                # Define a tag 'atualiza' como Falso
                e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.atualiza","False"])
                # Verifica se a tag 'ok' está ativada
                if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.ok"):
                    # Define a tag 'ok' como Falso
                    e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.ok","False"])
                    # Atualiza os valores do dicionário 'dados_enviar' e envia os dados para a API
                    dados_enviar["okButton"] = True
                    dados_enviar["stopButton"] = False
                    c.post(key,dados_enviar)
                    # Aguarda 0,5 segundos antes de resetar os valores do dicionário 'dados_enviar'
                    time.sleep(0.5)
                    dados_enviar["okButton"] = False
                    dados_enviar["stopButton"] = False
                    # Verifica se a tag 'stop' está ativada
                    c.post(key,dados_enviar)
                if e3.read_tag("Dados.apis.Operation_LoadCellCalibration.stop"):
                    # Define a tag 'stop' como Falso
                    e3.write_tag(["Dados.apis.Operation_LoadCellCalibration.stop","False"])
                    # Atualiza os valores do dicionário 'dados_enviar' e envia os dados para a API
                    dados_enviar["okButton"] = False
                    dados_enviar["stopButton"] = True
                    c.post(key,dados_enviar)
                    # Aguarda 0,5 segundos antes de resetar os valores do dicionário 'dados_enviar'
                    time.sleep(0.5)
                    dados_enviar["okButton"] = False
                    dados_enviar["stopButton"] = False
                    c.post(key,dados_enviar)
        except Exception as e:
            # Exibe a exceção e a mensagem de erro, caso ocorra
            print("Erro na Interface_LoadCellCalibration: {}".format(e))


def Interface_Output_test():
    # Define a list of tags to be used in this function
    tag_list=[
        "man_auto_test",
        "vel_torq_test",
        "setpoint-vel",
        "setpoint_torq",
        "time_in_torq",
        "time_in_vel"
    ]
    # Infinite loop to continuously check and update the interface
    while True:
        try:
            # Check if the interface needs to be updated
            if e3.read_tag("Dados.apis.Interface_Output_test.atualiza"):
                # Set the update flag to False
                e3.write_tag(["Dados.apis.Interface_Output_test.atualiza","False"])
                # Read data from tags
                dados_recebidos=e3.read_tag(tag_list)
                # Update the interface with the data received
                c.get("Operations_Servers_Interface/Interface_Output_test?man_auto_test={}&vel_torq_test={}&setpoint-vel={}&setpoint_torq={}&time_in_torq={}&time_in_vel={}".format(dados_recebidos[0],dados_recebidos[1],dados_recebidos[2],dados_recebidos[3],dados_recebidos[4],dados_recebidos[5]))
        # Handle exceptions and print an error message
        except Exception as e:
            print("Erro na Interface_Output_test: {}".format(e))

#?        
def Interface_Read_Datalog():
    pass

#?
def Interface_RoadTests():
    # Define a chave para acessar a interface dos testes de estrada
    key="Operations_Servers_Interface/Interface_RoadTests"
    # Inicializa o dicionário para enviar dados para a interface
    dados_enviar = {"TestStart": False, "UserStop": False}
    # Loop infinito para atualizar continuamente a interface
    while True:
        try:
            # Verifica se o teste de durabilidade deve ser iniciado
            if e3.read_tag("Dados.apis.Operation_Durab_Teste.start"):
                # Define o valor da tag de início como Falso
                e3.write_tag(["Dados.apis.Operation_Durab_Teste.start","False"])
                # Atualiza os dados a serem enviados
                dados_enviar["TestStart"] = True
                dados_enviar["UserStop"] = False
                # Envia os dados para a interface    
                c.post(key, dados_enviar)
                time.sleep(0.5)
                # Verifica se é necessário atualizar a tag de aquecimento
            if e3.read_tag("Dados.apis.Operation_Warmup.atualiza"):
                # Define o valor da tag de atualização como Falso
                e3.write_tag(["Dados.apis.Operation_Warmup.atualiza","False"])
                # Lê o valor da tag de parada
                t=e3.read_tag("Dados.apis.Operation_Warmup.stop")
                # Atualiza os dados a serem enviados
                dados_enviar["TestStart"] = False
                dados_enviar["UserStop"] = t
                # Envia os dados para a interface   
                c.post(key, dados_enviar)
                time.sleep(0.5)
                # Reinicia os valores no dicionário de dados_enviar
                dados_enviar["TestStart"] = False
                dados_enviar["UserStop"] = False
                # Envia os dados atualizados para a interface    
                c.post(key, dados_enviar)
        # Trata exceções e imprime uma mensagem de erro
        except Exception as e:
            print("Erro na Interface_RoadTests: {}".format(e))

#?
def Interface_RoadTests_Driver():
    pass

#?
def Interface_SamplePositioning():
    # Loop infinito para atualizar continuamente a interface
    while True:
        # Verifica se a tag de parada da operação de posicionamento da amostra está ativa
        try:
            if e3.read_tag("Dados.apis.Operation_SamplePositioning.stop"):
                # Define o valor da tag de parada como Falso
                e3.write_tag(["Dados.apis.Operation_SamplePositioning.stop","False"])
                # Atualiza a interface com o valor de parada do supervisório
                c.get("Operations_Servers_Interface/Interface_SamplePositioning?Stop_Supervisorio={}".format("True"))
        # Trata exceções e imprime uma mensagem de erro
        except Exception as e:
            print("Erro na Interface_SamplePositioning: {}".format(e))


def Interface_RoadTests_Driver():
    {'Distancia_percorrida': 0, 'Velocidade_Target_RoadTests': 0, 'Velocidade_Encoder_km_h': 0}
    key = "Operations_Servers_Interface/Interface_RoadTests_Driver"
    resultado=c.get(key)



def Interface_Open_Alcapao_PL():
    # Define a chave para acessar a interface de abertura do alçapão e PL
    key = "Operations_Servers_Interface/Interface_Open_Alcapao_PL"
    # Inicializa o dicionário para enviar dados para a interface
    al = False
    pl = False
    dados_enviar = {"Alcapao": al, "PL": pl}
    # Loop infinito para atualizar continuamente a interface
    while True:
        try:
            # Verifica se a tag de atualização da operação de abertura do alçapão e PL está ativa
            if e3.read_tag("Dados.apis.Operation_Open_Alcapao_PL.atualiza"):
                # Define o valor da tag de atualização como Falso
                e3.write_tag(["Dados.apis.Operation_Open_Alcapao_PL.atualiza","False"])
                 # Lê o valor da tag alcapao
                al=e3.read_tag("Dados.apis.Operation_Open_Alcapao_PL.alcapao")
                # Verifica se o valor de alcapao não é verdadeiro e atribui o valor Falso
                if al!=True:
                    al=False
                # Lê o valor da tag PL
                pl=e3.read_tag("Dados.apis.Operation_Open_Alcapao_PL.pl")
                # Verifica se o valor de PL não é verdadeiro e atribui o valor Falso
                if pl!=True:
                    pl=False
                # Atualiza os dados a serem enviados
                dados_enviar["Alcapao"] = al
                dados_enviar["PL"] = pl
                # Envia os dados para a interface
                c.post(key, dados_enviar)
        # Trata exceções e imprime uma mensagem de erro
        except Exception as e:
            print("Erro na Interface_Open_Alcapao_PL: {}".format(e))
    


async def wsocket():
    # Estabelece uma conexão WebSocket com o endereço e porta especificados
    async with websockets.connect('ws://169.254.62.198:6123') as websocket:
        # Aguarda 5 segundos antes de iniciar o loop
        await asyncio.sleep(5)
        # Loop infinito para comunicação WebSocket
        while True:
            # Envia uma mensagem para o servidor WebSocket
            await websocket.send("{}".format(0))
             # Aguarda a resposta do servidor WebSocket
            response = await websocket.recv()
            try:
                # Carrega os dados da resposta em formato JSON
                data=json.loads(response)
                # Cria a lista 'r' com base nos dados recebidos e compara com os dados anteriores
                r = [["Dados.apis.websocket.{}".format(d[0]), data[d[0]]] for d in r_data if data[d[0]] != d[1]]
                # Se a lista 'r' não estiver vazia, escreve as tags atualizadas
                if r:
                    e3.write_tag(r)
                # Atualiza os valores anteriores na lista 'r_data'
                for d in r_data:
                    d[1] = data[d[0]]
                # Atualiza o valor da tag de heartbeat
                e3.write_tag(["Dados.apis.heartbeat",1])
            except Exception as e:
                print("Falha:{}{}".format(e,d[0]))
            # Aguarda 0,1 segundo antes de reiniciar o loop
            await asyncio.sleep(0.1)
            



e3=elipse()
c=crio("http://169.254.62.198:8001/DinaCON_WebService/")

t=[]
t.append(threading.Timer(0.5, Operation_Coast_Down))
t.append(threading.Timer(0.5, Interface_RoadTests))
t.append(threading.Timer(0.5, Operation_SamplePositioning))
t.append(threading.Timer(0.5, Interface_SamplePositioning))
t.append(threading.Timer(0.5, Interface_FreeTest))
t.append(threading.Timer(0.5, Operation_FreeTest))
t.append(threading.Timer(0.5, Operation_LoadCellCalibration))
t.append(threading.Timer(0.5, Interface_Input_LoadCell_Arrays))
t.append(threading.Timer(0.5, Interface_LoadCellCalibration))
t.append(threading.Timer(0.5, Interface_Open_Alcapao_PL))
t.append(threading.Timer(0.5, Operation_RoadTest))
t.append(threading.Timer(0.5, Operation_Curve_Loss_Static))
t.append(threading.Timer(0.5, Interface_Curve_Loss_Static))
t.append(threading.Timer(0.5, Operation_Durab_Teste))
t.append(threading.Timer(0.5, Operation_Warmup))
t.append(threading.Timer(0.5, Interface_Output_test))


for th in t:
    th.start()
while 1:
    try:
        asyncio.get_event_loop().run_until_complete(wsocket())
    except:
        pass
for th in t:
    th.join()