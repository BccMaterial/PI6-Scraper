from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://stake.bet.br/esportes/futebol/brasil/brasileirao-serie-a")

    wait = WebDriverWait(driver, 20)

    # Aceitar cookies primeiro
    try:
        aceitar_cookies = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#gdpr-snackbar-accept")))
        aceitar_cookies.click()
        print("Cookies aceitos.")
    except Exception as e:
        print("Botão de aceitar cookies não encontrado ou já aceito.", e)

    time.sleep(2)

    # Aceitar confirmação de maior de 18 anos
    try:
        aceitar_18 = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div.fade.age-verification-modal.modal.show > div > div > div > button.btn.variant-action")
        ))
        aceitar_18.click()
        print("Confirmação de 18 anos aceita.")
    except Exception as e:
        print("Botão de confirmação 18 anos não encontrado ou já aceito.", e)

    # Dá um scroll para garantir que os jogos sejam carregados
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Espera até os jogos aparecerem ou timeout
    timeout = 30  # segundos
    start_time = time.time()

    while True:
        linhas = driver.find_elements(By.CSS_SELECTOR, "li.KambiBC-sandwich-filter__event-list-item")
        if len(linhas) > 0:
            print(f"{len(linhas)} jogos encontrados.")
            break
        if time.time() - start_time > timeout:
            print("Timeout esperando os jogos carregarem.")
            break
        time.sleep(1)

    # Tira print para verificar o que está na tela
    driver.save_screenshot("output/pagina_apos_modais.png")
    print("Screenshot salva em output/pagina_apos_modais.png")

    if len(linhas) == 0:
        print("Nenhum jogo encontrado, saindo.")
    else:
        with open("output/dados.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['time_casa', 'time_fora', 'dia_jogo', 'hora_jogo','mult_vitoria_time_1','mult_empate','mult_vitoria_time_2'])

            for linha in linhas:
                try:
                    time_casa = linha.find_element(By.CSS_SELECTOR,
                        'div.KambiBC-event-participants > div:nth-child(1) > div.KambiBC-event-participants__name-participant-name').text.strip()

                    botoes = linha.find_elements(By.CSS_SELECTOR, 'div.KambiBC-bet-offer__outcomes button')
                    odds = [x.text.strip() for x in botoes[:len(botoes)-2]]
                    
                    print(f"Odds encontradas: {odds}")
                    mult_vitoria_time_1 = odds[0]
                    mult_empate = odds[1]
                    mult_vitoria_time_2 = odds[2]

                    time_fora = linha.find_element(By.CSS_SELECTOR,
                        'div.KambiBC-event-participants > div:nth-child(2) > div.KambiBC-event-participants__name-participant-name').text.strip()

                    dia_jogo = linha.find_element(By.CSS_SELECTOR, 'span.KambiBC-event-item__start-time--date').text.strip()
                    hora_jogo = linha.find_element(By.CSS_SELECTOR, 'span.KambiBC-event-item__start-time--time').text.strip()

                    writer.writerow([time_casa, time_fora, dia_jogo, hora_jogo, mult_vitoria_time_1, mult_empate, mult_vitoria_time_2])
                except Exception as e:
                    print(f"Erro ao extrair uma linha: {e}")

        print(f"{len(linhas)} jogos salvos em outputs/dados.csv")

finally:
    driver.quit()


##gdpr-snackbar-accept
#gdpr-snackbar-accept
#body > div.fade.age-verification-modal.modal.show > div > div > div > button.btn.variant-action
