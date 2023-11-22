DRUG FINDER

Drug Finder es una aplicación que permite hacer búsquedas en la base de datos del Centro de Información de Medicamentos de la AEMPS (Agencia Española del Medicamento y Productos Sanitarios) y obtener información química de los principios activos de estos medicamentos procedente de la base de datos PubChem, dependiente del Instituto Nacional de Salud de Estados Unidos (NIH en inglés).

La aplicación permite:
    1. Hacer búsquedas en la base de datos del CIMA por nombre de medicamento, principio activo o indicación terapéutica.
    2. Obtener una lista con los medicamentos resultantes de la búsqueda en un archivo de texto con formato csv.
    3. Consultar en pantalla información detallada de cada medicamento aparecido en la búsqueda.
    4. Consultar el prospecto en línea de cada medicamento mediante la apertura automática del navegador por defecto del sistema.
    5. Descargar el prospecto en formato pdf.
    6. Obtener una lista de los principios activos presentes en el medicamento.
    7. Obterner información sobre la estructura química de cada principio activo.
    8. Descargar una imagen de la estructura química de cada principio activo.

Aplicación desarrollada como actividad final de la asignatura Programación Avanzada perteneciente al Curso de Experto en Programación en Python de la Universidad Internacional de Valencia por Jose Rodríguez Couceiro (15/02/2023)

DRUG FINDER 2.0

Extensión para la asignatura Bases de Datos (13/02/2023)

Se ha añadido un pquete ("db") que permite guardar una base de datos relacional a partir de la lista de medicamentos resultantes de la búsqueda contra la API del AEMPs. Se incluyen el modelo entidad-relación y modelo relacional de la base de datos en la carpeta "config/models".

La aplicación tolera aportar entradas nuevas a una base de datos ya existente. En la carpeta "outputs" se puede encontrar una base de datos ('meds_alergia.db') construida de esta forma, que es el resultado de combinar varias búsquedas de medicamentos para la alergia, palabras clave relacionadas con la alergia y principios activos utilizados típicamente para combatirla.

El entorno virtual de la aplicación ha sido creado con pipenv. Para poner en marcha la aplicación hay que lanzar el entorno virtual en la carpeta "Actividad_Final" con el comando 'pipenv shell' e instalarla: 'pipenv install -e .'. Para iniciar, escribir 'drug_finder'.

