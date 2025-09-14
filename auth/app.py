from flask import Flask,jsonify
from extensions import db,jwt
from auth import auth_bp
from marshmallow import ValidationError,fields,Schema

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:root@host.docker.internal:3306/microservice"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["JWT_SECRET_KEY"]="super-secret-key" 

    @app.errorhandler(ValidationError)
    def handle_validation(e):
        return jsonify({"error": e.messages}), 400



    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp,url_prefix="/auth")

    with app.app_context():
        db.create_all()
    return app

if __name__=="__main__":
    app=create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)

