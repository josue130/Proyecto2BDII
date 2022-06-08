from distutils.spawn import spawn
import requests
from bs4 import BeautifulSoup
import random
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from csv import writer
from time import sleep
import sys

sys.setrecursionlimit(1000000000)
contador = 0
contenido_paginas = ""

pagina = "" 
soup = 0
linkToScrape = ""
allLinks = 0
paginas = ""
ContEscritura = 0

lista_aritulos = ["a", "an", "the", "some", "The", "A", "An", ".", ",", ":", ";",
                "svg", "png", "jpg", "and", "And", "for", "For", "alt", "Alt", "In", "in", "Of", "of", "`", "``"]


def stemmer(text_list):
    global lista_aritulos
    ps = PorterStemmer()
    sentence = ""
    for word in text_list:
        if word in lista_aritulos:
            continue
        else:
            sentence += ps.stem(word) + " "
    return sentence


def scrapeWikiArticle(url):
    global contador
    global contenido_paginas
    global soup
    global linkToScrape
    global allLinks
    global ContEscritura
    global paginas

    response = requests.get( url=url,  )
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find(id="firstHeading")
    
    allLinks = soup.find(id="bodyContent").find_all("a")
    
    random.shuffle(allLinks)
    
    for link in allLinks:
        
        linkToScrape = link
        
        try:
            
            if str(linkToScrape['href'])[0:6] != "/wiki/":
                continue

            if str(linkToScrape['href'])[0:14] == "/wiki/Special:" or str(linkToScrape['href'])[0:11] == "/wiki/User:" or str(linkToScrape['href'])[0:11] == "/wiki/File:" or str(linkToScrape['href'])[0:16] == "/wiki/User_talk:":
                continue
            
            else:
                #print( contador )
                print(linkToScrape['href'])
                content = soup.find( class_="mw-parser-output")
                
                Information_Page(content,title.text)
                
                ContEscritura+=1
                contador+=1
                print(ContEscritura)
                break
        except:
            continue

    if ContEscritura == 50:
        with open("ArchivoPrueba.txt", 'a', encoding = 'utf-8' ) as file:
            file.write(paginas)
            ContEscritura = 0
            paginas=""
            sleep(5)
    
    
    if contador != 100:
        
        scrapeWikiArticle("https://en.wikipedia.org" + linkToScrape['href'])
        
    else:
        print("Finalizado")
    
                    
def Information_Page(content,title):
    global pagina
    global soup

    pagina += "<h1>"+" "+ title + "\n"
    subs_content = ""
    contenido_paginas = ""

    try:
        for i in content:
            
            Content_aux = str(i)
            
            if Content_aux[0:4] != '<h1>' and Content_aux[0:3] != '<p>' and Content_aux[0:4] != '<h2>' and Content_aux[0:4] != '<h3>' :
                continue
            else:
                
                if  Content_aux[0:2] == '<h':
                    #print( pagina )
                    subs_list = word_tokenize(i.text)
                    
                    subs_content += stemmer(subs_list) + "\n"

                    
                    pagina += Content_aux[0:4]+ " " + subs_content
                    
                    subs_content = ""
                    
                else:
                    paragraph_list = word_tokenize(i.text)
                    
                    contenido_paginas += stemmer(paragraph_list) + "\n"
                    
                    pagina += Content_aux[0:3]+ " "+ contenido_paginas
                    
                    contenido_paginas = ""
        images()
        References()
        pagina = ""
    except:
        print(content)


def References():
    global soup
    global pagina
    global paginas
    try:
        reflist = soup.find(["div"], class_="reflist")
        
        if len(reflist["class"]) > 1:
            reflist = reflist.find_next_sibling("div")
            if reflist.findChild("div") is not None:
                if len(reflist.find_next("div")["class"]) > 1:
                    references_descrption = soup.find(["div"], class_=(str(reflist.find_next("div")["class"][0]) + " " + str(reflist.find_next("div")["class"][1])))
                    pagina += str(references_descrption.find(["ol"], class_="references").text) + "\n"

                    references_link = references_descrption.find(["ol"], class_="references").find_all("a")
                    contador = 0
                    contador_referencias = 1

                    for x in references_link:
                        if contador != (len(references_link) - 1):
                            if (str(references_link[contador]["href"]).startswith("http://")) or (str(references_link[contador]["href"]).startswith("https://")):
                                pagina += str (references_link[contador]["href"]) + "[ " + str(contador_referencias) + " ]" +"\n"
                                contador += 1
                                contador_referencias += 1

                            else:
                                pagina += str (references_link[contador]["href"]) + "\n"
                                contador += 1

                    pagina += "[fin]" + "\n"
                    paginas += pagina

                else:
                    references_descrption = soup.find(["div"], class_=(str(reflist.find_next("div")["class"][0])))
                    pagina += str(references_descrption.find(["ol"], class_="references").text) + "\n"

                    references_link = references_descrption.find(["ol"], class_="references").find_all("a")
                    contador = 0
                    contador_referencias = 1

                    for x in references_link:
                        if contador != (len(references_link) - 1):
                            if (str(references_link[contador]["href"]).startswith("http://")) or (str(references_link[contador]["href"]).startswith("https://")):
                                pagina += str (references_link[contador]["href"]) + "[ " + str(contador_referencias) + " ]" +"\n"
                                contador += 1
                                contador_referencias += 1

                            else:
                                pagina += str (references_link[contador]["href"]) + "\n"
                                contador += 1

                    pagina += "[fin]" + "\n"
                    paginas += pagina

            if reflist.findChild("div") is None:
                ol_list_text = reflist.find(["ol"], class_="references").text
                pagina += str(ol_list_text)
                ol_list = reflist.find(["ol"], class_="references").find_all("a")
                contador = 0
                contador_referencias = 1

                for x in ol_list:
                    if contador != (len(ol_list) - 1):
                        if (str(ol_list[contador]["href"]).startswith("http://")) or (str(ol_list[contador]["href"]).startswith("https://")):
                            pagina += str (ol_list[contador]["href"]) + "[ " + str(contador_referencias) + " ]" +"\n"
                            contador += 1
                            contador_referencias += 1

                        else:
                            pagina += str (ol_list[contador]["href"]) + "\n"
                            contador += 1
                        
                pagina += "[fin]" + "\n"
                paginas += pagina

        else:
            if reflist.findChild("div") is not None:
                references_descrption = soup.find(["div"], class_=str(reflist.find_next("div")["class"][0]))
                pagina += str(references_descrption.find(["ol"], class_="references").text) + "\n"

                references_link = references_descrption.find(["ol"], class_="references").find_all("a")
                contador = 0
                contador_referencias = 1

                for x in references_link:
                    if contador != (len(references_link) - 1):
                        if (str(references_link[contador]["href"]).startswith("http://")) or (str(references_link[contador]["href"]).startswith("https://")):
                            pagina += str (references_link[contador]["href"]) + "[ " + str(contador_referencias) + " ]" +"\n"
                            contador += 1
                            contador_referencias += 1

                        else:
                            pagina += str (references_link[contador]["href"]) + "\n"
                            contador += 1

                pagina += "[fin]" + "\n"
                paginas += pagina

            if reflist.findChild("div") is None:
                ol_list_text = reflist.find(["ol"], class_="references").text
                pagina += str(ol_list_text)
                ol_list = reflist.find(["ol"], class_="references").find_all("a")
                contador = 0
                contador_referencias = 1

                for x in ol_list:
                    if contador != (len(ol_list) - 1):
                        if (str(ol_list[contador]["href"]).startswith("http://")) or (str(ol_list[contador]["href"]).startswith("https://")):
                            pagina += str (ol_list[contador]["href"]) + "[ " + str(contador_referencias) + " ]" +"\n"
                            contador += 1
                            contador_referencias += 1

                        else:
                            pagina += str (ol_list[contador]["href"]) +"\n"
                            contador += 1
                        
                pagina += "[fin]" + "\n"
                paginas += pagina

    except:
        pagina += "\n" + "[fin]" + "\n"
        paginas += pagina
        

def images():
    global soup
    global pagina
    global paginas

    nombre_stemming = ""
    lista_imagenes = soup.find_all("img")

    for imagen in lista_imagenes:
        nombre = imagen["alt"]
        url = imagen["src"]
        nombre_tokenized = word_tokenize(nombre)
        nombre_stemming += stemmer(nombre_tokenized)
        pagina += "\n alt-" + nombre_stemming
        pagina += "\n" + url

    paginas += pagina
    pagina = ""


scrapeWikiArticle("https://en.wikipedia.org/wiki/Aldo-keto_reductase")