import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from auth import logout_from_alonwa, logout_from_cga
from cga import terminate_temp_from_cga, terminate_to_qualify_from_cga
from common import Prestation, NavigationUiState, Status, Subscriber, UserLogin, gen_qualifier_termination_report, println

"""
    termination of temporary interventions
"""


def terminate_temp_in_alonwa(
    driver: webdriver.Edge,
    wait: WebDriverWait,
    month: int,
    uis: NavigationUiState,
    all_subs: list[Subscriber],
    cga_driver: webdriver.Edge,
    cga_wait: WebDriverWait,
    max: int | None = None
) -> bool:
    current_month = datetime.date.today().month
    # waiting and navigating to the intervention page where we can see all the pending interventions
    menu_intervention = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//li/a[@href='https://serviceplus.canal-plus.com/index.php?action=INTER_PENDING']"))
    )
    uis.is_login_alonwa = True
    menu_intervention.click()

    # Clicking the menu option inorder to get the temporary interventions
    menu_intervention_type = wait.until(EC.visibility_of_element_located(
        (By.ID, "intervention_status_select-button")))
    menu_intervention_type.click()
    temp_menu_opt = driver.find_element(By.ID, 'ui-id-7')
    temp_menu_opt.click()

    # Setting to show 100 intervention per page
    driver.find_element(
        By.XPATH, "//select[@name='tbl_inter_pending_length']/option[last()]").click()

    # Wait until the loading bar disappear and then Waiting till the table is fully loaded to select it
    wait.until_not(EC.visibility_of_element_located(
        (By.ID, 'tbl_inter_pending_processing')))
    table = wait.until(EC.visibility_of_element_located(
        (By.ID, 'tbl_inter_pending')))

    # All the rows of intervention data except the 2 first rows which are just meta data
    all_rows = table.find_elements(By.TAG_NAME, "tr")[2:]
    # A matrix of cells for each row
    all_rows_cells = [row.find_elements(By.TAG_NAME, "td") for row in all_rows]
    # A matrix of all links to get the
    all_links = [cells[10].find_element(
        By.TAG_NAME, 'a') for cells in all_rows_cells]
    links = {}  # Will contain filtered link objects such that there is no repetition. This is because many technicians can appear
    for link in all_links:
        links[link.text] = link
    uis.page_alonwa_interventions = driver.current_window_handle

    # For each link, we click and get the tech id from profile then navigate to the planning of the technician
    
    i = 1
    num_tech = len(links.values())
    println(f"{num_tech}")

    
    println(f"Nombre total de Technicien = {num_tech}", Status.SUCCESS)
    if not (max is None or max > num_tech):
        num_tech = max
    println(f"Nombre a traiter = {num_tech}", Status.SUCCESS)

    for link in links.values():
        link.click()
        wait.until(EC.new_window_is_opened)
        uis.page_alonwa_tech_profile = driver.window_handles[-1]
        driver.switch_to.window(uis.page_alonwa_tech_profile)
        tech_id = driver.find_element(By.ID, 'ID_TECH').text
        tech_name = driver.find_element(By.ID, 'NOM').text

        println(f"{i}/{num_tech}: [Nom = {tech_name}, Tech ID = {tech_id}]")
        

        # Find and click on the see planning button for navigation then wait for the loading spinner to dissapear
        form = driver.find_elements(
            By.XPATH, "//form[@action='https://serviceplus.canal-plus.com/index.php']")[-1]
        form.submit()
        wait.until_not(EC.visibility_of_element_located(
            (By.ID, 'dialog_loader'))
        )
        for k in range(month, current_month):
            btn_prev = driver.find_element(By.CLASS_NAME, 'fc-button-prev')
            btn_prev.click()
            wait.until_not(EC.visibility_of_element_located(
                (By.ID, 'dialog_loader')))
        uis.page_alonwa_tech_planning = driver.current_window_handle

        # Get all the events then only keep ones which are temporary only. A temporary event does not have a complete id
        # E.g Complete is "INTERVENTION: 21478798218" while incomplete is "INTERVENTION"

        all_events = driver.find_elements(
            By.XPATH, "//div[@class='fc-event fc-event-hori fc-event-start fc-event-end']")
        for event in all_events:

            text = event.find_element(By.CLASS_NAME, 'fc-event-title').text
            # For each incomplete event we get to the details page and copy the decoder number if it exists else we skip
            if (text.strip() == 'INTERVENTION'):
                event.click()
                wait.until(EC.new_window_is_opened)
                uis.page_alonwa_intervention_details = driver.window_handles[-1]
                driver.switch_to.window(uis.page_alonwa_intervention_details)
                wait.until(EC.visibility_of_element_located(
                    (By.ID, 'ui-id-11')))

                try:
                    subscriber = Subscriber(
                        tech_id=tech_id,
                        decoder_num=driver.find_element(
                            By.ID, 'ref_decodeur0').get_attribute('value').strip(),
                    )
                    status = terminate_temp_from_cga(
                        cga_driver, cga_wait, uis, subscriber)
                    if status:
                        println(f"{subscriber.decoder_num}: cloturé",
                                Status.SUCCESS)
                    else:
                        println(
                            f"{subscriber.decoder_num}: non cloturé (valider, annuler ou inconnu)", Status.FAILED)
                except Exception as e:
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


def terminate_qualify_from_alonwa(driver: webdriver.Edge, wait: WebDriverWait, uis: NavigationUiState, all_subs: list[Subscriber], cga_driver: webdriver.Edge,  cga_wait: WebDriverWait, tech_ids: list[str], max: int | None) -> list[Subscriber]:
    # waiting and navigating to the intervention page where we can see all the pending interventions
    menu_intervention = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//li/a[@href='https://serviceplus.canal-plus.com/index.php?action=INTER_PENDING']")))
    uis.is_login_alonwa = True
    menu_intervention.click()

    # Clicking the menu option inorder to get the temporary interventions
    menu_intervention_type = wait.until(EC.visibility_of_element_located(
        (By.ID, "intervention_status_select-button")))
    menu_intervention_type.click()
    to_qualify_menu_option = driver.find_element(By.ID, 'ui-id-4')
    to_qualify_menu_option.click()

    # Setting to show 100 intervention per page
    driver.find_element(
        By.XPATH, "//select[@name='tbl_inter_pending_length']/option[last()]").click()

    # Wait until the loading bar disappear and then Waiting till the table is fully loaded to select it
    wait.until_not(EC.visibility_of_element_located(
        (By.ID, 'tbl_inter_pending_processing')))
    table = wait.until(EC.visibility_of_element_located(
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
        println(f"{i+1}/{num_subs}: [Abonné = {subscriber.sub_id}]")
        status = terminate_to_qualify_from_cga(
            cga_driver, cga_wait, uis, subscriber, tech_ids)
        if status:
            k += 1
            println(
                f"Cloturer avec l'id = {subscriber.tech_id}", Status.SUCCESS)
        else:
            println(f"Aucun Id trouver pour cloturer", Status.FAILED)
        all_subs.append(subscriber)
        
    x = logout_from_alonwa(driver, wait, uis)
    x == True
    y = logout_from_cga(cga_driver, cga_wait, uis)
    y == True
    println(f"{k}/{num_subs} Cloturer", Status.SUCCESS)

    return True
