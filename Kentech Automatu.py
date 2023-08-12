import sys
from common import *
from auth import *
from cga import *
from alonwa import *
from selenium.webdriver.edge.service import Service

from date_ui_state import data_ui_state


# DRIVER_PATH = r'msedgedriver.exe'    

def ask_timeout(d_uis: data_ui_state):
    println("Modifier le temps necessaire pour crasher(en seconde). N'entrer rien si vous voulez les parametres par defauts")
    try:
        d_uis.timeout = int(input("\t> Timeout(par defaut = 30s): "))
    except Exception as e:
        println("Entrée invalid. La valeur par defaut de 30s a ete prise.", Status.FAILED)
   
def ask_num_process(d_uis: data_ui_state):
    println("Modifier le temps necessaire pour crasher(en seconde). N'entrer rien si vous voulez les parametres par defauts")
    try:
        d_uis.num_to_process = int(input("\t> Nombre max de clotures(par defaut = INFINI): "))
    except Exception as e:
        println("Entrée invalid. La valeur par defaut qui est de 'INFINI' a ete prise", Status.FAILED)


def main():
    a = False
    b = False

    d_uis = data_ui_state()

    init_app()
    println(f"{'Kentech Automatu':.^100}", Status.HEADING)
    println(f"{'Version Demo':.^100}", Status.ATTENTION)
    println(f"{'By KENTECH SERVICE, 691940977' :.^100}", Status.HEADING)
    println("Bienvenu sur Kentech Automatu. Ce logiciel vous permettra de: ", Status.HEADING)
    println("\t - Automatisation des clotures des interventions Temporaires et a qualifier")
    println("\t - Automatisation des recoltes d'informations sur des Abonne canal et des techniciens")
    println("\t - Et bien d'autres")
    println("\t - Rapport Excel generer et ouvert automatiquement apres chaque operation")
    println("\t - Utiliser le Click droit pour coller.", Status.HEADING)
    println("Veuillez fournir les informations demander et appuyez sur entrer pour valider. Utiliser le Click et non Ctr+V droit pour Coller")
    println("Finalement, assurer vous que vous avez une bonne connexion!")
    print('\n\n')

    opt = ''
    show_account_check = True

    while True:
        uis = NavigationUiState()
        println(f"{'Acceuil':.^100}")
        print()
        if not has_cga_account():
            println('Compte CGA Introuvable', Status.FAILED)
            println(f"{'Ajout du compte CGA':.^100}")
            while True:
                cga_name = input("\t> Utilisateur: ")
                cga_password = get_password("\t> Mot de passe: ")
                cga_password_confirm = get_password("\t> Confirmer le mot de passe: ")
                if cga_password == cga_password_confirm:
                    save_cga_account_to_db(cga_name, cga_password)
                    break
                else:
                    println('Les mots de passe doivent etre identiques', Status.FAILED)
            print()
        elif show_account_check: 
            println('Compte CGA Trouver', Status.SUCCESS)
        
    
        if not has_alonwa_account():
            println('Compte ALONWA Introuvable', Status.FAILED)
            println(f"{'Ajout du compte ALONWA':.^100}")
            while True:
                alonwa_name = input("\t> Identifiant: ")
                alonwa_password = get_password("\t> Mot de passe: ")
                alonwa_password_confirm = get_password("\t> Confirmer le mot de passe: ")
                if alonwa_password == alonwa_password_confirm:
                    save_alonwa_account_to_db(alonwa_name, alonwa_password)
                    break
                else:
                    println('Les mots de passe doivent etre identiques', Status.FAILED)
            print()
        elif show_account_check:  
            println('Compte Alonwa Trouver', Status.SUCCESS)

        show_account_check = False
        print()

        println("Que voulez vous faire? ")
        println("\t1- Cloturer les interventions 'temporaires'.", Status.HEADING)
        println("\t2- Cloturer les interventions 'A qualifier'.", Status.HEADING)
        println("\t3- Obtenir des informations realtifs au abonnes.", Status.HEADING)
        println("\t4- Obtenir des informations relatifs au prestations.", Status.HEADING)
        println("\t5- Effacer le login CGA.", Status.HEADING)
        println("\t6- Effacer le login ALONWA.", Status.HEADING)
        println("\t7- Effacer les Tech ids.", Status.HEADING)
        println("\t8- Tout Effacer", Status.ATTENTION)
        println("\t9- Aide general", Status.HEADING)
        println("")
        println("\t10- Quitter", Status.HEADING)
        print()

        try:
            opt = int(input('\t> Choix: '))
        except Exception as e:
            println('Entrer un nombre de 1 a 7.', Status.FAILED)
            print()
            continue

        if opt == 1:
            current_month = datetime.date.today().month
            println(f"{'Instructions':-^50}")
            println("Vous etes sur le point de cloturer toutes les interventions en etat 'Temporaires' du mois que vous allez entrer  sur ALONWA grace au CGA.")
            print(f"Entrez un mois entre 1 et {current_month}")
            try:
                print()
                month = int(input("\t> Mois: "))
                if month > current_month:
                    println("Mois invalid. Par defaut, nous allons selectionner le mois present", Status.FAILED)
            except Exception as e:
                println("Mois invalid. Par defaut, nous allons selectionner le mois present", Status.FAILED)
                month = current_month
            ask_timeout(d_uis)
            ask_num_process(d_uis)
            println(f"{'Debut':-^50}\n")
            
            # Debut
            
            subscribers:list[Subscriber] = []
            try:
                edge_options_1 = webdriver.EdgeOptions()
                # edge_options_1.add_argument('--headless')
                # edge_options_1.add_experimental_option("detach", True)
                edge_options_1.add_experimental_option('excludeSwitches', ['enable-logging'])
                alonwa_driver = webdriver.Edge(options=edge_options_1,)
                alonwa_wait = WebDriverWait(alonwa_driver, d_uis.timeout)
                a = login_to_alonwa(alonwa_driver, alonwa_wait, get_alonwa_user(), uis)
                if a:
                    edge_options_2 = webdriver.EdgeOptions()
                    # edge_options_2.add_argument('--headless')
                    # edge_options_2.add_experimental_option("detach", True)
                    edge_options_2.add_experimental_option('excludeSwitches', ['enable-logging'])
                    cga_driver = webdriver.Edge(options=edge_options_2)
                    cga_wait = WebDriverWait(cga_driver, d_uis.timeout)
                    b= login_to_cga(cga_driver, cga_wait, get_cga_user(), uis)
                    if b:
                        terminate_temp_in_alonwa(alonwa_driver, alonwa_wait, month,uis,subscribers, cga_driver, cga_wait, d_uis.num_to_process)
            except Exception as e:
                print(e)
                println("Verifier votre connexion internet", Status.FAILED)
            m = gen_temp_termination_report(month, subscribers)
            alonwa_driver.quit()
            if a:
                cga_driver.quit()
            println(f"{'Fin':-^50}")
            
        elif opt == 2:
            println(f"{'Instructions':-^50}")
            println("Vous etes sur le point de cloturer toutes les interventions en etat 'a qualifier' sur ALONWA grace au CGA.")
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
            subscribers:list[Subscriber] = []
            
            try:
                edge_options_1 = webdriver.EdgeOptions()
                edge_options_1.add_experimental_option("detach", True)
                edge_options_1.add_experimental_option('excludeSwitches', ['enable-logging'])
                alonwa_driver = webdriver.Edge(options=edge_options_1)
                alonwa_wait = WebDriverWait(alonwa_driver, d_uis.timeout)
                a = login_to_alonwa(alonwa_driver, alonwa_wait, get_alonwa_user(), uis)
                if a:
                    edge_options_2 = webdriver.EdgeOptions()
                    edge_options_2.add_experimental_option("detach", True)
                    edge_options_2.add_experimental_option('excludeSwitches', ['enable-logging'])
                    cga_driver = webdriver.Edge(options=edge_options_2)
                    cga_wait = WebDriverWait(cga_driver, d_uis.timeout)
                    b = login_to_cga(cga_driver, cga_wait, get_cga_user(), uis)
                    if b:
                        terminate_qualify_from_alonwa(alonwa_driver, alonwa_wait, uis, subscribers, cga_driver, cga_wait, get_tech_ids(), d_uis.num_to_process)

            except Exception as e:
                println("Verifier votre connexion internet", Status.FAILED)
                print(e)
            m = gen_qualifier_termination_report(subscribers)
            if a:
                cga_driver.quit()
            alonwa_driver.quit()
            println(f"{'Fin':-^50}") 

        elif opt == 3:
            println(f"{'Instructions':-^50}")
            println("Vous etes sur le point de recuperer les informations des abonnes sur le CGA")
            println("Vous pouvez le faire grace a une liste de: ")
            println("\t 1- Numeros de Telephones")
            println("\t 2- Numeros des Decodeurs")
            println("\t 3- ID des Abonnes")
            println("Utiliser le click droit pour coller, ensuite sur Entrer puis Ctrl+Z sur Windows pour enregistrer", Status.HEADING)
            print("\t Autres pour annuler.")
            input_opt = 0 
            query_field: SubQueryField
            while True:
                try:
                    input_opt = int(input("\t> Choix: "))
                    break
                except Exception as e:
                    println("L'option doit etre entre 1 et 3. Si vous voulez annuler, choisiser un autre nombre.")
            println("Utiliser le click droit pour coller, ensuite sur Entrer puis Ctrl+Z sur Windows pour enregistrer", Status.HEADING)
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
                edge_options_1.add_experimental_option("detach", True)
                edge_options_1.add_experimental_option('excludeSwitches', ['enable-logging'])
                cga_driver = webdriver.Edge(options=edge_options_1)
                cga_wait = WebDriverWait(cga_driver, d_uis.timeout)
                b = login_to_cga(cga_driver, cga_wait, get_cga_user(), uis)
                if b:
                    get_all_subscriber_data_from(cga_driver, uis, cga_wait, subscribers, subscriber_query, query_field)
            except Exception as e:
                println("Verifier votre connexion internet", Status.FAILED)
            m = gen_subscriber_data_report(subscribers, query_field)
            cga_driver.quit()
            println(f"{'Fin':-^50}")

        elif opt == 4:
            println(f"{'Instructions':-^50}")
            println("Vous etes sur le point d'obtenir les etats des prestations(installation canal+) grace au numeros de decodeurs")
            println("Utiliser le click droit pour coller, ensuite sur Entrer puis Ctrl+Z sur Windows pour enregistrer", Status.HEADING)
            println("Coller la liste des numeros de decodeurs. Chaque numero doit etre sur ca ligne ....")
            text = sys.stdin.read().strip()
            decoders = text.split("\n")
            println("Liste temporairement enregistrer", Status.SUCCESS)
            ask_timeout(d_uis)
            prestations:list[Prestation] = []
            
            try:
                edge_options_1 = webdriver.EdgeOptions()
                edge_options_1.add_experimental_option("detach", True)
                edge_options_1.add_experimental_option('excludeSwitches', ['enable-logging'])
                cga_driver = webdriver.Edge(options=edge_options_1)
                cga_wait = WebDriverWait(cga_driver, d_uis.timeout)
                b = login_to_cga(cga_driver, cga_wait, get_cga_user(), uis)
                if b:
                    x = cga_get_state_of_prestation_from_decoders(cga_driver,cga_wait, uis, decoders, prestations)
                    x == True
            except Exception as e:
                println("Verifier votre connexion internet", Status.FAILED)
                print(e)
            m = gen_prestation_data_report(prestations)
            cga_driver.quit()
            println(f"{'Fin':-^50}") 
            
        elif opt == 5:
            println("Si vous continuer, vous allez devoir re-introduire vos information de login CGA la prochaine fois.")
            opt = input("\t> 'C' pour continuer > ")
            if opt.lower() == 'c':
                clear_cga_account()
                show_account_check = False
            print()
            continue
    
        elif opt == 6:
            println("Si vous continuer, vous allez devoir re-introduire vos information de login Alonwa la prochaine fois.")
            opt = input("\t'C' pour continuer > ")
            if opt.lower() == 'c':
                clear_alonwa_account()
                show_account_check = False
            print()
            continue

        elif opt == 7:
            println("Si vous continuer, vous allez devoir re-introduire les ids des techniciens.")
            opt = input("\t> 'C' pour continuer ")
            if opt.lower() == 'c':
                clear_tech_ids()
            print()
            continue
        elif opt == 8:
            println("Si vous continuer, les rapports et tout autres information seront irreversiblement supprimer.", Status.ATTENTION)
            opt = input("\t> 'C' pour continuer: ")
            if opt.lower() == 'c':
                re_init_app()
            print()
            continue


        elif opt == 9:
            println("Cette automate prend le controle temporaire de votre Navigateur Edge de preference.")
            println('(i) Au cour de cette operation, votre navigateur va ouvrir des nombreuses page.')
            println("(ii) Il est vivent considerer de rester spectateur, et de ne pas interagir avec c'est pas.")
            println("(iii) Vous pouvez neanmoins continuer a utiliser votre machine et ouvrir une nouvel fenetre de votre navigateur.")
            println("(iv) Cette operation necessite un connexion internet stable afin de bien terminer")
            println("(v) A la fin de l'operation, un rapport detaille sera generer. Veuillez patienter")
            println("(vi) L'automat peut avoir besoin d'une liste de valeurs(decodeur, telephone etc)\n \t Veuillez coller cette liste de valeurs avec le click-droit si Ctrl+V ne marche pas. La liste doit contenir une valeur par lignes.")
            println("(vii) Ctrl+C ou Ctrl+M pour quitter le program a tout moment")
            println("Pour plus d'information et proposition, contacter LADO SAHA au 691940977 ou 670709383")
            continue 

        elif opt == 10:
            println(f"{'Au revoir':.^100}") 
            print() 
            break     

        else:
            println('Entrer un nombre entr 1 et 10.', Status.FAILED)
            print()
            continue
        
                

if init_app():   
    main()
# def progress_bar(total):
#     for i in range(total):
#         sys.stdout.write('\r')
#         sys.stdout.write("[%-20s] %d%%" % ('='*int(20*i/total), int(100*i/total)))
#         sys.stdout.flush()
#         time.sleep(0.25)
#     sys.stdout.write('\r')
#     sys.stdout.write("[%-20s] %d%%" % ('='*20, 100))
#     sys.stdout.flush()
#     print()

# progress_bar(10)



