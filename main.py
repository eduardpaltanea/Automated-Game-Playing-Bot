from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

#Am creat butonul de trebuie apasat in while
cookie_button = driver.find_element(By.ID, value="cookie")

timeout = time.time() + 5  #timeout de 5 secunde
five_min = time.time() + 5 * 60

items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

while True:
    cookie_button.click()
    if time.time() > timeout:

        #Am creat un dictionar cu optiunile care pot sa fie cumparate key=ID si value=pretul ca numar intreg
        options_to_buy = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        list_of_option_prices = []
        for option in options_to_buy:
            option_id = option.get_attribute("id")
            option_text = option.text
            if option_text != "":
                option_price = int(option_text.split("-")[1].strip().replace(",", ""))
                list_of_option_prices.append(option_price)
        options_dict = {}
        for n in range(len(list_of_option_prices)):
            options_dict[list_of_option_prices[n]] = item_ids[n]

        #Trebuie sa vad acum cati bani am ca numar intreg
        money_element = driver.find_element(by=By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        #Trebuie sa fac un dictionar cu id si valorile pentru care am bani o data la 5 secunde
        what_can_i_afford = {}
        for cost, id in options_dict.items():
            if cookie_count > cost:
                what_can_i_afford[cost] = id

        #Trebuie sa iau acum valoarea maxima din acel dictionar si sa dau mai departe id-ul maxim
        max_option = max(what_can_i_afford)
        to_purchase_id = what_can_i_afford[max_option]

        #Apas pe optiunea care are valoarea maxima pe care o pot cumpara
        driver.find_element(By.ID, value=to_purchase_id).click()

        timeout = time.time() + 5
        #Daca trece de 5 minute programu o sa printeze cate cookie-uri pe secunda a facut in timpul respectiv si iese din loop
        if time.time() > five_min:
            cookie_per_sec = driver.find_element(By.ID, value="cps").text
            print(cookie_per_sec)
            break







