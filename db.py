import json
import uuid


from common import println, d, Status, PATH_FILE_ACCOUNT


# class AlonwaAccount:
#     def __init__(
#             self,
#             region: str,
#             name: str,
#             password: str,
#             account_id: str = str(uuid.uuid4()),
#             is_default: bool = False
#     ):
#         self.account_id = account_id
#         self.region = region
#         self.name = name
#         self.password = password
#         self.is_default = is_default
#
#     @property
#     def to_dict(self):
#         return {
#             'account_id': self.account_id,
#             'name': self.name,
#             'region': self.region,
#             'password': self.password
#         }
#
#     @property
#     def desc_str(self):
#         return f"Alonwa(Service+){d} Region: {self.region} {d} Nom: {self.name}"
#
#     def __str__(self):
#         return f"Region={self.region}, nom={self.name}, ID={self.account_id}"
#
#
# class CGAAccount:
#     def __init__(
#             self,
#             name: str,
#             password: str,
#             region: str,
#             account_id: str = str(uuid.uuid4()),
#             is_default: bool = False
#     ):
#         self.account_id = account_id
#         self.region = region,
#         self.name = name
#         self.password = password
#         self.is_default = is_default
#
#     @property
#     def to_dict(self):
#         return {
#             'account_id': self.account_id,
#             'region': self.region,
#             'name': self.name,
#             'password': self.password,
#             'is_default': self.is_default
#         }
#
#     @property
#     def desc_str(self):
#         return f"CGA {d} Region: {self.region} {d} Nom: {self.name}"
#
#     def __str__(self):
#         return f"nom={self.name} ID={self.account_id}"
#
#
# def dict_to_alonwa_account(data: dict[str, str], is_default: bool = False):
#     return AlonwaAccount(
#         account_id=data['account_id'],
#         region=data['region'],
#         name=data['name'],
#         password=data['password'],
#         is_default=is_default
#     )
#
#
# def dict_to_cga_account(data: dict[str, str], is_default: bool = False):
#     return CGAAccount(
#         account_id=data['account_id'],
#         name=data['name'],
#         password=data['password'],
#         region=data['region'],
#         is_default=is_default
#     )
#
#
# def save_alonwa_account_to_db(account: AlonwaAccount):
#     println('Enregistrement du compte ALONWA', Status.LOADING)
#     data = {}
#     try:
#         with open(PATH_FILE_ACCOUNT, 'r') as file:
#             # We update account
#             data = json.load(file)
#             data['alonwa'][account.account_id] = account.to_dict
#     except Exception as e:
#         if e == FileNotFoundError:
#             data = {
#                 'alonwa': {
#                     account.account_id: account.to_dict
#                 }
#             }
#         else:
#             data['cga'][account.account_id] = account.to_dict
#
#     with open(PATH_FILE_ACCOUNT, 'w') as file:
#         json.dump(data, file)
#     println('Enregistrement Terminer', Status.SUCCESS)
#
#
# def save_cga_account_to_db(account: CGAAccount):
#     println('Enregistrement du compte CGA', Status.LOADING)
#     data = {}
#     try:
#         with open(PATH_FILE_ACCOUNT, 'r') as file:
#             # We update account
#             data = json.load(file)
#             data['cga'][account.account_id] = account.to_dict
#     except Exception as e:
#         if e == FileNotFoundError:
#             data = {
#                 'cga': {
#                     account.account_id: account.to_dict
#                 }
#             }
#         else:
#             data['cga'][account.account_id] = account.to_dict
#
#     with open(PATH_FILE_ACCOUNT, 'w') as w_file:
#         json.dump(data, w_file)
#     println('Enregistrement Terminer', Status.SUCCESS)
#
#
# def delete_alonwa_account_from_db(account_id: str):
#     println('Suppression du compte ALONWA', Status.LOADING)
#     with open(PATH_FILE_ACCOUNT, 'r') as file:
#         # We update account
#         data = json.load(file)
#         data['alonwa'].pop(account_id)
#         if data['alonwa_default'] == account_id:
#             data['alonwa_default'] = ''
#
#     with open(PATH_FILE_ACCOUNT, 'w') as w_file:
#         json.dump(data, w_file)
#
#     println('Suppression Terminé', Status.SUCCESS)
#
#
# def delete_cga_account_from_db(account_id: str):
#     println('Suppression du compte CGA', Status.LOADING)
#     with open(PATH_FILE_ACCOUNT, 'r') as file:
#         # We update account
#         data = json.load(file)
#         data['cga'].pop(account_id)
#         if data['cga_default'] == account_id:
#             data['cga_default'] = ''
#
#     with open(PATH_FILE_ACCOUNT, 'w') as w_file:
#         json.dump(data, w_file)
#
#     println('Suppression Terminé', Status.SUCCESS)
#
#
# def set_default_alonwa_account(account_id: str):
#     println("Prioritisation d'un compte ALONWA", Status.LOADING)
#     with open(PATH_FILE_ACCOUNT, 'r') as file:
#         # We update account
#         data = json.load(file)
#         data['alonwa_default'] = account_id
#
#     with open(PATH_FILE_ACCOUNT, 'w') as w_file:
#         json.dump(data, w_file)
#
#     println('Prioritisation Terminé', Status.SUCCESS)
#
#
# def set_default_cga_account(account_id: str):
#     println("Prioritisation d'un compte CGA", Status.LOADING)
#     with open(PATH_FILE_ACCOUNT, 'r') as file:
#         # We update account
#         data = json.load(file)
#         data['cga_default'] = account_id
#
#     with open(PATH_FILE_ACCOUNT, 'w') as w_file:
#         json.dump(data, w_file)
#
#     println('Prioritisation  Terminé', Status.SUCCESS)
#
#
# def get_default_alonwa_account_id():
#     println('Recherche du compte ALONWA par defaut', Status.LOADING)
#     try:
#         with open(PATH_FILE_ACCOUNT, 'r') as file:
#             # We update account
#             data = json.load(file)
#             default = data['alonwa_default']
#
#     except Exception as e:
#         default = ''
#
#     if default != '':
#         println('Compte ALONWA par défaut trouvé', Status.SUCCESS)
#     else:
#         println('Compte ALONWA par défaut introuvable. Veuillez définir un', Status.FAILED)
#     return default
#
#
# def get_default_cga_account_id():
#     println('Recherche du compte CGA par défaut', Status.LOADING)
#     try:
#         with open(PATH_FILE_ACCOUNT, 'r') as file:
#             # We update account
#             data = json.load(file)
#             default = data['cga_default']
#     except Exception as e:
#         default = ''
#
#     if default != '':
#         println('Compte CGA par défaut trouvé', Status.SUCCESS)
#     else:
#         println('Compte CGA par défaut introuvable. Veuillez définir un', Status.FAILED)
#     return default
#
#
# def get_alonwa_accounts_from_db():
#     println('Récuperation des comptes ALONWA', Status.LOADING)
#     accounts = []
#     try:
#         with open(PATH_FILE_ACCOUNT, 'r') as file:
#             # We update account
#             data = json.load(file)
#             try:
#                 alonwa_default = data['alonwa_default']
#             except Exception as e:
#
#                 alonwa_default = ''
#             accounts = [dict_to_alonwa_account(data['alonwa'][account_id], alonwa_default == account_id) for account_id
#                         in data['alonwa']]
#     except Exception as e:
#         pass
#
#     if len(accounts) == 0:
#         println('Aucun comptes ALONWA trouvé. Veuillez en ajouter.', Status.FAILED)
#     else:
#         println(f'Comptes ALONWA trouvé: {len(accounts)}', Status.SUCCESS)
#     return accounts
#
#
# def get_cga_accounts_from_db():
#     println('Récuperation des comptes CGA', Status.LOADING)
#     accounts = []
#     try:
#         with open(PATH_FILE_ACCOUNT, 'r') as file:
#             # We update account
#             data = json.load(file)
#             try:
#                 cga_default = data['cga_default']
#             except Exception as e:
#
#                 cga_default = ''
#             accounts = [dict_to_cga_account(data['cga'][account_id], cga_default == account_id) for account_id in
#                         data['cga']]
#     except Exception as e:
#         pass
#     if len(accounts) == 0:
#         println('Aucun comptes CGA trouvé. Veuillez en ajouter.', Status.FAILED)
#     else:
#         println(f'Comptes CGA trouvé: {len(accounts)}', Status.SUCCESS)
#     return accounts
#
#
# def get_default_alonwa_account():
#     with open(PATH_FILE_ACCOUNT, 'r') as f:
#         data = json.load(f)
#         alonwa_default = data['alonwa_default']
#         return dict_to_alonwa_account(data['alonwa'][alonwa_default], True)
#
#
# def get_default_cga_account():
#     with open(PATH_FILE_ACCOUNT, 'r') as f:
#         data = json.load(f)
#         cga_default = data['cga_default']
#         return dict_to_alonwa_account(data['cga'][cga_default], True)
#
# # delete_alonwa_account_from_db('d03495d4-8146-4b4b-9361-866e079e8d76')
# # get_alonwa_accounts_from_db()
# # print(save_alonwa_account_to_db(AlonwaAccount("Centre", "TAKIAMPI", "JOES")))
