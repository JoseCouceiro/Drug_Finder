import streamlit as st
from drug_finder.cima_streamlit import Search
from drug_finder.handle_data import HandleData
from drug_finder.print_data import PrintMedInfo
from drug_finder.translator import Translate
from drug_finder.pubchem import Pubchem
from drug_finder.db.database_handle import DataBase


class Motor:
    """
    Esta clase es la que se encarga de mostrar por consola los menús que el usuario necesita navegar para conseguir la información. Aclaración: me gustaría hacerle una GUI si tengo tiempo, esto es una solución provisional.
    La clase se compone de dos tipos de funciones:
        
        - Funciones de navegación: se encargan de imprimir en pantalla los menús de navegación y llamar a los métodos necesarios en respuesta a los 'inputs' del usuario. Son de tres tipos:
                > Función 'welcome': inicia la navegación llamando al primer menú. A partir de ahí, cada menú llama al siguiente para que se sucedan unos a otros incluso cuando el usuario vuelve a un menú anterior.
                > Funciones diplay{n}: muestra el menú de opciones en pantalla, recoge el 'input' del usuario, lo procesa para comprobar que es correcto y llama a la función 'process_choice{n}' correspondiente introduciendo el 'input' procesado como parámetro.
                > Funciones __process_choice{n}: llaman a las funciones necesarias para realizar la tarea que el usuario ha seleccionado. También llaman a menús previos para que el usuario pueda realizar varias búsquedas sin salir de la aplicación.
        
        - Funciones que despliegan información: imprimen por pantalla la información de un principio activo o medicamento:
                > __select_medicine: obtiene la información de un medicamento y la imprime en pantalla. Utiliza métodos de las clases HandleData y PrintMedInfo.
                > __retrieve_compound_data: obtiene la información de un principio activo, la imprime en pantalla y descarga la imagen de su estructura utilizando métodos de la clase Pubchem.

        - Funciones que controlan los inputs: se valen de bucles 'while' para pedir al usuario el 'input' en el formato correcto tantas veces como haga falta para evitar errores:
                > __check_length: comprueba que las búsquedas de medicamento tengan al menos tres letras para evitar búsquedas ambiguas y con demasiado tiempo de espera.
                > __check_input: comprueba que los inputs sean de tipo 'dígito' cuando así se requiere y que estén en el rango apropiado.
    """

    def __init__(self):
        self.__searcher = Search()
        self.__handler = HandleData()
        self.__printer = PrintMedInfo()
        self.__translator = Translate()
        self.__pubchem = Pubchem()
        self.__db = DataBase()

    #FUNCIONES DE NAVEGACIÓN
    #MENU 1

    def med_list(self, response):
        if response == {}:
            st.write('\nNo results to show, please repeat your search')
            st.write('Check your spelling and remember that the database is in Spanish\n')
            return False   
        else:
            st.write("\nHere are the results:\n")
            __number_medicines = 0
            for __pag, __dic in response.items():
                for __med in __dic['resultados']:
                    __number_medicines +=1
                    st.write(f'{__number_medicines} ' + __med['nombre'])
            return __number_medicines


    def welcome(self):
        st.title('\nWELCOME TO DRUG FINDER')
        query = self.__display1()
        if query:
            self.__process_choice1(query)
        

    def __display1(self):
        st.write("\nYou may search for a medicine or an active compound:\n")
        medicine = st.text_input('Search a medicine')
        compound = st.text_input('Search an active compound')
        indication = st.text_input('Search by therapeutic indication')
        return medicine, compound, indication
    
    def __process_choice1(self, selection):
        medicine = selection[0]
        compound = selection[1] 
        indication = selection[2]
        if medicine:
            print(medicine)
            __search_term = self.__searcher.find_medicines(medicine)
            __func = self.__searcher.find_medicines
            __posting = False

            """ elif selection =='2':
            __search_term = self.__searcher.find_principles()
            __func = self.__searcher.find_principles
            __posting = False

            elif selection == '3':
            __search_term = self.__searcher.find_therapeutic_indication()
            __func = self.__searcher.find_therapeutic_indication
            __posting = True
        
            elif selection =='4':
            print('Ok, Bye!')
            exit()
            """
    
            self.__check_length(__search_term, __func)
            print('length checked')
            self.__searcher.search_motor(__posting)
            print('posting whatever')        
            self.__handler.save_json(self.__searcher.data_json,self.__searcher.response_dict)
            print('json_saved')
            self.__productive_search = self.med_list(self.__searcher.response_dict)
            
        #if self.__productive_search == False:
            #self.__display1()  

        #self.__display2()      

    """
    #MENU 2

    def __display2(self):
        print('\nPlease, select what you would like to do:\n')
        __choice2 = input( "  1. Generate a database or append to an existing one\n"
                           "  2. Get the list of medicines as a csv file\n"
                           "  3. Select one medicine from the list\n"
                           "  4. Back to select your medicine\n"
                           "  5. Exit\n")
        __nchoices = 5
        __output = self.__check_input(__choice2, __nchoices)
        self.__process_choice2(__output)

    def __process_choice2(self, selection):
        if selection == '1':
            regs = self.__db.get_register_nums(self.__searcher.response_dict)
            meds = self.__db.post_registers(regs)
            self.__db.generate_database(meds)
            print("\nWould you like to do anything else?")
            self.__display2()
        
        elif selection == '2':
            self.__handler.to_csv(self.__searcher.nombre,self.__searcher.response_dict)
            print("\nWould you like to do anything else?")
            self.__display2()

        elif selection == '3':
            self.__select_medicine()

        elif selection == '4':
            self.__display1()

        elif selection == '5':
            print('OK, bye!')
            exit()

        self.__display3()

    #MENU 3

    def __display3(self):
        print('\nWhat would you like to do?\n')
        __choice3 = input("1. Read drug documentation online\n"
                        "2. Get drug documentation in pdf\n"
                        "3. Explore active compounds\n"
                        "4. Select another medicine\n"
                        "5. Go back to main menu\n"
                        "6. Exit application\n")

        __nchoices = 6
        __output = self.__check_input(__choice3, __nchoices)
        self.__process_choice3(__output)

    def __process_choice3(self, selection):        
        if selection == '1': 
            self.__handler.read_info_online(self.nregistro)
            self.__display3()
            
        elif selection == '2':
            self.__handler.get_pdfs(self.__searcher.response_sing.json())
            
        elif selection == '3':
            self.__retrieve_compound_data()

        elif selection == '4':
            self.__printer.med_list(self.__searcher.response_dict)
            self.__select_medicine()
            self.__display3()
        
        elif selection == '5':
            self.__display1()

        elif selection == '6':
            print('OK, bye!')
            exit()
        
        self.__display4()

    #MENU 4

    def __display4(self):
        __choice4 = input("\nWould you like to do anything else?\n"
                "  1. Make a new search for drugs or active compounds\n"
                "  2. Go back to the list of medicines\n"
                "  3. Go back to the medicine menu\n"
                "  4. Exit program\n" )

        __nchoices = 4
        __output = self.__check_input(__choice4, __nchoices)
        self.__process_choice4(__output)

    def __process_choice4(self, selection):
        if selection == '1':
            self.__display1()

        elif selection == '2':
            self.__printer.med_list(self.__searcher.response_dict)
            self.__display2()

        elif selection == '3':
            self.__display3()

        elif selection =='4':
            print('Ok, Bye!')
            exit()

    #FUNCIONES ADICIONALES
    #Funciones que despliegan información    

    def __select_medicine(self):
        __medicine_choice = input('\nPlease, select a medicine by its number: ')
        __nchoices = self.__productive_search
        __medicine_num = self.__check_input(__medicine_choice, __nchoices)
        self.nregistro = self.__handler.find_nregistro(int(__medicine_num),self.__searcher.response_dict)

        self.__searcher.find_medicine(self.nregistro)
        self.__searcher.search_motor_sing()
         
        self.__handler.save_json_sing(self.__searcher.data_json_sing,self.__searcher.response_sing.json())
        self.__printer.basic_info(self.__searcher.response_sing.json())

    def __retrieve_compound_data(self):
        __comp_choice = input("\nPlease, select an active compound by its number:\n")
        __nchoices = self.__printer.number_compounds
        __comp_num = self.__check_input(__comp_choice, __nchoices)
        __comp_name = self.__handler.get_principle_name(__comp_num,self.__searcher.response_sing.json())

        __en_comp_name = self.__translator.translate_to_en(__comp_name)
        comp_props = self.__pubchem.get_compound_props(__en_comp_name.text)   
        self.__pubchem.get_png(__en_comp_name, comp_props)

    """#Funciones que controlan los inputs

    def __check_length(self, search_term, func):
        while len(search_term) < 3:
            print("Query must be at least 3 characters long")
            search_term = func()
    """

    def __check_input(self, choice, nchoices):
        if type(choice) != str:
            choice = str(choice)
        __choiceisright = False
        while __choiceisright ==False:
            while choice.isdigit() == False:
                choice = input(f"Please, select a number from 1 to {nchoices}\n")
            else:    
                try:
                    while int(choice) not in range (1, nchoices + 1):
                        choice = input(f"Please, select a number from 1 to {nchoices}\n")       
                    else : 
                        __choiceisright = True
                        return choice
                except:
                    choice = input(f"Please, select a number from 1 to {nchoices}\n") 
            
 """