# from controllers.receta import RecetaController
from flask import Flask
from conexion_bd import base_de_datos
from models.ingrediente import IngredienteModel
from models.receta import RecetaModel
from models.preparacion import PreparacionModel
from models.recetas_ingredientes import RecetaIngredienteModel
from models.log import LogModel

from controllers.ingrediente import (IngredientesController, 
                                    IngredienteController, 
                                    FiltroIngredientesControllers)
from controllers.preparacion import PreparacionesController
from controllers.receta import RecetasController,RecetaController
from controllers.receta_ingrediente import RecetaIngredientesController

from flask_restful import Api
from os import environ
from dotenv import load_dotenv
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
load_dotenv()

# CONFIGURACION SWAGGER FLASK

SWAGGER_URL = "/api/docs"

# indicar la ubicacion del archivo JSON
API_URL = "/static/swagger.json"
swagger_blueprint = get_swaggerui_blueprint(
    base_url=SWAGGER_URL,
    api_url=API_URL,
    config={
        'app_name': 'Reposteria Flask - Documentacion Swagger'
    }
)

# FIN DE CONFIGURACION

app = Flask(__name__)
#
app.register_blueprint(swagger_blueprint)


CORS(app=app, origin='*', methods=['GET','POST','PUT','DELETE'], allow_headers='Content-type')
api = Api(app=app)
#                                        mysql://username:password@host/db_name
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
# si se establece True SqlAchemy rastreara las modificaciones de los objetos (modelos) y lanzara señales de cambio, su valor predeterminado es None . igual habilita el tracking pero emite una advertencia que en futuras versiones se removera el valor x default None y si o si tendremos que indicar un valor inicial
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicia la conexion con la bd para darle las credenciales definidias en el app.config
base_de_datos.init_app(app)

# eliminara todas las tablas registradas en nuestro proyecto
# base_de_datos.drop_all(app=app)


# creara las tablas aun no mapeadas y si todo esta bien no devolvera nada
base_de_datos.create_all(app=app)


@app.route("/")
def initial_controller():
    return {
        "message": "Bienvenido a mi API de REPOSTERIA 🥧"
    }


# ZONA DE ENRUTAMIENTO
api.add_resource(IngredientesController, '/ingredientes', '/ingredientes/<int:id>')
api.add_resource(FiltroIngredientesControllers, '/buscar_ingrediente')
# api.add_resource(IngredienteController, '/ingrediente')
api.add_resource(IngredienteController, '/ingrediente/<int:id>')

api.add_resource(RecetasController, '/recetas')
api.add_resource(RecetaIngredientesController, '/recetas_ingredientes')
api.add_resource(RecetaController, '/receta/<int:id>')

api.add_resource(PreparacionesController, '/preparaciones', '/preparaciones/<int:id>')
if __name__ == '__main__':
    app.run(debug=True)