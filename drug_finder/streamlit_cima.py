import requests

class Search:

    def __init__(self):
        self.__base_url = 'https://cima.aemps.es/cima/rest/'
        self.data_json = 'lista_de_medicamentos.json'

    def find_medicine(self, nregistro):
        self.__url = self.__base_url + 'medicamento?'
        self.nombre = nregistro
        self.__condition = 'nregistro'
        self.data_json_sing = 'propiedades_de_medicamento.json'

    def find_medicines(self, medicine):
        self.__url = self.__base_url + 'medicamentos?'   
        self.nombre = medicine
        self.__condition = 'nombre'
        return self.nombre
        
    def find_principles(self, compound):
        self.__url = self.__base_url + 'medicamentos?'
        self.nombre = compound
        self.__condition = 'practiv1'
        return self.nombre

    def find_therapeutic_indication(self, indication):
        self.__url = self.__base_url + 'buscarEnFichaTecnica'
        self.__data = [{
                        "seccion":"4.1",
                        "texto": indication,
                        "contiene":1
                     }]
        return self.__data[0]['texto']

    def search_motor_sing(self):     
        self.response_sing = requests.get(self.__url + f'{self.__condition}={self.nombre}')
        return self.response_sing.json()

    def search_motor(self, posting):
        self.response_dict = {}
        __params = {'pagina': 0}
        
        __running = True
        while __running:
            __params['pagina'] += 1

            if posting == False:    
                self.__response = requests.get(self.__url + f'{self.__condition}={self.nombre}', params=__params)
            else:
                self.__response = requests.post(url = self.__url, json = self.__data, params=__params)

            if self.__response.json()['totalFilas'] == 0:
                __running = False         
            else:
                self.response_dict[f"pagina_{__params['pagina']}"] = self.__response.json()

