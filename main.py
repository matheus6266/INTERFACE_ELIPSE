from e3 import elipse
from threading import Thread
import requests
import json
import time
import asyncio
import websockets
import win32timezone
import numpy as np


mensagem_teste={
    "PolCoefsReportArray_Force": [
        [
            106.5338577449528,
            -1.48725090752238,
            0.0612099127218051
        ],
        [
            112.8828802734295,
            -1.859140793256678,
            0.06709914871386276
        ],
        [
            115.8317783678892,
            -1.955355314255652,
            0.06772241408327145
        ],
        [
            114.0388577681192,
            -1.912418723472847,
            0.06757629824469839
        ]
    ],
    "PolCoefsReportArray_Time": [
        [
            0,
            0,
            0
        ],
        [
            102.2591014453209,
            -1.64440145095758,
            0.006830959380051297
        ],
        [
            102.8787776139776,
            -1.65607378880008,
            0.006888812361749867
        ],
        [
            103.174736260157,
            -1.664257840263656,
            0.006936910725031192
        ]
    ],
    "MaxDif_Force_Pista": [
        -2.425708384836042,
        -4.223200379051121,
        -5.635571669102575,
        -6.544179277548949,
        -7.001287604747489,
        -7.104438496252953,
        -6.853631952065257,
        -6.248867972184428,
        -5.290146556610466,
        -3.977467705343315,
        -2.310831418383088,
        -0.2154789091268867,
        2.310188437620013,
        5.213670696601753,
        8.494967867818559
    ],
    "Std_Dev_Force": [
        0.3637096992299655,
        0.2430602751611258,
        0.15809401462245,
        0.1380875452542768,
        0.1786967349360268,
        0.2362442527170711,
        0.2907282503455892,
        0.3368667478130354,
        0.3737457660089097,
        0.4021720702435522,
        0.424077494501336,
        0.4424598610119391,
        0.4614215948375745,
        0.4860384711728244,
        0.5218324912405894
    ],
    "Std_Dev_Force_Percent": [
        0.3090105592811925,
        0.1868502046437105,
        0.1084039790680856,
        0.08370666703233483,
        0.09532145997745912,
        0.1107348684884012,
        0.1198433077657913,
        0.1224027838833111,
        0.120095810091132,
        0.1147180728250985,
        0.1078211878173455,
        0.1006894749373828,
        0.09437607944877019,
        0.08971155774845271,
        0.08726098147183506
    ],
    "MaxDif_Time_Pista": [
        0.6220826336175271,
        0.772384030338273,
        0.774527871577515,
        0.6935700528860096,
        0.5771464525217862,
        0.4624977804451884,
        0.3534436068207931,
        0.2570963953311534,
        0.1759740859885426,
        0.1097424867210517,
        0.05680144954588862,
        0.01514602635020346,
        -0.01720668486024568,
        -0.04203242400031204,
        -0.06084070032206679
    ],
    "Std_Dev_Time": [
        0.07540463629449738,
        0.04129682183486871,
        0.02139499732990685,
        0.01460131967798076,
        0.01462189682817036,
        0.01492773542829787,
        0.01421212874127262,
        0.01279887503591457,
        0.01110782487488664,
        0.009420384908855653,
        0.007892337937940445,
        0.006596530657542032,
        0.005556193218146272,
        0.004765062915085582,
        0.004197866135196894
    ],
    "Std_Dev_Time_Percent": [
        0.3084610282281247,
        0.1867065168052587,
        0.1084440054292747,
        0.08371625948794968,
        0.09526926914604104,
        0.1106863028996918,
        0.1198272558930858,
        0.122422618058193,
        0.1201435557883877,
        0.114781469475326,
        0.1078871942647769,
        0.1007461696551898,
        0.09441402561754941,
        0.08972513158336456,
        0.08724947800745515
    ]
}









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

class crio:
    def __init__(self,url):
            self.url=url

    def post(self,endpoint,data):
        result=requests.post(self.url+"/"+endpoint,json=data,verify=False)
        return (result.text)

    def get(self,endpoint):
        result=requests.get(url=self.url+endpoint)
        return json.loads(result.text)
        

def coastd(massa_veiculo,coef_pista_a,coef_pista_b,coef_pista_c,data):
    velocidade_padrao = np.array(list(range(25, 101, 5)))

    # Agora, 'data' é uma variável que contém o conteúdo do arquivo json. Você pode trabalhar com ela como faria com um dicionário normal em Python.
    coef_1_a = data["PolCoefsReportArray_Force"][1][0]
    coef_1_b = data["PolCoefsReportArray_Force"][1][1]
    coef_1_c = data["PolCoefsReportArray_Force"][1][2]
    coef_2_a = data["PolCoefsReportArray_Force"][2][0]
    coef_2_b = data["PolCoefsReportArray_Force"][2][1]
    coef_2_c = data["PolCoefsReportArray_Force"][2][2]
    coef_3_a = data["PolCoefsReportArray_Force"][3][0]
    coef_3_b = data["PolCoefsReportArray_Force"][3][1]
    coef_3_c = data["PolCoefsReportArray_Force"][3][2]

    dt_max = data["MaxDif_Time_Pista"]
    df_max = data["MaxDif_Force_Pista"]

    # Cálculo Pista
    forca_pista = (coef_pista_c*(velocidade_padrao*velocidade_padrao) + coef_pista_b*velocidade_padrao + coef_pista_a)
    tempo_pista = (1.015*massa_veiculo)*((5/3.6)/forca_pista)

    # Cálculo Ensaio 1
    forca_1 = (coef_1_c*(velocidade_padrao*velocidade_padrao) + coef_1_b*velocidade_padrao + coef_1_a)
    tempo_1 = (1.015*massa_veiculo)*((5/3.6)/forca_1)

    # Cálculo Ensaio 2
    forca_2 = (coef_2_c*(velocidade_padrao*velocidade_padrao) + coef_2_b*velocidade_padrao + coef_2_a)
    tempo_2 = (1.015*massa_veiculo)*((5/3.6)/forca_2)

    # Cálculo Ensaio 3
    forca_3 = (coef_3_c*(velocidade_padrao*velocidade_padrao) + coef_3_b*velocidade_padrao + coef_3_a)
    tempo_3 = (1.015*massa_veiculo)*((5/3.6)/forca_3)


    ################### ENVIAR ##########################

    # Teste de Pista
    f_pista = list(reversed(forca_pista))
    t_pista = list(reversed(tempo_pista))

    # Ensaio 1
    f_teste1 = list(reversed(forca_1))
    t_teste1 = list(reversed(tempo_1))

    # Ensaio 2
    f_teste2 = list(reversed(forca_2))
    t_teste2 = list(reversed(tempo_2))

    # Ensaio 3
    f_teste3 = list(reversed(forca_3))
    t_teste3 = list(reversed(tempo_3))

    # Delta Tempo Máximo
    dt_max

    # Delta Força Máxima
    df_max

    dados_envio = {
        "t_pista": t_pista,
        "t_teste1": t_teste1,
        "t_teste2": t_teste2,
        "t_teste3": t_teste3,
        "dt_max": dt_max,
        "f_teste_pista": f_pista,
        "f_teste1": f_teste1,
        "f_teste2": f_teste2,
        "f_teste3": f_teste3,
        "df_max": df_max
    }

    return dados_envio


#Operations

def Operation_Coast_Down():
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
        try:
            t=e3.read_tag("Dados.apis.Operation_Coast_Down.btn")
            if t==True:
                print("Rodando Coast Down")
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
                print("Resultado {}".format(r))
                #r=json.loads(r)
                #e3.write_tag([
                #    ["Dados.amostraselecionada.cAcalculado",r["coefPistaDina_Calc"][0]],
                #    ["Dados.amostraselecionada.cBcalculado",r["coefPistaDina_Calc"][1]],
                #    ["Dados.amostraselecionada.cCcalculado",r["coefPistaDina_Calc"][2]]]
                #)
        except Exception as e:
            print(e)
        time.sleep(0.5)

def Operation_Coast_Down_R2():
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
                r1=coastd(dados_enviar["massaAmostra"],dados_enviar["coefPistaRolamento"][0],dados_enviar["coefPistaRolamento"][1],dados_enviar["coefPistaRolamento"][2],r)
                #print("e3:{}".format(r1))
                e3.write_tag([
                        ["Dados.amostraselecionada.cAcalculado",round(r["PolCoefsReportArray_Force"][0][0],4)],
                        ["Dados.amostraselecionada.cBcalculado",round(r["PolCoefsReportArray_Force"][0][1],4)],
                        ["Dados.amostraselecionada.cCcalculado",round(r["PolCoefsReportArray_Force"][0][2],4)],
                        ["Dados.Relatorios.CoastDown.pista.fpista1",round(r1["f_teste_pista"][14],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista2",round(r1["f_teste_pista"][13],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista3",round(r1["f_teste_pista"][12],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista4",round(r1["f_teste_pista"][11],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista5",round(r1["f_teste_pista"][10],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista6",round(r1["f_teste_pista"][9],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista7",round(r1["f_teste_pista"][8],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista8",round(r1["f_teste_pista"][7],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista9",round(r1["f_teste_pista"][6],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista10",round(r1["f_teste_pista"][5],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista11",round(r1["f_teste_pista"][4],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista12",round(r1["f_teste_pista"][3],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista13",round(r1["f_teste_pista"][2],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista14",round(r1["f_teste_pista"][1],3)],
                        ["Dados.Relatorios.CoastDown.pista.fpista15",round(r1["f_teste_pista"][0],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista1",round(r1["t_pista"][14],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista2",round(r1["t_pista"][13],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista3",round(r1["t_pista"][12],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista4",round(r1["t_pista"][11],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista5",round(r1["t_pista"][10],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista6",round(r1["t_pista"][9],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista7",round(r1["t_pista"][8],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista8",round(r1["t_pista"][7],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista9",round(r1["t_pista"][6],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista10",round(r1["t_pista"][5],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista11",round(r1["t_pista"][4],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista12",round(r1["t_pista"][3],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista13",round(r1["t_pista"][2],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista14",round(r1["t_pista"][1],3)],
                        ["Dados.Relatorios.CoastDown.pista.tpista15",round(r1["t_pista"][0],3)],
                        ["Dados.Relatorios.CoastDown.teste3.c0",round(r["PolCoefsReportArray_Force"][3][0],4)],
                        ["Dados.Relatorios.CoastDown.teste3.c1",round(r["PolCoefsReportArray_Force"][3][1],4)],
                        ["Dados.Relatorios.CoastDown.teste3.c2",round(r["PolCoefsReportArray_Force"][3][2],4)],
                        ["Dados.Relatorios.CoastDown.teste3.t1",round(r1["t_teste3"][14],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t2",round(r1["t_teste3"][13],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t3",round(r1["t_teste3"][12],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t4",round(r1["t_teste3"][11],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t5",round(r1["t_teste3"][10],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t6",round(r1["t_teste3"][9],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t7",round(r1["t_teste3"][8],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t8",round(r1["t_teste3"][7],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t9",round(r1["t_teste3"][6],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t10",round(r1["t_teste3"][5],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t11",round(r1["t_teste3"][4],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t12",round(r1["t_teste3"][3],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t13",round(r1["t_teste3"][2],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t14",round(r1["t_teste3"][1],3)],
                        ["Dados.Relatorios.CoastDown.teste3.t15",round(r1["t_teste3"][0],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f1",round(r1["f_teste3"][14],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f2",round(r1["f_teste3"][13],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f3",round(r1["f_teste3"][12],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f4",round(r1["f_teste3"][11],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f5",round(r1["f_teste3"][10],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f6",round(r1["f_teste3"][9],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f7",round(r1["f_teste3"][8],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f8",round(r1["f_teste3"][7],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f9",round(r1["f_teste3"][6],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f10",round(r1["f_teste3"][5],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f11",round(r1["f_teste3"][4],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f12",round(r1["f_teste3"][3],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f13",round(r1["f_teste3"][2],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f14",round(r1["f_teste3"][1],3)],
                        ["Dados.Relatorios.CoastDown.teste3.f15",round(r1["f_teste3"][0],3)],
                        ["Dados.Relatorios.CoastDown.teste2.c0",round(r["PolCoefsReportArray_Force"][2][0],4)],
                        ["Dados.Relatorios.CoastDown.teste2.c1",round(r["PolCoefsReportArray_Force"][2][1],4)],
                        ["Dados.Relatorios.CoastDown.teste2.c2",round(r["PolCoefsReportArray_Force"][2][2],4)],
                        ["Dados.Relatorios.CoastDown.teste2.t1",round(r1["t_teste2"][14],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t2",round(r1["t_teste2"][13],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t3",round(r1["t_teste2"][12],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t4",round(r1["t_teste2"][11],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t5",round(r1["t_teste2"][10],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t6",round(r1["t_teste2"][9],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t7",round(r1["t_teste2"][8],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t8",round(r1["t_teste2"][7],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t9",round(r1["t_teste2"][6],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t10",round(r1["t_teste2"][5],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t11",round(r1["t_teste2"][4],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t12",round(r1["t_teste2"][3],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t13",round(r1["t_teste2"][2],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t14",round(r1["t_teste2"][1],3)],
                        ["Dados.Relatorios.CoastDown.teste2.t15",round(r1["t_teste2"][0],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f1",round(r1["f_teste2"][14],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f2",round(r1["f_teste2"][13],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f3",round(r1["f_teste2"][12],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f4",round(r1["f_teste2"][11],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f5",round(r1["f_teste2"][10],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f6",round(r1["f_teste2"][9],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f7",round(r1["f_teste2"][8],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f8",round(r1["f_teste2"][7],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f9",round(r1["f_teste2"][6],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f10",round(r1["f_teste2"][5],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f11",round(r1["f_teste2"][4],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f12",round(r1["f_teste2"][3],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f13",round(r1["f_teste2"][2],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f14",round(r1["f_teste2"][1],3)],
                        ["Dados.Relatorios.CoastDown.teste2.f15",round(r1["f_teste2"][0],3)],
                        ["Dados.Relatorios.CoastDown.teste1.c0",round(r["PolCoefsReportArray_Force"][1][0],4)],
                        ["Dados.Relatorios.CoastDown.teste1.c1",round(r["PolCoefsReportArray_Force"][1][1],4)],
                        ["Dados.Relatorios.CoastDown.teste1.c2",round(r["PolCoefsReportArray_Force"][1][2],4)],
                        ["Dados.Relatorios.CoastDown.teste1.t1",round(r1["t_teste1"][14],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t2",round(r1["t_teste1"][13],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t3",round(r1["t_teste1"][12],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t4",round(r1["t_teste1"][11],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t5",round(r1["t_teste1"][10],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t6",round(r1["t_teste1"][9],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t7",round(r1["t_teste1"][8],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t8",round(r1["t_teste1"][7],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t9",round(r1["t_teste1"][6],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t10",round(r1["t_teste1"][5],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t11",round(r1["t_teste1"][4],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t12",round(r1["t_teste1"][3],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t13",round(r1["t_teste1"][2],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t14",round(r1["t_teste1"][1],3)],
                        ["Dados.Relatorios.CoastDown.teste1.t15",round(r1["t_teste1"][0],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f1",round(r1["f_teste1"][14],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f2",round(r1["f_teste1"][13],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f3",round(r1["f_teste1"][12],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f4",round(r1["f_teste1"][11],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f5",round(r1["f_teste1"][10],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f6",round(r1["f_teste1"][9],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f7",round(r1["f_teste1"][8],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f8",round(r1["f_teste1"][7],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f9",round(r1["f_teste1"][6],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f10",round(r1["f_teste1"][5],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f11",round(r1["f_teste1"][4],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f12",round(r1["f_teste1"][3],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f13",round(r1["f_teste1"][2],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f14",round(r1["f_teste1"][1],3)],
                        ["Dados.Relatorios.CoastDown.teste1.f15",round(r1["f_teste1"][0],3)],
                        ["Dados.Relatorios.CoastDown.delta.t1",round(r1["dt_max"][14],3)],
                        ["Dados.Relatorios.CoastDown.delta.t2",round(r1["dt_max"][13],3)],
                        ["Dados.Relatorios.CoastDown.delta.t3",round(r1["dt_max"][12],3)],
                        ["Dados.Relatorios.CoastDown.delta.t4",round(r1["dt_max"][11],3)],
                        ["Dados.Relatorios.CoastDown.delta.t5",round(r1["dt_max"][10],3)],
                        ["Dados.Relatorios.CoastDown.delta.t6",round(r1["dt_max"][9],3)],
                        ["Dados.Relatorios.CoastDown.delta.t7",round(r1["dt_max"][8],3)],
                        ["Dados.Relatorios.CoastDown.delta.t8",round(r1["dt_max"][7],3)],
                        ["Dados.Relatorios.CoastDown.delta.t9",round(r1["dt_max"][6],3)],
                        ["Dados.Relatorios.CoastDown.delta.t10",round(r1["dt_max"][5],3)],
                        ["Dados.Relatorios.CoastDown.delta.t11",round(r1["dt_max"][4],3)],
                        ["Dados.Relatorios.CoastDown.delta.t12",round(r1["dt_max"][3],3)],
                        ["Dados.Relatorios.CoastDown.delta.t13",round(r1["dt_max"][2],3)],
                        ["Dados.Relatorios.CoastDown.delta.t14",round(r1["dt_max"][1],3)],
                        ["Dados.Relatorios.CoastDown.delta.t15",round(r1["dt_max"][0],3)],
                        ["Dados.Relatorios.CoastDown.delta.f1",round(r1["df_max"][14],3)],
                        ["Dados.Relatorios.CoastDown.delta.f2",round(r1["df_max"][13],3)],
                        ["Dados.Relatorios.CoastDown.delta.f3",round(r1["df_max"][12],3)],
                        ["Dados.Relatorios.CoastDown.delta.f4",round(r1["df_max"][11],3)],
                        ["Dados.Relatorios.CoastDown.delta.f5",round(r1["df_max"][10],3)],
                        ["Dados.Relatorios.CoastDown.delta.f6",round(r1["df_max"][9],3)],
                        ["Dados.Relatorios.CoastDown.delta.f7",round(r1["df_max"][8],3)],
                        ["Dados.Relatorios.CoastDown.delta.f8",round(r1["df_max"][7],3)],
                        ["Dados.Relatorios.CoastDown.delta.f9",round(r1["df_max"][6],3)],
                        ["Dados.Relatorios.CoastDown.delta.f10",round(r1["df_max"][5],3)],
                        ["Dados.Relatorios.CoastDown.delta.f11",round(r1["df_max"][4],3)],
                        ["Dados.Relatorios.CoastDown.delta.f12",round(r1["df_max"][3],3)],
                        ["Dados.Relatorios.CoastDown.delta.f13",round(r1["df_max"][2],3)],
                        ["Dados.Relatorios.CoastDown.delta.f14",round(r1["df_max"][1],3)],
                        ["Dados.Relatorios.CoastDown.delta.f15",round(r1["df_max"][0],3)]
                    ]
                )
        except Exception as e:
            print(e)
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
            c.post(key, dados_envia)

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
        "Dados.apis.Operation_Curve_Loss_Static.f0",
        "Dados.apis.Operation_Curve_Loss_Static.f1",
        "Dados.apis.Operation_Curve_Loss_Static.f2"
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
                "RoadVelArray": [0 for a in range(0,60*60*24)]
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
                "RoadVelArray": [0 for a in range(0,60*60*24)],

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
                    "warmupVelocity": [int(dados_recebidos[0]),int(dados_recebidos[1]),int(dados_recebidos[2]),int(dados_recebidos[3]),int(dados_recebidos[4]),0],
                    "warmupTime": [int(dados_recebidos[5]),int(dados_recebidos[6]),int(dados_recebidos[7]),int(dados_recebidos[8]),int(dados_recebidos[9]),5]
                }
                print("s1")
                c.post(key,dados_enviar)
                print("s2")
        except Exception as e:
            print(e)
        time.sleep(0.5)




#Server Interface


def Interface_Curve_Loss_Static():
    while 1:
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
    while 1:
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
        except Exception as e:
            print(e)
        time.sleep(10)



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
#t.append(Thread(target=Operation_Coast_Down))
t.append(Thread(target=Operation_Coast_Down_R2))
t.append(Thread(target=Operation_RoadTest))
t.append(Thread(target=Operation_Curve_Loss_Static))
t.append(Thread(target=Interface_Curve_Loss_Static))
t.append(Thread(target=Operation_Durab_Teste))


for th in t:
    th.start()



async def echo(websocket):
    async for message in websocket:
        try:
            await websocket.send("{\"Forca_Calibrada\":"+str(r_data[1][1])+",\"Velocidade_kmh\":"+str(r_data[0][1])+",\"start\":"+str((int(r_data[11][1])&4)==4).lower()+",\"stop\":"+str((int(r_data[11][1])&8)==8).lower()+",\"end\":"+str((int(r_data[11][1])&2)==2).lower()+"}")
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
for th in t:
    th.join()