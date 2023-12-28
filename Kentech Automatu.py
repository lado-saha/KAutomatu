import sys
from auth import *
from cga import *
from alonwa import *
from common import *
from selenium.webdriver.edge import service
# C:\Users\FAMILLE\AppData\Local\Programs\Python\Python311\Lib\site-packages\selenium\webdriver\edge\service.py

from date_ui_state import DataUiState

from visual import title_printer


def ask_timeout(d_uis: DataUiState):
    println(
        "Modifier le temps necessaire pour crasher(en seconde). N'entrer rien si vous voulez les parametres par "
        "defaults")
    try:
        d_uis.timeout = int(input("\t> Timeout(par défaut = 30s): "))
        println(f"Timeout = {d_uis.timeout}s", Status.SUCCESS)
    except Exception as e:
        println("Entrée invalid. La valeur par défaut de 30s a ete prise.", Status.FAILED)
    print()


def ask_month_interval(d_uis: DataUiState):
    current_month = datetime.date.today().month
    println(
        "Definissez l'interval temporel (en mois) pour faire la recherche. L'intervalle est entre le mois que vous "
        "allez choisir et le mois present, (inclusive). Ne mettez rien pour l'intervalle par default")
    try:
        start = int(input(f"\t> Debut (par défaut ={current_month}): "))
        if start > current_month:
            println(
                f"La fin doit etre inférieur ou égal au mois present({current_month}). L'interval par défaut à été pri",
                Status.FAILED)
        else:
            d_uis.month_start = start
            println(f"Interval: mois {d_uis.month_start} au mois {current_month}", Status.SUCCESS)
    except Exception as e:
        println("Entrée invalid. L'interval par défaut a ete pri.", Status.FAILED)
    print()


def ask_num_process(d_uis: DataUiState):
    println(
        "Modifier le nombre de clotures ou personne ou entite a traiter.")
    try:
        d_uis.num_to_process = int(input("\t> Nombre max de clotures(par défaut = INFINI): "))
    except Exception as e:
        println("Entrée invalid. La valeur par défaut qui est de 'INFINI' a ete prise", Status.FAILED)


def main():
    d_uis = DataUiState()

    println(f"{'Kentech Automatu':.^100}", Status.HEADING)
    println(f"{'Version Demo':.^100}", Status.NEGATIVE_ATTENTION)
    title_printer()
    println(f"{'By KENTECH SERVICE, 691940977' :.^100}", Status.HEADING)
    println("Bienvenu sur Kentech Automatu. Ce logiciel vous permettra de: ", Status.HEADING)
    println("\t - Automatisation des clotures des interventions Temporaires et a qualifier")
    println("\t - Automatisation des recoltes d'informations sur des Abonne canal et des techniciens")
    println("\t - Et bien d'autres")
    println("\t - Rapport Excel generer et ouvert automatiquement apres chaque operation")
    println("\t - Utiliser le Click droit pour coller.", Status.HEADING)
    println(
        "Veuillez fournir les informations demander et appuyez sur entrer pour valider. Utiliser le Click et non "
        "Ctr+V droit pour Coller")
    println("Finalement, assurer vous que vous avez une bonne connexion!")
    print('\n\n')

    opt = ''

    while True:
        is_cga_ok = False
        is_alonwa_ok = False

        uis = NavigationUiState()
        alonwa_driver = None
        cga_driver = None

        println(f"{'Acceuil':.^100}")
        num_alonwa = len(get_alonwa_accounts_from_db())
        default_alonwa = get_default_alonwa_account_id()
        num_cga = len(get_cga_accounts_from_db())
        default_cga = get_default_cga_account_id()
        println(f"{'':*^100}")

        println("Que voulez vous faire? ")

        if num_alonwa != 0 and default_alonwa != '':
            println("\t1- Ajouter, modifier, supprimer ou prioritiser vos Comptes ALONWA.", Status.HEADING)
        else:
            println("\t1- (urgent) Ajouter, modifier, supprimer ou prioritiser vos Comptes ALONWA.",
                    Status.POSITIVE_ATTENTION)

        if num_cga != 0 and default_cga != '':
            println("\t2- Ajouter, modifier, supprimer ou prioritiser vos Comptes CGA.", Status.HEADING)
        else:
            println("\t2- (urgent) Ajouter, modifier, supprimer ou prioritiser vos Comptes CGA.",
                    Status.POSITIVE_ATTENTION)

        println("\t3- Cloturer les interventions 'temporaires'.", Status.HEADING)
        println("\t4- Cloturer les interventions 'A qualifier'.", Status.HEADING)
        println("\t5- Obtenir des informations relatifs aux abonnes.", Status.HEADING)
        println("\t6- Obtenir des informations relatifs aux prestations.", Status.HEADING)
        println("\t7- Obtenir les numéros de telephones des abonnés sur ALONWA.", Status.HEADING)
        println("\t8- Effacer les Tech ids.", Status.HEADING)
        println("\t9- Tout Effacer", Status.NEGATIVE_ATTENTION)
        println("\t10- Aide general", Status.HEADING)
        println("\t11- (urgent) Quoi de neuf?", Status.POSITIVE_ATTENTION)
        println("\t12- Quitter", Status.HEADING)
        print()

        try:
            opt = int(input('\t> Choix: '))
        except Exception as e:
            println('Entrer un nombre de 1 a 12.', Status.FAILED)
            print()
            continue

        if opt == 1:
            while True:
                print()
                println(f"{'Comptes Alonwa':-^50}")
                accounts = get_alonwa_accounts_from_db()
                println(f"\tN° \t\tCompte")
                println(f"\t{'':=^50}")
                if len(accounts) != 0:
                    for account in enumerate(accounts, start=1):
                        if account[1].is_default:
                            println(f"\t{account[0]}  {account[1]}", Status.POSITIVE_ATTENTION)
                        else:
                            println(f"\t{account[0]}  {account[1]}")
                else:
                    println(f"\tAucun compte trouvé")

                print()

                println("Que voulez vous faire?")
                println("\t1- Ajouter un compte", Status.HEADING)
                if len(accounts) != 0:
                    println("\t2- Modifier un compte", Status.HEADING)
                    println("\t3- Supprimer un compte", Status.NEGATIVE_ATTENTION)
                    println("\t4- Définir un compte ALONWA par défaut", Status.HEADING)

                println("\t5- pour quitter!")
                try:
                    sub_opt = int(input('\t> Choix: '))
                    if len(accounts) == 0 and sub_opt != 1 and sub_opt != 5:
                        sub_opt += 10
                except Exception as e:
                    println('Entrer un nombre de 1 a 5.', Status.FAILED)
                    continue
                if sub_opt == 1:
                    println(f"{'Ajout du compte ALONWA':.^100}")
                    while True:
                        a_region = input("\t> Region: ")
                        a_name = input("\t> Identifiant: ")
                        a_password = get_password("\t> Mot de passe: ")
                        a_password_confirm = get_password("\t> Confirmer le mot de passe: ")
                        if a_password == a_password_confirm:
                            save_alonwa_account_to_db(
                                AlonwaAccount(region=a_region, name=a_name, password=a_password,
                                              account_id=str(uuid.uuid4()))
                            )
                            break
                        else:
                            println('Les mots de passe doivent etre identiques', Status.FAILED)
                elif sub_opt == 2:
                    println(f"{'Modification du compte ALONWA':.^100}")
                    print("Veuillez choisir le compte que vous voulez modifier en utilisant sont N°")
                    while True:
                        try:
                            a_number = int(input("\t> N°: "))
                            var = accounts[a_number - 1]
                        except Exception as e:
                            println('Aucun compte associer. ', Status.FAILED)
                            print()
                            continue
                        a_region = input("\t> Region: ")
                        a_name = input("\t> Identifiant: ")
                        a_password = get_password("\t> Mot de passe: ")
                        a_password_confirm = get_password("\t> Confirmer le mot de passe: ")
                        if a_password == a_password_confirm:
                            save_alonwa_account_to_db(
                                AlonwaAccount(region=a_region, name=a_name, password=a_password,
                                              account_id=accounts[a_number - 1].account_id))
                            break
                        else:
                            println('Les mots de passe doivent etre identiques', Status.FAILED)
                elif sub_opt == 3:
                    println(f"{'Suppression du compte ALONWA':.^100}")
                    print("Veuillez choisir le compte que vous voulez modifier en utilisant sont N°")
                    while True:
                        try:
                            a_number = int(input("\t> N°: "))
                            delete_alonwa_account_from_db(accounts[a_number - 1].account_id)
                            break
                        except Exception as e:
                            println("Compte n'a pas pu etre supprimer. ", Status.FAILED)
                            continue
                elif sub_opt == 4:
                    println(f"{'Compte par default ALONWA':.^100}")
                    print("Veuillez choisir le compte que vous voulez utiliser par défaut en utilisant sont N°")
                    while True:
                        try:
                            a_number = int(input("\t> N°: "))
                            set_default_alonwa_account(accounts[a_number - 1].account_id)
                            break
                        except Exception as e:
                            println("Compte n'a pas pu etre trouvé ou supprimé. ", Status.FAILED)
                            continue
                elif sub_opt == 5:
                    print()
                    break

                else:
                    if len(accounts) != 0:
                        println("Entrer un nombre de 1 a 5, Status.FAILED")
                    else:
                        println('Entrer soit 1 ou 5', Status.FAILED)
            continue

        if opt == 2:
            while True:
                print()
                println(f"{'Compte CGA':-^50}")
                accounts = get_cga_accounts_from_db()
                println(f"\tN° \t\tCompte")
                println(f"\t{'':=^50}")
                if len(accounts) != 0:
                    for account in enumerate(accounts, start=1):
                        if account[1].is_default:
                            println(f"\t{account[0]}  {account[1]}", Status.POSITIVE_ATTENTION)
                        else:
                            println(f"\t{account[0]}  {account[1]}")
                else:
                    println(f"\tAucun compte trouvé")

                print()

                println("Que voulez vous faire?")
                println("\t1- Ajouter un compte", Status.HEADING)
                if len(accounts) != 0:
                    println("\t2- Modifier un compte", Status.HEADING)
                    println("\t3- Supprimer un compte", Status.NEGATIVE_ATTENTION)
                    println("\t4- Définir un compte CGA par défaut", Status.HEADING)
                println("\t5- pour quitter!")
                try:
                    sub_opt = int(input('\t> Choix: '))
                    if len(accounts) == 0 and sub_opt != 1 and sub_opt != 5:
                        sub_opt += 10
                except Exception as e:
                    println('Entrer un nombre de 1 a 5.', Status.FAILED)
                    continue
                if sub_opt == 1:
                    println(f"{'Ajout du compte CGA':.^100}")
                    while True:
                        c_region = input("\t> Region: ")
                        c_name = input("\t> Utilisateur: ")
                        c_password = get_password("\t> Mot de passe: ")
                        c_password_confirm = get_password("\t> Confirmer le mot de passe: ")
                        if c_password == c_password_confirm:
                            save_cga_account_to_db(
                                CGAAccount(name=c_name, password=c_password, region=c_region,
                                           account_id=str(uuid.uuid4())))
                            break
                        else:
                            println('Les mots de passe doivent etre identiques', Status.FAILED)
                elif sub_opt == 2:
                    println(f"{'Modification du compte CGA':.^100}")
                    print("Veuillez choisir le compte que vous voulez modifier en utilisant sont N°")
                    while True:
                        try:
                            a_number = int(input("\t> N°: "))
                            var = accounts[a_number - 1]
                        except Exception as e:
                            println('Aucun compte associer. ', Status.FAILED)
                            print()
                            continue
                        c_region = input("\t> Region: ")
                        c_name = input("\t> Utilisateur: ")
                        c_password = get_password("\t> Mot de passe: ")
                        c_password_confirm = get_password("\t> Confirmer le mot de passe: ")
                        if c_password == c_password_confirm:
                            save_cga_account_to_db(CGAAccount(name=c_name, password=c_password, region=c_region,
                                                              account_id=accounts[a_number - 1].account_id))
                            break
                        else:
                            println('Les mots de passe doivent etre identiques', Status.FAILED)
                elif sub_opt == 3:
                    println(f"{'Suppression du compte CGA':.^100}")
                    print("Veuillez choisir le compte que vous voulez modifier en utilisant sont N°")
                    while True:
                        try:
                            a_number = int(input("\t> N°: "))
                            delete_cga_account_from_db(accounts[a_number - 1].account_id)
                            break
                        except Exception as e:
                            println("Compte n'a pas pu etre supprimer. ", Status.FAILED)
                            continue
                elif sub_opt == 4:
                    println(f"{'Compte par default ALONWA':.^100}")
                    print("Veuillez choisir le compte que vous voulez utiliser par défaut en utilisant sont N°")
                    while True:
                        try:
                            a_number = int(input("\t> N°: "))
                            set_default_cga_account(accounts[a_number - 1].account_id)
                            break
                        except Exception as e:
                            println("Compte n'a pas pu etre trouvé ou suprpimé. ", Status.FAILED)
                            continue

                elif sub_opt == 5:
                    print()
                    break

                else:
                    if len(accounts) != 0:
                        println("Entrer un nombre de 1 a 5, Status.FAILED")
                    else:
                        println('Entrer soit 1 ou 5', Status.FAILED)
            continue

        if opt == 3:

            if default_alonwa == '':
                println("Aucun compte alonwa par défaut trouver.", Status.FAILED)
                continue
            if default_cga == '':
                println("Aucun compte cga par défaut trouver.", Status.FAILED)
                continue

            current_month = datetime.date.today().month
            println(f"{'Instructions':-^50}")
            println(
                "Vous etes sur le point de cloturer toutes les interventions en etat 'Temporaires' du mois que vous "
                "allez entrer  sur ALONWA grace au CGA.")
            print(f"Entrez un mois entre 1 et {current_month}")
            try:
                print()
                month = int(input("\t> Mois: "))
                if month > current_month:
                    println("Mois invalid. Par défaut, nous allons selectionner le mois present", Status.FAILED)
            except Exception as e:
                println("Mois invalid. Par défaut, nous allons selectionner le mois present", Status.FAILED)
                month = current_month
            ask_timeout(d_uis)
            ask_num_process(d_uis)
            println(f"{'Debut':-^50}\n")

            # Debut

            subscribers: list[Subscriber] = []
            try:
                edge_options_1 = webdriver.EdgeOptions()
                edge_options_1.add_experimental_option('excludeSwitches', ['enable-logging'])
                alonwa_driver = webdriver.Edge(options=edge_options_1)
                alonwa_wait = WebDriverWait(alonwa_driver, d_uis.timeout)
                is_cga_ok = login_to_alonwa(alonwa_driver, alonwa_wait, get_default_alonwa_account(), uis)
                if is_cga_ok:
                    edge_options_2 = webdriver.EdgeOptions()
                    edge_options_2.add_experimental_option('excludeSwitches', ['enable-logging'])
                    cga_driver = webdriver.Edge(options=edge_options_2)
                    cga_wait = WebDriverWait(cga_driver, d_uis.timeout)
                    is_alonwa_ok = login_to_cga(cga_driver, cga_wait, get_default_cga_account(), uis)
                    if is_alonwa_ok:
                        terminate_temp_in_alonwa(alonwa_driver, alonwa_wait, month, uis, subscribers, cga_driver,
                                                 cga_wait, d_uis.num_to_process)
            except Exception as e:
                print(e)
                println("Verifier votre connexion internet", Status.FAILED)
            gen_temp_termination_report(month, subscribers)
            if is_alonwa_ok:
                alonwa_driver.quit()
            if is_cga_ok:
                cga_driver.quit()
            println(f"{'Fin':-^50}")

        elif opt == 4:
            if default_alonwa == '':
                println("Aucun compte alonwa par défaut trouver.", Status.FAILED)
                continue
            if default_cga == '':
                println("Aucun compte cga par défaut trouver.", Status.FAILED)
                continue
            println(f"{'Instructions':-^50}")
            println(
                "Vous etes sur le point de cloturer toutes les interventions en etat 'a qualifier' sur ALONWA grace "
                "au CGA.")
            println("Verification des tech ids donner.", Status.LOADING)
            if not has_tech_ids():
                println("Liste des tech ids introuvable", Status.FAILED)
                println(f"{'Ajout des Tech Ids':.^100}")
                println("Appuyez sur Ctrl+Z sur Windows pour enregistrer")
                println("Coller la liste des id des techniciens. Chaque Ids doit etre sur ca ligne ....")
                text = sys.stdin.read().strip()
                tech_ids = text.split("\n")
                save_tech_ids(tech_ids)
            else:
                println("Techs ids trouvé", Status.SUCCESS)
            ask_timeout(d_uis)
            ask_num_process(d_uis)
            println(f"{'Debut':-^50}\n")
            subscribers: list[Subscriber] = []

            try:
                edge_options_1 = webdriver.EdgeOptions()
                edge_options_1.add_experimental_option('excludeSwitches', ['enable-logging'])
                alonwa_driver = webdriver.Edge(options=edge_options_1)
                alonwa_wait = WebDriverWait(alonwa_driver, d_uis.timeout)
                is_alonwa_ok = login_to_alonwa(alonwa_driver, alonwa_wait, get_default_alonwa_account(), uis)
                if is_alonwa_ok:
                    edge_options_2 = webdriver.EdgeOptions()
                    edge_options_2.add_experimental_option('excludeSwitches', ['enable-logging'])
                    cga_driver = webdriver.Edge(options=edge_options_2)
                    cga_wait = WebDriverWait(cga_driver, d_uis.timeout)
                    is_cga_ok = login_to_cga(cga_driver, cga_wait, get_default_cga_account(), uis)
                    if is_cga_ok:
                        terminate_qualify_from_alonwa(alonwa_driver, alonwa_wait, uis, subscribers, cga_driver,
                                                      cga_wait, get_tech_ids(), d_uis.num_to_process)

            except Exception as e:
                println("Verifier votre connexion internet", Status.FAILED)
                print(e)
            gen_qualifier_termination_report(subscribers)
            if is_cga_ok:
                cga_driver.quit()
            if is_alonwa_ok:
                alonwa_driver.quit()
            println(f"{'Fin':-^50}")

        elif opt == 5:
            if default_cga == '':
                println("Aucun compte cga par défaut trouver.", Status.FAILED)
                continue
            println(f"{'Instructions':-^50}")
            println("Vous etes sur le point de recuperer les informations des abonnes sur le CGA")
            println("Vous pouvez le faire grace a une liste de: ")
            println("\t 1- Numeros de Telephones")
            println("\t 2- Numeros des Decodeurs")
            println("\t 3- ID des Abonnes")
            println("Utiliser le click droit pour coller, ensuite sur Entrer puis Ctrl+Z sur Windows pour enregistrer",
                    Status.HEADING)
            print("\t Autres pour annuler.")

            query_field: SubQueryField
            while True:
                try:
                    input_opt = int(input("\t> Choix: "))
                    break
                except Exception as e:
                    println("L'option doit etre entre 1 et 3. Si vous voulez annuler, choisiser un nombre autre.")
            println("Utiliser le click droit pour coller, ensuite sur Entrer puis Ctrl+Z sur Windows pour enregistrer",
                    Status.HEADING)
            if input_opt == 1:
                query_field = SubQueryField.PHONE
                println("Coller la liste des Numeros de Telephone. Chaque numeros doit etre sur ca ligne ....")
            elif input_opt == 2:
                query_field = SubQueryField.DECODER
                println("Coller la liste des Numeros de Decodeurs. Chaque numeros doit etre sur ca ligne ....")
            elif input_opt == 3:
                query_field = SubQueryField.SUBSCRIBER_ID
                println("Coller la liste des IDs des Abonnes. Chaque id doit etre sur ca ligne ....")
            else:
                continue

            text = sys.stdin.read().strip()
            subscriber_query = text.split("\n")
            println("Liste temporairement enregistrer", Status.SUCCESS)
            subscribers: list[Subscriber] = []
            ask_timeout(d_uis)

            println(f"{'Debut':-^50}\n")
            try:
                edge_options_1 = webdriver.EdgeOptions()
                edge_options_1.add_experimental_option('excludeSwitches', ['enable-logging'])
                cga_driver = webdriver.Edge(options=edge_options_1)
                cga_wait = WebDriverWait(cga_driver, d_uis.timeout)
                is_cga_ok = login_to_cga(cga_driver, cga_wait, get_default_cga_account(), uis)
                if is_cga_ok:
                    get_all_subscriber_data_from(cga_driver, uis, cga_wait, subscribers, subscriber_query, query_field)
            except Exception as e:
                print(e)
                println("Verifier votre connexion internet", Status.FAILED)
            m = gen_subscriber_data_report(subscribers, query_field)
            if is_cga_ok:
                cga_driver.quit()
            println(f"{'Fin':-^50}")

        elif opt == 6:
            if default_cga == '':
                println("Aucun compte cga par défaut trouver.", Status.FAILED)
                continue
            println(f"{'Instructions':-^50}")
            println(
                "Vous etes sur le point d'obtenir les etats des prestations(installation canal+) grace au numeros de "
                "decodeurs")
            println("Utiliser le click droit pour coller, ensuite sur Entrer puis Ctrl+Z sur Windows pour enregistrer",
                    Status.HEADING)
            println("Coller la liste des numeros de decodeurs. Chaque numero doit etre sur ca ligne ....")
            text = sys.stdin.read().strip()
            decoders = text.split("\n")
            println("Liste temporairement enregistrer", Status.SUCCESS)
            ask_timeout(d_uis)
            prestations: list[Prestation] = []

            try:
                edge_options_2 = webdriver.EdgeOptions()
                edge_options_2.add_experimental_option('excludeSwitches', ['enable-logging'])
                cga_driver = webdriver.Edge(options=edge_options_2)
                cga_wait = WebDriverWait(cga_driver, d_uis.timeout)
                is_cga_ok = login_to_cga(cga_driver, cga_wait, get_default_cga_account(), uis)
                if is_cga_ok:
                    cga_get_state_of_prestation_from_decoders(cga_driver, cga_wait, uis, decoders, prestations)
            except Exception as e:
                println("Verifier votre connexion internet", Status.FAILED)
                print(e)
            m = gen_prestation_data_report(prestations)
            if is_cga_ok:
                cga_driver.quit()
            println(f"{'Fin':-^50}")

        elif opt == 7:
            if default_alonwa == '':
                println("Aucun compte alonwa par défaut trouver.", Status.FAILED)
                continue
            println(f"{'Instructions':-^50}")
            println(
                "Vous etes sur le point d'obtenir les numéros de téléphones de vos abonnés grace à leur numero "
                "d'abonné.")
            println("Utiliser le click droit pour coller, ensuite sur Entrer puis Ctrl+Z sur Windows pour enregistrer",
                    Status.HEADING)
            println("Coller la liste des numeros d'abonnés. Chaque numéro doit etre sur ca ligne ....")
            text = sys.stdin.read().strip()
            sub_ids = text.split("\n")
            println("Liste temporairement enregistrer", Status.SUCCESS)
            ask_month_interval(d_uis)
            ask_timeout(d_uis)
            all_subs: list[Subscriber] = []
            try:
                edge_options_1 = webdriver.EdgeOptions()
                edge_options_1.add_experimental_option('excludeSwitches', ['enable-logging'])
                alonwa_driver = webdriver.Edge(options=edge_options_1)
                alonwa_wait = WebDriverWait(alonwa_driver, d_uis.timeout)
                is_alonwa_ok = login_to_alonwa(alonwa_driver, alonwa_wait, get_default_alonwa_account(), uis)
                if is_alonwa_ok:
                    get_subs_phones_from_subs_ids(alonwa_driver, alonwa_wait, uis, all_subs, sub_ids, d_uis)
            except Exception as e:
                println("Verifier votre connexion internet", Status.FAILED)
            gen_subscriber_data_report_phone(all_subs)
            if is_alonwa_ok:
                alonwa_driver.quit()
            println(f"{'Fin':-^50}")

        elif opt == 8:
            println("Si vous continuer, vous allez devoir re-introduire les ids des techniciens.")
            opt = input("\t> 'C' pour continuer ")
            if opt.lower() == 'c':
                clear_tech_ids()
            print()
            continue
        elif opt == 9:
            println("Si vous continuer, les rapports et tout autres information seront irreversiblement supprimer.",
                    Status.NEGATIVE_ATTENTION)
            opt = input("\t> 'C' pour continuer: ")
            if opt.lower() == 'c':
                re_init_app()
            print()
            continue

        elif opt == 10:
            println("Cette automate prend le controle temporaire de votre Navigateur Edge de preference.")
            println('(i) Au cour de cette operation, votre navigateur va ouvrir des nombreuses page.')
            println("(ii) Il est vivent considerer de rester spectateur, et de ne pas interagir avec c'est pas.")
            println(
                "(iii) Vous pouvez neanmoins continuer a utiliser votre machine et ouvrir une nouvel fenetre de votre "
                "navigateur.")
            println("(iv) Cette operation necessite un connexion internet stable afin de bien terminer")
            println("(v) A la fin de l'operation, un rapport detaille sera generer. Veuillez patienter")
            println(
                "(vi) L'automat peut avoir besoin d'une liste de valeurs(decodeur, telephone etc)\n \t Veuillez "
                "coller cette liste de valeurs avec le click-droit si Ctrl+V ne marche pas. La liste doit contenir "
                "une valeur par lignes.")
            println("(vii) Ctrl+C ou Ctrl+M pour quitter le program a tout moment")
            println("Pour plus d'information et proposition, contacter LADO SAHA au 691940977 ou 670709383")
            continue

        elif opt == 11:
            println(f"{'Quoi de neuf':-^100}")
            println("Dernier mise a jour: Jeudi le 24 aout 2023")
            println("A propos de la mise a jour")
            println(
                "\t - Vous pouvez, grace a l'option '1' ajouter, supprimer, modifier et choisir un compte par defaut "
                "alonwa. Le compte par default sera utliliser comme le login sur le site Service plus(alonwa)",
                Status.SUCCESS)
            println(
                "\t - Vous pouvez, grace a l'option '2' ajouter, supprimer, modifier et choisir un compte par defaut "
                "cga. Le compte par default sera utliliser comme le login sur le site CGA",
                Status.SUCCESS)

            println("Mise a jour: Mercredi 17 aout 2023")
            println("A propos de la mise a jour")
            println(
                "\t - Vous pouvez, grace a l'option '7' recuperer les numéros de téléphones des abonnés grace aux "
                "numéros d'abonnés sur ALONWA. ",
                Status.SUCCESS)
            println(f"{'=':-^50}")
            println("Mise a jour: Lundi 14 aout 2023")
            println("A propos de la mise a jour")
            println("\t - Resolution du probleme de clotures au niveau du Recapitulatif d'intervention ",
                    Status.SUCCESS)
            println("\t - Ajout de messages plus claires",
                    Status.SUCCESS)
            println("")
            print()
            continue

        elif opt == 12:
            println(f"{'Au revoir':.^100}")
            print()
            break

        else:
            println('Entrer un nombre entre 1 et 12.', Status.FAILED)
            print()
            continue


if init_app():
    main()
else:
    print("")
    input()
