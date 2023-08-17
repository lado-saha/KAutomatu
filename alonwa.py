import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from auth import logout_from_alonwa, logout_from_cga
from cga import terminate_temp_from_cga, terminate_to_qualify_from_cga
from common import NavigationUiState, Status, Subscriber, println, InterventionState
from date_ui_state import DataUiState

"""
    termination of temporary interventions
"""


def get_subs_phones_from_subs_ids(
        driver: webdriver.Edge,
        wait: WebDriverWait,
        uis: NavigationUiState,
        all_subs: list[Subscriber],
        sub_ids: list[str],
        d_uis: DataUiState
) -> bool:
    current_month = datetime.date.today().month
    # waiting and navigating to the intervention page where we can see all the pending interventions
    menu_intervention = wait.until(ec.visibility_of_element_located(
        (By.XPATH, "//li/a[@href='https://serviceplus.canal-plus.com/index.php?action=INTER_PENDING']"))
    )
    menu_intervention.click()
    # Setting to show 100 intervention per page
    driver.find_element(
        By.XPATH, "//select[@name='tbl_inter_pending_length']/option[last()]").click()
    wait.until_not(ec.visibility_of_element_located((By.ID, 'tbl_inter_pending_processing')))

    if d_uis.month_start != current_month:
        set_start_date(driver, wait, d_uis.month_start)

    int_states = (InterventionState.TO_PLANIFY, InterventionState.TO_QUALIFY, InterventionState.TERMINATED_OK,
                  InterventionState.VALIDATED)
    n = len(sub_ids)
    for i, sub_id in enumerate(sub_ids):
        println(f"{i + 1} sur {n}: Recherche du Tel pour l'abonné '{sub_id}'", Status.LOADING)
        is_found = False
        subscriber = Subscriber(sub_id=sub_id)
        for state in int_states:
            # Clicking the menu option inorder to get the temporary interventions
            menu_intervention_type = wait.until(ec.visibility_of_element_located(
                (By.ID, "intervention_status_select-button")))
            menu_intervention_type.click()
            temp_menu_opt = driver.find_element(By.ID, state.menu_item)
            temp_menu_opt.click()

            while True:
                # Wait until the loading bar disappear and then Waiting till the table is fully loaded to select it
                wait.until_not(ec.visibility_of_element_located((By.ID, 'tbl_inter_pending_processing')))
                table = driver.find_element(By.ID, 'tbl_inter_pending')
                all_rows = table.find_elements(By.XPATH, f".//tr[td[5]//span[contains(text(), '{sub_id}')]]")
                println(f'{state.value}Found{len(all_rows)}')
                if len(all_rows) != 0:
                    title = (all_rows[-1].find_element(By.XPATH, ".//td[5]")
                    .find_element(By.XPATH, ".//span").get_attribute(
                        'title'
                    ))
                    subscriber.phone = title.split('-')[-1].strip()
                    is_found = True
                    break
                else:
                    btn_next = driver.find_element(By.ID, 'tbl_inter_pending_next')
                    if 'ui-state-disabled' in btn_next.get_attribute('class'):
                        break
                    else:
                        btn_next.click()

            if is_found:
                break
        all_subs.append(subscriber)
        if is_found:
            println(f"{all_subs[-1].phone}", Status.SUCCESS)
        else:
            println(f"Aucun résultat", Status.FAILED)
    logout_from_alonwa(driver, wait, uis)
    println("Terminé!", Status.SUCCESS)
    return True


def set_start_date(driver: webdriver.Edge, wait: WebDriverWait, start: int):
    start_date = driver.find_element(By.ID, 'intervention_from_datecrea')
    start_date.click()
    calendar = driver.find_element(By.CLASS_NAME, 'ui-datepicker-calendar')
    first_day = calendar.find_element(By.XPATH, ".//td[a[contains(text(), '1')]]")

    while int(first_day.get_attribute('data-month')) + 1 > start:
        driver.find_element(By.CSS_SELECTOR,"a.ui-datepicker-prev.ui-corner-all").click()
        calendar = driver.find_element(By.CLASS_NAME, 'ui-datepicker-calendar')
        first_day = calendar.find_element(By.XPATH, ".//td[a[contains(text(), '1')]]")

    first_day.click()
    driver.find_element(By.ID, 'btn_period_valid').click()
    wait.until_not(ec.visibility_of_element_located((By.ID, 'tbl_inter_pending_processing')))


def terminate_temp_in_alonwa(
        driver: webdriver.Edge,
        wait: WebDriverWait,
        month: int,
        uis: NavigationUiState,
        all_subs: list[Subscriber],
        cga_driver: webdriver.Edge,
        cga_wait: WebDriverWait,
        max_operations: int = None
) -> bool:
    current_month = datetime.date.today().month
    # waiting and navigating to the intervention page where we can see all the pending interventions
    menu_intervention = wait.until(ec.visibility_of_element_located(
        (By.XPATH, "//li/a[@href='https://serviceplus.canal-plus.com/index.php?action=INTER_PENDING']"))
    )
    menu_intervention.click()

    # Clicking the menu option inorder to get the temporary interventions
    menu_intervention_type = wait.until(ec.visibility_of_element_located(
        (By.ID, "intervention_status_select-button")))
    menu_intervention_type.click()
    temp_menu_opt = driver.find_element(By.ID, 'ui-id-7')
    temp_menu_opt.click()

    # Setting to show 100 intervention per page
    driver.find_element(
        By.XPATH, "//select[@name='tbl_inter_pending_length']/option[last()]").click()

    # Wait until the loading bar disappear and then Waiting till the table is fully loaded to select it
    wait.until_not(ec.visibility_of_element_located(
        (By.ID, 'tbl_inter_pending_processing')))
    table = wait.until(ec.visibility_of_element_located(
        (By.ID, 'tbl_inter_pending')))

    # All the rows of intervention data except the 2 first rows which are just meta data
    all_rows = table.find_elements(By.TAG_NAME, "tr")[2:]
    # A matrix of cells for each row
    all_rows_cells = [row.find_elements(By.TAG_NAME, "td") for row in all_rows]
    # A matrix of all links to get the
    all_links = [cells[10].find_element(
        By.TAG_NAME, 'a') for cells in all_rows_cells]
    links = {}
    # Will contain filtered link objects such that there is no repetition. This is because many technicians can appear
    for link in all_links:
        links[link.text] = link
    uis.page_alonwa_interventions = driver.current_window_handle

    # For each link, we click and get the tech id from profile then navigate to the planning of the technician

    i = 1
    num_tech = len(links.values())
    println(f"{num_tech}")

    println(f"Nombre total de Technicien = {num_tech}", Status.SUCCESS)
    if not (max_operations is None or max_operations > num_tech):
        num_tech = max_operations
    println(f"Nombre a traiter = {num_tech}", Status.SUCCESS)

    for link in links.values():
        link.click()
        wait.until(ec.new_window_is_opened)
        uis.page_alonwa_tech_profile = driver.window_handles[-1]
        driver.switch_to.window(uis.page_alonwa_tech_profile)
        tech_id = driver.find_element(By.ID, 'ID_TECH').text
        tech_name = driver.find_element(By.ID, 'NOM').text

        println(f"{i}/{num_tech}: [Nom = {tech_name}, Tech ID = {tech_id}]")

        # Find and click on the see planning button for navigation then wait for the loading spinner to dissapear
        form = driver.find_elements(
            By.XPATH, "//form[@action='https://serviceplus.canal-plus.com/index.php']")[-1]
        form.submit()
        wait.until_not(ec.visibility_of_element_located(
            (By.ID, 'dialog_loader'))
        )
        for k in range(month, current_month):
            btn_prev = driver.find_element(By.CLASS_NAME, 'fc-button-prev')
            btn_prev.click()
            wait.until_not(ec.visibility_of_element_located(
                (By.ID, 'dialog_loader')))

        uis.page_alonwa_tech_planning = driver.current_window_handle

        # Get all the events then only keep ones which are temporary only. A temporary event does not have a complete id
        # E.g Complete is "INTERVENTION: 21478798218" while incomplete is "INTERVENTION"

        all_events = driver.find_elements(
            By.XPATH, "//div[@class='fc-event fc-event-hori fc-event-start fc-event-end']")
        for event in all_events:
            text = event.find_element(By.CLASS_NAME, 'fc-event-title').text
            # For each incomplete event we get to the details page and copy the decoder number if it exists else we skip
            if text.strip() == 'INTERVENTION':
                event.click()
                wait.until(ec.new_window_is_opened)
                uis.page_alonwa_intervention_details = driver.window_handles[-1]
                driver.switch_to.window(uis.page_alonwa_intervention_details)
                wait.until(ec.visibility_of_element_located(
                    (By.ID, 'ui-id-11')))
                subscriber = Subscriber()
                try:
                    subscriber = Subscriber(
                        tech_id=tech_id,
                        decoder_num=driver.find_element(By.ID, 'ref_decodeur0').get_attribute('value').strip(),
                    )
                    status = terminate_temp_from_cga(cga_driver, cga_wait, uis, subscriber)
                    if status:
                        println(f"{subscriber.decoder_num}: cloturé", Status.SUCCESS)
                    else:
                        println(
                            f"{subscriber.decoder_num}: non cloturé (valider, annuler ou inconnu)", Status.FAILED)
                except Exception as e:
                    println(str(e), Status.FAILED)
                    println(
                        f"Compte rendu incomplet, pas de numero decodeur", Status.FAILED)
                all_subs.append(subscriber)
                driver.close()
                driver.switch_to.window(uis.page_alonwa_tech_planning)
        driver.close()
        driver.switch_to.window(uis.page_alonwa_interventions)
        i += 1
        if i == num_tech:
            break
    logout_from_alonwa(driver, wait, uis)
    logout_from_cga(cga_driver, cga_wait, uis)
    println(f"{num_tech} clotures du mois {month} terminés")
    return True


"""
    Termination of a to qualify
"""


def terminate_qualify_from_alonwa(driver: webdriver.Edge, wait: WebDriverWait, uis: NavigationUiState,
                                  all_subs: list[Subscriber], cga_driver: webdriver.Edge, cga_wait: WebDriverWait,
                                  tech_ids: list[str], max: int | None) -> bool:
    # waiting and navigating to the intervention page where we can see all the pending interventions
    menu_intervention = wait.until(ec.visibility_of_element_located(
        (By.XPATH, "//li/a[@href='https://serviceplus.canal-plus.com/index.php?action=INTER_PENDING']")))
    uis.is_login_alonwa = True
    menu_intervention.click()

    # Clicking the menu option inorder to get the temporary interventions
    menu_intervention_type = wait.until(ec.visibility_of_element_located(
        (By.ID, "intervention_status_select-button")))
    menu_intervention_type.click()
    to_qualify_menu_option = driver.find_element(By.ID, 'ui-id-4')
    to_qualify_menu_option.click()

    # Setting to show 100 intervention per page
    driver.find_element(
        By.XPATH, "//select[@name='tbl_inter_pending_length']/option[last()]").click()

    # Wait until the loading bar disappear and then Waiting till the table is fully loaded to select it
    wait.until_not(ec.visibility_of_element_located(
        (By.ID, 'tbl_inter_pending_processing')))
    table = wait.until(ec.visibility_of_element_located(
        (By.ID, 'tbl_inter_pending')))

    # All the rows of intervention data except the 2 first rows which are just meta data
    # we get the reference ids
    all_rows = table.find_elements(By.TAG_NAME, "tr")[2:]
    # A matrix of cells for each row
    all_rows_cells = [row.find_elements(By.TAG_NAME, "td") for row in all_rows]
    subscriber_ids = [cells[4].text.strip() for cells in all_rows_cells]

    uis.page_alonwa_interventions = driver.current_window_handle

    num_subs = len(subscriber_ids)
    println(f"Nombre total de Interventions = {num_subs}", Status.SUCCESS)

    if not (max is None or max > num_subs):
        num_subs = max
    println(f"Nombre a traiter = {num_subs}", Status.SUCCESS)

    k = 1

    # For each link, we click and get the tech id from profile then navigate to the planning of the technician
    for i in range(0, num_subs):
        subscriber = Subscriber(
            sub_id=subscriber_ids[i]
        )
        println(f"{i + 1}/{num_subs}: [Abonné = {subscriber.sub_id}]")
        status = terminate_to_qualify_from_cga(
            cga_driver, cga_wait, uis, subscriber, tech_ids)
        if status:
            k += 1
            println(
                f"Cloturer avec l'id = {subscriber.tech_id}", Status.SUCCESS)
        else:
            println(f"Aucun Id trouver pour cloturer", Status.FAILED)
        all_subs.append(subscriber)

    logout_from_alonwa(driver, wait, uis)
    logout_from_cga(cga_driver, cga_wait, uis)
    println(f"{k}/{num_subs} Cloturer", Status.SUCCESS)

    return True
