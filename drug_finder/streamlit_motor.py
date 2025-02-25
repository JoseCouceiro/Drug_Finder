import streamlit as st
import random
from drug_finder.streamlit_cima import Search
from drug_finder.handle_data import HandleData
from drug_finder.streamlit_print_data import PrintMedInfo
from drug_finder.translator import Translate
from drug_finder.streamlit_pubchem import Pubchem
from drug_finder.db.database_handle import DataBase


class Motor:

    def __init__(self):
        self.__searcher = Search()
        self.__handler = HandleData()
        self.__printer = PrintMedInfo()
        self.__translator = Translate()
        self.__pubchem = Pubchem()
        self.__db = DataBase()
        if 'dynamic_buttons' not in st.session_state:
            st.session_state.dynamic_buttons = {}
            st.session_state.dynamic_buttons_deployed = True
        self.__nsearches = 0

    #FUNCIONES DE NAVEGACIÓN
    #MENU 1
    

    def create_dynamic_button(self, button_key, label):
        if button_key not in st.session_state.dynamic_buttons:
            st.session_state.dynamic_buttons[button_key] = False  # Initialize button state

        # Create the button
        if st.button(label, key=button_key):
            st.session_state.dynamic_buttons[button_key] = True  # Update button state on click

    def med_list(self, response):
        if response == {}:
            st.write('\nNo results to show, please repeat your search')
            st.write('Check your spelling and remember that the database is in Spanish\n')
            return False   
        else:
            st.write("\nHere are the results:\n")
            __number_medicines = 0
            __key = 0
            for __pag, __dic in response.items():
                self.button_dic = dict()
                for __med in __dic['resultados']:
                    __number_medicines +=1
                    __key +=1
                    if st.session_state.get('dynamic_buttons_deployed', False):
                        self.create_dynamic_button(__key, f'{__number_medicines} ' + __med['nombre'])
                        if st.session_state.dynamic_buttons.get(__number_medicines, False):
                            self.__searcher.find_medicines(__med['nombre'])
                            self.__searcher.search_motor(False) 
                            self.__select_medicine(1)
                    st.session_state.dynamic_buttons_deployed = True
                    
            return __number_medicines
        
    def __select_medicine(self, choice):
        self.nregistro = self.__handler.find_nregistro(choice,self.__searcher.response_dict)

        self.__searcher.find_medicine(self.nregistro)
        self.__searcher.search_motor_sing()
         
        self.__handler.save_json_sing(self.__searcher.data_json_sing,self.__searcher.response_sing.json())
        self.basic_info(self.__searcher.response_sing.json(), self.nregistro)
        

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
        med_list = self.med_list(self.__searcher.response_dict)
        return med_list
    
    def __process_choice1(self, selection):
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
        
    def basic_info(self, response_sing, nregistro):
        for __key, __value in self.__printer.interest_data_strings.items():
            if response_sing[__value] == True:
                response_sing[__value] = 'Sí'
            if response_sing[__value] == False:
                response_sing[__value] = 'No'        
            st.write(f"  **{__key}**: {response_sing[__value]}")
        
        for __key, __value in self.__printer.interest_data_dics.items():       
            st.write(f"  **{__key}**: {response_sing[__value]['nombre'].capitalize()}")
        
        for __key, __value in self.__printer.interest_data_lists.items():        
            st.write(f'  **{__key}:**')
            for __activep in response_sing[__value]:
                if st.button(f"{__activep['nombre'].capitalize()}", key=str(nregistro) + __activep['nombre']):
                    st.write(__activep['nombre'])
                    self.__retrieve_compound_data(1)
  
    def __retrieve_compound_data(self, comp_num):
        __comp_name = self.__handler.get_principle_name(comp_num,self.__searcher.response_sing.json())
        __en_comp_name = self.__translator.translate_to_en(__comp_name)
        self.__pubchem.get_compound_props(__en_comp_name.text)

    #Funciones que controlan los inputs

    def __check_length(self, search_term, func):
        while len(search_term) < 3:
            raise ValueError("Query must be at least 3 characters long")
            