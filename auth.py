import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from common import NavigationUiState, Status, println, CGAAccount, AlonwaAccount

LOGIN_CGA_URL = 'https://cgaweb-afrique.canal-plus.com/cgaweb/'
LOGIN_ALONWA_URL = 'https://serviceplus.canal-plus.com/'


def login_to_cga(
        driver: webdriver.Edge,
        wait: WebDriverWait,
        account: CGAAccount,
        uis: NavigationUiState
) -> bool:
    if not uis.is_login_cga:
        try:
            println(f"Connexion entant que {account.name} sur CGA {account.region}", Status.LOADING)
            driver.get(LOGIN_CGA_URL)
            iframe = driver.find_element(By.NAME, 'cgaweb')
            driver.switch_to.frame(iframe)
            username_field = driver.find_element(By.ID, 'cuser')
            username_field.send_keys(account.name)
            password_field = driver.find_element(By.ID, 'pass')
            password_field.send_keys(account.password)
            # Find the login button and click it
            login_button = driver.find_element(By.NAME, 'login')
            login_button.click()
            wait.until(ec.visibility_of_element_located((By.NAME, 'titleFrame')))
            uis.page_cga_home = driver.current_window_handle
            uis.is_login_cga = True
            println(f"Connecté", Status.SUCCESS)
        except Exception as e:
            uis.error = e
            println(f"Connexion Impossible. Verifiez votre login et/ou votre connexion Internet", Status.FAILED)
    else:
        println(f"Deja connecté", Status.SUCCESS)
    return uis.is_login_cga


def logout_from_cga(
        driver: webdriver.Edge,
        wait: WebDriverWait,
        uis: NavigationUiState
) -> bool:
    if uis.is_login_cga:
        try:
            println(f"Déconnexion du CGA", Status.LOADING)
            driver.switch_to.window(uis.page_cga_home)
            iframe = driver.find_element(By.NAME, 'cgaweb')
            driver.switch_to.frame(iframe)
            script = "parent.location='/cgaweb/servlet/cgaweb.servlet.DeconnexionServlet';"
            driver.execute_script(script)
            driver.switch_to.window(uis.page_cga_home)
            # In case our account becomes locked
            btn_logout = wait.until(ec.visibility_of_element_located((By.NAME, 'logout')))
            btn_logout.click()
            println(f"Déconnexion", Status.SUCCESS)
        except Exception as e:
            println(f"Deconnexion Impossible", Status.FAILED)
            uis.error = e

    return True


def logout_from_alonwa(
        driver: webdriver.Edge,
        wait: WebDriverWait,
        uis: NavigationUiState,
) -> bool:
    if uis.is_login_cga:
        println(f"Déconnexion de CANAL+ ALONWA", Status.LOADING)
        try:
            driver.switch_to.window(uis.page_alonwa_home)
            link = driver.find_element(
                by=By.XPATH,
                value='//a[@class="href_deco" and @href="https://serviceplus.canal-plus.com/index.php?action=LOGOUT"]')
            link.click()
            wait.until(ec.visibility_of_element_located((By.ID, 'in_username')))
            println(f"Déconnexion", Status.SUCCESS)
        except Exception as e:
            uis.error = e
    return True


def login_to_alonwa(
        driver: webdriver.Edge,
        wait: WebDriverWait,
        account: AlonwaAccount,
        uis: NavigationUiState,
) -> bool:
    if not uis.is_login_alonwa:
        println(f"Connexion entant que {account.name} sur Service plus {account.region}", Status.LOADING)
        try:
            driver.get(LOGIN_ALONWA_URL)
            username_field = driver.find_element(By.ID, 'in_username')
            username_field.send_keys(account.name)
            password_field = driver.find_element(By.ID, 'in_password')
            password_field.send_keys(account.password)
            login_button = driver.find_element(By.CLASS_NAME, "submit")
            login_button.click()
            wait.until(ec.visibility_of_element_located((By.ID, 'home_header')))
            uis.page_alonwa_home = driver.current_window_handle
            uis.is_login_alonwa = True
            println(f"Connecté", Status.SUCCESS)
        except Exception as e:
            println(f"Connexion Impossible. Verifiez votre login et/ou votre connexion Internet", Status.FAILED)
            uis.error = e
    else:
        println(f"Deja connecté", Status.SUCCESS)
    return uis.is_login_alonwa
