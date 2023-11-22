import math
import re

import webbrowser
from importlib import resources
import requests
import json

class HandleData():
    """
    Esta clase se encarga de buscar informacion en las respuestas que obtiene la clase 'cima.Seaarch' y salvarla a disco, abrirla en el navegador de internet o almacenarla en una variable para ser usado por funciones de otras clases. Contiene tres tipos de funciones:
    
        - Funciones que almacenan datos temporales: almacenan las respuestas a los 'requests' como archivos json en la carpeta 'temp'. Estos json se sobreescriben cada vez que se realiza una búsqueda. Aclaración: no son necesarias para que la aplicación funcione y no aportan nada al usuario, pero me resultaron muy útiles durante el desarrollo para ir analizando las respuestas, así que he decidido dejarlas para posibles desarrollos futuros.
                > save_json_sing(): guarda la respuesta obtenida por el método 'Search.search_motor_sing'.
                > save_json(): guarda la respuesta obtenida por el método 'Search.search_motor'.

        - Funciones que obtienen datos internos: buscan información en las respuestas y devuelven un dato que será utilizado por otras funciones:
                > find_nregistro(): obtiene el número de registro de una medicina a partir del número que tiene en la lista de medicamentos que se imprime después de cada búsqueda.
                > get_principle_name(): obtiene el nombre de los principios activos presentes en una medicina a partir de su número en la lista de principios que se imprime al mostrar las propiedades de cada medicamento.

        - Funciones que devuelven datos al usuario: 
                > read_info_online(): abre una página del navegador de internet por defecto del sistema con la página web del prospecto de la medicina.
                > get_pdfs(): descarga el prospecto de la medicina en formato pdf en la carpeta 'outputs'.
                > to_csv(): descarga un archivo de texto en formato csv con la lista de medicamentos resultante de las búsquedas.
    """

    def __init__(self):
        self.__base_url_info = "https://cima.aemps.es/cima/dochtml/p/"

    #Funciones que producen archivos temporales

    def save_json(self, name, response):
        with open(resources.path('drug_finder.temp',name), 'w') as __file:
            json.dump(response, __file)

    def save_json_sing(self, name, response):
        with open(resources.path('drug_finder.temp',name), 'w') as __file:
            json.dump(response, __file)

    #Funciones que obtienen datos internos
  
    def find_nregistro(self, medicine_num, response):
        __page_num = math.ceil(medicine_num / 25)
        __resto = medicine_num % 25
        __div = math.floor(medicine_num / 25)

        if __resto == 0:
            __med_num = int(medicine_num / __div)
        elif __resto == medicine_num:
            __med_num = medicine_num
        elif __resto < 25:
            __med_num =  __resto
  
        self.__nregistro = response[f'pagina_{__page_num}']['resultados'][__med_num-1]['nregistro']
        return self.__nregistro

    def get_principle_name(self, ap_num, response):
        return response['principiosActivos'][int(ap_num)-1]['nombre']

    #Funciones que devuelven datos al usuario

    def read_info_online(self,nregistro):
        __url = self.__base_url_info + f"{nregistro}/Prospecto.html"
        __webpage = requests.get(__url)
        
        if __webpage.status_code == 404:
            print(f'Error 404: Prospect not available in database')    
        else:
            print("\nThe webpage will open in your browser")
            webbrowser.open_new_tab(__url)    

    def get_pdfs(self, response):
        __nombre = "_".join(re.split('\W+',response['nombre'])[0:2])
        __forma = response['formaFarmaceutica']['nombre'].split()[0]
        __docs = response['docs']
        
        try:           
            for __el in __docs:    
                if __el["tipo"] == 2:
                    __url = response['docs'][__docs.index(__el)]['url']
            __file = requests.get(__url)
            with open(resources.path('drug_finder.outputs',f"Prospecto_{__nombre}_{__forma}.pdf"),'wb') as __pdf:
                __pdf.write(__file.content)        
            print("\nProspect downloaded to outpust folder")       
        except:
            print('Prospect not available in database')
            pass
        
    def to_csv(self,name,response):      
        self.__i = 0      
        with open(resources.path('drug_finder.outputs',f'List_of_medicines_{name}.txt'), 'w') as __drugs:
            for _,__dic in response.items():
                for __med in __dic['resultados']:
                    self.__i += 1
                    __drugs.write(f"{self.__i},{__med['nombre']}\n")
        print("\ncsv file saved in outputs folder")
    









