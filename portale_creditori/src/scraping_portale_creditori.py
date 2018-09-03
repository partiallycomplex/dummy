import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime


class PortaleCreditori(object):

    ''' Ricerca per Ragione Sociale: key -> "txt_testo"
        Ricerca per Partita Iva: key -> "txt_piva"
    '''

    the_url = "http://www.portalecreditori.it/"

    def __init__(self, chromedriver_path):
        self.driver_path = chromedriver_path
        chrome_opts = Options()  
        chrome_opts.add_argument("--headless")  
        self.browser = webdriver.Chrome(self.driver_path, chrome_options = chrome_opts)

    def GetDataFromRagioneSociale(self, name):
        self.__get_data_from_key__("txt_testo", name)

    def GetDataFromPIva(self, piva):
        self.__get_data_from_key__("txt_piva", piva)

    def GetResults(self):
        return (self.numero_ruolo, self.tribunale, self.procedura, self.data_apertura.strftime("%d/%m/%Y"), self.giudice, self.curatore)

    def CloseBrowser(self):
        self.browser.close()

    def CloseConnection(self):
        self.browser.quit()

    def __get_data_from_key__(self, key, value):
        self.browser.get(PortaleCreditori.the_url)
        self.__show_fields__()

        field = self.browser.find_element_by_id(key)
        field.send_keys(value)

        self.__submit_request__()
        results = self.__fetch_data__()

        self.__fill_fields__(results)
        self.CloseBrowser()

    def __submit_request__(self):
        submit = self.browser.find_element_by_name("filtro") 
        submit.send_keys(Keys.RETURN)

    def __fetch_data__(self):
        table = self.browser.find_element_by_xpath('//*[@id="elenco"]/tbody/tr[2]/td[1]/a')
        table.send_keys(Keys.RETURN)
        table_txt = self.browser.find_element_by_class_name("table-vertical-header").text
        return dict((k.strip(), v.strip()) for k,v in (item.split(":") for item in table_txt.split("\n")))
 
    def __fill_fields__(self, input_dictionary):
        self.ragione_sociale = input_dictionary["Ragione sociale"]
        self.indirizzo = input_dictionary["Indirizzo"]
        self.codice_fiscale =input_dictionary["Codice fiscale"]
        self.partita_iva = input_dictionary["Partita Iva"]
        self.procedura = input_dictionary["Tipo di procedura"]
        self.data_apertura = datetime.strptime(input_dictionary["Dichiarata il"], "%d/%m/%Y").date()
        self.numero_ruolo = input_dictionary["Numero"]
        self.pec = input_dictionary["PEC della procedura"]
        self.giudice = input_dictionary["Giudice Delegato"]
        self.tribunale = input_dictionary["Tribunale"]
        self.curatore = input_dictionary["Curatore"]


    def __show_fields__(self):
        show_fields = self.browser.find_element_by_xpath("//input[@placeholder='Mostra filtri']")
        show_fields.send_keys(Keys.RETURN)

    def __del__(self):
        self.CloseConnection()


chrome_driver_path = "D:/codice/chromedriver/chromedriver.exe"
name = 'Immobiliare Dama Srl'
test = PortaleCreditori(chrome_driver_path)
test.GetDataFromRagioneSociale(name)
print(test.GetResults())
test.CloseConnection()


''' PROVA DOWNLOAD RAGIONE SOCIALE '''

import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

chrome_opts = Options()  
chrome_opts.add_argument("--headless")  
driver = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_opts)
base_url = 'http://www.portalecreditori.it/procedure.php?altre=fallimenti'
driver.get(base_url)
num_pages =driver.find_element_by_xpath("/html/body/div[1]/div/div/div/main/div/div/div/i/b")


page_number = 1
url = base_url + "&page=" + str(page_number)
driver.get(url)
names = []


while True:
    current_page_field = int(driver.find_element_by_xpath('/html/body/div[1]/div/div/div/main/div/div/div/input').get_attribute('value'))
    while current_page_field != page_number:
        time.sleep(1)

    page_number = int(driver.find_element_by_xpath('/html/body/div[1]/div/div/div/main/div/div/div/input').get_attribute('value'))
    print('Page ' + str(page_number))
    row_count = len(driver.find_elements_by_xpath('//*[@id="elenco"]/tbody/tr'))
    num = range(2, row_count)
    for i in num:
        path = '//*[@id="elenco"]/tbody/' + 'tr[' + str(i) + ']' + '/td[1]'
        name = driver.find_element_by_xpath(path).text
        names.append(name)

    page_number = page_number + 1
    url = base_url + "&page=" + str(page_number)
    driver.get(url)

print(len(names))

def write_list_to_file(the_list, filename):
    """Write the list to csv file."""

    with open(filename, "w") as outfile:
        outfile.write("RAGIONE SOCIALE")
        outfile.write("\n")
        for entries in the_list:
            outfile.write(entries)
            outfile.write("\n")

#Creating .csv file. 
file_path = "data/ragione_sociale.csv"
write_list_to_file(names, file_path)

print("ciao")