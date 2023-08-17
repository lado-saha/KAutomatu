import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from auth import logout_from_cga
from common import Prestation, NavigationUiState, PrestationState, Status, SubQueryField, SubStates, Subscriber, println

"""
    This is the page where we can type the decoder number and return the user details then click on the link to get
    the full details
"""


def launch_cga_prospect(driver: webdriver.Edge, wait: WebDriverWait, uis: NavigationUiState) -> bool:
    if not uis.is_cga_prospect_open:
        try:
            uis.cga_frame_title = wait.until(
                ec.visibility_of_element_located((By.NAME, 'titleFrame')))
            driver.switch_to.frame(uis.cga_frame_title)
            uis.page_cga_home = driver.current_window_handle
            driver.find_element(By.ID, 'ss').click()
            wait.until(ec.new_window_is_opened)
            uis.page_cga_prospect = driver.window_handles[-1]
            uis.is_cga_prospect_open = True
        except Exception as e:
            uis.error = e.__str__()
    driver.switch_to.window(uis.page_cga_prospect)
    return uis.is_cga_prospect_open


"""
    This is used to click on the subscriber_id and try to conclude it from the prospect 
    uses the decoder number
"""


def terminate_temp_from_cga(driver: webdriver.Edge, wait: WebDriverWait, uis: NavigationUiState,
                            subscriber: Subscriber) -> bool:
    launch_cga_prospect(driver, wait, uis)
    field = wait.until(ec.visibility_of_element_located((By.NAME, 'numdec')))
    field.clear()
    field.send_keys(subscriber.decoder_num)

    try:
        btn_search = driver.find_element(By.NAME, 'search')
        btn_search.click()
        table = wait.until(ec.visibility_of_element_located(
            (By.ID, 'subscriberDTABLE')))
        rows: list[any] = table.find_elements(By.TAG_NAME, "tr")[1:]
        rows.reverse()  # Reverse to get the latest data
        for row in rows:
            cells = [cell for cell in row.find_elements(By.TAG_NAME, 'td')]
            if cells[11].text != '':
                subscriber.sub_id = cells[0].text.strip()
                subscriber.name = cells[2].text.strip()
                subscriber.formula = cells[8].text.strip()
                subscriber.link = cells[0].find_element(By.TAG_NAME, 'a')
                break
        subscriber.link.click()

    except Exception as e:
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except Exception as ex:
            uis.error = e.__str__()
        subscriber.state = SubStates.NOT_FOUND
        return False

    driver.switch_to.window(uis.page_cga_home)

    uis.frame_cga_main = driver.find_element(By.NAME, 'cgaweb')
    driver.switch_to.frame(uis.frame_cga_main)
    uis.frame_cga_info = driver.find_element(By.NAME, '_right')
    driver.switch_to.frame(uis.frame_cga_info)

    driver.execute_script(
        "executeLink('/cgaweb/modsubscriberservice.do','','(*_*)Automatu',this); void(0);")
    # Dummy test just to make sure that the script continues and finishes its execution

    try:
        element = driver.find_element(
            By.XPATH, "//a[contains(@href, 'appelPostLink')]")
    except Exception as e:
        try:
            anteniste_table = driver.find_element(By.ID, 'ABOPRESTDTABLE')
            row = anteniste_table.find_elements(By.TAG_NAME, "tr")[1]
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells[4].text.strip() == 'Oui' or cells[4].text.strip() == 'Yes':
                subscriber.state = SubStates.VALIDATED
            else:
                subscriber.state = SubStates.CANCELLED
        except Exception as e1:
            subscriber.state = SubStates.NO_PRESTATION
        uis.error = "Deja Valider ou annuler ou non inserer."
        return False

    element.click()
    wait.until(ec.new_window_is_opened)
    uis.page_alonwa_closure = driver.window_handles[-1]
    driver.switch_to.window(uis.page_alonwa_closure)

    try:
        wait.until(ec.visibility_of_element_located((By.ID, 'INTER_REGUL')))
        check_box = driver.find_element(By.ID, "INTER_REGUL")
        driver.execute_script("arguments[0].removeAttribute('disabled')", check_box)
        check_box.click()

        tech_id_field = driver.find_element(By.ID, 'regul_inter_tech_regul')
        tech_id_field.send_keys(subscriber.tech_id)
        btn_ok = driver.find_element(By.ID, 'regul_btn_regul')
        btn_ok.click()

        btn_confirm = wait.until(ec.visibility_of_element_located(
            (By.XPATH, "//button[span[text()='Confirmer']]")))
        btn_confirm.click()
        subscriber.state = SubStates.WAS_SUCCESS_VALIDATED
        return True
    except Exception as exc:
        subscriber.state = SubStates.WAS_ERROR_VALIDATED
        return False


"""
    This is used to close the 'à qualifier', using a list of tech_ids provided
    Uses the sub_id
"""


def terminate_to_qualify_from_cga(driver: webdriver.Edge, wait: WebDriverWait, uis: NavigationUiState,
                                  subscriber: Subscriber, tech_ids: list[str]) -> bool:
    launch_cga_prospect(driver, wait, uis)
    sub_id_field = wait.until(
        ec.visibility_of_element_located((By.NAME, 'numabo')))
    sub_id_field.clear()
    sub_id_field.send_keys(subscriber.sub_id)
    try:
        btn_search = driver.find_element(By.NAME, 'search')
        btn_search.click()
        table = wait.until(ec.visibility_of_element_located(
            (By.ID, 'subscriberDTABLE')))
        rows: list[any] = table.find_elements(By.TAG_NAME, "tr")[1:]
        rows.reverse()  # Reverse to get the latest data
        for row in rows:
            cells = [cell for cell in row.find_elements(By.TAG_NAME, 'td')]
            if cells[11].text != '' and cells[0].text != '':
                subscriber.decoder_num = cells[11].text.strip()
                subscriber.name = cells[2].text.strip()
                subscriber.formula = cells[8].text.strip()
                subscriber.link = cells[0].find_element(By.TAG_NAME, 'a')
                break
        subscriber.link.click()
    except Exception as e:
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except Exception as ex:
            pass
        subscriber.state = SubStates.NOT_FOUND
        uis.error = e.__str__()
        return False

    driver.switch_to.window(uis.page_cga_home)

    uis.frame_cga_main = driver.find_element(By.NAME, 'cgaweb')
    driver.switch_to.frame(uis.frame_cga_main)
    uis.frame_cga_info = driver.find_element(By.NAME, '_right')
    driver.switch_to.frame(uis.frame_cga_info)
    driver.execute_script(
        "executeLink('/cgaweb/modsubscriberservice.do','','(*_*)Ngwan',this); void(0);")
    # Dummy test just to make sure that the script continues and finishes its execution

    try:
        driver.find_element(
            By.XPATH, "//a[contains(@href, 'appelPostLink')]").click()
    except Exception as e:
        try:
            anteniste_table = driver.find_element(By.ID, 'ABOPRESTDTABLE')
            row = anteniste_table.find_elements(By.TAG_NAME, "tr")[1]
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells[4].text.strip() == 'Oui' or cells[4].text.strip() == 'Yes':
                subscriber.state = SubStates.VALIDATED
            else:
                subscriber.state = SubStates.CANCELLED

        except Exception as e1:
            subscriber.state = SubStates.NO_PRESTATION

        return False

    wait.until(ec.new_window_is_opened)
    uis.page_alonwa_closure = driver.window_handles[-1]
    driver.switch_to.window(uis.page_alonwa_closure)

    try:
        wait.until(ec.visibility_of_element_located((By.ID, 'INTER_REGUL')))
        check_box = driver.find_element(By.ID, "INTER_REGUL")
        driver.execute_script("arguments[0].removeAttribute('disabled')", check_box)
        check_box.click()

        for i in range(0, len(tech_ids)):
            try:
                tech_id_field = driver.find_element(
                    By.ID, 'regul_inter_tech_regul')
                tech_id_field.clear()
                tech_id_field.send_keys(tech_ids[i].strip())
                btn_ok = driver.find_element(By.ID, 'regul_btn_regul')
                driver.execute_script('arguments[0].click();', btn_ok)
                time.sleep(0.5)
            except Exception as e:
                print(e)
                btn_confirm = driver.find_element(
                    By.XPATH,
                    '//button[@class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only" and '
                    'span[@class="ui-button-text" and text()="Confirmer"]]')
                driver.execute_script('arguments[0].click();', btn_confirm)
                subscriber.tech_id = tech_ids[i - 1]
                subscriber.state = SubStates.WAS_SUCCESS_VALIDATED
                return True
        uis.error = "No ID found"
        return False
    except Exception as exp:
        subscriber.state = SubStates.WAS_ERROR_VALIDATED
        return True


"""
    use phone numbers to get subscriber data
"""


def get_all_subscriber_data_from(driver: webdriver.Edge, uis: NavigationUiState, wait: WebDriverWait,
                                 all_subscribers: list[Subscriber], queries: list[str],
                                 query_field: SubQueryField) -> bool:
    launch_cga_prospect(driver, wait, uis)
    n = len(queries)
    i = 0
    k = 1

    for query in queries:
        i += 1
        subscribers: list[Subscriber] = []
        fail_sub = Subscriber(state=SubStates.NOT_FOUND)

        driver.switch_to.window(uis.page_cga_prospect)
        if query_field == SubQueryField.PHONE:
            fail_sub.phone = query
            field = wait.until(ec.visibility_of_element_located(
                (By.NAME, 'phonenumber')))
            field.clear()
            field.send_keys(f'00237{query}')
        elif query_field == SubQueryField.DECODER:
            fail_sub.decoder_num = query
            field = wait.until(
                ec.visibility_of_element_located((By.NAME, 'numdec')))
            field.clear()
            field.send_keys(query)
        else:
            fail_sub.sub_id = query
            field = wait.until(
                ec.visibility_of_element_located((By.NAME, 'numabo')))
            field.clear()
            field.send_keys(query)

        try:
            btn_search = driver.find_element(By.NAME, 'search')
            btn_search.click()
            table = wait.until(ec.visibility_of_element_located(
                (By.ID, 'subscriberDTABLE'))
            )
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]
            rows_cells = [row.find_elements(By.TAG_NAME, "td") for row in rows]

            for j in range(0, len(rows_cells)):
                temp_sub = Subscriber(
                    sub_id=rows_cells[j][0].text,
                    name=rows_cells[j][2].text,
                    formula=rows_cells[j][8].text,
                    decoder_num=rows_cells[j][11].text,
                    link=rows_cells[j][0].find_element(By.TAG_NAME, 'a')
                )
                if query_field == SubQueryField.PHONE:
                    temp_sub.phone = query
                subscribers.append(temp_sub)

            for subscriber in subscribers:
                # driver.switch_to.window(uis.page_cga_prospect)
                subscriber.link.click()
                driver.switch_to.window(uis.page_cga_home)
                uis.frame_cga_main = wait.until(
                    ec.visibility_of_element_located((By.NAME, 'cgaweb')))
                driver.execute_script(
                    "javascript:executeLink('/cgaweb/modaddress.do?todo=','Automatu', 'Adresse',this); void(0);")
                driver.switch_to.frame(uis.frame_cga_main)

                uis.frame_cga_title = wait.until(
                    ec.visibility_of_element_located((By.NAME, 'titleFrame')))
                uis.frame_cga_info = wait.until(
                    ec.visibility_of_element_located((By.NAME, '_right')))

                # Getting the phone number
                driver.switch_to.frame(uis.frame_cga_info)
                phone_table = driver.find_element(By.ID, 'tdmobile1')
                phone_cells = [cell for cell in phone_table.find_elements(By.TAG_NAME, 'input')]
                temp_phone_num = f"{phone_cells[1].get_attribute('value')}{phone_cells[2].get_attribute('value')}{phone_cells[3].get_attribute('value')}"
                print(temp_phone_num)
                subscriber.phone = temp_phone_num

                driver.switch_to.window(uis.page_alonwa_home)
                driver.switch_to.frame(uis.frame_cga_main)
                driver.switch_to.frame(uis.frame_cga_title)
                period = wait.until(
                    ec.visibility_of_element_located((By.XPATH, '//div[@id="period"]/b')))
                subscriber.date_period_str = period.text.strip()
                temp_phone_num = ''
                all_subscribers += subscribers
                println(
                    f"{i}/{n}: ({len(subscribers)}) trouve pour {query}", Status.SUCCESS)
                k += 1
        except Exception as e:
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except Exception as ex:
                pass
            all_subscribers.append(fail_sub)
            uis.error = f'{query} not found'
            println(f"{i}/{n}: aucun trouve pour {query}", Status.FAILED)

    println(f"Terminer avec {k}/{n} trouver", Status.SUCCESS)
    logout_from_cga(driver, wait, uis)
    return True


"""
    This uses the decoder numbers to find the corresponding antennist code.
"""


def cga_get_state_of_prestation_from_decoders(driver: webdriver.Edge, wait: WebDriverWait, uis: NavigationUiState,
                                              decoders: list[str], prestations: list[Prestation]) -> bool:
    i = 0
    n = len(decoders)
    for decoder_num in decoders:
        i += 1
        prestation = Prestation(decoder_num=decoder_num)
        launch_cga_prospect(driver, wait, uis)
        subscriber_field = wait.until(
            ec.visibility_of_element_located((By.NAME, 'numdec')))
        subscriber_field.clear()
        subscriber_field.send_keys(decoder_num)
        try:
            btn_search = driver.find_element(By.NAME, 'search')
            btn_search.click()
            table = wait.until(ec.visibility_of_element_located(
                (By.ID, 'subscriberDTABLE')))
            row = table.find_elements(By.TAG_NAME, "tr")[-1]
            sub_cells = row.find_elements(By.TAG_NAME, "td")
            link = sub_cells[0].find_element(By.TAG_NAME, 'a')
            prestation.sub_id = sub_cells[0].text
            link.click()
        except Exception as e:
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except Exception as ex:
                pass
            prestation.state = PrestationState.UNKNOWN_DECODER
            println(f"{i}/{n}: Decodeur Inconnu", Status.FAILED)
            prestations.append(prestation)
            continue

        driver.switch_to.window(uis.page_cga_home)
        uis.frame_cga_main = driver.find_element(By.NAME, 'cgaweb')
        driver.switch_to.frame(uis.frame_cga_main)
        uis.frame_cga_info = driver.find_element(By.NAME, '_right')
        driver.switch_to.frame(uis.frame_cga_info)

        driver.execute_script(
            "executeLink('/cgaweb/modsubscriberservice.do','','(*_*)Ngwan',this); void(0);")
        # Dummy test just to make sure that the script continues and finishes its execution

        try:
            prestation_table = driver.find_element(By.ID, 'ABOPRESTDTABLE')
        except Exception as e:
            prestation.state = PrestationState.NO_PRESTATION
            println(f"{i}/{n}: Aucune prestation trouvé", Status.FAILED)
            prestations.append(prestation)
            continue

        row = prestation_table.find_elements(By.TAG_NAME, "tr")[1]
        cells = row.find_elements(By.TAG_NAME, "td")
        prestation.tech_cga_ref = cells[3].text.strip()
        if cells[4].text.strip() == 'Oui' or cells[4].text.strip() == 'Yes':
            prestation.state = PrestationState.VALIDATED
        else:
            prestation.state = PrestationState.CANCELLED
        prestations.append(prestation)
        println(f"{i}/{n}: Prestation trouvé", Status.SUCCESS)

    println("Terminer", Status.SUCCESS)
    logout_from_cga(driver, wait, uis)
    return True
