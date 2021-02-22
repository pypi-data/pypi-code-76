import pandas as pd
import datetime
import urllib
import urllib.request
import json
import requests
import io


class Reportes:
    def __init__(self):
        self.__cargar()
        self.lista_emisoras = self.diccionario.keys()
        self.estado = 'Reportes trimestrales'
        self.__mxn_usd()
        self.__reportan_usd()
        print('Instancia lista')
        print('Unidades:  Millones')
        print(f'ATENCION: Las siguientes emisoras reportan sus resultados en USD:')
        print(self.reportan_usd)

    def __cargar(self):
        # url = 'https://github.com/dabu-io/reportes_trimestrales_json/raw/main/reportes_trimestrales.json'
        url = 'http://bit.ly/dabu_json'

        datos = requests.get(url)
        self.diccionario = json.loads(datos.content)
        # print(self.diccionario)

    def __cargar_datos(self):
        dicc_local = {}

        for fecha in self.fechas:
            for concepto, valor in self.diccionario[self.emisora][self.estado][fecha][self.reporte].items():
                if concepto not in dicc_local:
                    dicc_local[concepto] = {}
                dicc_local[concepto][fecha] = valor
        return pd.DataFrame.from_dict(dicc_local, orient='index')

    def __reportan_usd(self):
        lista_usd = []
        for emisora in self.lista_emisoras:
            if self.diccionario[emisora]['Metadata']['Moneda/Currency'] == 'USD':
                lista_usd.append(emisora)
        lista_usd.sort()
        self.reportan_usd = lista_usd

    def __rango_fechas(self):
        return pd.date_range(self.fechas[0], self.fechas[1], freq='Q').format()

    def __mxn_usd(self):
        url = "https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarSeries"
        payload = {'idCuadro': 'CF102',
                   'sector': '6',
                   'version': '3',
                   'locale': 'es',
                   'anoInicial': '2017',
                   'anoFinal': '',
                   'tipoInformacion': '4,1',
                   'formatoHorizontal': 'false',
                   'metadatosWeb': 'true',
                   'formatoCSV.x': '59',
                   'formatoCSV.y': '16',
                   'series': 'SF43718'}
        files = []
        headers = {
            'Cookie': 'JSESSIONID=0acdd227765f069f940255fcc094; TS018df36d=0189f484afcc09c523bdc6133ded20abcf456b392fc1f269fa533db92baa97d4b3984b145b2458d2f98dc970f914f395fc34f3dac71f5df64d8d09fff4d6d6d658cb92a6f3; TS0175f232=0189f484af8797f17be53d16a40e5e3b5aecb7e94803c50f7a321441fe784d8d6939ec64615be5926c3b519d2b9b9c7791b5fffd3d772b3a1ac8dd4973319c703c33de589b; ser25268080=642664106.36895.0000'
        }

        response = requests.request("POST", url, data=payload, headers=headers, files=files)
        data = response.content.decode('utf8', errors='ignore')
        df = pd.read_csv(io.StringIO(data), skiprows=19, header=None, parse_dates=True, dayfirst=True, index_col=0)
        df.index.rename('Fecha', inplace=True)
        df.rename(columns={1: 'MXN/USD'}, inplace=True)
        self.mxn_usd = df

    def informacion(self, emisora):
        moneda = self.diccionario[emisora]['Metadata']['Moneda/Currency']
        print(f'Moneda con la que reporta {emisora}: {moneda}')

    def balance(self, emisora, fechas, rango=False):
        """
        PARAMETROS:
        -----------
        emisora : str
            Clave de emisora
        fecha : lista
            Lista con fechas (formato AAAA-mm-dd).
            Debe de incluir por lo menos dos fechas diferentes.
            El resultado se regresa en el órden que se ingresaron las fechas.
            Puedes utilizar un rango de fechas (inicio, fin).  Cambiar el parámetro "range" = True.
        range : bool
            Default = False.  Cambiarlo a True si estás usando un rango de fechas.
        Ejemplo utilizando rango de fechas:
            balance_g('amx', ['2019-01-01', '2019-12-31'], rango = True)"""
        self.emisora = emisora.upper()
        self.fechas = fechas
        self.rango = rango
        self.reporte = 'Balance'
        if self.rango is True:
            self.fechas = self.__rango_fechas()
        return self.__cargar_datos()

    def resultados(self, emisora, fechas, rango=False):
        """
        PARAMETROS:
        -----------
        emisora : str
            Clave de emisora
        fecha : lista
            Lista con fechas (formato AAAA-mm-dd).
            Debe de incluir por lo menos dos fechas diferentes.
            El resultado se regresa en el órden que se ingresaron las fechas.
            Puedes utilizar un rango de fechas (inicio, fin).  Cambiar el parámetro "range" = True.
        range : bool
            Default = False.  Cambiarlo a True si estás usando un rango de fechas.
        Ejemplo utilizando rango de fechas:
            resultados('amx', ['2019-01-01', '2019-12-31'], rango = True)
        """
        self.emisora = emisora.upper()
        self.fechas = fechas
        self.rango = rango
        self.reporte = 'Income'
        if self.rango is True:
            self.fechas = self.__rango_fechas()
        return self.__cargar_datos()

    def flujos(self, emisora, fechas, rango=False):
        """
        PARAMETROS:
        -----------
        emisora : str
            Clave de emisora
        fecha : lista
            Lista con fechas (formato AAAA-mm-dd).
            Debe de incluir por lo menos dos fechas diferentes.
            El resultado se regresa en el órden que se ingresaron las fechas.
            Puedes utilizar un rango de fechas (inicio, fin).  Cambiar el parámetro "range" = True.
        range : bool
            Default = False.  Cambiarlo a True si estás usando un rango de fechas.
        Ejemplo utilizando rango de fechas:
            flujos('amx', ['2019-01-01', '2019-12-31'], rango = True)
        """
        self.emisora = emisora.upper()
        self.fechas = fechas
        self.rango = rango
        self.reporte = 'CashFlows'
        if self.rango is True:
            self.fechas = self.__rango_fechas()
        return self.__cargar_datos()

    def comparar(self, estado, fecha, acciones='', usd_a_mxn=False):
        """
        PARAMETEROS:
        -----------
            De una lista de emisoras se compara un estado financieroen de un trimestre específico.
        estado : str
            El estado financiero a seleccionar ('balance_g', 'ingresos', 'flujos').
        fecha : str
            Una fecha en formato 'AAAA-mm-dd'.
        acciones : list
            Una lista con las acciones a analizar
        Ejemplo:
            comparar(estado='income', '2020-03-31', ['amx', 'femsa', 'ac', 'kof'])
        """
        if len(acciones) == 0:
            acciones = list(self.lista_emisoras)
            acciones.sort()
        df_resultados = pd.DataFrame()
        lista_errores = []
        for accion in acciones:
            try:
                # Aquí quiero llamar al métedo seleccionado como si fuera una varibale pero no se
                # como hacerlo:  la idea es algo así df = datos.x(accion, [fecha, '2017-06-30'])
                # donde x es el estado financiero.  Por lo pronto voy a hacer un chorizo de if's
                if estado == 'balance':
                    df = self.balance(accion, [fecha, '2017-03-31'])
                elif estado == 'resultados':
                    df = self.resultados(accion, [fecha, '2017-03-31'])
                elif estado == 'flujos':
                    df = self.flujos(accion, [fecha, '2017-03-31'])
            except:
                lista_errores.append(accion)
                continue
            df_resultados[accion] = df[fecha]

        if usd_a_mxn is True:
            emisoras_usd = self.reportan_usd
            mxn_usd = self.mxn_usd.loc[fecha][0]
            for emisora in emisoras_usd:
                if emisora not in df_resultados.columns:
                    emisoras_usd.remove(emisora)
            df_resultados[emisoras_usd] = df_resultados[emisoras_usd] * mxn_usd
            print(f'Tipo de cambio FIX MXN/USD {fecha}:  {mxn_usd}')
        return df_resultados


class Precios:
    """
        PARAMETROS
        ----------
            emisoras : str, o lista
                La lista puede contener una o más emisoras.  Si la emisora cotiza utilizando una serie, esta debe
                de agregarse al parámetro.  Por ejemplo “CEMEXCPO”.
            fecha_inicial : str
                La fecha debe de ingresarse bajo el formato “AAAA-MM-DD”.  Por ejemplo "2020-12-15"
            fecha_final : str
                La fecha debe de ingresarse bajo el formato “AAAA-MM-DD”.  Por ejemplo "2020-12-15
            frecuencia : str, default '1d'
                La frecuencia puede ser diaria ('1d'), semanal ('1wk'), o mensual ('1mo')
            tipo_precio : str, default ‘Cierre Ajustado’
                En cado de consultar precios de dos o más acciones, solo se entrega el DataFrame
                con un tipo de precio.  Se puede cambiar el precio por “apertura”, “max”, “min”,
                “cierre” y "cierre ajustado"

        ALGUNAS LISTA DE EMISORAS
        --------
        Estas son algunas de las emisoras de la BMV que se pueden consultar
        'AC', 'AEROMEX', 'ALEATIC', 'ALFAA', 'ALPEKA', 'ALSEA', 'AMXL', 'ARA',
        'ASURB', 'AUTLANB', 'AXTELCPO', 'AZTECACPO', 'BIMBOA', 'BOLSAA', 'CEMEXCPO',
        'CHDRAUIB', 'CUERVO', 'ELEKTRA', 'ELEMENT', 'FEMSAUBD', 'GAPB', 'GCARSOA1',
        'GENTERA', 'GFAMSAA', 'GMEXICOB', 'GRUMAB', 'GSANBORB-1', 'HCITY', 'HERDEZ',
        'HOMEX', 'IENOVA', 'KIMBERA', 'KOFUBL', 'KUOB', 'LABB', 'LALAB', 'LIVEPOLC-1',
        'MFRISCOA-1', 'NEMAKA', 'OMAB', 'ORBIA', 'PAPPEL', 'PASAB', 'PE&OLES', 'PINFRA',
        'POCHTECB', 'POSADASA', 'SIMECB', 'SITESB-1','SORIANAB', 'TLEVISACPO','VITROA',
        'VOLARA','WALMEX'
    """

    def __init__(self, emisora, inicio, final, frecuencia='1d', tipo_precio='cierre ajustado'):
        self.emisora = emisora
        self.inicio = inicio
        self.final = final
        self.frecuencia = frecuencia
        self.tipo_precio = tipo_precio
        self.__cierre()

    def __cierre(self):
        self.__tiempo_epoch()
        self.__verificar_orden()
        self.__tipo_entrada()
        self.__ejecutar()

    def __ejecutar(self):
        if self.entrada == list:
            self.__cargar_multiples()
        else:
            self.__cargar_emisora()

    def __tipo_entrada(self):
        if type(self.emisora) == list and len(self.emisora) > 1:
            self.entrada = type(self.emisora)
        elif type(self.emisora) == list:
            self.emisora = self.emisora[0]
            self.entrada = type(self.emisora)
        else:
            self.entrada = type(self.emisora)

    def __construccion_url(self):
        if self.emisora.upper() == 'IPC':
            self.url = f'https://query1.finance.yahoo.com/v7/finance/download/^MXX?period1={self.epoch0}&period2={self.epoch1}&interval={self.frecuencia}&events=history&includeAdjustedClose=true'
        else:
            self.url = f'https://query1.finance.yahoo.com/v7/finance/download/{self.emisora.upper()}.mx?period1={self.epoch0}&period2={self.epoch1}&interval={self.frecuencia}&events=history&includeAdjustedClose=true'

    def __tiempo_epoch(self):
        self.epoch0 = datetime.datetime.strptime(self.inicio, "%Y-%m-%d").date().strftime('%s')
        self.epoch1 = datetime.datetime.strptime(self.final, "%Y-%m-%d").date().strftime('%s')

    def __verificar_orden(self):
        if self.epoch0 > self.epoch1:
            raise Exception(f'Fecha final es menor a la fecha inicial.')

    def __crear_dataframe(self):
        rango_fechas = pd.date_range(self.inicio, self.final)
        return pd.DataFrame(index=rango_fechas)

    def __cargar_emisora(self):
        self.__construccion_url()
        df = pd.read_csv(self.url, index_col=0, parse_dates=True)
        df.rename(
            {'Open': 'Apertura', 'High': 'Máximo', 'Low': 'Mínimo', 'Close': 'Cierre', 'Adj Close': 'Cierre Ajustado'},
            axis=1, inplace=True)
        orden_columnas = ['Apertura', 'Máximo', 'Mínimo', 'Cierre', 'Cierre Ajustado']
        df = df.reindex(columns=orden_columnas)
        df.index.names = ['Fecha']
        df.sort_index(inplace=True)
        df.dropna(inplace=True)
        self.resultado = df

    def __cargar_multiples(self):
        df_precios = self.__crear_dataframe()
        self.lista = self.emisora.copy()
        for accion in self.lista:
            self.emisora = accion
            df = self.__cargar_emisora()
            df_precios = df_precios.join(self.resultado[self.tipo_precio.title()])
            df_precios.rename({self.tipo_precio.title(): accion.upper()}, axis=1, inplace=True)

        df_precios.dropna(how='all', inplace=True)
        df_precios.index.names = ['Fecha']

        self.resultado = df_precios


class Intradia:
    """
     Parámetros
    ----------
        emisoras : str, o lista
            Ticker de la emisora.  La lista puede contener una o más emisoras.  Si la emisora cotiza
            utilizando una serie, esta debe de agregarse al parámetro.  Ejemplo “CEMEXCPO”.
        inicio : str
            La fecha debe de ingresarse bajo el formato “AAAA-MM-DD”.  Ejemplo "2020-12-12"
        final : str
            La fecha debe de ingresarse bajo el formato “AAAA-MM-DD”.  Ejemplo "2020-12-15
        Intervalo : str, default '1m' (1minuto)
            Se puede cambiar el intervalo de tiempo a '2m', '5m', '15m', '30m', '60m', '90m'

    IMPORTANTE
    ----------
    YAHOO FINANCE guarda datos hasta de 29 días de la fecha actual en intervalos de 1m

    Emisoras
    --------
    lista_emisoras =['AC', 'AEROMEX', 'ALEATIC', 'ALFAA', 'ALPEKA', 'ALSEA', 'AMXL', 'ARA',
                  'ASURB', 'AUTLANB', 'AXTELCPO', 'AZTECACPO', 'BIMBOA', 'BOLSAA', 'CEMEXCPO',
                  'CHDRAUIB', 'CUERVO', 'ELEKTRA', 'ELEMENT', 'FEMSAUBD', 'GAPB', 'GCARSOA1',
                  'GENTERA', 'GFAMSAA', 'GMEXICOB', 'GRUMAB', 'GSANBORB-1', 'HCITY', 'HERDEZ',
                  'HOMEX', 'IENOVA', 'KIMBERA', 'KOFUBL', 'KUOB', 'LABB', 'LALAB', 'LIVEPOLC-1',
                  'MFRISCOA-1', 'NEMAKA', 'OMAB', 'ORBIA', 'PAPPEL', 'PASAB', 'PE&OLES', 'PINFRA',
                  'POCHTECB', 'POSADASA', 'SIMECB', 'SITESB-1','SORIANAB', 'TLEVISACPO','VITROA',
                  'VOLARA','WALMEX']
   """

    def __init__(self, emisora, inicio, final, intervalo='1m'):
        self.emisora = emisora
        self.inicio = inicio
        self.final = final
        self.intervalo = intervalo
        self.__intradia()

    def __intradia(self):
        self.__tiempo_epoch()
        self.__verificar_argumentos()
        self.__construccion_url()
        self.__cargar_intradia()

    def __tiempo_epoch(self):
        self.epoch0 = datetime.datetime.strptime(self.inicio, "%Y-%m-%d").date().strftime('%s')
        self.epoch1 = datetime.datetime.strptime(self.final, "%Y-%m-%d").date().strftime('%s')
        self.rango_fechas = pd.to_datetime(self.final).date() - pd.to_datetime(self.inicio).date()

    def __verificar_argumentos(self):
        if self.epoch1 < self.epoch0:
            raise Exception('Fecha final es menor a la fecha inicial.')
        elif self.rango_fechas > pd.Timedelta(7, 'days') and self.intervalo == '1m':
            raise Exception('Rango de periodo no debe de ser mayor a 7 dias para intervalo de 1m.')
        elif self.rango_fechas > pd.Timedelta(60, 'days'):
            raise Exception('Rango de periodo no debe de ser mayor a 60 dias.')
        elif self.intervalo not in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo',
                                    '3mo']:
            raise Exception(f'Intervalo invalido.  Intervalo seleccionado {self.intervalo}')

    def __construccion_url(self):
        if self.emisora.upper() == 'IPC':
            self.url = f'https://query1.finance.yahoo.com/v8/finance/chart/^MXX?period1={self.epoch0}&period2={self.epoch1}&interval={self.intervalo}'
        else:
            self.url = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.emisora.upper()}.mx?period1={self.epoch0}&period2={self.epoch1}&interval={self.intervalo}'

    def __cargar_intradia(self):
        datos_crudos = urllib.request.urlopen(self.url).read()
        datos_json = json.loads(datos_crudos)
        datos = datos_json['chart']['result'][0]
        timestamp = datos['timestamp']
        apertura = datos['indicators']['quote'][0]['open']
        maximo = datos['indicators']['quote'][0]['high']
        minimo = datos['indicators']['quote'][0]['low']
        cierre = datos['indicators']['quote'][0]['close']

        precios = pd.DataFrame(
            {'Fecha/Hora': timestamp, 'Apertura': apertura, 'Máximo': maximo, 'Mínimo': minimo, 'Cierre': cierre})
        # la hora original es GMT, para cambiarla a MX le resto 6 horas
        precios['Fecha/Hora'] = pd.to_datetime(precios['Fecha/Hora'], unit='s') + pd.Timedelta(-6, 'hours')

        precios.set_index('Fecha/Hora', inplace=True)
        self.resultado = precios
