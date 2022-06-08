import os.path
import sys
import requests
from collections import Counter
import mysql.connector
import pymysql


Lista2A = []
Lista2B = []
Lista2C = []
Lista1E = []
Lista1B = []
Lista1A = []
Lista1F = []
lista_apartado_d = []
lista_apartado_c = []

connection = pymysql.connect(
    host = "localhost",
    user="root",
    password="password",
    db="Consultas"
    )

my_cursor = connection.cursor()

connection.commit()


def obtenerDatos():
    global Lista1A
    # file = open ("Prueba.txt","r",encoding='utf-8')
    # data = file.read()
    data = sys.stdin.read()
    data2 = data
    data = data.split("[fin]")
    # data2 = data
    # data = data.split("[fin]") # Dividimos la informacion pro paginas , [pag1,pag2, .... , pag?]
    # file.close()
    cont = 0

##    Apartado2A(data)
##    print("******************************")
##    Apartado2C(data2)
##    InsertInto2A()
##    InsertInto2C()
    for i in data:
        if i == "":
            continue
        else:
            Informacion = data[cont]
            
            ApartadoA(Informacion)
            #ApartadoF(Informacion)
            # Apartado2B(Informacion)
            #ApartadoE(Informacion)
            #ApartadoB(Informacion)
            
            print("-----------------------------------------")
    
            cont+=1
    print(Lista1A)
    # InsertInto2B()
    #Insert1A()
    #Insert1F()
    #Insert1B()
    #Insert1E()
    
    
def ApartadoA(Info):
    global Lista1A
    try:
        Titulos = Info.count("<h1>") + Info.count("<h2>") + Info.count("<h3>")
        Info = Info.split("\n")
        Info = [ele for ele in Info if ele.strip()]
        Titulo_pagina = str(Info[0])[5:].lower()
        Lista1A +=[[Titulo_pagina, "CantidadDeTitulos",Titulos]]
    except:
        print("")

def Insert1A():
    global Lista1A
    print("Estoy insertando A")
    cursor = connection.cursor()
    for i in Lista1A:
        pagina = i[0]
        CantidadTitulos = i[2]
        sql = "INSERT into Apartado1A(pagina,CantidadTitulos) values (%s,%s)"
        datos = (pagina,CantidadTitulos)
        cursor.execute(sql,datos)
        connection.commit()
    

def ApartadoF(Info):
    global Lista1F
    try:
        signos = ".,:;-[]{}()'\"@/¿?¡!"
        a_espacios = str.maketrans(signos, " "*len(signos))
        palabras = str.translate(Info, a_espacios).lower().split()
        contador = Counter(palabras)
        #print(contador.most_common(1))
        palabra_a_comparar = contador.most_common(1)[0][0].lower()
        Info = Info.split("\n")
        Info = [ele for ele in Info if ele.strip()]
        Titulo_pagina = str(Info[0])[5:].lower()
        #print(Titulo_pagina)
        res = palabra_a_comparar in Titulo_pagina
        if res == True:
            Lista1F += [[Titulo_pagina,"PalabraMásComún",palabra_a_comparar,"Si está"]]
        else:
            Lista1F += [[Titulo_pagina,"PalabraMásComún",palabra_a_comparar,"No está"]]
            
    except:
        print("")

def Insert1F():
    global Lista1F
    print("Estoy insertando F")
    cursor = connection.cursor()
    for i in Lista1F:
        pagina = i[0]
        PalabraComun = i[2]
        Aparece = i[3]
        sql = "INSERT into Apartado1F(pagina,PalabraComun,Aparece) values (%s,%s,%s)"
        datos = (pagina,PalabraComun,Aparece)
        cursor.execute(sql,datos)
        connection.commit()
        
def ApartadoB(Info):
    global Lista1B
    try:
        Titulos = ""
        Info = Info.split("\n")
        Info = [ele for ele in Info if ele.strip()]
        Titulo_pagina = str(Info[0])[5:]

        for i in Info:
            if i.startswith("<h1>") or i.startswith("<h2>")  or i.startswith("<h3>") :
                Titulos += i[5:] + "\n"


        signos = ".,:; - []{}()'\"@/¿?¡!*+1234567890"
        a_espacios = str.maketrans(signos, " "*len(signos))
        palabras = str.translate(Titulos, a_espacios).lower().split()
        PalabrasDistintas = len(list(set(palabras)))

        Lista1B += [[Titulo_pagina, "PalabrasDiferentesPorTitulo",PalabrasDistintas]]
    except:
        print("")
    #print(Lista1B)
            
def Insert1B():
    global Lista1B
    print("Estoy insertando B")
    cursor = connection.cursor()
    for i in Lista1B:
        pagina = i[0]
        PalabrasDistintas = i[2]
        sql = "INSERT into Apartado1B(pagina,PalabrasDistintas) values (%s,%s)"
        datos = (pagina,PalabrasDistintas)
        cursor.execute(sql,datos)
        connection.commit()
def ApartadoE(Info):
    global Lista1E
    try:
        TextoAlt = ""
        Cantidad = 0
        Info = Info.split("\n")
        Info = [ele for ele in Info if ele.strip()]
        Titulo_pagina = str(Info[0])[5:]
        
        for i in Info:
            if i.startswith(" alt-") == True:
                if i[5:] == "":
                    continue
                else:
                    Cantidad+=1
                    TextoAlt+= i[5:] + "\n"
            else:
                continue
            
        signos = ".,:;-[]{}()'\"@/¿?¡!*+1234567890"
        a_espacios = str.maketrans(signos, " "*len(signos))
        palabras = str.translate(TextoAlt, a_espacios).lower().split()
        PalabrasDistintas = len(list(set(palabras)))
        Lista1E += [[Titulo_pagina,"CantidadAlt",Cantidad,"PalabrasDistintas",PalabrasDistintas]]
    except:
        print("")
    #print(Lista1E)
def Insert1E():
    global Lista1E
    print("Estoy insertando E")
    cursor = connection.cursor()
    for i in Lista1E:
        pagina = i[0]
        CantidadAlt = i[2]
        PalabrasDistintas = i[4]
        sql = "INSERT into Apartado1E(pagina, CantidadAlt,PalabrasDistintas) values (%s,%s,%s)"
        datos = (pagina,CantidadAlt,PalabrasDistintas)
        cursor.execute(sql,datos)
        connection.commit()
    

def ApartadoC(pagina):
    lineas = pagina.split("\n")
    cantidad_links = 0
    cantidad_links_activos = 0
    titulo = ""

    for linea in lineas:
        if linea.startswith("<h1>"):
            titulo = linea.replace("<h1>", "")
        try:
            if linea.startswith("http://") or linea.startswith("https://"):
                cantidad_links += 1
                respuesta = requests.get(linea)
                if respuesta.ok:
                    cantidad_links_activos += 1
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"

    print("\n\n")
    print("Página: " + titulo)
    print("Cantidad de referencias que tienen links: " + str(cantidad_links))
    print("Cantidad de links activos: " + str(cantidad_links_activos))
    print("\n\n")


def Apartado2C(Info):
    Data = Info
    Info = Info.split("\n")
    
    Parrafos = ""
    TitulosH1 = ""
    SubTitulosH2 = ""
    SubTitulosH3 = ""
    Referencias = ""
    Imagenes = ""
    for i in Info:
        
        if i.startswith("<p>") == True:
            Parrafos += i[4:] + "\n"
        elif i.startswith("<h1>") == True:
            TitulosH1 += i[5:] + "\n"
        elif i.startswith("<h2>") == True:
            SubTitulosH2 +=i[5:] + "\n" 
        elif i.startswith("<h3>") == True:
            SubTitulosH3 +=i[5:] + "\n"
    Apartado2C_AUX(Data,Parrafos,TitulosH1,SubTitulosH2,SubTitulosH3)


def Apartado2C_AUX(Data,Parrafos,TitulosH1,SubTitulosH2,SubTitulosH3):
    global Lista2C
    signos = ".,:;-[]{}()'\"@/¿?¡!*+1234567890"
    a_espacios = str.maketrans(signos, " "*len(signos))
    palabras = str.translate(Data, a_espacios).lower().split()
    palabras = list(set(palabras))

    TotalPalabrasParrafo = str.translate(Parrafos, a_espacios).lower().split()
    TotalPalabrasParrafo = len(list(set(TotalPalabrasParrafo)))-1

    TotalPalabrasTitulosH1 = str.translate(TitulosH1, a_espacios).lower().split()
    TotalPalabrasTitulosH1 = len(list(set(TotalPalabrasTitulosH1)))-1

    TotalPalabrasSubTitulosH2 = str.translate(SubTitulosH2, a_espacios).lower().split()
    TotalPalabrasSubTitulosH2 = len(list(set(TotalPalabrasSubTitulosH2)))-1

    TotalPalabrasSubTitulosH3 = str.translate(SubTitulosH3, a_espacios).lower().split()
    TotalPalabrasSubTitulosH3 = len(list(set(TotalPalabrasSubTitulosH3)))-1

    
    for i in palabras:

        PorcentajeP=0
        PorcentajeH1=0
        PorcentajeSubH2=0
        PorcentajeSubH3=0
        if Parrafos.count(i) > 0:
            PorcentajeP = Parrafos.count(i) / TotalPalabrasParrafo
            PorcentajeP*=100
             
        if TitulosH1.count(i) > 0:
            PorcentajeH1 = TitulosH1.count(i) / TotalPalabrasTitulosH1
            PorcentajeH1*=100 
        if SubTitulosH2.count(i) > 0:
            PorcentajeSubH2 = SubTitulosH2.count(i) / TotalPalabrasSubTitulosH2
            PorcentajeSubH2*=100
        if SubTitulosH3.count(i) > 0:
            PorcentajeSubH3 = SubTitulosH3.count(i) / TotalPalabrasSubTitulosH3
            PorcentajeSubH3*=100

        Lista2C+= [[i,"<h1>", PorcentajeH1,"<h2>",PorcentajeSubH2,"<h3>",PorcentajeSubH3,"<p>",PorcentajeP]]

        #print(Lista2C)
            
def InsertInto2C():
    global Lista2C
    print ("Estoy Insertando 2C")
    cursor = connection.cursor()
    for i in Lista2C:
        palabra = i[0]
        PorcentajeH1 = i[2]
        PorcentajeSubH2 = i[4]
        PorcentajeSubH3 = i[6]
        parrafo = i[8]
        sql = "INSERT into Apartado2C(palabra,PorcentajeH1,PorcentajeSubH2,PorcentajeSubH3,parrafo) values (%s,%s,%s,%s,%s)"
        datos = (palabra,PorcentajeH1,PorcentajeSubH2,PorcentajeSubH3,parrafo)
        cursor.execute(sql,datos)
        connection.commit()

        
    
def Apartado2A(Info):

    palabras = ListaPalabras(Info)
    for palabra in palabras:
        Apartado2A_AUX(palabra,Info)
            
def Apartado2A_AUX(palabra,Info):
    
    global Lista2A
    cont = 0
    for i in Info:

        res = palabra in i
        if res == True:
            Info_AUX = Info[cont].split("\n")
            Info2 = [ele for ele in Info_AUX if ele.strip()]
            Titulo_pagina = str(Info2[0])[5:]
            cantidad = Info[cont].count(palabra)
            Lista2A+=[[Titulo_pagina,palabra,cantidad]]
        cont += 1
        continue


def InsertInto2A():
    global Lista2A
    print ("Estoy Insertando 2A")
    cursor = connection.cursor()
    for i in Lista2A:
        pagina = i[0]
        palabra = i[1]
        cantidad = i[2]
        sql = "INSERT into Apartado2A(pagina, palabra,cantidad) values (%s,%s,%s)"
        datos = (pagina,palabra,cantidad)
        cursor.execute(sql,datos)
        connection.commit()

    
def Apartado2B(Pag):

    global Lista2B
    try:
        signos = ".,:;-[]{}()'\"@/¿?¡!*+1234567890"
        a_espacios = str.maketrans(signos, " "*len(signos))
        palabras = str.translate(Pag, a_espacios).lower().split()
        palabras = list(set(palabras))
        Total = len(palabras)-1
        info = Pag.split("\n")
        info_aux = [ele for ele in info if ele.strip()]
        Titulo_pagina = str(info_aux[0])[5:]
        print(Titulo_pagina)
        
        for i in palabras:
            CantidadPalabras = Pag.count(i)
            Porcentaje = CantidadPalabras/Total 
            Porcentaje*=100
            Lista2B += [[Titulo_pagina,i,Porcentaje,CantidadPalabras]]
    
            #print(Lista2B)
    except:
        print("")
        

def InsertInto2B():
    global Lista2B
    print ("Estoy Insertando 2B")
    cursor = connection.cursor()
    for i in Lista2B:
        pagina = i[0]
        palabra = i[1]
        porcentaje = i[3]
        sql = "INSERT into Apartado2B(pagina, palabra,porcentaje) values (%s,%s,%s)"
        datos = (pagina,palabra,porcentaje)
        cursor.execute(sql,datos)
        connection.commit()
        


            
def ListaPalabras(Info):
    Lista = []
    cont = 0

    for i in Info:
        if i == "":
            continue
        else:
            Informacion = Info[cont]
            signos = ".,:;-[]{}()'\"@/¿?¡!"
            a_espacios = str.maketrans(signos, " "*len(signos))
            Lista+= str.translate(Informacion, a_espacios).lower().split()
            cont+=1
    palabras = list(set(Lista))
    return palabras
        

def insertar_apartado_c():
    global lista_apartado_c
    global my_cursor
    global my_data_base
    for i in lista_apartado_c:
        titulo = i[0]
        cantidad_links = i[1]
        cantidad_links_activos = i[2] 
        sql = "INSERT INTO Apartado_C(titulo, cantidad_links, cantidad_links_activos) VALUES (%s,%s,%s)"
        datos = (titulo, cantidad_links,cantidad_links_activos)
        my_cursor.execute(sql,datos)
        my_data_base.commit()


def insertar_apartado_d():
    global lista_apartado_d
    global my_cursor
    global my_data_base
    for i in lista_apartado_d:
        titulo = i[0]
        numero_link = i[1]
        cantidad_veces_link = i[2] 
        sql = "INSERT INTO Apartado_D(titulo, numero_link, cantidad_veces_link) VALUES (%s,%s,%s)"
        datos = (titulo, numero_link,cantidad_veces_link)
        my_cursor.execute(sql,datos)
        my_data_base.commit()


def ApartadoC(pagina):
    global lista_apartado_c
    lineas = pagina.split("\n")
    cantidad_links = 0
    cantidad_links_activos = 0
    titulo = ""

    for linea in lineas:
        if linea.startswith("<h1>"):
            titulo = linea.replace("<h1>", "")
        try:
            if linea.startswith("http://") or linea.startswith("https://"):
                cantidad_links += 1
                respuesta = requests.get(linea.rsplit("[")[0])
                if respuesta.ok:
                    cantidad_links_activos += 1
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"
    lista_apartado_c.append([titulo, cantidad_links, cantidad_links_activos])

    print("\n\n")
    print("Página: " + titulo)
    print("Cantidad de referencias que tienen links: " + str(cantidad_links))
    print("Cantidad de links activos: " + str(cantidad_links_activos))
    print("\n\n")


def ApartadoD(pagina):
    lineas = pagina.split("\n")
    contador = 0
    lista_resultados = []
    titulo = ""

    for linea in lineas:
        if linea.startswith("<h1>"):
            titulo = linea.replace("<h1>", "")

        if linea.startswith("http://") or linea.startswith("https://"):
            indice_inicial = linea.rfind("[")
            referencia = linea[indice_inicial:]
            contador = contar_referencias(lineas, referencia) - 1
            lista_resultados.append([titulo, contador])
    
    mostrar_referencias(lista_resultados)


def mostrar_referencias(lista_resultados):
    contador = 1
    for i in lista_resultados:
        print("\nLa referencia " +str(contador) + " se usa " +str(i[1]) + " veces")
        lista_apartado_d.append([i[0], contador, i[1]])
        contador += 1


def contar_referencias(lineas, referencia):
    total_referencias = 0
    for linea in lineas:
        total_referencias += linea.count(referencia)
    return total_referencias




obtenerDatos()






#Archivo = sys.stdin

#print(Archivo)
##for line in sys.stdin:
##        if isinstance(line,str):
##            print(line[0])
##        else:
##            continue
