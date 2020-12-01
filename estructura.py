
 
        "******************** MODULO BASICO ******************" 


        'Se encuentran en el los datos básico a partir de los cuáles el resto de script \
        procesa la información '

Input_zona = {coordenadas UTM: , coordenadas WGS84: , poligono:.shp,
              subpoligonos:, lineas:.shp, puntos:.shp imagen:.tiff ,
               }

- 

    - Utilizada para descargar las imagenes SENTINEL, LANDAT
    - Utilizada para la función de cálculo meteo (para importar input_meteo
                                                   de la zona)

Input_variables_suelo_fijas = ('N','P','K','M.O', 'aniones', 'cationes', 'textura', 'estructura' )
'de las muestras de suelo tomadas'

Input_geologia = mapa{caracteristicas:{variable:valor}}
'obtenido de los mapas geologicos (IGN) pertenecientes a input_zona'

Input_variable_cultivos = {}

mapa_potencial_climatico = 


            "******************** MODULO CLIMA ******************"
            
            
            'Calcula el potencial_climatico de una especie para una zona dada, \
            potencial climático actual, en 2040, 2070 y 2099 \
            información de utilidad para tomar decisiones sobre la evolución \
            del cultivar a largo plazo, con la oportunidad de transformarlo \
            en caso de que no sean los cultivos óptimos en las próximas décadas. \
            \
            \
            Utiliza la información del módulo básico (zona) y del módulo cultivos, \
            además de la información climática de los input_clima (REDIAM)\
            \
            \
            El resultado son 4 mapas de potencialidad por especie y zona, a nivel visual, \
            la información numérica de las variables, más el mapa, se guardan en DB \
            se utilizan para el estudio preliminar de evaluación de la viabilidad \
            del cultivo actual fente al cambio climático. \
            Y que opciones de transformación pueden ser las más favorables.'
            
            
'Podría hacerse con los datos de REDIAM, teniendo así Andalucía como marco de estudio, \
acotando en este caso a nivel regional el estudio ofrecido por el módulo clima. \
El resto de módulos puede aplicarse a cualquier zona, al menos de España y Europa'

Input_clima_2000 = 

Input_clima_2020 =

Input_clima_2040 =

Input_clima_2070 = 

Input_clima_2099 = 



potencial_climatico = 'mapa del potencial_climatico de x especie en la zona de estudio/cultivo'


            "******************** MODULO METEO ******************"
            
            'o descarga información meteorológica de AEMET u otra, o conecta de alguna forma \
            para visualizar la info de la zona sin tener que incluir nada propio en la aplicación'



    input_zona
    
    Input_meteo = 
        > actualización climática (e.g. aemet)
        exportar datos diariamente y agregar a variables
    
    
            "******************** MODULO USUARIO ******************"

Input_usuario = 
#acceso a cuenta, conexion con base de datos espacial

Input_infousu = recopilación de info previa del usuario y su cultivo, 


        "******************** MODULO IMAGEN_SATELITE ******************"
        
        "Automatiza la descarga de imagenes de la constelación SENTINEL (y LANDAT) \
        introduciendo la zona en las web de descargas, como LandViewer obteniendo la capa \
        guardandola en la variable imagen_dia (junto con imagen_fecha), \
        después pasarla por las funciones_basicas (clase con diferentes métodos), \
        almacenar los resultados en imagen_resultados, actualizar el PANEL_DE_CONTROL, \
        despues de actualizarlo, guardar imagen_dia + imagen_fecha + imagen_resultados en la DB, \
        \
        \
        se ejecuta diariamente un script sencillo de comprobación, que ve si se ha subido \
        una nueva imagen de la zona, en caso de que sí, s ejecutan los demás script:\
        descarga y almacenamiento, aplicacion de funciones, transferencia de datos, informe (...,\
        \
        \
        En la aplicación, el resultado de la ejecución del módulo imagen es una serie de mapas \
        para las diferentes funciones_basicas calculadas + un informe + alertas + informe tras  \
        revisión, donde de inclurían cosas en caso necesario o se contactaría con el usuario    \
        en caso de gravedad o urgencia \
        \
        \
        \
        Utilizar los paquetes y modulos para gestión de imagenes sentinel, \
        sobre todo en las funciones y el procesamiento de las imágenes \
        SENTINEL HUB (necesita usuario) - GitHub modulos: SINERGISE, \.
        "
        
        """ **RASTERIO LIBRARY: permite leer, inspeccionar, visualizar y escribir
        datos geoespaciales raster (GeoTIFF y otros). Puede trabajar con SATImage,
        MDT, DRONEimage. Importar bandas a entorno interactivo python
        
            In order to work with Python in Windows users we recommend to work with Anaconda that you can download free from: https://www.anaconda.com/download/

            Rasterio and other geospatial libraries can be a little bit tricky to install, this is a tutorial to install these libraries without problems: https://youtu.be/4ybddFC80fU

            More information about Rasterio: https://github.com/mapbox/rasterio
            
            TUTORIAL : https://www.hatarilabs.com/ih-en/sentinel2-images-explotarion-and-processing-with-python-and-rasterio
        
        Sentinel Hub Python Package >> acceder al servicio de mamas MWS o WCS.
        Ayuda a seleccionar bandas de trabajo, la combinación RGB y los momentos temporales
        necesarios en el timelapse
        
        Sentinel Hub Cloud Detector >> permite trabajar con las librerias de  Python 
        para identificar coberturas de nubes y filtrar fotogramas innecesarios 
        en el timelapse
        
        Sentinel Hub Timelapse >> crear timelapse en .GIF
        
        Sentinel PlayGround > acceder a los visores Sentinel para localizar y
        combinar bandas de imágenes satélite
        
        **EO Browser descargar imágenes (Sentinel, Landsat, Modis, Envisat
        **LandViewer
        **https://scihub.copernicus.eu/dhus/#/home
        
        
        **https://geoinnova.org/blog-territorio/sig-creacion-de-timelapses-de-sentinel-con-python/
        **http://www.gisandbeers.com/personalizar-servicios-wms-de-imagenes-satelite-sentinel/ """
    
    
        


imagen_dia = {archivo de imagen}

"a la imagen satelital descargada se le aplica un método para recortarla y dejar solo la zona de estudio"

imagen_recorte = imagen_dia.recorte(input_zona.shp)

imagen_reproject = imagen_recorte.proyect(SRC)
'la imagen recortada se reproyecta'

input_zona = 

 

Imagen_fecha = {fecha, nubes, radiacion, datos_tecnicos}



def class imagen_resultados

imagen_resultados = {tras la apliación de funciones_basicas, se exportan a PANEL_DE_CONTROL,
                     INFORME Y A BASE DE DATOS}

imagen_alertas = {}

    metodos:
        - .exportar (aplicado a PC, BD, INF)

def class informe ():
    
    'Resultados finales de imagen_resultados que puede descargar el usuario en PFD, \
    además de ver el panel de control. Este informe es básico y preliminar, \
    Tras la interpretración de los resultados por mí, entendiendome como experto \
    en la interpretación de imágenes satélite y sus resultados asociados'

modelo_informe =

    'plantilla en la que se incluyen los imagen_resultados, iamgen_alertas'

    Imagen_informe = 



def class funciones_basicas():
    
    - NDVI 
    - humedad
    - temperatura
    - plagas
    - etc
    - alertas (a partir de las demás funciones calcula de hay alertas de diferentes tipos)
    
    
    
    
    
    
    
        "******************** MODULO PANEL__DE_CONTROL ******************"
        
        'Interface visual en la que se ve la información del informe, consulta y se interactúa. \
        se puede acceder desde éste a toda la información almacenada de la zona\s del usuario '


        
        'Programación de interfaz gráfico sencillo (inicio, carpetas, meteo, gráficos, mapas, \
         etc, e.g. cuaderno, \ lo importante es el backend, \
        el frontend ya se podrá mejorar en un futuro.'
        
        



        "******************** MODULO ESPECIES ******************"

    'Toda la información de las especies guardada en una base de datos en la cuál se hacen \
     consultas SQL-PostGIS para exportarla a las funciones de otros módulos \
     asignar a las variables la importación de la fila que corresponda de cada tabla de la DB \
      
      '


Clases:

- Árboles

    
    Subclase
    
    - grupo (citrico, fruto_seco, olivo, vid, fruto_carnoso)
    
            Infraclase:
            
                - especie
                
                
    Variables:
    
        - Input_suelo = (suelo_idoneas,  suelo_tolerables, suelo_intolerable)
        - Input_clima = clima_idoneas,  clima_tolerables, clima_intolerable)
            'diferentes temperaturas (max,min,med, etc), balance hídrico, etc'
        - Input_produccion = (rendimiento_optimo, rendimiento_medio, rendimiento min)
    
    Relación con las variables: 
    
        
        input_variables_suelo_fijas + input_geologia
        
            - estado_inicial_suelo (resultado de calculo de funciones)
            
        input_clima
        
            - 
        
        input_meteo + input_zona
        
            -estado_dinamico (resultado de calculo de funciones diariamente)
            
        
        


- Arbustos

     Subclases
    
            - especie

- Herbáceas







"******************** MODULO SENSORES ******************"

'Esto ya es pasarse, pero en un futuro... sería el empleo de sensores en campo, \
estaciones de medición que medin dinámicamente y esta info se almacena, se procesa \
se representa en gráficos o tablas, visibles desde el panel de control, \
y se activan alarmas en caso de problemas, e.g. humedad baja > necesidad de riego.'


Input_sensores = (humedad, temperatura)

