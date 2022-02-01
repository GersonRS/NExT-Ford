def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/aula15'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
