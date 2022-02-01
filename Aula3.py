from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

browser = webdriver.Chrome(r"C:\Users\lukef\Desktop\chromedriver.exe")

# pegando a cotação do Dólar
browser.get("https://www.google.com/")
browser.find_element_by_xpath(
    "html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input"
).send_keys("Cotação Dólar", Keys.ENTER)

cotacao_dolar = browser.find_element_by_xpath(
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]'
).get_attribute("data-value")

print(cotacao_dolar)

# pegando a cotação do Euro
browser.get("https://www.google.com/")
browser.find_element_by_xpath(
    "html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input"
).send_keys("Cotação Euro", Keys.ENTER)

cotacao_euro = browser.find_element_by_xpath(
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]'
).get_attribute("data-value")

print(cotacao_euro)

# pegando a cotação do Ouro
browser.get("https://www.melhorcambio.com/ouro-hoje")

cotacao_ouro = browser.find_element_by_xpath(
    '/html/body/div[6]/div[1]/div/div/input[2]'
).get_attribute("value")

cotacao_ouro = cotacao_ouro.replace(",", ".")
print(cotacao_ouro)

# abrindo o arquivo
file = pd.read_excel(r"Intensivão\aula3 - Web Scraping\Produtos.xlsx")
print(file)

# atualizar coluna de Cotação para:
# cotacao_dolar if file["Moeda"] == Dólar
# cotacao_euro if file["Moeda"] == Euro
# cotacao_ouro if file["Ouro"] == Ouro
file.loc[file["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
file.loc[file["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
file.loc[file["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

# atualizar Preço Base Reais = Preço Base Original * cotação
file["Preço Base Reais"] = file["Preço Base Original"] * file["Cotação"]

# atualizar Preço Final = Preço Base Reais * Margem
file["Preço Final"] = file["Preço Base Reais"] * file["Margem"]

# formatação em R$, com divisores de mil e 2 casas decimais (centavos)
# if header contains "Preço", formatar desta maneira
file["Preço Base Original"] = file["Preço Base Original"].map(
    "R$ {:.2F}".format)
file["Preço Base Reais"] = file["Preço Base Reais"].map("R$ {:.2F}".format)
file["Preço Final"] = file["Preço Final"].map("R$ {:.2F}".format)

# exportar nova planilha de excel com valores atualizados
file.to_excel(
    r"Intensivão\aula3 - Web Scraping\Produtos Novo.xlsx", index=False)
