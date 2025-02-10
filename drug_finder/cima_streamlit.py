import requests

class Search:
    """
    Esta es la clase encargada de realizar las búsquedas en la base de datos del CIMA (Centro de Información de Medicamentos de la Agencia Española de Medicamentos y productos Sanitarios -AEMPS-). Se proporciona como dato de inicio de la clase la dirección base de la API REST del CIMA. La clase contiene dos tipos de funciones:

        - Funciones 'find_...()': se encargan de inicializar las variables de búsqueda dependiendo de cuál sean los requerimientos de ésta:
                > find_medicine: búsqueda de las propiedades de un medicamento en concreto.
                > find_medicines: búsqueda de todos los medicamentos que contengan una palabra clave en el nombre.
                > find_principles: búsqueda de medicamentos por principio activo.
                > find_therapeutic_indication: búsqueda de medicamentos según sus indicaciones terapéuticas.

        - Funciones 'search_motor_...()': hacen el 'request' utilizando los parámetros y almacenan la respuesta en una variable de clase:
                > search_motor_sing: utiliza los parámetros de la función find_medicine y almacena la respuesta en formato json.
                > search_motor: utiliza los parámetros del resto de funciones de la clase. Construye un diccionario organizado con las respuestas obtenidas (archivos json con 25 medicamentos cada uno). Aclaración: para cuando me di cuenta de que podría haber iterado sobre las respuesta sin necesidad de construir este diccionario, ya había muchas funciones que dependían de él así que decidí dejarlo así. La función recibe un parámetro 'posting' que determina si debe hacerse un 'request' de tipo 'get' o 'post'.
    """

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
        
    def find_principles(self):
        self.__url = self.__base_url + 'medicamentos?'
        self.nombre = input('\nPlease, write the name of the active compound: ')
        self.__condition = 'practiv1'
        return self.nombre

    def find_therapeutic_indication(self):
        self.__url = self.__base_url + 'buscarEnFichaTecnica'
        self.__data = [{
                        "seccion":"4.1",
                        "texto":input('\nPlease, write a keyword: '),
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

