from importlib import resources
import json

from drug_finder.config import cfg_item
from drug_finder.db.connection import create_connection, execute_query
from drug_finder.cima import Search
from drug_finder.translator import Translate
from drug_finder.pubchem import Pubchem

    
class DataBase():

    """Esta clase genera una base de datos en la carpeta "outputs" a partir de las listas de medicamentos obtenidas en las búsquedas efectuadas contra la API de la AEMPS. Por cada uno de estos medicamentos, la clase se encarga de almacenar información seleccionada de las respuestas de la API (he guardado un ejemplo de esta respuesta en formato json en la carpeta "temp" con el nombre: "meds_prop_example.json"). Además, para cada uno de los principios activos presentes en cada medicamento, la clase efectua una búsqueda en la base de datos Pubchempy y los almacena. La clase toma funciones prestadas de los módulos "cima", "translator" y "pubchem" para lo que instancia una clase "Search()", "Translate()" y "Pubchem()" respectivamente en su función de inicio.
    
    Existen 3 tipos de funciones en la clase:
        -Funciones que se encargan de procesar datos para poder enviarlos a la base de datos de manera ordenada:
            
            "get_register_nums():  obtiene una lista con los números de registro de cada medicamento de la lista obtenida tras consultar la API del AEMPS"
            
            "post_register_nums(): por cada número de registro en la lista generada por "get_register_nums(), esta función envía una búsqueda a la API del AEMPS y obtiene una lista de diccionarios, cada uno de ellos con información pormenorizada de cada medicamento (la función almacena esta lista en formato json en la carpeta "temp", esto no es necesario para que funcione la aplicación, pero muy útil para el desarrollo de la app)". Tanto enviar las búsquedas a la API, como procesarlas en formato json, lo hacen dos funciones de la clase "Search()" importada del módulo "cima" (es decir, pertenecen a la asignatura de Programación Avanzada). Al igual que "get_register_nums()", esta función se corre en el móduclo motor (el encargado de generar los menús interactivos de la app), previamente a "generate_database()" (son funciones que pondría en el "módulo handle_data", pero dejo aquí para facilitar la corrección)

            "get_compounds_dic": toma la lista de medicamentos generada por "post_registers()" y crea una lista de principios activos con datos pormenorizados obtenidos de la API de Pubchem, que se almacena como variable de clase (y como archivo json en "temp", para comodidad del programador). Para ello hace uso de la funcion "translate_to_en()" del módulo "translator" (que traduce los principios activos al inglés, creada para la actividad de Programación Avanzada) y "get_compound_dic()" del módulo Pubchem (creada para la actividad de Bases de Datos). Tambíen crea otra lista de clase ("empyt_compounds") con los nombre de los compuestos que no devuelven información tras la búsqueda en Pubchem.

        -"generate_database()": función que ordena todas las demás funciones para que se activen en orden

        -Funciones que envían instrucciones SQL: a su vez de dos tipos:
            
            Funciones "create_table_...()": insertan tablas en la base de datos. Las tablas se pueden consultar en los modelos "entidad-relación" y "relacional" incluidos en la actividad en la carpeta "resources/models...". Son funciones muy sencillas que envian una instrucción convencional que se les ha proporcionado en el código como un "string", excepto las funciones que crean las tablas MEDICINES y ACTIVE_PRINCIPLES, que explico a continuación:

                "create_table_medicines()": en esta función intenté automatizar la creación de la tabla con las claves obtenidas en las respuestas de la API del AEMPS, sin embargo me resultó imposible porque las claves cambian de un medicamento a otro (por ejemplo, la clave "fotos" aparece sólo si hay fotografías del medicamento), lo que dificulta la inserción automática de los datos. Al final opté por almacenar claves de interés en el archivo "config.json" (en la carpeta "resources/config") y automatizar la creación de las columnas de la tabla a partir de este archivo. De esta manera, se puede modificar el número de columnas sin acceder al código. También añade a la instrucción SQL una clave foránea a la tabla ADMINISTRATION_ROUTES. A todas las columnas se les da el tipo TEXT, ya que el valor matemático no es relevante (y da problemas en la mayoría de los casos, ya que muchos códigos varían de tipo en las respuestas de la API), excepto a los buleanos, que se transforman en enteros (1 ó 0).
                
                "create_table_pactivos()": las columnas de la tabla ACTIVE_PRINCIPLES vienen de dos APIS distintas, así que la función se adapta a esto. Envía una instrucción con las columnas para la id, el código y el nombre de la AEMPS y genera de forma automatizada las columnas procedentes de la respuesta enviada por la API de Pubchem (esta es más fiable y el número de claves es constante en todas las búsquedas). Algunas de las claves se descartan porque no me interesan en este momento. Todas las columnas son de tipo TEXT porque el valor matemático no es relevante.

            Funciones "insert_data_...()": funcionan de manera similar a las funciones "create_table_...()", pero en vez de tomar las claves, toman los valores de esas correspondientes a esas claves para insertarlos en una intrucción SQL de tipo "INSERT VALUES". De nuevo, no tienen mucha complicación excepto las funciones que insertan los datos de las tablas MEDICINES Y ACTIVE_PRINCIPLES:

                "insert_data_medicines()": recorre cada una de las claves dadas por la respuesta de la API de la AEMPS. Con esta clave acude al archivo config.json y obtien el valor "inst" para esta clave. Este valor decide en una sentencia if qué parte del valor correspondiente a cada clave de la respuesta de la API tomará la función para construir la instrucción SQL, dependiendo de si es una lista, un diccionario, un string o un entero. Gracias a este archivo json, se pueden insertar o quitar columnas y rellenarlas en la tabla MEDICINES sin tocar el código.
                 
                "self.__insert_data_pactivos()": al igual que "create_table_pactivos()", esta función obtiene datos de las respuestas de las APIs de AEMPS y Pubmed. Toma los valores de las claves indicadas de la AEMPS y construye una instrucción SQL con ellas. Con la respuesta de Pubmed lo hace de forma automatizada, tomando el valor correspondiente a la clave de forma sucesiva. Para coordinar la introducción de datos entre AEMPS y Pubchem, se establece una cuenta por cada valor introducido. Para evitar buscar varias veces el mismo compuesto (que generará un error UNIQUE en la base de datos y consumirá recursos), los compuestos ya buscados se almacenan en un set por su identificador 'cid' y se evita insertar los compuestos ya presentes en él con una sentencia if. Esta estrategia se usa en todas las tablas principales. De momento, por falta de tiempo, no hay una manera de evitar los errores unique cuando se añaden entradas a una base de datos después de cerrar el programa, pero estos errores no paran el programa por lo que los nuevas entradas se añaden igual.
    """

    def __init__(self):
        self.__searcher = Search()
        self.__translator = Translate()
        self.__pcp = Pubchem()
        
    def get_register_nums(self, response_dict):
        __register_nums = []
        for __pag, __dic in response_dict.items():
            for __med in __dic['resultados']:
                __register_nums.append(__med['nregistro'])
        return __register_nums

    def post_registers(self, nregister_lst):
        __response_list = []
        for nregister in nregister_lst:
            self.__searcher.find_medicine(nregister)
            med_props_json = self.__searcher.search_motor_sing()
            __response_list.append(med_props_json)
            with open(resources.path('drug_finder.temp','med_props_list.json'), 'w') as __file:
                json.dump(__response_list, __file)
        return __response_list
    
    def __get_compounds_dic(self, response_list):
        self.__ap_response_list = []
        self.__empty_compounds = []
        for __med in response_list:
            for __ap in __med['principiosActivos']:
                __compound_es = __ap['nombre']
                __compound_en = self.__translator.translate_to_en(__compound_es)
                comp_dic = self.__pcp.get_compound_dic(__compound_en.text)
                self.__ap_response_list.append(self.__pcp.comp_dic)
                if not comp_dic:
                    self.__empty_compounds.append(__compound_es)
        with open(resources.path('drug_finder.temp','ap_props_list.json'), 'w') as __file:
            json.dump(self.__ap_response_list, __file)
    
    def generate_database(self, response_list):
        #database connection
        self.__connection = create_connection(resources.path("drug_finder.outputs",f"{input('Please, insert database name (name.db): ')}"))
        self.__connection.execute("PRAGMA foreign_keys = 1")
        
        #integration of data from Pubchem
        self.__get_compounds_dic(response_list)  
        
        #creating tables
        self.__create_table_vias_administracion()
        self.__create_table_medicines()   
        self.__create_table_pactivos(self.__ap_response_list)
        self.__create_table_activity()
        self.__create_table_excipients()
        self.__create_table_contain()
        self.__create_table_atcs()
        self.__create_table_classify()
        self.__create_table_documents()
        
        #inserting data
        self.__insert_data_vias_administracion(response_list)
        self.__insert_data_medicines(response_list)     
        self.__insert_data_pactivos(response_list, self.__ap_response_list, self.__empty_compounds)
        self.__insert_data_activity(response_list, self.__empty_compounds)
        self.__insert_data_excipients(response_list)
        self.__insert_data_contain(response_list)
        self.__insert_data_atcs(response_list)
        self.__insert_data_classify(response_list) 
        self.__insert_data_documents(response_list)
      
    def __create_table_medicines(self):
        self.__table_keys = []
        __query = """CREATE TABLE IF NOT EXISTS MEDICINES("""
        for __attr in cfg_item("med_attributes"):
            self.__table_keys.append(__attr)
            __column = cfg_item("med_attributes", f"{__attr}", "column")
            __typ = cfg_item("med_attributes", f"{__attr}", "type")
            __query += f"""{__column} {__typ},"""  
        __query += f"""PRIMARY KEY (AEMPS_register_number),
                FOREIGN KEY (administration_id) REFERENCES ADMINISTRATION_ROUTES (id_AEMPS)
            );"""
        #print(__query)
        execute_query(self.__connection, __query)

    def __insert_data_medicines(self, response_list):  
        __query_list = []               
        for __med in response_list:
            __prop_list = [] 
            for __key, __prop in __med.items():
                if __key in self.__table_keys:
                    type_num = {cfg_item("med_attributes", f"{__key}", "inst")}
                    if type_num == {1}:
                        inst = f"'{__prop}'"
                    if type_num == {2}:
                        inst = f"{int(__prop)}"
                    if type_num == {3}:
                        inst = f"'{__prop['aut']}'"
                    if type_num == {4}:
                        inst = f"'{__prop['nombre']}'"
                    if type_num == {5}:
                        inst = f"'{__prop[0]['id']}'"
                    __prop_list.append(inst)
            __prop_str = ','.join(__prop_list)
            __query_list.append(f"INSERT INTO MEDICINES VALUES({__prop_str});")
        for __query in __query_list:
            #print(__query)
            execute_query(self.__connection, __query)       

    def __create_table_pactivos(self, ap_list):    
        __query = """CREATE TABLE IF NOT EXISTS ACTIVE_PRINCIPLES("""
        __query += """id_AEMPS TEXT PRIMARY KEY,
                    Code_AEMPS TEXT,
                    Name TEXT"""
        for __key in ap_list[0].keys():
            if __key in {'atoms', 'bonds', 'elements', 'record'}:
                pass
            else:
                __query += f""", {__key} TEXT"""
        __query += ");"
        #print(__query)
        execute_query(self.__connection, __query)

    def __insert_data_pactivos(self, response_list, ap_list, empty_compounds):
        __i = 0
        __check_compounds = set()
        for __med in response_list:
            for __ap in __med['principiosActivos']:
                if __ap['nombre'] not in __check_compounds:
                    __check_compounds.add(__ap['nombre'])
                    __query = f"""INSERT INTO ACTIVE_PRINCIPLES VALUES ('{__ap["id"]}', '{__ap["codigo"]}', '{__ap["nombre"]}'"""
                    if __ap['nombre'] not in empty_compounds:
                        for __key, __value in ap_list[__i].items():
                            if str(__key) not in {"atoms", "bonds", "elements", "record"}:
                                if __value == None:
                                    __query += f", {'NULL'}"
                                else:
                                    __query += f", '{__value}'"
                    else:
                        __query = f"""INSERT INTO ACTIVE_PRINCIPLES (id_AEMPS, Code_AEMPS, Name) VALUES ('{__ap["id"]}', '{__ap["codigo"]}', '{__ap["nombre"]}'"""
                    __i += 1
                    __query += ");"
                    #print(__query)
                    execute_query(self.__connection, __query)

    
    def __create_table_activity(self):
        __query = """CREATE TABLE IF NOT EXISTS ACTIVITY(
                nregistro_med INTEGER,
                id_pactivo TEXT,
                Amount INTEGER,
                Unit TEXT,
                CONSTRAINT PK_ACTIVITY PRIMARY KEY(nregistro_med,id_pactivo),
                FOREIGN KEY('nregistro_med') REFERENCES MEDICINES('AEMPS_register_number'),
                FOREIGN KEY('id_pactivo') REFERENCES ACTIVE_PRINCIPLES('id_AEMPS')
            );"""
        #print(__query)
        execute_query(self.__connection, __query)
       
    def __insert_data_activity(self, response_list, empty_compounds):
        for __med in response_list:
            for __ap in __med['principiosActivos']:
                if __ap['nombre'] not in empty_compounds:
                    __query = f"""INSERT INTO ACTIVITY VALUES ({__med['nregistro']}, '{__ap['id']}', {__ap['cantidad']}, "{__ap['unidad']}");"""
                    #print(__query)
                    execute_query(self.__connection, __query)

       
    def __create_table_excipients(self):    
        __query = """CREATE TABLE IF NOT EXISTS EXCIPIENTS(
                    id_AEMPS INTEGER PRIMARY KEY,
                    Name TEXT
                );"""
        #print(__query)
        execute_query(self.__connection, __query)

    def __insert_data_excipients(self, response_list):
        __check_excip = set()
        for __med in response_list:
            try:
                for __excip in __med['excipientes']:
                    if __excip['id'] not in __check_excip:
                        __check_excip.add(__excip['id'])
                        __query = f"""INSERT INTO EXCIPIENTS VALUES ({__excip["id"]}, '{__excip["nombre"]}');"""
                        #print(__query)
                        execute_query(self.__connection, __query)
            except KeyError:
                print(f"The entry {__med['nombre']} does not contain any excipient")
                pass

    def __create_table_contain(self):
        __query = """CREATE TABLE IF NOT EXISTS CONTAIN(
                nregistro_med TEXT,
                id_excipient INTEGER,
                Amount TEXTO,
                Unit TEXTO,
                CONSTRAINT PK_CONTAIN PRIMARY KEY(nregistro_med,id_excipient),
                FOREIGN KEY('nregistro_med') REFERENCES MEDICINES('AEMPS_register_number'),
                FOREIGN KEY('id_excipient') REFERENCES EXCIPIENTS('id_AEMPS')
            );"""
        #print(__query)
        execute_query(self.__connection, __query)
       
    def __insert_data_contain(self, response_list):
        for __med in response_list:
            try:
                for __excip in __med['excipientes']:
                    __query = f"""INSERT INTO CONTAIN VALUES ('{__med['nregistro']}', {__excip['id']}, '{__excip['cantidad']}', "{__excip['unidad']}");"""
                    #print(__query)
                    execute_query(self.__connection, __query)
            except KeyError:
                pass

    def __create_table_atcs(self):  
        __query = """CREATE TABLE IF NOT EXISTS ATCS(
                    AEMPS_code TEXT PRIMARY KEY,
                    Name TEXT
                );"""
        #print(__query)
        execute_query(self.__connection, __query)

    def __insert_data_atcs(self, response_list):
        __check_atcs = set()
        for __med in response_list:
            try:
                for __atcs in __med['atcs']:
                    if __atcs['codigo'] not in __check_atcs:
                        __check_atcs.add(__atcs['codigo'])
                        __query = f"""INSERT INTO ATCS VALUES ('{__atcs["codigo"]}', '{__atcs["nombre"]}');"""
                        #print(__query)
                        execute_query(self.__connection, __query)
            except KeyError:
                print(f"The entry {__med['nombre']}does not contain any ATCS data")
                pass

    def __create_table_classify(self):
        __query = """CREATE TABLE IF NOT EXISTS CLASSIFY(
                nregistro_med TEXT,
                code_ATCS TEXT,
                CONSTRAINT PK_CLASSIFY PRIMARY KEY(nregistro_med,code_ATCS),
                FOREIGN KEY('nregistro_med') REFERENCES MEDICINES('AEMPS_register_number'),
                FOREIGN KEY('code_ATCS') REFERENCES ATCS('AEMPS_code')
            );"""
        #print(__query)
        execute_query(self.__connection, __query)
       
    def __insert_data_classify(self, response_list):
        for __med in response_list:
            try:
                for __atcs in __med['atcs']:
                    __query = f"""INSERT INTO CLASSIFY VALUES ('{__med["nregistro"]}', '{__atcs["codigo"]}');"""
                    #print(__query)
                    execute_query(self.__connection, __query)
            except KeyError:
                pass

    def __create_table_vias_administracion(self):
        __query = """CREATE TABLE IF NOT EXISTS ADMINISTRATION_ROUTES(
                    id_AEMPS TEXT PRIMARY KEY,
                    Name TEXT
                );"""
        #print(__query)
        execute_query(self.__connection, __query)

    def __insert_data_vias_administracion(self, response_list):
        __check_adm_routes = set()
        for __med in response_list:
            try:
                for __via_admin in __med['viasAdministracion']:
                    if __via_admin['id'] not in __check_adm_routes:
                        __check_adm_routes.add(__via_admin['id'])
                        __query = f"""INSERT INTO ADMINISTRATION_ROUTES VALUES ('{__via_admin["id"]}', '{__via_admin["nombre"]}');"""
                        #print(__query)
                        execute_query(self.__connection, __query)
            except KeyError:
                print(f"The entry {__med['nombre']} does not contain any administration route")
                pass

    def __create_table_documents(self):
        __query = """CREATE TABLE IF NOT EXISTS DOCUMENTS(
                    Type TEXT,
                    urlHtml TEXT PRIMARY KEY,
                    nregistro_med TEXT,
                    FOREIGN KEY('nregistro_med') REFERENCES MEDICINES('AEMPS_register_number')
                );"""
        #print(__query)
        execute_query(self.__connection, __query)

    def __insert_data_documents(self, response_list):
        __change_type = {1: 'Data sheet', 2: 'Leaflet'}
        for __med in response_list:
            try:
                for __doc in __med['docs']:
                    __query = f"""INSERT INTO DOCUMENTS VALUES ('{__change_type[__doc['tipo']]}', '{__doc["urlHtml"]}', '{__med["nregistro"]}');"""
                    #print(__query)
                    execute_query(self.__connection, __query)
            except KeyError:
                print(f"The entry {__med['nombre']} does not contain any documents")
                pass



