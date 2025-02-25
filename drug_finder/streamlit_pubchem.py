from importlib import resources
import streamlit as st
import json

import pubchempy as pcp

class Pubchem:

    '''
    Esta clase usa métodos de la librería 'pubchempy' para obtener información de los compuestos activos presentes en un medicamento. La librería pubchempy extrae los datos de la base de datos Pubchem dependiente del National Institute of Health de Estados Unidos a través de su API. 
    La clase ontiene dos funciones:

            - get_compound_props(): se vale del método 'get_compounds' de 'pubchempy' para obtener la informacion de los compuestos presentes en Pubchem que coinciden con el nonmbre del principio activo escogido por el usuario. El método 'get_compounds' devuelve una lista de objetos de tipo 'compound', que tienen un método 'to_dict' para convertir la información de propiedades seleccionadas en un diccionario. La función 'get_compound_props' devuelve la lista de objetos 'compound' y, para cada uno de ellos, imprime por pantalla la información seleccionada. El nombre del principio activo de entrada debe haber sido previamente traducido al inglés por el método 'Translator.translate_to_en'.

            - get_png(): recibe como entradas el nombre de un principio activo y la lista de objetos 'compound' obtenida por 'get_compound_props' a partir de él. Para cada 'compound', descarga mediante el método 'download' de pubchempy un archivo PNG con una representación de su estructura en la carpeta 'outputs'. El nombre de cada archivo PNG es la concatenación del nombre del principio activo y el 'cid' (un identificador único de Pubchem) del compuesto. Para obtener la imagen el método 'download' pide un identificador único del compuesto que en este caso es la 'inchikey'. Por última, imprime un aviso de que las estructuras han sido descargadas.

            - get_compound_dic(): recibe como entrada el nombre de un principio activo en inglés y obtiene el diccionario con todas sus propiedades (en la carpeta temp hay un guardado un ejemplo de este diccionario con el nombre: "ap_props_example.json"). Este diccionario se almacena como variable de clase. Para obtener este diccionario utiliza las funciones de Pubchempy "get_compounds" y "to_dict()". "get_compounds()" devuelve una lista de compuestos o una lista vacía en caso de que la búsqueda no sea fructífera. Dado que solo nos interesa el primer compuesto de esta lista, se obtiene el diccionario del índice [0], para evitar el Keyerror en caso de una búsqueda no fructífera, se incluye una sentencia if. Además, en caso de búsqueda infructuosa, la función devuelve False.
    '''

    def get_compound_props(self, compound_name):
        __compounds = pcp.get_compounds(compound_name, 'name')

        if len(__compounds) == 1:
            __verb = 'is'
        else:
            __verb = 'are'
        st.write(f'\nThere {__verb} {len(__compounds)} compounds matching this name:')

        #cid_list = list()
        for __comp in __compounds:
            st.write(f"  {__comp}")
            self.get_png(__comp.cid)
            #cid_list.append(__comp.cid)
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
            
            
            