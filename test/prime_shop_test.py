import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re


@pytest.fixture()
def driver():
    ch_driver = webdriver.Chrome(service=Service('C:/Windows/chromedriver-win64/chromedriver.exe'))
    ch_driver.maximize_window()
    ch_driver.get('https://rs.primeshop360.com/')
    wait=WebDriverWait(ch_driver, 50)

    yield ch_driver
    ch_driver.quit()

def accept_cookies(driver):

        wait = WebDriverWait(driver, 30)
        cookie_button = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.btn.cookies-accept-btn"))
        )
        driver.execute_script("arguments[0].click();", cookie_button)

def login(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    register_link = wait.until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//a[@href="https://rs.primeshop360.com/moj-nalog/" and @title="Moj nalog" and contains(., "Prijavi / Registruj se")]'))
    )

    driver.execute_script("arguments[0].click();", register_link)

    login_username_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    login_username_input.send_keys("bojanstupar089@gmail.com")

    login_password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_password_input.send_keys("Celarevo44!")

    login_button = wait.until(EC.visibility_of_element_located((By.NAME, "login")))
    driver.execute_script("arguments[0].click();", login_button)


def test_open_google_and_go_to_primeshop(driver):
    wait = WebDriverWait(driver, 30)

    site_logo=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[aria-label='Site logo']")))
    site_logo.is_displayed()

def test_register_successful_on_primeshop(driver):

    accept_cookies(driver)
    wait=WebDriverWait(driver, 30)


    register_link = wait.until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//a[@href="https://rs.primeshop360.com/moj-nalog/" and @title="Moj nalog" and contains(., "Prijavi / Registruj se")]'))
    )

    driver.execute_script("arguments[0].click();", register_link)

    create_account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.create-account-button")))
    driver.execute_script("arguments[0].click();", create_account_link)

    user_name=wait.until(EC.visibility_of_element_located((By.ID,"reg_username")))
    user_name.send_keys("Mile79")

    email_input=wait.until(EC.visibility_of_element_located((By.ID,"reg_email")))
    email_input.send_keys("bojanstupar089+test12@gmail.com")

    password_input=wait.until(EC.visibility_of_element_located((By.ID,"reg_password")))
    password_input.send_keys("Celarevo44!")

    register_button=wait.until(EC.visibility_of_element_located((By.NAME,"register")))
    driver.execute_script("arguments[0].click();", register_button)


    username_span = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.wd-tools-text"))
    ).text.strip().upper()

    assert "ZDRAVO, MILE79" in username_span,"The username is not expexted."

def test_register_email_invalid_format(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    register_link = wait.until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//a[@href="https://rs.primeshop360.com/moj-nalog/" and @title="Moj nalog" and contains(., "Prijavi / Registruj se")]'))
    )

    driver.execute_script("arguments[0].click();", register_link)

    create_account_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.create-account-button")))
    driver.execute_script("arguments[0].click();", create_account_link)

    email_input = wait.until(EC.visibility_of_element_located((By.ID, "reg_email")))
    email_input.send_keys("bokica")



    register_button = wait.until(EC.visibility_of_element_located((By.NAME, "register")))
    driver.execute_script("arguments[0].click();", register_button)

    time.sleep(5)

    # error_element = wait.until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.woocommerce-error li"))
    # )
    #
    # assert "Greška:\nMolim vas unesite odgovarajuću e-mejl adresu","Error isn't correct!"

    assert not email_input.get_property("validity")["valid"], "Email polje ne bi smelo biti validno"

def test_login_successful_on_primeshop(driver):
  login(driver)
  wait=WebDriverWait(driver, 30)

  username_span = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.wd-tools-text"))
    ).text.strip().upper()

  assert"ZDRAVO, BOJAN89" in username_span,"The username is not expexted."

def test_login_required_username(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    register_link = wait.until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//a[@href="https://rs.primeshop360.com/moj-nalog/" and @title="Moj nalog" and contains(., "Prijavi / Registruj se")]'))
    )

    driver.execute_script("arguments[0].click();", register_link)

    login_username_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    login_username_input.send_keys("")

    login_button = wait.until(EC.visibility_of_element_located((By.NAME, "login")))
    driver.execute_script("arguments[0].click();", login_button)

    error_element = driver.find_element(By.CSS_SELECTOR, ".woocommerce-error li")
    error_text = error_element.text

    assert "Korisničko ime je obavezno" in error_text,"Expected error message 'Korisničko ime je obavezno' was not found on the page."

def test_login_required_password(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    register_link = wait.until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//a[@href="https://rs.primeshop360.com/moj-nalog/" and @title="Moj nalog" and contains(., "Prijavi / Registruj se")]'))
    )

    driver.execute_script("arguments[0].click();", register_link)

    login_username_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    login_username_input.send_keys("bojanstupar089")

    login_password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_password_input.send_keys("")

    login_button = wait.until(EC.visibility_of_element_located((By.NAME, "login")))
    driver.execute_script("arguments[0].click();", login_button)

    error_element = driver.find_element(By.CSS_SELECTOR, ".woocommerce-error li")
    error_text = error_element.text

    assert"Polje za lozinku je prazno" in error_text,"Expected error message 'Polje za lozinku je prazno' was not found on the page."

def test_login_bad_credentials(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    register_link = wait.until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//a[@href="https://rs.primeshop360.com/moj-nalog/" and @title="Moj nalog" and contains(., "Prijavi / Registruj se")]'))
    )

    driver.execute_script("arguments[0].click();", register_link)

    login_username_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    login_username_input.send_keys("bojanstupar089")

    login_password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_password_input.send_keys("cel")

    login_button = wait.until(EC.visibility_of_element_located((By.NAME, "login")))
    driver.execute_script("arguments[0].click();", login_button)

    error_element = driver.find_element(By.CSS_SELECTOR, ".woocommerce-error li")
    error_text = error_element.text

    assert "Korisničko ime\nbojanstupar089\nnije registrovano na ovom sajtu. Ako niste sigurni u svoje korisničko ime, pokušajte sa vašom e-poštom umesto toga." in error_text

def test_login_click_forgot_password(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    register_link = wait.until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//a[@href="https://rs.primeshop360.com/moj-nalog/" and @title="Moj nalog" and contains(., "Prijavi / Registruj se")]'))
    )

    driver.execute_script("arguments[0].click();", register_link)

    forgot_password_link=wait.until(EC.element_to_be_clickable((By.XPATH,"//a[text()='Zaboravili ste šifru?']")))
    driver.execute_script("arguments[0].click();", forgot_password_link)

    element = driver.find_element(By.TAG_NAME, "p")
    text = element.text

    assert "Zaboravili ste lozinku? Upišite svoje korisničko ime ili adresu e-pošte. Primićete vezu za kreiranje nove lozinke putem e-pošte." in text,"Expected message isn't shown."

def test_prime_shop_click_whishlist_products_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    wishlist_products_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='Wishlist products']")))
    driver.execute_script("arguments[0].click();", wishlist_products_link)

    wishlist_products_heading=wait.until((EC.visibility_of_element_located((By.TAG_NAME, "p")))).text
    assert"Favoriti su prazni" in wishlist_products_heading, "Expected message isn't shown."

def test_prime_shop_click_cart_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    cart_link=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a[title='Korpa']")))
    driver.execute_script("arguments[0].click();", cart_link)

    empty_message = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.woocommerce-mini-cart__empty-message.empty.title"))).text
    assert "Nema proizvoda u korpi." == empty_message, "Expected empty cart message isn't shown."

def test_prime_shop_click_close_cart_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    cart_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='Korpa']")))
    driver.execute_script("arguments[0].click();", cart_link)

    close_cart_link=wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"Zatvori")))
    driver.execute_script("arguments[0].click();", close_cart_link)

def test_prime_shop_search_hair_dryer(driver):
    wait=WebDriverWait(driver, 30)

    search_input=wait.until(EC.visibility_of_element_located((By.NAME,"s")))
    search_input.click()
    search_input.send_keys("Fen za kosu")

    search_button=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"searchsubmit")))
    driver.execute_script("arguments[0].click();", search_button)

    search_result_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.wd-last"))).text
    assert "Rezultati pretrage za „Fen za kosu“" in search_result_text, "Expected search results message isn't shown."

def test_prime_shop_search_calma_pilow_add_to_cart(driver):
    login(driver)
    wait = WebDriverWait(driver, 30)
    actions=ActionChains(driver)


    search_input = wait.until(EC.visibility_of_element_located((By.NAME, "s")))
    search_input.click()
    search_input.send_keys("Kalma jastuk")

    search_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "searchsubmit")))
    driver.execute_script("arguments[0].click();", search_button)

    calma_infinity_item=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-id='17118']")))
    actions.move_to_element(calma_infinity_item).perform()

    add_item_to_cart=wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Dodaj u korpu']]")))
    driver.execute_script("arguments[0].click();", add_item_to_cart)



    # cart_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h2"))).text
    # assert"Ukupna vrednost korpe" in cart_heading, "Expected cart heading isn't shown."

    checkout_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.button.checkout.wc-forward")))

    assert checkout_button.text.upper() == "PLAĆANJE", "Dugme za plaćanje nije prikazano kako treba."
















