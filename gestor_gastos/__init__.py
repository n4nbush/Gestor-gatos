from flask import Blueprint

gastos_bp = Blueprint(
    'gastos',
    __name__,
    template_folder= '../templates',
    static_folder= '../static'
)

from . import routes