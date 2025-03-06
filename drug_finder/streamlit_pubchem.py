import streamlit as st
import pubchempy as pcp

class Pubchem:

    def print_compound_props(self, compound_name):
        __compounds = pcp.get_compounds(compound_name, 'name')

        if len(__compounds) == 1:
            __verb = 'is'
        else:
            __verb = 'are'
        st.write(f'\nThere {__verb} {len(__compounds)} compounds matching this name:')

        for __comp in __compounds:
            st.write(f"  **:red[{__comp}]**")
            self.get_png(__comp.cid)
            self.__prop_dict = __comp.to_dict(properties=['cid', 'charge', 'iupac_name', 'molecular_formula', 'molecular_weight'])
            __prop_list = ['CID', 'Charge', 'IUPAC name', 'Molecular formula', 'Molecular weight']
            for __tup in zip(__prop_list,list(self.__prop_dict.values())):
                st.write(f"   **{__tup[0]}**: {__tup[1]}")

    def get_png(self, cid):
        png_url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG'
        st.image(png_url)
        
    def get_compound_dic(self, compound_name): 
        __compound = pcp.get_compounds(compound_name, 'name')
        if __compound != []:
            self.comp_dic = __compound[0].to_dict()
            return self.comp_dic
        else:
            return False
            
            
            