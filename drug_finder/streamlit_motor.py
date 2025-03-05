import streamlit as st
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
        #self.__db = DataBase()
        if 'med_buttons' not in st.session_state:
            st.session_state.med_buttons = {}
            st.session_state.med_buttons_deployed = True
        if 'comp_buttons' not in st.session_state:
            st.session_state.comp_buttons = {}
            st.session_state.comp_buttons_deployed = True

    def welcome(self):
        st.title('\nWELCOME TO DRUG FINDER')
        query = self.__display1()
        if query:
            self.__process_choice(query)

    def __display1(self):
        st.write("\nYou may search for a medicine or an active compound:\n")
        medicine = st.text_input('Search a medicine')
        compound = st.text_input('Search an active compound')
        indication = st.text_input('Search by therapeutic indication')
        return medicine, compound, indication

    def __process_choice(self, selection):
        medicine = selection[0]
        compound = selection[1] 
        indication = selection[2]
        if medicine:
            st.write(f'**:blue[MEDICINE: ] {medicine}**')
            __search_term = self.__searcher.find_medicines(medicine)
            __func = self.__searcher.find_medicines
            __posting = False
            self.__display_medicines(__search_term, __posting)
        if compound:
            st.write(f'**:blue[COMPOUND: ] {compound}**')
            __search_term = self.__searcher.find_principles(compound)
            __func = self.__searcher.find_principles
            __posting = False
            self.__display_medicines(__search_term, __posting)
        if indication:
            st.write(f'**:blue[INDICATION: ] {indication}**')
            __search_term = self.__searcher.find_therapeutic_indication(indication)
            __func = self.__searcher.find_therapeutic_indication
            __posting = True
            self.__display_medicines(__search_term, __posting)
        download_csv = st.button('Download as csv')
        if download_csv: 
            self.__handler.to_csv(self.__searcher.nombre,self.__searcher.response_dict)

    def __create_med_button(self, button_key, label):
        if button_key not in st.session_state.med_buttons:
            st.session_state.med_buttons[button_key] = False  # Initialize button state
        # Create the button
        try:
            if st.button(label, key=button_key):
                st.session_state.med_buttons[button_key] = True  # Update button state on click
        except:
            pass

    def __create_comp_button(self, button_key, label):
        if button_key not in st.session_state.comp_buttons:
            st.session_state.comp_buttons[button_key] = False  # Initialize button state
        # Create the button
        try:
            if st.button(label, key=button_key):
                st.session_state.comp_buttons[button_key] = True  # Update button state on click
        except:
            pass

    def __display_medicines(self, query, post):
        self.__check_length(query)
        self.__searcher.search_motor(post)    
        #self.__handler.save_json(self.__searcher.data_json,self.__searcher.response_dict)
        return self.__print_med_list(self.__searcher.response_dict, query)

    def __print_med_list(self, response, query):
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
                    __key = str(__med['nregistro'])
                    if st.session_state.get('med_buttons_deployed', False):
                        self.__create_med_button(button_key=__key, label=f'{__number_medicines} ' + __med['nombre'])
                        if st.session_state.med_buttons.get(__med['nregistro'], False):
                            self.__searcher.find_medicines(__med['nombre'])
                            self.__searcher.search_motor(False) 
                            self.__display_compounds_info(__med['nregistro'])
                    st.session_state.med_buttons_deployed = True      
            return __number_medicines
        
    def __display_compounds_info(self, nregistro):
        self.__searcher.find_medicine(nregistro)
        response_sing = self.__searcher.search_motor_sing()
        self.__print_comp_info(response_sing, nregistro)
             
    def __print_comp_info(self, response_sing, nregistro):   
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
                if st.session_state.get('med_buttons_deployed', False):
                    __button_key = str(nregistro) + __activep['nombre']
                    self.__create_comp_button(button_key=__button_key, label=f"{__activep['nombre'].capitalize()}")
                    if st.session_state.comp_buttons.get(__button_key, False):
                        st.write(__activep['nombre'])
                        self.__print_compound_data(__activep['nombre'])
                st.session_state.comp_buttons_deployed = False                    
  
    def __print_compound_data(self, activep):
        __en_comp_name = self.__translator.translate_to_en(activep)
        self.__pubchem.print_compound_props(__en_comp_name.text)

    #Control Function

    def __check_length(self, search_term):
        try:
            if len(search_term) < 3:
                raise st.error("Query must be at least 3 characters long")
        except:
            pass
            