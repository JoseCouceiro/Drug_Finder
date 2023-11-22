class PrintMedInfo():
    """
    Esta clase selecciona la información de la respuesta obtenida por la clase 'Search' que se va a mostrar por pantalla y la imprime. Para ello tiene como variables de inicio unos diccionarios que asocian cada dato de interés del json de respuesta con el nombre que queremos darle a cada dato. Por ejemplo, para mostrar por pantalla el laboratorio que fabrica un medicamento, asociamos 'Laboratory' con 'labtitular'. Los datos del json pueden ser de tipo 'string', 'lista' o 'diccionario'. La clase contiene dos funciones:
            
            - med_list: usa el diccionario generado a partir de la respuesta por el método 'Search.search_motor' e imprime una lista de cada entrada con un número asociado que servirá para que el usuario pueda escoger qué medicamento quiere consultar. Si la búsqueda no ha sido productiva se obtiene un diccionario vacío. En ese caso la función imprime un aviso de que no se han obtenido resultados de la búsqueda y devuelve 'False'. Esta señal se interpreta durante la navegación por los menús de la clase 'Motor' para regresar al menú de búsquedas.
            
            - basic_info: usa la respuesta obtenida por el método 'Search.search_motor_sing' e imprime la información de un medicamento seleccionada en las variables de inicio.
    """

    def __init__(self):
        self.__interest_data_strings = {'Name': 'nombre',
                'Register' : 'nregistro',
                'Laboratory': 'labtitular',
                'Use': 'cpresc',
                'Generic': 'generico',
                'Prescription': 'receta',
                'Dosage' : 'dosis'
                }
        self.__interest_data_dics = {
                'Pharmaceutical form' : 'formaFarmaceutica'
                }
        self.__interest_data_lists = {
            'Active compounds': 'principiosActivos'
            }

    def basic_info(self, response_sing):
        print('\n')
        for __key, __value in self.__interest_data_strings.items():
            if response_sing[__value] == True:
                response_sing[__value] = 'Sí'
            if response_sing[__value] == False:
                response_sing[__value] = 'No'        
            print(f"  {__key}: {response_sing[__value]}")
        
        for __key, __value in self.__interest_data_dics.items():       
            print(f"  {__key}: {response_sing[__value]['nombre'].capitalize()}")

        self.number_compounds = 0
        for key, value in self.__interest_data_lists.items():        
            print(f'  {key}:')
            for __activep in response_sing[value]:
                self.number_compounds += 1
                print(f"    {self.number_compounds} {__activep['nombre'].capitalize()}")


    def med_list(self, response):
        if response == {}:
            print('\nNo results to show, please repeat your search')
            print('Check your spelling and remember that the database is in Spanish\n')
            return False   
        else:
            print("\nHere are the results:\n")
            __number_medicines = 0
            for __pag, __dic in response.items():
                for __med in __dic['resultados']:
                    __number_medicines +=1
                    print(f'{__number_medicines} ' + __med['nombre'])
            return __number_medicines

        