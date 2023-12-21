import pandas as pd


import mysql.connector
import pandas as pd
import numpy as np
#################################################################################
#################################################################################
"""Definimos las variables generales para atacar la base de datos"""
#Definimos un cursor con el que atacar a la DB
cnx = mysql.connector.connect(
    user="admin",
    password="admin123",
    host="portfolio-proyect.cze2nnbbx5pc.eu-west-3.rds.amazonaws.com")
cursor = cnx.cursor()
#Definimos una función mediante la que ejecutar las querys
def make_query(code):
    cursor.execute(code)
    results = cursor.fetchall()
    cnx.commit()
    return(results)
#Definimos una función mediante la que ejecutar las querys devolviendo un dataframe
def make_query_dataframe(code):
    cursor.execute(code)
    results = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Obtener los nombres de las columnas
    df = pd.DataFrame(results, columns=column_names)  # Crear el DataFrame
    return df

# delit_type = pd.read_csv("delitosportipo.csv", sep=";",encoding="latin_1")
# delit_gender = pd.read_csv("delitosporcondena.csv",sep=";",encoding="latin-1")
# viogen = pd.read_csv("viogen.csv",sep=";",encoding="latin-1")

make_query("USE portfolio")
delit_type = make_query_dataframe("SELECT * FROM delit_type")
delit_gender = make_query_dataframe("SELECT * FROM delit_gender")
viogen = make_query_dataframe("SELECT * FROM viogen")

# Data preprocessing

# Devolvemos los NaN originales del dataframe que desaparecieron al montar la base de datos
delit_type.replace("", np.nan, inplace=True)

# Arreglamos los tipos de datos

delit_type['Periodo'] = delit_type['Periodo'].astype(int)
delit_type['Total'] = delit_type['Total'].astype(int)
delit_gender['Periodo'] = delit_gender['Periodo'].astype(int)
delit_gender['Total'] = delit_gender['Total'].astype(int)
viogen['Periodo'] = viogen['Periodo'].astype(int)
viogen['Total'] = viogen['Total'].astype(int)


# Renombramos las columnas por comodidad

delit_type.rename(columns={"Tipo de Delito: Nivel 1":"Nv1",
                            "Tipo de Delito: Nivel 2":"Nv2",
                            "Tipo de Delito: Nivel 3":"Nv3"},inplace=True)

delitos_nv2_dict = {
        '10 Contra la intimidad, derecho a la propia imagen'                                           :'Contra la intimidad, derecho a la propia imagen',
        '11 Contra el honor'                                                                           :'Contra el honor',
        '12 Contra las relaciones familiares'                                                          :'Contra las relaciones familiares',
        '13 Contra el patrimonio y el orden socioeconómico'                                            :'Contra el patrimonio y el orden socioeconómico',
        '14 Contra la Hacienda Pública y Seguridad Social'                                             :'Contra la Hacienda Pública y Seguridad Social',
        '15 BIS Contra los derechos de los ciudadanos extra'                                           :'Contra los derechos de los ciudadanos extranjeros',
        '15 Contra los derechos de los trabajadores'                                                   :'Contra los derechos de los trabajadores',
        '16 Ordenación del territorio, urbanismo, protecció'                                           :'Ordenación del territorio, urbanismo, protección del patrimonio histórico y medio ambiente',
        '17 Contra la seguridad colectiva'                                                             :'Contra la seguridad colectiva',
        '18 Falsedades'                                                                                :'Falsedades',
        '19 Contra la Administración Pública'                                                          :'Contra la Administración Pública',
        '20 Contra la Administración de Justicia'                                                      :'Contra la Administración de Justicia',
        '21 Contra la Constitución'                                                                    :'Contra la Constitución',
        '22 Contra el orden público'                                                                   :'Contra el orden público',
        '23 Traición, contra la paz y defensa nacional'                                                :'Traición, contra la paz y defensa nacional',
        '24 Contra la Comunidad Internacional'                                                         :'Contra la Comunidad Internacional',
        "1 Homicidio y sus formas"                                                                     :"Homicidio y sus formas",
        "2 Aborto"                                                                                     :"Aborto",
        "3 Lesiones"                                                                                   :"Lesiones",
        "4 Lesiones al feto"                                                                           :"Lesiones al feto",
        "5 Manipulación genética"                                                                      :"Manipulación genética",
        "6 Contra la libertad"                                                                         :"Contra la libertad",
        "7 BIS Trata de seres humanos"                                                                 :"Trata de seres humanos",
        "7 Torturas e integridad moral"                                                                :"Torturas e integridad moral",
        "8 Contra la libertad e indemnidad sexuales"                                                   :"Contra la libertad e indemnidad sexuales",
        "9 Omisión del deber de socorro"                                                               :"Omisión del deber de socorro"
    }
for k,v in delitos_nv2_dict.items():
    delit_type.loc[delit_type["Nv2"]==k, "Nv2"] = v

# Renombramos el nv3 de delitos

delitos_nv3_dict = {'6.1 Detenciones ilegales y secuestro':'Detenciones ilegales y secuestro', 
                    '6.2 Amenazas':'Amenazas',
                     '6.3 Coacciones':'Coacciones', 
                     '8.1 Agresiones sexuales':'Agresiones sexuales', 
                     '8.2 Abusos sexuales':'Abusos sexuales',
                     '8.2 BIS Abusos y agresiones sexuales a menores de 16 años':'Abusos y agresiones sexuales a menores de 16 años',
                     '8.3 Acoso sexual':'Acoso sexual', 
                     '8.4 Exhibicionismo y provocación sexual':'Exhibicionismo y provocación sexual',
                     '8.5 Prostitución y corrupción menores':'Prostitución y corrupción menores',
                     '10.1 Descubrimiento y revelación de secretos':'Descubrimiento y revelación de secretos',
                     '10.2 Allanamiento de morada':'Allanamiento de morada', 
                     '11.1 Calumnias':'Calumnias', 
                     '11.2 Injurias':'Injurias',
                     '12.1 Matrimonios ilegales':'Matrimonios ilegales',
                     '12.2 Suposición de parto y alteración de la paternidad':'Suposición de parto y alteración de la paternidad',
                     '12.3 Contra los derechos y deberes familiares':'Contra los derechos y deberes familiares', 
                     '13.1 Hurtos':'Hurtos',
                     '13.2 Robos':'Robos', 
                     '13.3 Extorsión':'Extorsión',
                     '13.4 Robo y hurto de uso de vehículo':'Robo y hurto de uso de vehículo', 
                     '13.5 Usurpación':'Usurpación',
                     '13.6 Defraudaciones':'Defraudaciones', 
                     '13.7 Frustración de la ejecución':'Frustración de la ejecución',
                     '13.7 BIS Insolvencias punibles':'Insolvencias punibles',
                     '13.8 Alteración de precios en concursos y subastas públicas':'Alteración de precios en concursos y subastas públicas',
                     '13.9 Daños':'Daños', 
                     '13.11 Propiedad intelectual e industrial':'Propiedad intelectual e industrial',
                     '13.12 De la sustracción de cosa propia a su utilidad social o cultural':'De la sustracción de cosa propia a su utilidad social o cultural',
                     '13.13 Delitos societarios':'Delitos societarios',
                     '13.14 Receptación y blanqueo de capitales':'Receptación y blanqueo de capitales',
                     '16.1 Ordenación del territorio y el urbanismo':'Ordenación del territorio y el urbanismo',
                     '16.2 Patrimonio histórico':'Patrimonio histórico',
                     '16.3 Recursos naturales y medio ambiente':'Recursos naturales y medio ambiente',
                     '16.4 Protección de flora, fauna y animales domésticos':'Protección de flora, fauna y animales domésticos',
                     '17.1 Delitos de riesgo catastrófico':'Delitos de riesgo catastrófico', 
                     '17.2 Incendios':'Incendios',
                     '17.3 Contra la salud pública':'Contra la salud pública', 
                     '17.4 Contra la seguridad vial':'Contra la seguridad vial',
                     '18.1 Falsificación de moneda y efectos timbrados':'Falsificación de moneda y efectos timbrados',
                     '18.2 Falsedades documentales':'Falsedades documentales',
                     '18.3 Fabricación o tenencia de útiles para falsificación':'Fabricación o tenencia de útiles para falsificación',
                     '18.4 Usurpación del estado civil':'Usurpación del estado civil',
                     '18.5 Usurpación de funciones públicas':'Usurpación de funciones públicas',
                     '19.1 Prevaricación de los funcionarios públicos':'Prevaricación de los funcionarios públicos',
                     '19.2 Abandono destino':'Abandono destino', 
                     '19.3 Desobediencia y denegación auxilio':'Desobediencia y denegación auxilio',
                     '19.4 Infidelidad custodia documentos':'Infidelidad custodia documentos', 
                     '19.5 Cohecho':'Cohecho',
                     '19.6 Tráfico influencias':'Tráfico influencias', 
                     '19.7 Malversación':'Malversación',
                     '19.8 Fraudes y exacciones ilegales':'Fraudes y exacciones ilegales',
                     '19.9 Negociaciones prohibidas a los funcionarios':'Negociaciones prohibidas a los funcionarios',
                     '20.1 Prevaricación':'Prevaricación',
                     '20.2 Omisión de los deberes de impedir delitos':'Omisión de los deberes de impedir delitos',
                     '20.3 Encubrimiento':'Encubrimiento',
                     '20.4 Realización arbitraria del propio derecho':'Realización arbitraria del propio derecho',
                     '20.5 Acusación y denuncia falsa':'Acusación y denuncia falsa', 
                     '20.6 Falso testimonio':'Falso testimonio',
                     '20.7 Obstrucción a la justicia':'Obstrucción a la justicia',
                     '20.8 Quebrantamiento de condena':'Quebrantamiento de condena',
                     '20.9 Contra la Administración de Justicia de la Corte Penal Internacional':'Contra la Administración de Justicia de la Corte Penal Internacional',
                     '21.1 Rebelión':'Rebelión', 
                     '21.2 Contra la Corona':'Contra la Corona',
                     '21.3 Contra las Instituciones del Estado':'Contra las Instituciones del Estado',
                     '21.4 Ejercicio de los derechos fundamentales':'Ejercicio de los derechos fundamentales',
                     '21.5 Cometidos por funcionarios contra libertad individual':'Cometidos por funcionarios contra libertad individual',
                     '21.6 Ultrajes a España':'Ultrajes a España', 
                     '22.1 Sedición':'Sedición',
                     '22.2 Atentados contra la autoridad y de la resistencia y desobediencia':'Atentados contra la autoridad y de la resistencia y desobediencia',
                     '22.3 Desórdenes públicos':'Desórdenes públicos',
                     '22.5 Tenencia, tráfico, depósito de armas y explosivos':'Tenencia, tráfico, depósito de armas y explosivos',
                     '22.6 Organizaciones y grupos criminales':'Organizaciones y grupos criminales',
                     '22.7 Organizaciones y grupos terroristas y delitos de terrorismo':'Organizaciones y grupos terroristas y delitos de terrorismo',
                     '23.1 Traición':'Traición',
                     '23.2 Que comprometen la paz o independencia del Estado':'Que comprometen la paz o independencia del Estado',
                     '23.3 Descubrimiento y revelación de secretos':'Descubrimiento y revelación de secretos',
                     '24.1 Contra el derecho de gentes':'Contra el derecho de gentes', 
                     '24.2 Genocidio':'Genocidio',
                     '24.2 BIS Lesa humanidad':'Lesa humanidad',
                     '24.3 Contra las personas y bienes protegidos':'Contra las personas y bienes protegidos'}
for k,v in delitos_nv3_dict.items():
    delit_type.loc[delit_type["Nv3"]==k, "Nv3"] = v

delitos_tipo_py = delit_type.groupby("Periodo")["Total"].sum().reset_index()

# Incremento anual delitos en términos absolutos

delitos_tipo_py['Incremento'] = delitos_tipo_py['Total'] - delitos_tipo_py['Total'].shift(1)
delitos_tipo_py['Incremento'] = delitos_tipo_py['Incremento'].fillna(0)

# Incremento anual delitos en términos relativos
delitos_tipo_py['Incremento%'] = (delitos_tipo_py['Total'] - delitos_tipo_py['Total'].shift(1)) / delitos_tipo_py['Total'].shift(1) * 100
delitos_tipo_py['Incremento%'] = delitos_tipo_py['Incremento%'].fillna(0)


# Total delitos por tipo
delitos_tipo_pt = delit_type.groupby(["Nv2", "Periodo"])["Total"].sum().reset_index()

# Delitos por tipo por año
del_tip_2013 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2013]
del_tip_2014 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2014]
del_tip_2015 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2015]
del_tip_2016 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2016]
del_tip_2017 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2017]
del_tip_2018 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2018]
del_tip_2019 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2019]
del_tip_2020 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2020]
del_tip_2021 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2021]

dict_years = {2013:del_tip_2013, 2014:del_tip_2014, 2015:del_tip_2015, 
              2016:del_tip_2016, 2017:del_tip_2017, 2018:del_tip_2018,
              2019:del_tip_2019, 2020:del_tip_2020, 2021:del_tip_2021}

# Incremento absoluto de delito por tipo por año
delitos_tipo_pt['Incremento'] = delitos_tipo_pt['Total'] - delitos_tipo_pt['Total'].shift(1)
delitos_tipo_pt['Incremento'] = delitos_tipo_pt['Incremento'].fillna(0)

# Incremento relativo de delito por tipo por año
delitos_tipo_pt['Incremento%'] = (delitos_tipo_pt['Total'] - delitos_tipo_pt['Total'].shift(1)) / delitos_tipo_pt['Total'].shift(1) * 100
delitos_tipo_pt['Incremento%'] = delitos_tipo_pt['Incremento%'].fillna(0)

def assign_nv2_5(x):
    if x in ['Homicidio y sus formas', 'Aborto', 'Lesiones', 'Lesiones al feto']:
        return 'Delitos contra la vida y la integridad física'
    elif x in ['Contra la libertad', 'Torturas e integridad moral', 'Trata de seres humanos']:
        return 'Delitos contra la libertad'
    elif x == 'Contra la libertad e indemnidad sexuales':
        return 'Delitos sexuales'
    elif x in ['Contra la intimidad, derecho a la propia imagen', 'Contra el honor']:
        return 'Delitos contra la intimidad y el honor'
    elif x == 'Contra las relaciones familiares':
        return 'Delitos contra las relaciones familiares'
    elif x == 'Contra los derechos de los trabajadores':
        return 'Delitos contra los derechos de los trabajadores'
    elif x in ['Contra el patrimonio y el orden socioeconómico', 'Falsedades']:
        return 'Delitos contra el patrimonio y el orden socioeconómico'
    elif x in ['Contra la Administración Pública', 'Contra la Administración de Justicia', 'Contra la Hacienda Pública y Seguridad Social']:
        return 'Delitos contra la Administración Pública'
    elif x in ['Contra la Constitución', 'Contra el orden público', 'Traición, contra la paz y defensa nacional']:
        return 'Delitos contra la Constitución y el orden público'
    elif x == 'Ordenación del territorio, urbanismo, protección del patrimonio histórico y medio ambiente':
        return 'Delitos relacionados con el medio ambiente y la planificación territorial'
    elif x in ['Contra la seguridad colectiva', 'Contra la Comunidad Internacional', 'Contra los derechos de los ciudadanos extranjeros', 'Omisión del deber de socorro']:
        return 'Delitos contra la seguridad'
    else:
        return x
        
delit_type['Nv2.5'] = delit_type['Nv2'].apply(assign_nv2_5)

# Total delitos por tipo
delitos_tipo_pt = delit_type.groupby(["Nv2", "Periodo"])["Total"].sum().reset_index()

# Delitos por tipo por año
del_tip_2013 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2013]
del_tip_2014 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2014]
del_tip_2015 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2015]
del_tip_2016 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2016]
del_tip_2017 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2017]
del_tip_2018 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2018]
del_tip_2019 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2019]
del_tip_2020 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2020]
del_tip_2021 = delitos_tipo_pt[delitos_tipo_pt["Periodo"]==2021]

dict_years = {2013:del_tip_2013, 2014:del_tip_2014, 2015:del_tip_2015, 
              2016:del_tip_2016, 2017:del_tip_2017, 2018:del_tip_2018,
              2019:del_tip_2019, 2020:del_tip_2020, 2021:del_tip_2021}


spain_population = {2013: 46727890, 2014: 46512199, 2015: 46449565, 
                    2016: 46440099, 2017: 46528966, 2018: 46658447, 
                    2019: 46937060, 2020: 47332614, 2021: 47400798}

for k, v in spain_population.items():
    delitos_tipo_py.loc[delitos_tipo_py["Periodo"] == k, "Poblacion"] = v

delitos_tipo_py["Tasa_Crim"] = (delitos_tipo_py["Total"] / (delitos_tipo_py["Poblacion"]/1000)) * 100

# Incremento anual delitos en términos absolutos

delitos_tipo_py['Incremento'] = delitos_tipo_py['Total'] - delitos_tipo_py['Total'].shift(1)
delitos_tipo_py['Incremento'] = delitos_tipo_py['Incremento'].fillna(0)

# Incremento anual delitos en términos relativos
delitos_tipo_py['Incremento%'] = (delitos_tipo_py['Total'] - delitos_tipo_py['Total'].shift(1)) / delitos_tipo_py['Total'].shift(1) * 100
delitos_tipo_py['Incremento%'] = delitos_tipo_py['Incremento%'].fillna(0)


delitos_tipo_pt_2 = delit_type.groupby(["Nv2.5", "Periodo"])["Total"].sum().reset_index()

# Incremento anual delitos en términos relativos
delitos_tipo_pt_2['Incremento'] = delitos_tipo_pt_2['Total'] - delitos_tipo_pt_2['Total'].shift(1)
delitos_tipo_pt_2['Incremento'] = delitos_tipo_pt_2['Incremento'].fillna(0)

# Incremento anual delitos en términos relativos
delitos_tipo_pt_2['Incremento%'] = (delitos_tipo_pt_2['Total'] - delitos_tipo_pt_2['Total'].shift(1)) / delitos_tipo_pt_2['Total'].shift(1) * 100
delitos_tipo_pt_2['Incremento%'] = delitos_tipo_pt_2['Incremento%'].fillna(0)

# Matriz de correlación entre delitos
delit_subset = delitos_tipo_pt_2[["Nv2.5","Periodo", "Incremento"]]
corr_delit = delit_subset.pivot(index="Periodo",columns="Nv2.5",values="Incremento")
corr_delit = corr_delit.corr()

# Condenados por género y año filtrados

gender_filtered = delit_gender[(delit_gender["Número de delitos"] == "Total") & (delit_gender["Nacionalidad"] == "Total") & (delit_gender["Edad"] == "Total ")]

# Filtro por género (Sin uso)
gender_filtered_mal = gender_filtered[gender_filtered["Sexo"] == "Hombres"]
gender_filtered_fem = gender_filtered[gender_filtered["Sexo"] == "Mujeres"]

# Filtros por año
gender_2021 = gender_filtered[gender_filtered["Periodo"]==2021]
gender_2020 = gender_filtered[gender_filtered["Periodo"]==2020]
gender_2019 = gender_filtered[gender_filtered["Periodo"]==2019]
gender_2018 = gender_filtered[gender_filtered["Periodo"]==2018]
