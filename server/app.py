#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):

        response =make_response("<h1> hello world </h1>",200)
        return response
api.add_resource(Home,"/")

class NewsLetter(Resource):
    def get(self):
        newsletter =Newsletter.query.all()
        news_list=[ns.to_dict()for ns in newsletter]
        response =make_response(news_list,200)

        return response
    
    def post(self):
        newsletter =Newsletter(
            title =request.form["title"],
            body =request.form["body"]
            )
        
        db.session.add(newsletter)
        db.session.commit()
        response =make_response(newsletter.to_dict(),201)

        return response 
    
api.add_resource(NewsLetter,"/newsletter")


class NewsletterId(Resource):
    def get(self,id):
        newsletter=Newsletter.query.get(id)
        newsletter_dict =newsletter.to_dict()
        response =make_response(newsletter_dict,200)

        return response
    def patch(self,id):
        newsletter =Newsletter.query.get(id)

        for atr in request.form:
            setattr(newsletter,atr,request.form.get(atr))
        db.session.add(newsletter)
        db.session.commit()
        newsletter_dict=newsletter.to_dict()
        response=make_response(newsletter_dict,200)

        return response    
    def delete(self,id):
        newsletter =Newsletter.query.get(id)
        db.session.delete(newsletter)
        db.session.commit()
        message ={"item status":"deleted successfully"}
        response =make_response(message,200)
        return response

            

api.add_resource(NewsletterId,"/newsletter/<int:id>")




if __name__ == '__main__':
    app.run(port=5555, debug=True)
