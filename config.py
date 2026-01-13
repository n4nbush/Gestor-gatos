import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # base de datos
    DATABASE_FOLDER = os.path.join(BASE_DIR,'data_base')
    DATABASE = os.path.join(DATABASE_FOLDER,'gastos.db')

    BACKUP_FOLDER = os.path.join(BASE_DIR,'gestor_gastos/backup')
    BACKUP = os.path.join(BACKUP_FOLDER,)