from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OFFERS_PATH = BASE_DIR.joinpath('json_files', 'offers.json')
ORDERS_PATH = BASE_DIR.joinpath('json_files', 'orders.json')
USERS_PATH = BASE_DIR.joinpath('json_files', 'users.json')
