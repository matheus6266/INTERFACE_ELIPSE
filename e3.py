import win32com.client
import time,datetime

class elipse:
    def __init__(self):
        """
        Funcoes disponiveis
        read_tag - tag ou [tag1,tag2,...,tagx]
        write_tag - [tag,valor] ou [[tag1,valor1],[tag2,valor2],...,[tagx,valorx]] - Resposta True para escrita correta 
        """
        self.E3=win32com.client.Dispatch('{80327130-FFDB-4506-B160-B9F8DB32DFB2}')
        

    def read_tag(self,tag): 
        """
        tag: String ou lista de String - Retorna o valor lido. Caso não encontre a tag ou o server esteja parado retorna none.
        """
        if type(tag) is list:
            result=[]
            for t in tag:
                result.append(self.E3.ReadValue(t)[3])
            return result
        return self.E3.ReadValue(tag)[3]

    def write_tag(self,data,teste=False):
        """
        write_tag - [tag,valor] ou [[tag1,valor1],[tag2,valor2],...,[tagx,valorx]] - Resposta True para escrita correta
        """
        timestamp=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if type(data[0]) is list:
            result=[]
            for tag in data:
                result.append(self.E3.WriteValue(tag[0],timestamp,192,tag[1]))
            return result
        if teste:
            s=self.E3.WriteValue(data[0],timestamp,192,data[1])
            if not s:
                pass
                #self.E3=win32com.client.Dispatch('{80327130-FFDB-4506-B160-B9F8DB32DFB2}')
                #return s
            return s
        return self.E3.WriteValue(data[0],timestamp,192,data[1])

#if __name__=="__main__":
#    e3=elipse()
#    x=0
#    while 1:
#        resultado_escrita=e3.write_tag([["Dados.apis.heartbeat",1]])
#        print("Resultado das escritas {}".format(resultado_escrita))
#        x=x+1
#        print("Leitura das tags:{}".format(e3.read_tag(["Dados.apis.heartbeat"])))
#        time.sleep(1)
