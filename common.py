import base64
import datetime
from enum import Enum
import msvcrt
import subprocess
import time
import json
import os
import shutil
from colorama import init
import locale


# from getmac import get_mac_address

# import uuid

# import os


def d() -> str:
    loc = locale.getlocale()
    language_code = loc[0][:2]
    if language_code.lower() == 'fr':
        return ';'
    else:
        return ','


class Status(Enum):
    SUCCESS = 1
    FAILED = 2
    LOADING = 3
    HEADING = 4
    NEGATIVE_ATTENTION = 5
    POSITIVE_ATTENTION = 6
    T_CYAN = 10
    T_BLUE = 11
    T_GREEN = 12



class SubQueryField(Enum):
    PHONE = 'Numero de telephone'
    DECODER = 'Numero de decodeur'
    SUBSCRIBER_ID = "Id de l'abonner"

    def __str__(self) -> str:
        return self.value


class SubStates(Enum):
    VALIDATED = 'Deja Valider'
    CANCELLED = 'Annuler'
    NOT_FOUND = 'Inconnu'
    WAS_ERROR_VALIDATED = "N'a pas pu etre validé. Nous"
    WAS_SUCCESS_VALIDATED = "A pu etre validé"
    NO_PRESTATION = 'Aucune Prestation'
    NONE = ''

    def __str__(self) -> str:
        return self.value


class PrestationState(Enum):
    VALIDATED = 'Validé'
    CANCELLED = 'Annulé'
    UNKNOWN_DECODER = 'Decodeur Inconnu'
    NO_PRESTATION = 'Aucune Prestation'
    NONE = ''

    def __str__(self) -> str:
        return self.value


PATH_BASE = os.path.expanduser('~/Documents') + '\\Kentech AUTOMATU'
PATH_FILE_ACCOUNT = PATH_BASE + '\\DB\\account.json'
PATH_FILE_TECH_IDS = PATH_BASE + '\\DB\\tech_ids.txt'
PATH_BASE_TEMP_REPORT = PATH_BASE + '\\Rapports\\Clotures des temporaires'
PATH_BASE_QUALIF_REPORT = PATH_BASE + '\\Rapports\\Clotures des à qualifiers'
PATH_BASE_SUBS_DATA = PATH_BASE + '\\Rapports\\Données des abonnes'
PATH_BASE_PRESTATION_STATE = PATH_BASE + '\\Rapports\\Etat des prestations'


def init_app() -> bool:
    init()
    x = mac_matters()
    # mac_matters()
    documents_folder = os.path.expanduser('~/Documents')
    base_folder = os.path.join(documents_folder, 'Kentech AUTOMATU')
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        db_folder = os.path.join(base_folder, 'DB')
        rapport_folder = os.path.join(base_folder, 'Rapports')
        os.makedirs(db_folder)
        subprocess.run(['attrib', '+h', db_folder])
        os.makedirs(rapport_folder)
        os.makedirs(os.path.join(rapport_folder, 'Clotures des temporaires'))
        os.makedirs(os.path.join(rapport_folder, 'Clotures des à qualifiers'))
        os.makedirs(os.path.join(rapport_folder, 'Données des abonnes'))
        os.makedirs(os.path.join(rapport_folder, 'Etat des prestations'))
    return x


def re_init_app():
    println("Suppression des Donnees", Status.SUCCESS)
    shutil.rmtree(PATH_BASE)
    println("Suppression des Donnees", Status.SUCCESS)
    println("Reinitialisation", Status.LOADING)
    init_app()
    println("Reinitialisation", Status.SUCCESS)


class NavigationUiState:
    def __init__(
            self,
            session_id: str = '',
            session_url: str = '',
            is_login_cga: bool = False,
            is_login_alonwa: bool = False,
            is_cga_prospect_open: bool = False,
            frame_cga_title: any = '',
            frame_cga_main: any = '',
            frame_cga_info: any = '',
            page_cga_home: str = '',
            page_cga_prospect: str = '',
            page_alonwa_home: str = '',
            page_alonwa_tech_profile: str = '',
            page_alonwa_tech_planning: str = '',
            page_alonwa_intervention: str = '',
            page_alonwa_intervention_details: str = '',
            page_alonwa_closure: str = '',
            error: str = '',
    ):
        """Initializes the navigation UI state."""
        self.session_id = session_id
        self.session_url = session_url
        self.is_login_cga = is_login_cga
        self.is_login_alonwa = is_login_alonwa
        self.is_cga_prospect_open = is_cga_prospect_open
        self.frame_cga_title = frame_cga_title
        self.frame_cga_main = frame_cga_main
        self.frame_cga_info = frame_cga_info
        self.page_cga_home = page_cga_home
        self.page_cga_prospect = page_cga_prospect
        self.page_alonwa_home = page_alonwa_home
        self.page_alonwa_tech_profile = page_alonwa_tech_profile
        self.page_alonwa_tech_planning = page_alonwa_tech_planning
        self.page_alonwa_interventions = page_alonwa_intervention
        self.page_alonwa_intervention_details = page_alonwa_intervention_details
        self.page_alonwa_closure = page_alonwa_closure
        self.error = error

    def __str__(self):
        """Returns a string representation of the navigation UI state."""
        return (
            f"NavigationUiState(session_id={self.session_id}, "
            f"session_url={self.session_url}, "
            f"is_login_cga={self.is_login_cga}, "
            f"is_login_alonwa={self.is_login_alonwa}, "
            f"is_cga_prospect_open={self.is_cga_prospect_open}, "
            f"frame_cga_title={self.frame_cga_title}, "
            f"frame_cga_main={self.frame_cga_main}, "
            f"frame_cga_info={self.frame_cga_info}, "
            f"page_cga_home={self.page_cga_home}, "
            f"page_cga_prospect={self.page_cga_prospect}, "
            f"page_alonwa_home={self.page_alonwa_home}, "
            f"page_alonwa_tech_profile={self.page_alonwa_tech_profile}, "
            f"page_alonwa_tech_planning={self.page_alonwa_tech_planning}, "
            f"page_alonwa_intervention={self.page_alonwa_interventions}, "
            f"page_alonwa_intervention_details={self.page_alonwa_intervention_details}",
            f"error={self.error}"
        )


class UserLogin:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


class Subscriber:
    def __init__(self, decoder_num: str = '', sub_id: str = '', name: str = '', formula: str = '', phone='',
                 link: any = None, tech_id: str = '', expiry_date: str = '', state: SubStates = SubStates.NONE):
        """Initializes the subscriber.
        Args:
            sub_id: The subscriber ID.
            name: The subscriber name.
            decoder_num: The decoder number.
            formula: The formula.
            link: The link to cga contract
        """
        self.sub_id = sub_id
        self.name = name
        self.decoder_num = decoder_num
        self.formula = formula
        self.tech_id = tech_id
        self.link = link
        self.phone = phone
        self.date_period_str = expiry_date
        self.state = state

    def __str__(self):
        """Returns a string representation of the subscriber."""
        return f"Subscriber {self.sub_id}: {self.name}{d()} {self.decoder_num}{d()} {self.formula}"

    def report_for_temp_termination(self) -> str:
        return f"\n{self.decoder_num}{d()} {self.sub_id}{d()} {self.name}{d()} {self.formula}{d()} {self.state}{d()} {self.tech_id}"

    def report_for_data(self) -> str:
        start = ''
        stop = ''
        try:
            period = self.date_period_str.split('-')
            start = period[0]
            stop = period[1]
        except Exception as e:
            pass
        return f"\n{self.decoder_num}{d()} {self.sub_id}{d()} {self.phone}{d()} {self.name}{d()} {self.formula}{d()} {start}{d()} {stop}{d()} {self.state}"

    def report_phone(self) -> str:
        return f"\n{self.sub_id}{d()}{self.phone}{d()}"

class Prestation:
    def __init__(
            self,
            decoder_num: str = '',
            tech_cga_ref: str = '',
            sub_id: str = '',
            state: PrestationState = PrestationState.NONE
    ) -> None:
        self.decoder_num = decoder_num
        self.tech_cga_ref = tech_cga_ref
        self.sub_id = sub_id
        self.state = state

    def __str__(self) -> str:
        return f'\n{self.decoder_num}{d()} {self.sub_id}{d()} {self.state}{d()} {self.tech_cga_ref}'


"""
    Ai type print
"""


def gen_prestation_data_report(prestations: list[Prestation]):
    println(f"Generation du Rapport Excel", Status.LOADING)
    now = datetime.datetime.now()
    report = f"""
    Kentech AUTOMATU{d()} By KENTECH{d()} 6919409777{d()}ladokihosaha@gmail.com{d()}{d()}{d()}{d()}{d()}
    Generé le {now.strftime('%Y-%m-%d %H:%M:%S')}{d()}{d()}{d()}{d()}{d()}{d()}{d()}
    Titre: Etats des Prestations{d()}{d()}{d()}{d()}{d()}{d()}{d()}
    CGA name: {get_cga_user().username}{d()}{d()}{d()}{d()}{d()}{d()}{d()}
    {d()}{d()}{d()}{d()}{d()}
    Num Decodeur{d()} Num Abonne{d()} Etat, Referenc{d()} CGA Antenist"""
    if len(prestations) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for presentation in prestations:
            report += presentation.__str__()

    path = f"{PATH_BASE_PRESTATION_STATE}\\donnes_prestation_{now.strftime('%Y-%m-%d %H-%M')}.csv"
    with open(path, 'w') as f:
        f.write(report)
        println(f"Rapport Excel: {path}", Status.SUCCESS)
        println(f"Ouverture du rapport", Status.LOADING)
        os.startfile(f.name)
        println(f"Ouverture du rapport", Status.SUCCESS)


"""
    Ai type print
"""


def gen_subscriber_data_report(subscribers: list[Subscriber], query_field: SubQueryField):
    println(f"Generation du Rapport Excel", Status.LOADING)
    now = datetime.datetime.now()
    report = f"""
    Kentech AUTOMATU{d()} By KENTECH{d()}6919409777{d()}ladokihosaha@gmail.com{d()}{d()}{d()}{d()}{d()}
    Generé le {now.strftime('%Y-%m-%d %H:%M:%S')}{d()}{d()}{d()}{d()}{d()}{d()}{d()}
    Titre: Donnees des Abonnes{d()}{d()}{d()}{d()}{d()}{d()}{d()}
    Recharcher par: {query_field}{d()}{d()}{d()}{d()}{d()}{d()}{d()}
    CGA name: {get_cga_user().username}{d()}{d()}{d()}{d()}{d()}{d()}{d()}
    {d()}{d()}{d()}{d()}{d()}
    Num Decodeur{d()} Num Abonne{d()} Numero de telephone{d()} Nom d'abonne{d()} Formule{d()} Debut{d()} Fin{d()} Etat"""
    if len(subscribers) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for sub in subscribers:
            report += sub.report_for_data()
    path = f"{PATH_BASE_SUBS_DATA}\\donnes_par_{query_field}_{now.strftime('%Y-%m-%d %H-%M')}.csv"
    with open(path, 'w') as f:
        f.write(report)
        println(f"Rapport Excel: {path}", Status.SUCCESS)
        println(f"Ouverture du rapport", Status.LOADING)
        os.startfile(f.name)
        println(f"Ouverture du rapport", Status.SUCCESS)

def gen_subscriber_data_report_phone(subscribers: list[Subscriber]):
    println(f"Generation du Rapport Excel", Status.LOADING)
    now = datetime.datetime.now()
    report = f"""
    Kentech AUTOMATU{d()} By KENTECH{d()}6919409777{d()}ladokihosaha@gmail.com{d()}{d()}{d()}{d()}{d()}
    Generé le {now.strftime('%Y-%m-%d %H:%M:%S')}{d()}
    Titre: Numéros de téléphone des abonnés{d()}
    ALONWA name: {get_alonwa_user().username}{d()}
    
     Num Abonne{d()} Numéro de téléphone{d()}"""
    if len(subscribers) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for sub in subscribers:
            report += sub.report_phone()
    path = f"{PATH_BASE_SUBS_DATA}\\telephone_par_{now.strftime('%Y-%m-%d %H-%M')}.csv"
    with open(path, 'w') as f:
        f.write(report)
        println(f"Rapport Excel: {path}", Status.SUCCESS)
        println(f"Ouverture du rapport", Status.LOADING)
        os.startfile(f.name)
        println(f"Ouverture du rapport", Status.SUCCESS)

def gen_temp_termination_report(month: int, subscribers: list[Subscriber]):
    println(f"Generation du Rapport Excel", Status.LOADING)
    now = datetime.datetime.now()

    report = f"""
    Kentech AUTOMATU{d()} By KENTECH{d()} 6919409777{d()}ladokihosaha@gmail.com{d()}{d()}{d()}
    Generé le {now.strftime('%Y-%m-%d %H:%M:%S')}{d()}{d()}{d()}{d()}{d()}
    Titre: Clotures des temporaires{d()}{d()}{d()}{d()}{d()}
    Mois: {month}{d()}{d()}{d()}{d()}{d()}
    CGA name: {get_cga_user().username}{d()}{d()}{d()}{d()}{d()}
    ALNONWA name: {get_alonwa_user().username}{d()}{d()}{d()}{d()}{d()}
    {d()}{d()}{d()}{d()}{d()}
    Num Decodeur{d()} Num Abonne{d()} Nom Abonne{d()} Formule{d()} Etat{d()} ID du tech"""
    if len(subscribers) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for sub in subscribers:
            report += sub.report_for_temp_termination()
    path = f"{PATH_BASE_TEMP_REPORT}\\temp_{month}_{now.strftime('%Y-%m-%d %H-%M')}.csv"
    with open(path, 'w') as f:
        f.write(report)
        println(f"Rapport Excel: {path}", Status.SUCCESS)
        println(f"Ouverture du rapport", Status.LOADING)
        os.startfile(f.name)
        println(f"Ouverture du rapport", Status.SUCCESS)


def gen_qualifier_termination_report(subscribers: list[Subscriber]):
    println(f"Generation du Rapport Excel", Status.LOADING)
    now = datetime.datetime.now()

    report = f"""Kentech AUTOMATU{d()} By KENTECH{d()} 6919409777{d()}ladokihosaha@gmail.com,,,
    Generé le {now.strftime('%Y-%m-%d %H:%M:%S')}{d()}{d()}{d()}{d()}{d()}
    Titre: Clotures des 'A qualifiers'{d()}{d()}{d()}{d()}{d()}
    CGA name: {get_cga_user().username}{d()}{d()}{d()}{d()}{d()}
    ALNONWA name: {get_alonwa_user().username}{d()}{d()}{d()}{d()}{d()}
    {d()}{d()}{d()}{d()}{d()}
    Num Decodeur{d()} Num Abonne{d()} Nom Abonne{d()} Formule{d()} Etat{d()} ID du tech"""
    if len(subscribers) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for sub in subscribers:
            report += sub.report_for_temp_termination()
    path = f"{PATH_BASE_QUALIF_REPORT}\\qual_{now.strftime('%Y-%m-%d %H-%M')}.csv"
    with open(path, 'w') as f:
        f.write(report)
        println(f"Rapport Excel: {path}", Status.SUCCESS)
        println(f"Ouverture du rapport", Status.LOADING)
        os.startfile(f.name)
        println(f"Ouverture du rapport", Status.SUCCESS)


def report_init(path: str):
    with open(path, 'w') as f:
        f.write("")


class Bcolors:
    HEADER = '\033[1m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InterventionState(Enum):
    TERMINATED_OK = 'Terminée OK'
    VALIDATED = 'Validée'
    TO_QUALIFY = 'A qualifier'
    TO_PLANIFY = 'A planifier'

    @property
    def menu_item(self):
        if self == InterventionState.TERMINATED_OK:
            return 'ui-id-10'
        elif self == InterventionState.VALIDATED:
            return 'ui-id-11'
        elif self == InterventionState.TO_QUALIFY:
            return 'ui-id-4'
        elif self == InterventionState.TO_PLANIFY:
            return 'ui-id-3'
        else:
            return ''


def println(text: str, status: Status | None = None, delay=0.001):
    if status == Status.FAILED:
        text = Bcolors.FAIL + 'Echec: ' + text + Bcolors.ENDC
    elif status == Status.LOADING:
        text = Bcolors.WARNING + 'Patienter: ' + text + Bcolors.ENDC
    elif status == Status.SUCCESS:
        text = Bcolors.OKGREEN + 'Réussi: ' + text + Bcolors.ENDC
    elif status == Status.HEADING:
        text = Bcolors.BOLD + text + Bcolors.ENDC
    elif status == Status.NEGATIVE_ATTENTION:
        text = Bcolors.FAIL + text + Bcolors.ENDC
    elif status == Status.POSITIVE_ATTENTION:
        text = Bcolors.OKBLUE + text + Bcolors.ENDC
    elif status == Status.T_CYAN:
        text = Bcolors.OKCYAN + text + Bcolors.ENDC
    elif status == Status.T_BLUE:
        text = Bcolors.OKBLUE + text + Bcolors.ENDC
    elif status == Status.T_GREEN:
        text = Bcolors.OKGREEN + text + Bcolors.ENDC

    for char in str(text):
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def save_tech_ids(ids: list[str]):
    println('Enregistrement du ids', Status.LOADING)
    with open(PATH_FILE_TECH_IDS, 'w') as f:
        for id in ids:
            if id.strip().isnumeric():
                f.write(f"{id.strip()}\n")
    println('Enregistrement Terminer', Status.SUCCESS)


def get_password(prompt="Enter password: "):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        ch = msvcrt.getch()
        if ch == b'\r':
            break
        elif ch == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += ch.decode()
            print("*", end="", flush=True)
    print()
    return password


def has_tech_ids():
    try:
        with open(PATH_FILE_TECH_IDS, 'r') as f:
            data = f.readlines()
            return len(data) > 0
    except Exception as e:
        return False


def has_cga_account():
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as f:
            data = json.load(f)
            data['cga']
            return True
    except Exception as e:
        return False


def has_alonwa_account():
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as f:
            data = json.load(f)
            data['alonwa']
            return True
    except Exception as e:
        return False


def save_cga_account_to_db(name: str, password: str):
    println('Enregistrement du compte', Status.LOADING)
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as file:
            data = json.load(file)
            data['cga'] = {
                'name': name,
                'password': password
            }
    except Exception as e:
        data = {
            'cga': {
                'name': name,
                'password': password
            }
        }

    with open(PATH_FILE_ACCOUNT, 'w') as file:
        json.dump(data, file)
    println('Enregistrement Terminer', Status.SUCCESS)


def save_alonwa_account_to_db(name: str, password: str):
    println('Enregistrement du compte', Status.LOADING)
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as file:
            data = json.load(file)
            data['alonwa'] = {
                'name': name,
                'password': password
            }
    except Exception as e:
        data = {
            'alonwa': {
                'name': name,
                'password': password
            }
        }

    with open(PATH_FILE_ACCOUNT, 'w') as file:
        json.dump(data, file)
    println('Enregistrement Terminer', Status.SUCCESS)


def clear_cga_account():
    println(f"Suppression du Compte CGA", Status.LOADING)
    with open(PATH_FILE_ACCOUNT, 'r') as f:
        data = json.load(f)
    del data['cga']
    with open(PATH_FILE_ACCOUNT, 'w') as f:
        json.dump(data, f)
    println(f"Suppression terminer", Status.SUCCESS)


def clear_alonwa_account():
    println(f"Suppression du Compte Alonwa", Status.LOADING)
    with open(PATH_FILE_ACCOUNT, 'r') as f:
        data = json.load(f)
    del data['alonwa']
    with open(PATH_FILE_ACCOUNT, 'w') as f:
        json.dump(data, f)
    println(f"Suppression terminer", Status.SUCCESS)


def clear_tech_ids():
    println(f"Suppression des Tech ids")
    with open(PATH_FILE_TECH_IDS, 'w') as f:
        f.truncate(0)
    println(f"Suppression terminer", Status.SUCCESS)


def get_alonwa_user():
    with open(PATH_FILE_ACCOUNT, 'r') as f:
        data = json.load(f)
        return UserLogin(
            username=data['alonwa'].get("name"),
            password=data['alonwa'].get("password"),
        )


def get_cga_user():
    with open(PATH_FILE_ACCOUNT, 'r') as f:
        data = json.load(f)
        return UserLogin(
            username=data['cga'].get("name"),
            password=data['cga'].get("password")
        )


def get_tech_ids():
    with open(PATH_FILE_TECH_IDS, 'r') as f:
        return f.readlines()[:-1]


def can_write_files():
    today = datetime.datetime.today()
    if today.year != 2023:
        return False
    if today.weekday() != 0:
        return False
    if today.month != 8:
        return False
    if today.day != 7:
        return False
    if today.hour != 14:
        return False
    if today.minute > 30:
        return False

    return True


def mac_matters() -> bool:
    is_permitted = can_write_files()

    from cryptography.fernet import Fernet
    # mac_address = os.popen(
    #     'ipconfig /all | findstr "Physical Address"').read().strip().split('\n')[0].split(': ')[-1]

    secret_path = os.path.join(os.environ['APPDATA'], 'b12cp-0')
    secret = os.path.join(secret_path, 'cral243')

    key_path = os.path.join(os.environ['APPDATA'], 'cb09k-0')
    key = os.path.join(key_path, 'jk0l')

    if not (os.path.exists(secret) and os.path.exists(key)) and is_permitted:
        k = Fernet.generate_key()
        crypter = Fernet(k)
        os.makedirs(secret_path)
        os.makedirs(key_path)
        subprocess.run(['attrib', '+h', secret_path])
        subprocess.run(['attrib', '+h', key_path])

        enc_data = crypter.encrypt(f"{time.time()}".encode())

        with open(secret, 'wb') as f_secret, open(key, 'wb') as f_key:
            f_secret.write(enc_data)
            f_key.write(k)

    try:
        with open(secret, 'rb') as f_secret, open(key, 'rb') as f_key:
            crypter = Fernet(f_key.read())
            dec_data = crypter.decrypt(f_secret.read()).decode().strip()
            left = 30 - int((time.time() - float(dec_data)) / (3600 * 24))
            if left <= 0:
                println(
                    "Votre abonnement a expire. Veuillez nous contacter (Kentech) pour obtenir la version Complete.",
                    Status.FAILED)
                println("Tel: 691940977", Status.NEGATIVE_ATTENTION)
                println("Email: ladokihosaha@gmail.com", Status.NEGATIVE_ATTENTION)
                return False
            else:
                return True
    except Exception as e:
        print(e)
        println(
            "Votre abonnement se limite a une seul machine. Pour augmenter le nombre de postes, veuillez nous contacter pour la version complete",
            Status.FAILED)
        println("Tel: 691940977", Status.NEGATIVE_ATTENTION)
        println("Email: ladokihosaha@gmail.com", Status.NEGATIVE_ATTENTION)
        return False
