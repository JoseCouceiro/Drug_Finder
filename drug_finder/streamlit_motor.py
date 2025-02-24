import streamlit as st
from drug_finder.streamlit_cima import Search
from drug_finder.handle_data import HandleData
from drug_finder.streamlit_print_data import PrintMedInfo
from drug_finder.translator import Translate
from drug_finder.pubchem import Pubchem
from drug_finder.db.database_handle import DataBase


class Motor:

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
                self.button_dic = dict()
                for __med in __dic['resultados']:
                    __number_medicines +=1
                    button = st.button(f'{__number_medicines} ' + __med['nombre'])
                    self.button_dic[__number_medicines] = button
            return __number_medicines
        
    def __select_medicine(self, choice):
        self.nregistro = self.__handler.find_nregistro(choice,self.__searcher.response_dict)

        self.__searcher.find_medicine(self.nregistro)
        self.__searcher.search_motor_sing()
         
        self.__handler.save_json_sing(self.__searcher.data_json_sing,self.__searcher.response_sing.json())
        self.__printer.basic_info(self.__searcher.response_sing.json())


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
    
    def __display_medicines(self, query, func, post):
        self.__check_length(query, func)
        self.__searcher.search_motor(post)    
        self.__handler.save_json(self.__searcher.data_json,self.__searcher.response_dict)
        return self.med_list(self.__searcher.response_dict)
    
    def __process_choice1(self, selection):
        st.write('RUNNING PROCESS_CHOICE1')
        medicine = selection[0]
        compound = selection[1] 
        indication = selection[2]
        if medicine:
            st.write('MEDICINE: ', medicine)
            __search_term = self.__searcher.find_medicines(medicine)
            __func = self.__searcher.find_medicines
            __posting = False
            self.__display_medicines(__search_term, __func, __posting)
  

        if compound:
            st.write('COMPOUND: ', compound)
            __search_term = self.__searcher.find_principles(compound)
            __func = self.__searcher.find_principles
            __posting = False
            self.__display_medicines(__search_term, __func, __posting)

        if indication:
            st.write('INDICATION: ', indication)
            __search_term = self.__searcher.find_therapeutic_indication(indication)
            __func = self.__searcher.find_therapeutic_indication
            __posting = True
            self.__display_medicines(__search_term, __func, __posting)
                
        download_csv = st.button('Download as csv')
        if download_csv: 
            self.__handler.to_csv(self.__searcher.nombre,self.__searcher.response_dict)


        #MENU 2

        """ def __display2(self):
            print('\nPlease, select what you would like to do:\n')
            __choice2 = input( "  1. Generate a database or append to an existing one\n"
                            "  2. Get the list of medicines as a csv file\n"
                            "  3. Select one medicine from the list\n"
                            "  4. Back to select your medicine\n"
                            "  5. Exit\n")
            __nchoices = 5
            __output = self.__check_input(__choice2, __nchoices)
            self.__process_choice2(__output) """

        """ def __process_choice2(self, selection):
            if selection == '1':
                regs = self.__db.get_register_nums(self.__searcher.response_dict)
                meds = self.__db.post_registers(regs)
                self.__db.generate_database(meds)
                print("\nWould you like to do anything else?")
                self.__display2()"""  

        """ elif selection == '5':
            print('OK, bye!')
            exit()

        self.__display3() """

    """
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
    """
    
    """
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
            raise ValueError("Query must be at least 3 characters long")

    """ def __check_input(self, choice, nchoices):
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
                    choice = input(f"Please, select a number from 1 to {nchoices}\n")  """
            