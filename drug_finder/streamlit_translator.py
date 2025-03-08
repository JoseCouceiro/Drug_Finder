import deepl
import streamlit as st


class Translate:
    """
    Esta clase se encarga de traducir el nombre de los principios activos del español (tal como se encuentran en la base de datos del CIMA) al inglés (el idioma de Pubchem) para poder introducirlos en las funciones de la clase 'Pubchem'. Para ello se vale de la librería 'deepl', que facilita el manejo de la API de la web de la IA DeepL. Aclaración : las traducciones de los nombres de los principios activos obtenidas por DeepL han funcionado bien en los 10 ó 12 de casos que he probado, pero espero que funcionen siempre sin errores debido a que se trata de lenguaje muy técnico.
    Hay dos variables de inicio de la clase que son una instancia de la clase 'Translator' de 'deepl' y una variable que almacena la llave de autentificación de DeepL (guardada en el archivo config.json en la carpeta resources/config) necesaria para instanciar la clase 'Translator'
    
    La clase contiene un único método 'translate_to_en', que recibe el nombre del principio activo en español, lo traduce al inglés usando el método 'translate_text' de 'deepl' y devuelve el nombre en inglés
    """

    def __init__(self):
        
        self.__auth_key = st.secrets["deepl"]
        self.__translator = deepl.Translator(self.__auth_key)

    def translate_to_en(self, principle):
        __compound_en = self.__translator.translate_text(principle, target_lang = "EN-US")

        return __compound_en