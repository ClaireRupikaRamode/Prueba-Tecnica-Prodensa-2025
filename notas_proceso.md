1. Para iniciar el proyecto, usualmente lo primero es crear un entorno virtual para el proyecto, para así mantener un control de las dependencias.
Ejecutando en la terminal:

///python -m venv venv
source venv/bin/activate #Ya que me encuentro en Linux
pip install --upgrade pip
pip install requests pdfplumber pandas numpy thefuzz flask flask-cors tqdm

Para instalar las dependencias de forma automatizada basta con ejecutar:
///pip install -r requirements.txt

2. Luego crear la estructura del proyecto:

#Nota: Primero pensaba utilizar esta estructura básica:

Prueba_Tecnica/
| data/                # archivos de origen
├──  scripts/
|    ├── descargar.py
|    ├── pdf_a_csv.py
|    ├── immex_cruce.py
|    ├── utils.py
|    ├── app.py             # web view
|
├──  outputs/
|    ├── padrón.csv
|    ├── immex_rfc.csv

#Nota: Sin embargo, al momento de estar realizando la parte B, he decidido organizarme mejor y distribuirlo de una forma más profesional:

Prueba_Tecnica/
│
├── README.md                    # Instrucciones de ejecución
├── requirements.txt             # Dependencias necesarias
├── notas_proceso.md            # Mi proceso durante la prueba
│
├── src/                        # Código fuente dividido por secciones
│   ├── __init__.py
│   ├── downloaders/           # Descargas de archivos
│   │   ├── __init__.py
│   │   ├── sat_downloader.py
│   │   └── immex_downloader.py
│   │
│   ├── processors/            # Procesamiento y conversiones
│   │   ├── __init__.py
│   │   ├── pdf_processor.py
│   │   └── data_cleaner.py
│   │
│   ├── matchers/              # Cruce de datos
│   │   ├── __init__.py
│   │   └── company_matcher.py
│   │
│   └── webapp/                # Vista web
│       ├── __init__.py
│       ├── app.py
│       └── templates/
│           └── index.html
|
├── scripts/                           #Ejecución directa de cada parte solicitada
│   ├── parte_a.py                     # Script Parte A
│   ├── parte_b.py                     # Script Parte B
│   └── parte_c.py                     # Script Parte C
│
├── data/                      # Datos crudos
│   ├── raw/                   # Archivos descargados sin cambios
│   └── inter/                 # Resultados intermedios/incompletos
│
└──  outputs/                   # Resultados finales

Considero que la organización es una parte bastante importante en los proyectos y la considero indispensable antes, durante y después de la realización de un proyecto.

3. Comenzando con la Parte A de la prueba.
Decidí automatizar el proceso de descarga del archivo desde el portal del SAT con el script 'sat_downloader.py' utilizando la librería 'requests', bastando con ejecutarlo para recibir el PDF directamente en la carpeta 'data/raw', sin embargo, este código es solo una función que debe ser llamada por otro código, en este caso 'parte_a.py'

4. Lo siguiente es extraer todo el texto de las tablas que vienen en el PDF, así que haciendo uso de la libería pdfplumber se puede extraer todo el texto de cada página.

#Nota: Intenté realizarlo primero con la biblioteca 'camelot-py', sin embargo, esta no procesó correctamente los datos, generando al final un CSV con información mezclada.

Intenté muchas veces realizar la extracción de datos, sin embargo, siempre
se quedaba trabada la extracción hasta el 'ID 999', esto debido a que estaba utilizando como patrón de extracción lo siguiente:

///pattern = re.compile(r'^(\d+)\s+([A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3})\s+(.+)$')

Lo que causaba que al pasar de la cifra 999 se dejara de extraer datos, ya que el PDF separaba los ID al pasar de 1000 con una ',' haciendo que el script descartara todo lo que no fuera solamente un número, al final bastó hacer una pequeña modificación al patrón de extracción de la siguiente manera:

///pattern = re.compile(r'^([\d,]+)\s+([A-Z&Ñ0-9]{12,13})\s+(.+)$')

Con unas cuantas modificaciones no solo empezó a detectarse correctamente los ID en su totalidad para su extracción, si no que al cambiar la forma en la que se identifica el RFC y el nombre permite que no se lleguen a mezclar datos al recibir datos más complejos que no entren en las reglas que había colocado anteriormente.

#Nota: Se pueden observar los intentos fallidos en la carpeta 'data/outputs' con el nombre '_prueba_#.csv'

Lo siguiente en esta función es filtrar los datos acorde a lo que no debe interpretarse como datos relevantes:

///if not line or 'Página' in line or 'Padrón' in line or 'Registros Activos' in line

Después se extrae el ID (ya incluyendo las comas), el RFC y el nombre
Para posteriormente limpiar los ID acabando con números limpios.

///id_num_with_comma, rfc, nombre = match.groups()
    id_num = id_num_with_comma.replace(',', '')
    all_rows.append({'ID': id_num, 'RFC': rfc, 'NOMBRE': nombre})

Como precaución para confirmar que todo esté siendo procesado correctamente se muestra qué lineas no se están capturando como datos para el CSV.

///if len(all_rows) > 990 and len(all_rows) < 1010:
    print(f"Pág {page_num}, Línea no capturada: '{line}'")

Finalmente con la biblioteca pandas se crea el DataFrame acorde a los datos que queremos.

///df = pd.DataFrame(all_rows, columns=['ID', 'RFC', 'NOMBRE'])
    df = df.drop_duplicates()
    return df

Se continua con la función que termina de limpiar los datos del DataFrame, tal como eliminar los espacios de sobra y ordenar los datos por su número de ID.

///def clean_padron_data(df):
    """Limpieza adicional del DataFrame."""
    # Elimina espacios extra en los nombres y RFC
    df['NOMBRE'] = df['NOMBRE'].str.strip()
    df['RFC'] = df['RFC'].str.strip()
    # Convierte ID a numérico (si es necesario)
    df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
    # Ordena por ID
    df = df.sort_values('ID').reset_index(drop=True)
    return df


5. Ya que están bien definidas las funciones que van a realizar todo el proceso entonces se crea el código que va a ejercer como "ejecutor principal" 'parte_a.py'

Esto siguiendo una estructura de 3 etapas, para poder llevar un mejor control de lo que está ocurriendo, en qqué orden y facilitar la corrección de errores así como permitir futuras implementaciones o cambios a funciones ya existentes.

Y para cada etapa se agrega tanto un comentario para quien lea el código, como un print() informativo para el usuario que ejecute el mismo, para monitoreo durante ejecución.

6. Al completar la primera parte del proyecto, para asegurar un backup, así como para mantener un control de versiones, se crea un repositorio en Github para el proyecto.

#Nota: link al repositorio (https://github.com/ClaireRupikaRamode/Prueba-Tecnica-Prodensa-2025), este a pesar de ser público al momento de entregar la prueba, será eliminado tras su revisión.

Se crea el primer commit bajo el nombre "Parte A" para preservar todo el avance realizado hasta el momento.

Tras un par de correcciones en la gramática de las notas y una breve revisión del código que conforma toda la parte A, se crea el segundo commit bajo el nombre "Parte A Completada"

7. Continuando con la Parte B de la prueba.
Lo primero, al igual que en la parte A, es automatizar la descarga del archivo con el que vamos a trabajar, para crear 'immex_downloader.py' fue suficiente con replicar el código de 'sat_downloader.py' cambiando unos detalles, tales como cambiar el link de donde se obtendrá la descarga y dejando de nuevo la URL como una variable para permitir cambiar el link fácilmente.

8. Después se crea un código que va a normalizar el texto ('data_cleaner.py') que vamos a extraer del excel con el que vamos a trabajar, de forma que al procesar todo obtengamos datos limpios y no haya mezclas, errores y al momento de hacer el match obtengamos los mejores resultados posibles.

#Nota: Para facilitar la creación de este código decidí basarme en la estructura que obtuve del CSV resultado de ejecutar 'parte_a.py', de forma que la función se encarga de eliminar acentos, puntos y espacios.

9. Lo siguiente es un código que inicie el cruce entre los datos del IMMEX con los del padrón de importadores, creando nuevas columnas donde se encontrarán los nombres procesados y normalizados por 'data_claner.py', siendo estas 'NOMBRE_NORM' y 'RAZON_SOCIAL_NORM'.
Luego se buscan las coincidencias, valorando si son una coincidencia exacta, si es aproximada o si no hay coincidencia alguna.
Al final se añaden los resultados en columnas donde se añade el RFC (de haber alguno que coincida) y donde se muestre el porcentaje de de coincidencia de los datos.

10. Se crea el código que va a ejecutar todas las funciones realizadas para esta parte de la prueba ('parte_b'), comenzando por cargar el CSV resultado de la parte A, luego se llama a la función que ejecuta la descarga del archivo excel a utilizar.
Lo siguiente que realiza el script es colocar las reglas para leer el excel, esto ya que el archivo cuenta con 4 filas al inicio que no son datos que se puedan utilizar.

#Nota: Tuve varios resultados fallidos y errores al ejecutar el código por no tomar en cuenta las primeras 4 filas del inicio, es por eso que al final decidí añadir la parte en la que se salta la lectura de dichas filas. 

Se realiza el cruce de datos y se guarda el resultado en un CSV en la carpeta 'outputs/', finalmente, se muestra un porcentaje de de la tasa de coincidencia total.

11. Al completar la segunnda parte de la prueba, se actualiza el backup y se añade una nueva versión , creando el tercer commit bajo el nombre "Parte B Completada"

12. Finalizando con el proyecto, llegamos a la parte C de la prueba.
Lo primero en este caso es crear 'app.py' que será la base con la que funcione el sitio web, primero localizando los directorios en donde se encontrarán los archivos más importantes para esta prueba (los resultados), e indicando los nombres que tienen estos archivos para que se descarguen exclusivamente esos resultados y evitar algún error si se llega a introducir archivos extra en la misma carpeta.

Después, ya que se solicitaron barras de progreso en la parte web, se indica el estado global de los procesos como "no iniciados" y con un progreso de 0.

Se configura que al ejecutar la parte A del proyecto la barra de progreso avance acorde a los procesos que está realizando el código, avanzando un 10% al concluir la descarga del PDF, un 30% al iniciar el procesamiento del archivo, un 80% al estar guardando el archivo final y se agrega una verificación al final para marcar si el proceso ha terminado por completo generando el archvio, marcando un 100%, si no se pudo generar el archivo señalarlo al usuario, o en su defecto mostrar algún error ocurrido durante el proceso.

Después se realiza el mismo procedimiento al ejecutar la parte B, midiendo su progreso acorde a los procesos que se van realizando, marcando un 20% de avance al concluir la descarga del archivo que vamos a utilizar, luego un 50% al iniciar el cruce de datos, un 80% al llegar a la parte donde se asignan RFC acorde a los nombres obtenidos, y finalmente se vuelve a hacer una verificación al final con la misma estructura utilizada para la ejecución de la parte A.

Lo siguiente es colocar las funciones con las que se definen las rutas con las que va a trabajar todo el backend, tales como las rutas donde se realizarán las descargas, donde se verificará que estén los archivos finales, entre otros.

13. La siguiente parte que conforma la parte C es el archivo 'index.html' que será la estructura completa del frontend de la página web, se utiliza Bootstrap como framework por su rapidez de implementación y el hecho de permitir una variedad de elementos ya pre-diseñados.

#Nota: Esto debido a mi falta de experiencia con HTML.

Se utilizan componentes con los que darle una separación visual a "Parte A" de "Parte B", informar al usuario del estado de los procesos, se incluyen barras de progreso y se implementan botones para poder llevar a cabo la ejecución de los procesos y la descarga de archivos.

Se utiliza una parte de JavaScript para comunicación con el backend, `fetch()` para llamar a los endpoints de Flask sin necesitar recargar la página, `/api/status/` para actualizar el progreso de los procesos, y cada botón tiene 3 estados (inactivo, ejecutando, completado).

14. Finalmente se crea 'parte_c.py' que será el que ejecute toda la parte final de la prueba en conjunto.
esta se encarga básicamente de iniciar la aplicación web e indicarle al usuario qué dirección tiene que visitar en su navegador para poder probar las funciones del proyecto, así como señalar los procesos que se pueden realizar desde el sitio web e informar cómo detener el proceso.

###Notas finales: Problemas encontrados y soluciones

###Problema 1, Parte A: El regex fallaba al detectar un ID mayor a 999
Al ejecutar la parte A de la prueba esta dejaba de extraer datos del PDF base tras pasar del registro con ID 999, tras añadir código que imprimiera en pantalla qué lineas no se estaban capturando para analizar qué tenían en común, al recibir datos como que a partir de '1,000 ABC123456ABC Nombre' dejaba de capturarse todo lo demás, encontré que los ID se leían directamente con la coma que se utiliza para escribir cifras grandes, es decir, en vez de leerse como "1000", se leía directamente como "1,000".  Por lo que la parte del regex '^(\d+)' no era capaz de capturar los ID que no fueran únicamente números, es por eso que se tuvo que cambiar a '^([\d,]+)' para permitir incluir cifras con comas y más adelante se pudieran remover al limpiar datos.

###Problema 2, Parte B: Columnas incorrectas
Al ejecutar la parte B de la prueba esta primero marcaba error, indicando que no había ninguna columna con los datos que estaba señalando para su extracción como 'NOMBRE' o 'RAZON_SOCIAL', una vez más bastó con aañadir código que imprimiera lo que se estaba detectando al momento de procesar el archivo, recibiendo resultados en los que se estaban detectando las primeras lineas del archivo, es decir, 'DIRECTORIO DE PROGRAMAS IMMEX INFORMACIÓN ACTUALIZADA AL 31 DE OCTUBRE DE 2025 SECRETARÍA DE ECONOMÍA CON INFORMACIÓN DE VUCEM', como si fueran columnas, por lo que decidí agregar una línea de código que se saltara hasta la fila 5 del documento para empezar a leer las columnas.

###Problema 3, Parte B: Columnas con acentos en IMMEX
Luego de resolver el problema anterior empecé a recibir un error que indicaba que no se encontraba una columna con el nombre 'RAZON_SOCIAL', que era el nombre que indiqué que se buscara para empezar a generar 'RAZON_SOCIAL_NORM', esto debido a que en el archivo, esta columna se encontraba como 'RAZÓN_SOCIAL' (con acento).  Esto se pudo corregir rápidamente modificando en 'company_matcher.py' que se busque la columna con acento.

###Problema 4, Parte C: Rutas relativas en Flask
Al ejecutar la parte C de la prueba se llevaban a cabo todos los procesos correctamente, sin embargo, al momento de intentar descargar los archivos la página y la terminal marcaba error, indicando que no se encontraron archivos en '/src/webapp/outputs/', esto rápidamente me indicó que había un problema al definir los directorios ya que Flask buscaba desde 'src/webapp/', no desde raíz del proyecto.
Esto se solucionó agregando a 'app.py' un 'BASE_DIR' para construir rutas absolutas.

###Mejoras futuras:
Si tuviera más tiempo para realizar esta prueba, agregaría a todos los procesos una barra de progreso que indique el avance en tiempo real para hacer menos tediosa la espera para la finalización de cada parte en lugar de que se mida el progreso acorde a los procesos completados, en su defecto añadiría que en la terminal se muestre el avance acorde a qué página del documento de la parte A se encuentra en proceso y en qué linea del excel de la parte B se encuentra haciendo match ese proceso.