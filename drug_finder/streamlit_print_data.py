import streamlit as st

class PrintMedInfo():

    def __init__(self):
        self.interest_data_strings = {'Name': 'nombre',
                'Register' : 'nregistro',
                'Laboratory': 'labtitular',
                'Use': 'cpresc',
                'Generic': 'generico',
                'Prescription': 'receta',
                'Dosage' : 'dosis'
                }
        self.interest_data_dics = {
                'Pharmaceutical form' : 'formaFarmaceutica'
                }
        self.interest_data_lists = {
            'Active compounds': 'principiosActivos'
            }

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

        