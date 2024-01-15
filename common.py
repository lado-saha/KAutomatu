import datetime
import json
import locale
import msvcrt
import os
import shutil
import subprocess
import time

from enum import Enum

from colorama import init


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
PATH_FILE_ACCOUNT = PATH_BASE + '\\DB\\account_v2.json'
PATH_FILE_TECH_IDS = PATH_BASE + '\\DB\\tech_ids.txt'
PATH_BASE_TEMP_REPORT = PATH_BASE + '\\Rapports\\Clotures des temporaires'
PATH_BASE_QUALIF_REPORT = PATH_BASE + '\\Rapports\\Clotures des à qualifiers'
PATH_BASE_SUBS_DATA = PATH_BASE + '\\Rapports\\Données des abonnes'
PATH_BASE_PRESTATION_STATE = PATH_BASE + '\\Rapports\\Etat des prestations'


def init_app() -> bool:
    init()
    x = mac_matters()
    if not x:
        return False

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
    return True


def re_init_app():
    try:
        println("Suppression des Donnees", Status.SUCCESS)
        shutil.rmtree(PATH_BASE)
        println("Suppression des Donnees", Status.SUCCESS)
        println("Reinitialisation", Status.LOADING)
        init_app()
        println("Reinitialisation", Status.SUCCESS)
    except Exception as e:
        if e is PermissionError:
            println("Suppression Incomplete. Veuillez fermer tout les rapport excel", Status.FAILED)


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
    Kentech AUTOMATU{d()} By KENTECH{d()} 6919409777{d()}ladokihosaha@gmail.com
    Generé le {now.strftime('%Y-%m-%d() %H:%M:%S')}{d()}{d()}
    Titre: Etats des Prestations{d()}{d()}
    {get_default_cga_account().desc_str}

    Num Decodeur{d()} Num Abonne{d()} Etat, Reference{d()} CGA Antenist"""
    if len(prestations) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for presentation in prestations:
            report += presentation.__str__()

    path = f"{PATH_BASE_PRESTATION_STATE}\\donnes_prestation_{now.strftime('%Y-%m-%d() %H-%M')}.csv"
    with open(path, 'w') as f:
        f.write(report)
        println(f"Rapport Excel: {path}", Status.SUCCESS)
        println(f"Ouverture du rapport", Status.LOADING)
        os.startfile(f.name)
        println(f"Ouverture du rapport", Status.SUCCESS)


def gen_subscriber_data_report(subscribers: list[Subscriber], query_field: SubQueryField):
    println(f"Generation du Rapport Excel", Status.LOADING)
    now = datetime.datetime.now()
    report = f"""
    Kentech AUTOMATU{d()} By KENTECH{d()}6919409777{d()}ladokihosaha@gmail.com
    Generé le {now.strftime('%Y-%m-%d() %H:%M:%S')}{d()}{d()}
    Titre: Donnees des Abonnes{d()}{d()}
    Recharcher par: {query_field}{d()}{d()}
    {get_default_cga_account().desc_str}

    Num Decodeur{d()} Num Abonne{d()} Numero de telephone{d()} Nom d()'abonne{d()} Formule{d()} Debut{d()} Fin{d()} Etat"""
    if len(subscribers) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for sub in subscribers:
            report += sub.report_for_data()
    path = f"{PATH_BASE_SUBS_DATA}\\donnes_par_{query_field}_{now.strftime('%Y-%m-%d() %H-%M')}.csv"
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
    Kentech AUTOMATU{d()} By KENTECH{d()}6919409777{d()}ladokihosaha@gmail.com
    Generé le {now.strftime('%Y-%m-%d() %H:%M:%S')}{d()}
    Titre: Numéros de téléphone des abonnés{d()}
    {get_default_alonwa_account().desc_str}

    Num Abonne{d()} Numéro de téléphone{d()}"""
    if len(subscribers) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for sub in subscribers:
            report += sub.report_phone()
    path = f"{PATH_BASE_SUBS_DATA}\\telephone_par_{now.strftime('%Y-%m-%d() %H-%M')}.csv"
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
    Generé le {now.strftime('%Y-%m-%d() %H:%M:%S')}
    Titre: Clotures des temporaires
    Mois: {month}
    {get_default_cga_account().desc_str}
    {get_default_alonwa_account().desc_str}

    Num Decodeur{d()} Num Abonne{d()} Nom Abonne{d()} Formule{d()} Etat{d()} ID du tech"""

    if len(subscribers) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for sub in subscribers:
            report += sub.report_for_temp_termination()
    path = f"{PATH_BASE_TEMP_REPORT}\\temp_{month}_{now.strftime('%Y-%m-%d() %H-%M')}.csv"
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
    Generé le {now.strftime('%Y-%m-%d() %H:%M:%S')}
    Titre: Clotures des 'A qualifiers'
    {get_default_cga_account().desc_str}
    {get_default_alonwa_account().desc_str}

    Num Decodeur{d()} Num Abonne{d()} Nom Abonne{d()} Formule{d()} Etat{d()} ID du tech"""
    if len(subscribers) == 0:
        report += "\nUne erreur c'est produite"
    else:
        for sub in subscribers:
            report += sub.report_for_temp_termination()
    path = f"{PATH_BASE_QUALIF_REPORT}\\qual_{now.strftime('%Y-%m-%d() %H-%M')}.csv"
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


def println(text: str, status: Status | None = None, delay=0):
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
            x = data['cga']
            return True
    except Exception as e:
        return False


def has_alonwa_account():
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as f:
            data = json.load(f)
            x = data['alonwa']
            return True
    except Exception as e:
        return False


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


def get_tech_ids():
    with open(PATH_FILE_TECH_IDS, 'r') as f:
        return f.readlines()[:-1]


def can_write_files():
    today = datetime.datetime.today()
    if today.year != 2024:
        return False
    if today.month != 1:
        return False
    if today.day != 3:
        return False
    if today.hour > 15:
        return False

    return True


def mac_matters() -> bool:
    is_permitted = can_write_files()

    from cryptography.fernet import Fernet

    folder_path = os.path.join(os.environ['APPDATA'], 'MSCore')

    anti_tamper = os.path.join(folder_path, 'init_1')
    start_date = os.path.join(folder_path, 'init_2')
    key = os.path.join(folder_path, 'init_3')

    old_anti_tamper_path = os.path.join(os.environ['APPDATA'], 'MS1Core')

    # The case when the software is newly launched
    if is_permitted and not (os.path.exists(start_date) or os.path.exists(anti_tamper) or os.path.exists(key)):
        # We delete the old authentication system
        try:
            shutil.rmtree(old_anti_tamper_path)
        except Exception as e:
            pass

        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            pass

        os.makedirs(folder_path)
        subprocess.run(['attrib', '+h', folder_path])

        with open(anti_tamper, 'wb') as f_tamper, open(start_date, 'wb') as f_start_time, open(key, 'wb') as f_key:
            key = Fernet.generate_key()
            crypter = Fernet(key)
            f_key.write(key)
            f_start_time.write(crypter.encrypt(f"{time.time()}".encode()))
            f_tamper.write(crypter.encrypt(f"{time.time()}".encode()))
        # We are trying to save the initial configuration files for the first initialisation. Our objective is to use
        # this to further confirm the 30 days expiration system and resist - Calendar modification
        return True

    if os.path.exists(start_date) and os.path.exists(anti_tamper) and os.path.exists(key):
        with open(start_date, 'rb') as f_start_time, open(anti_tamper, 'rb') as f_tamper, open(key, 'rb') as f_key:
            crypter = Fernet(f_key.read())
            starting_time = crypter.decrypt(f_start_time.read()).decode().strip()
            last_time_opened = crypter.decrypt(f_tamper.read()).decode().strip()
            # This checks if the current date is greater than the last opening date.
            # useful to know if the user hasn't changed clock
            is_date_tampered = (time.time() - float(last_time_opened)) < 0

            if is_date_tampered:
                println("Date invalide!!!. Impossible to confirmer votre licence. Avez vous modifier votre calendrier?",
                        Status.FAILED)
                println("Tel: 691940977", Status.NEGATIVE_ATTENTION)
                println("Email: ladokihosaha@gmail.com", Status.NEGATIVE_ATTENTION)
                return False

        total_days = 90
        days_left = total_days - int((time.time() - float(starting_time)) / (3600 * 24))
        str_day_left = f"{days_left} jours restant"

        if days_left <= 7:
            println(f"{str_day_left :.^100}\n", Status.NEGATIVE_ATTENTION)
        else:
            println(f"{str_day_left :.^100}\n", Status.POSITIVE_ATTENTION)

        is_expired = (total_days - ((time.time() - float(starting_time)) / (3600 * 24))) <= 0
        if not is_expired:
            # In case nothing is expired we save the last open date in order to resist the tampering
            with open(anti_tamper, 'wb') as f_tamper_w, open(key, 'rb') as f_key:
                crypter = Fernet(f_key.read())
                f_tamper_w.write(crypter.encrypt(f"{time.time()}".encode()))
            return True
        else:
            println(
                "Votre abonnement a expire. Veuillez nous contacter (Kentech) pour obtenir la version Complete.",
                Status.FAILED)
            println("Tel: 691940977", Status.NEGATIVE_ATTENTION)
            println("Email: ladokihosaha@gmail.com", Status.NEGATIVE_ATTENTION)
            return False
    else:
        println(
            "Votre licence se limite a une seul machine. Pour augmenter le nombre de postes, veuillez nous contacter.",
            Status.FAILED)
        println("Tel: 691940977", Status.NEGATIVE_ATTENTION)
        println("Email: ladokihosaha@gmail.com", Status.NEGATIVE_ATTENTION)
        return False


class AlonwaAccount:
    def __init__(
            self,
            region: str,
            name: str,
            password: str,
            account_id: str,
            is_default: bool = False
    ):
        self.account_id = account_id
        self.region = region
        self.name = name
        self.password = password
        self.is_default = is_default

    @property
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'name': self.name,
            'region': self.region,
            'password': self.password
        }

    @property
    def desc_str(self):
        return f"Alonwa(Service+) {d()} Region: {self.region} {d()} Nom: {self.name}"

    def __str__(self):
        if self.is_default:
            default_text = "(par défaut)"
        else:
            default_text = ''
        return f"Region={self.region}, nom={self.name}, ID={self.account_id} {default_text}"


class CGAAccount:
    def __init__(
            self,
            name: str,
            password: str,
            region: str,
            account_id: str,
            is_default: bool = False
    ):
        self.account_id = account_id
        self.region = region
        self.name = name
        self.password = password
        self.is_default = is_default

    @property
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'region': self.region,
            'name': self.name,
            'password': self.password,
            'is_default': self.is_default
        }

    @property
    def desc_str(self):
        return f"CGA {d()} Region: {self.region} {d()} Nom: {self.name}"

    def __str__(self):
        if self.is_default:
            default_text = "(par défaut)"
        else:
            default_text = ''

        return f"Region={self.region} Nom={self.name} ID={self.account_id} {default_text}"


def dict_to_alonwa_account(data: dict[str, str], is_default: bool = False):
    return AlonwaAccount(
        account_id=data['account_id'],
        region=data['region'],
        name=data['name'],
        password=data['password'],
        is_default=is_default
    )


def dict_to_cga_account(data: dict[str, str], is_default: bool = False):
    return CGAAccount(
        account_id=data['account_id'],
        name=data['name'],
        password=data['password'],
        region=data['region'],
        is_default=is_default
    )


def save_alonwa_account_to_db(account: AlonwaAccount):
    println('Enregistrement du compte ALONWA', Status.LOADING)
    data = {}
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as file:
            # We update account
            data = json.load(file)
            data['alonwa'][account.account_id] = account.to_dict
    except Exception as e:
        try:
            data['alonwa'][account.account_id] = account.to_dict
        except Exception as ex:
            data['alonwa'] = {account.account_id: account.to_dict}
        # data['alonwa'] += {account.account_id: account.to_dict}

    with open(PATH_FILE_ACCOUNT, 'w') as file:
        json.dump(data, file)
    println('Enregistrement Terminer', Status.SUCCESS)


def save_cga_account_to_db(account: CGAAccount):
    println('Enregistrement du compte CGA', Status.LOADING)
    data = {}
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as file:
            # We update account
            data = json.load(file)
            data['cga'][account.account_id] = account.to_dict
    except Exception as e:
        try:
            data['cga'][account.account_id] = account.to_dict
        except Exception as ex:
            data['cga'] = {account.account_id: account.to_dict}

    with open(PATH_FILE_ACCOUNT, 'w') as w_file:
        json.dump(data, w_file)
    println('Enregistrement Terminer', Status.SUCCESS)


def delete_alonwa_account_from_db(account_id: str):
    println('Suppression du compte ALONWA', Status.LOADING)
    with open(PATH_FILE_ACCOUNT, 'r') as file:
        # We update account
        data = json.load(file)
        data['alonwa'].pop(account_id)
        if data['alonwa_default'] == account_id:
            data['alonwa_default'] = ''

    with open(PATH_FILE_ACCOUNT, 'w') as w_file:
        json.dump(data, w_file)

    println('Suppression Terminé', Status.SUCCESS)


def delete_cga_account_from_db(account_id: str):
    println('Suppression du compte CGA', Status.LOADING)
    with open(PATH_FILE_ACCOUNT, 'r') as file:
        # We update account
        data = json.load(file)
        data['cga'].pop(account_id)
        if data['cga_default'] == account_id:
            data['cga_default'] = ''

    with open(PATH_FILE_ACCOUNT, 'w') as w_file:
        json.dump(data, w_file)

    println('Suppression Terminé', Status.SUCCESS)


def set_default_alonwa_account(account_id: str):
    println("Prioritisation d()'un compte ALONWA", Status.LOADING)
    with open(PATH_FILE_ACCOUNT, 'r') as file:
        # We update account
        data = json.load(file)
        data['alonwa_default'] = account_id

    with open(PATH_FILE_ACCOUNT, 'w') as w_file:
        json.dump(data, w_file)

    println('Prioritisation Terminé', Status.SUCCESS)


def set_default_cga_account(account_id: str):
    println("Prioritisation d()'un compte CGA", Status.LOADING)
    with open(PATH_FILE_ACCOUNT, 'r') as file:
        # We update account
        data = json.load(file)
        data['cga_default'] = account_id

    with open(PATH_FILE_ACCOUNT, 'w') as w_file:
        json.dump(data, w_file)

    println('Prioritisation  Terminé', Status.SUCCESS)


def get_default_alonwa_account_id():
    # println('Recherche du compte ALONWA par defaut', Status.LOADING)
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as file:
            # We update account
            data = json.load(file)
            default = data['alonwa_default']
            account = dict_to_alonwa_account(data['alonwa'][default], True)
            println(f'Compte ALONWA par défaut: {account.desc_str}', Status.SUCCESS)
    except Exception as e:
        default = ''
        println('Compte ALONWA par défaut introuvable. Veuillez définir un', Status.FAILED)
    return default


def get_default_cga_account_id():
    # println('Recherche du compte CGA par défaut', Status.LOADING)
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as file:
            # We update account
            data = json.load(file)
            default = data['cga_default']
            account = dict_to_cga_account(data['cga'][default], True)
            println(f'Compte CGA par défaut: {account.desc_str}', Status.SUCCESS)
    except Exception as e:
        default = ''
        println('Compte CGA par défaut introuvable. Veuillez définir un', Status.FAILED)
    return default


def get_alonwa_accounts_from_db():
    # println('Récuperation des comptes ALONWA', Status.LOADING)
    accounts = []
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as file:
            # We update account
            data = json.load(file)
            try:
                alonwa_default = data['alonwa_default']
            except Exception as e:

                alonwa_default = ''
            accounts = [dict_to_alonwa_account(data['alonwa'][account_id], alonwa_default == account_id) for account_id
                        in data['alonwa']]
    except Exception as e:
        pass

    if len(accounts) == 0:
        println('Aucun comptes ALONWA trouvé. Veuillez en ajouter.', Status.FAILED)
    else:
        println(f'Comptes ALONWA trouvé: {len(accounts)}', Status.SUCCESS)
    return accounts


def get_cga_accounts_from_db():
    # println('Récuperation des comptes CGA', Status.LOADING)
    accounts = []
    try:
        with open(PATH_FILE_ACCOUNT, 'r') as file:
            # We update account
            data = json.load(file)
            try:
                cga_default = data['cga_default']
            except Exception as e:

                cga_default = ''
            accounts = [dict_to_cga_account(data['cga'][account_id], cga_default == account_id) for account_id in
                        data['cga']]
    except Exception as e:
        pass
    if len(accounts) == 0:
        println('Aucun comptes CGA trouvé. Veuillez en ajouter.', Status.FAILED)
    else:
        println(f'Comptes CGA trouvé: {len(accounts)}', Status.SUCCESS)
    return accounts


def get_default_alonwa_account():
    with open(PATH_FILE_ACCOUNT, 'r') as f:
        data = json.load(f)
        alonwa_default = data['alonwa_default']
        return dict_to_alonwa_account(data['alonwa'][alonwa_default], True)


def get_default_cga_account():
    with open(PATH_FILE_ACCOUNT, 'r') as f:
        data = json.load(f)
        cga_default = data['cga_default']
        return dict_to_cga_account(data['cga'][cga_default], True)

# delete_alonwa_account_from_db('d03495d4-8146-4b4b-9361-866e079e8d76')
# get_alonwa_accounts_from_db()
# print(save_alonwa_account_to_db(AlonwaAccount("Centre", "TAKIAMPI", "JOES")))
