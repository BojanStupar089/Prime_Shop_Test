import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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
    user_name.send_keys("Bojan09")

    email_input=wait.until(EC.visibility_of_element_located((By.ID,"reg_email")))
    email_input.send_keys("bojanstupar089+test14@gmail.com")

    password_input=wait.until(EC.visibility_of_element_located((By.ID,"reg_password")))
    password_input.send_keys("Celarevo44!")

    register_button=wait.until(EC.visibility_of_element_located((By.NAME,"register")))
    driver.execute_script("arguments[0].click();", register_button)


    username_span = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.wd-tools-text"))
    ).text.strip().upper()

    assert "ZDRAVO, MILE81" in username_span,"The username is not expexted."

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



    assert not email_input.get_property("validity")["valid"], f"The email input shouldn't be valid."

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
    accept_cookies(driver)
    wait=WebDriverWait(driver, 30)

    search_input=wait.until(EC.visibility_of_element_located((By.NAME,"s")))
    search_input.click()
    search_input.send_keys("Fen za kosu")

    search_button=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"searchsubmit")))
    driver.execute_script("arguments[0].click();", search_button)

    search_result_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.wd-last"))).text
    assert "Rezultati pretrage za „Fen za kosu“" in search_result_text, "Expected search results message isn't shown."

def test_prime_shop_search_calma_pillow_add_to_cart(driver):
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

    checkout_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.button.checkout.wc-forward")))

    assert checkout_button.text.upper() == "PLAĆANJE", "Dugme za plaćanje nije prikazano kako treba."

def test_prime_shop_search_calma_pillow_add_and_remove_to_cart(driver):
    login(driver)
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    search_input = wait.until(EC.visibility_of_element_located((By.NAME, "s")))
    search_input.click()
    search_input.send_keys("Kalma jastuk")

    search_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "searchsubmit")))
    driver.execute_script("arguments[0].click();", search_button)

    calma_infinity_item = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-id='17118']")))
    actions.move_to_element(calma_infinity_item).perform()

    add_item_to_cart = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Dodaj u korpu']]")))
    driver.execute_script("arguments[0].click();", add_item_to_cart)

    remove_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "remove_from_cart_button")))


    remove_button.click()

    empty_cart_msg = wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "woocommerce-mini-cart__empty-message")
    )).text

    assert "Nema proizvoda u korpi." in empty_cart_msg, f"Expected empty cart message not found. Actual message:'{empty_cart_msg}'"

def test_prime_shop_my_account_click_my_orders_item(driver):
    login(driver)
    wait=WebDriverWait(driver, 30)
    actions=ActionChains(driver)

    my_account_hover=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='Moj nalog']")))
    actions.move_to_element(my_account_hover).perform()

    my_order=wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Narudžbine']]")))
    driver.execute_script("arguments[0].click();", my_order)

    info_div = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "woocommerce-info")))
    expected_text = "Još nije plasirana nijedna narudžbina."

    assert expected_text in info_div.text, f"Expected text not found. Actual text: {info_div.text}"

def test_prime_shop_my_account_click_favorites_item(driver):

    login(driver)

    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    my_account_hover = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='Moj nalog']")))
    actions.move_to_element(my_account_hover).perform()

    my_favorites = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Favoriti']]")))
    driver.execute_script("arguments[0].click();", my_favorites)

    my_favorites_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Favoriti" in my_favorites_heading, "Expected Kontakt header isn't shown."

def test_prime_shop_fill_account_details_form_from_my_account(driver):
    login(driver)

    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    my_account_hover = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='Moj nalog']")))
    actions.move_to_element(my_account_hover).perform()

    account_details = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Detalji naloga']]")))
    driver.execute_script("arguments[0].click();", account_details)

    phone_input=wait.until(EC.visibility_of_element_located((By.NAME,"billing_phone")))
    phone_input.clear()
    phone_input.send_keys("123456")

    first_name_input=wait.until(EC.visibility_of_element_located((By.NAME,"account_first_name")))
    first_name_input.clear()
    first_name_input.send_keys("Bojan")

    last_name_input=wait.until(EC.visibility_of_element_located((By.NAME,"account_last_name")))
    last_name_input.clear()
    last_name_input.send_keys("Stupar")

    save_button=wait.until(EC.visibility_of_element_located((By.XPATH,"//button[text()='Sačuvaj promene']")))
    driver.execute_script("arguments[0].click();", save_button)

def test_prime_shop_hover_category_click_home_and_garden_link(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    actions=ActionChains(driver)

    category_hover=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"menu-open-label")))
    actions.move_to_element(category_hover).perform()

    category_click=wait.until(EC.visibility_of_element_located((By.XPATH,"//a[span[text()='Dom i vrt']]")))
    driver.execute_script("arguments[0].click();", category_click)

    hag_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Dom i vrt" in hag_heading, "Expected Kontakt header isn't shown."

def test_prime_shop_hover_category_click_cleaning_link_sort_products_by_price_ascending(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    category_hover = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "menu-open-label")))
    actions.move_to_element(category_hover).perform()

    category_click = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Čišćenje']]")))
    driver.execute_script("arguments[0].click();", category_click)

    dropdown = Select(driver.find_element(By.NAME, "orderby"))
    dropdown.select_by_value("popularity")
    time.sleep(0.5)
    dropdown.select_by_value("price")

    selected_option = dropdown.first_selected_option
    assert selected_option.get_attribute("value") == "price", "Expected selected option  isn't selected."

def test_prime_shop_click_store_link_and_sort_products_by_newest(driver):
    accept_cookies(driver)
    wait=WebDriverWait(driver, 30)

    store_link=wait.until(EC.visibility_of_element_located((By.XPATH,"//a[span[text()='Prodavnica']]")))
    driver.execute_script("arguments[0].click();", store_link)

    dropdown = Select(driver.find_element(By.NAME, "orderby"))
    dropdown.select_by_value("popularity")
    time.sleep(0.5)
    dropdown.select_by_value("date")

def test_prime_shop_click_store_link_filter_products_by_price_below_60000(driver):

    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    store_link = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Prodavnica']]")))
    driver.execute_script("arguments[0].click();", store_link)

    handles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-slider-handle")))

    right_handle = handles[1]

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", right_handle)

    actions = ActionChains(driver)
    actions.click_and_hold(right_handle).move_by_offset(-70, 0).release().perform()


    filter_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".price_slider_amount .button")))
    filter_button.click()


    max_price_value = wait.until(EC.presence_of_element_located((By.ID, "max_price"))).get_attribute("value")
    assert int(max_price_value) < 60000, f"The maximum price wasn't reduced; it's still{max_price_value}."

def test_prime_shop_click_store_link_fileter_products_on_discount(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    store_link = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Prodavnica']]")))
    driver.execute_script("arguments[0].click();", store_link)

    discount_check=wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"Na popustu")))
    driver.execute_script("arguments[0].click();", discount_check)

def test_prime_shop_click_contact_link_and_show_contact_page(driver):

    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    contact_link = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Kontakt']]")))
    driver.execute_script("arguments[0].click();", contact_link)

    contact_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Kontakt" in contact_heading, "Expected Kontakt header isn't shown."

def test_prime_shop_click_catalog_link_and_show_catalog_page(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    catalog_link = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Katalog']]")))
    driver.execute_script("arguments[0].click();", catalog_link)

    catalog_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Katalog" in catalog_heading, "Expected Kontakt header isn't shown."

def test_prime_shop_click_family_card_discount_and_show_page(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)
    wait = WebDriverWait(driver, 30)

    fcd_link = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Family card popust']]")))
    driver.execute_script("arguments[0].click();", fcd_link)

    fcd_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Family card" in fcd_heading, "Expected Kontakt header isn't shown."

def test_prime_shop_click_kalma_link_and_show_kalma_products(driver):
    accept_cookies(driver)

    wait = WebDriverWait(driver, 30)

    kalma_link=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='Kalma Home']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", kalma_link)
    driver.execute_script("arguments[0].click();", kalma_link)

    kalma_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Kalma Home")))
    assert "Kalma Home" in kalma_link.text, f"Expected 'Kalma Home' in link text, but got: '{kalma_link.text}'"

def test_prime_shop_click_royalty_line_link_and_show_royalty_line_products(driver):
    accept_cookies(driver)
    wait = WebDriverWait(driver, 30)

    royalty_line_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='Royalty Line']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", royalty_line_link)
    driver.execute_script("arguments[0].click();", royalty_line_link)

    royalty_line_heading = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Royalty Line"))).text
    assert "Royalty Line" in royalty_line_heading, f"Expected 'Royalty Line' in link text, but got: '{royalty_line_heading}'"


def test_prime_shop_click_facebook_link(driver):
    wait = WebDriverWait(driver, 30)

    facebook_link=wait.until(EC.visibility_of_element_located(((By.LINK_TEXT, "Facebook"))))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", facebook_link)
    driver.execute_script("arguments[0].click();", facebook_link)

def test_prime_shop_click_instagram_link(driver):
    wait = WebDriverWait(driver, 30)

    instagram_link= wait.until(EC.visibility_of_element_located(((By.LINK_TEXT, "Instagram"))))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", instagram_link)
    driver.execute_script("arguments[0].click();", instagram_link)

def test_prime_shop_logout(driver):
    login(driver)

    wait = WebDriverWait(driver, 30)
    actions = ActionChains(driver)

    my_account_hover = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[title='Moj nalog']")))
    actions.move_to_element(my_account_hover).perform()

    account_details = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='Odjavi se']]")))
    driver.execute_script("arguments[0].click();", account_details)

    expected_text = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "wd-tools-text"))).text
    assert "PRIJAVI / REGISTRUJ SE" in expected_text, f"Expected text it's not good."



























