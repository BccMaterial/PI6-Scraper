from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--incognito")

print("Iniciando o chrome...")
driver = webdriver.Chrome(options=chrome_options)

try:
    print("Realizando scraping da rodada atual do brasileirão...")

    driver.get("https://www.google.com/search?q=campeonato+brasileiro")
    wait = WebDriverWait(driver, 20)

    try:
        jogos = wait.until(EC.presence_of_all_elements_located(By.CSS_SELECTOR, "div.XQDFi div.gnP8Re")) #Também guarda todos os elementos com o CSS selector utilizado
        print(f"Foram encontrados {len(jogos)} jogos")

        for i, jogo in enumerate(jogos):
            try:
                print(f"Entrando no jogo {i}...")
                driver.execute_script("arguments[0].click();", jogo) #Utilizamos o .click() do JavaScript ao invés do .click() do Selenium pois o clique ocorre mesmo que esteja oculto ou fora da tela
                #Adicionar scraping em si:

            except Exception as e:
                print(f"Ocorreu o seguinte erro quando clicando no jogo {i}: {e}")

    except Exception as e:
        print(f"Não foi encontrado nenhum jogo: {e}")

finally:
    driver.quit()
