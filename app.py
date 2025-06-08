from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
import time
from models import SessionLocal, Contato, Denuncia, Evento, Informacao, User, create_tables

app = Flask(__name__)
api = Api(app)
CORS(app)

# Dependência do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

with app.app_context():
    create_tables()

# --- Recursos para Contatos ---
class ContatoListResource(Resource):
    def get(self):
        db = next(get_db())
        contatos = db.query(Contato).order_by(Contato.created_at.desc()).all()
        return jsonify([
            {
                "id": c.id,
                "title": c.title,
                "descricao": c.descricao,
                "local": c.local,
                "telefone": c.telefone,
                "email": c.email,
                "created_at": c.created_at
            } for c in contatos
        ])

    def post(self):
        db = next(get_db())
        data = request.get_json()
        if not data or not data.get("title") or not data.get("descricao"):
            return {"message": "Título e descrição são obrigatórios."}, 400

        try:
            new_contato = Contato(
                title=data["title"],
                descricao=data["descricao"],
                local=data.get("local"),
                telefone=data.get("telefone"),
                email=data.get("email"),
                created_at=int(time.time() * 1000) 
            )
            db.add(new_contato)
            db.commit()
            db.refresh(new_contato)
            return {
                "id": new_contato.id,
                "title": new_contato.title,
                "descricao": new_contato.descricao,
                "local": new_contato.local,
                "telefone": new_contato.telefone,
                "email": new_contato.email,
                "created_at": new_contato.created_at
            }, 201
        except IntegrityError:
            db.rollback()
            return {"message": "Já existe um contato com este título."}, 409
        except Exception as e:
            db.rollback()
            return {"message": f"Erro ao adicionar contato: {str(e)}"}, 500

class ContatoResource(Resource):
    def get(self, contato_id):
        db = next(get_db())
        contato = db.query(Contato).filter(Contato.id == contato_id).first()
        if not contato:
            return {"message": "Contato não encontrado."}, 404
        return {
            "id": contato.id,
            "title": contato.title,
            "descricao": contato.descricao,
            "local": contato.local,
            "telefone": contato.telefone,
            "email": contato.email,
            "created_at": contato.created_at
        }

    def put(self, contato_id):
        db = next(get_db())
        contato = db.query(Contato).filter(Contato.id == contato_id).first()
        if not contato:
            return {"message": "Contato não encontrado."}, 404

        data = request.get_json()
        if not data:
            return {"message": "Corpo da requisição vazio."}, 400

        try:
            if "title" in data:
                contato.title = data["title"]
            if "descricao" in data:
                contato.descricao = data["descricao"]
            if "local" in data:
                contato.local = data["local"]
            if "telefone" in data:
                contato.telefone = data["telefone"]
            if "email" in data:
                contato.email = data["email"]
            
            db.commit()
            db.refresh(contato)
            return {
                "id": contato.id,
                "title": contato.title,
                "descricao": contato.descricao,
                "local": contato.local,
                "telefone": contato.telefone,
                "email": contato.email,
                "created_at": contato.created_at
            }
        except IntegrityError:
            db.rollback()
            return {"message": "Já existe um contato com este título."}, 409
        except Exception as e:
            db.rollback()
            return {"message": f"Erro ao atualizar contato: {str(e)}"}, 500

    def delete(self, contato_id):
        db = next(get_db())
        contato = db.query(Contato).filter(Contato.id == contato_id).first()
        if not contato:
            return {"message": "Contato não encontrado."}, 404
        
        db.delete(contato)
        db.commit()
        return {"message": "Contato deletado com sucesso."}, 204

# --- Recursos para Denuncias ---
class DenunciaListResource(Resource):
    def get(self):
        db = next(get_db())
        denuncias = db.query(Denuncia).order_by(Denuncia.createdAt.desc()).all()
        return jsonify([
            {
                "id": d.id,
                "nome": d.nome,
                "identificar": d.identificar,
                "motivo": d.motivo,
                "descricao": d.descricao,
                "agressor": d.agressor,
                "createdAt": d.createdAt
            } for d in denuncias
        ])

    def post(self):
        db = next(get_db())
        data = request.get_json()
        if not data or not all(k in data for k in ["identificar", "motivo", "descricao", "createdAt"]):
            return {"message": "Campos obrigatórios (identificar, motivo, descricao, createdAt) ausentes."}, 400

        try:
            new_denuncia = Denuncia(
                nome=data.get("nome"),
                identificar=bool(data["identificar"]), # Converte para booleano
                motivo=data["motivo"],
                descricao=data["descricao"],
                agressor=data.get("agressor"),
                createdAt=data["createdAt"]
            )
            db.add(new_denuncia)
            db.commit()
            db.refresh(new_denuncia)
            return {
                "id": new_denuncia.id,
                "nome": new_denuncia.nome,
                "identificar": new_denuncia.identificar,
                "motivo": new_denuncia.motivo,
                "descricao": new_denuncia.descricao,
                "agressor": new_denuncia.agressor,
                "createdAt": new_denuncia.createdAt
            }, 201
        except Exception as e:
            db.rollback()
            return {"message": f"Erro ao salvar denúncia: {str(e)}"}, 500

class EventoListResource(Resource):
    def get(self):
        db = next(get_db())
        eventos = db.query(Evento).order_by(Evento.created_at.desc()).all()
        return jsonify([
            {
                "id": e.id,
                "title": e.title,
                "descricao": e.descricao,
                "local": e.local,
                "data": e.data,
                "created_at": e.created_at
            } for e in eventos
        ])

    def post(self):
        db = next(get_db())
        data = request.get_json()
        if not data or not data.get("title") or not data.get("descricao") or not data.get("data"):
            return {"message": "Título, descrição e data do evento são obrigatórios."}, 400

        try:
            new_evento = Evento(
                title=data["title"],
                descricao=data["descricao"],
                local=data.get("local"),
                data=data["data"],
                created_at=int(time.time() * 1000)
            )
            db.add(new_evento)
            db.commit()
            db.refresh(new_evento)
            return {
                "id": new_evento.id,
                "title": new_evento.title,
                "descricao": new_evento.descricao,
                "local": new_evento.local,
                "data": new_evento.data,
                "created_at": new_evento.created_at
            }, 201
        except IntegrityError:
            db.rollback()
            return {"message": "Já existe um evento com este título."}, 409
        except Exception as e:
            db.rollback()
            return {"message": f"Erro ao adicionar evento: {str(e)}"}, 500

# Adicione esta NOVA CLASSE para lidar com operações em um único evento (GET, PUT, DELETE)
class EventoResource(Resource):
    def get(self, evento_id):
        db = next(get_db())
        evento = db.query(Evento).filter(Evento.id == evento_id).first()
        if not evento:
            return {"message": "Evento não encontrado."}, 404
        return {
            "id": evento.id,
            "title": evento.title,
            "descricao": evento.descricao,
            "local": evento.local,
            "data": evento.data,
            "created_at": evento.created_at
        }

    def put(self, evento_id):
        db = next(get_db())
        evento = db.query(Evento).filter(Evento.id == evento_id).first()
        if not evento:
            return {"message": "Evento não encontrado."}, 404

        data = request.get_json()
        if not data:
            return {"message": "Corpo da requisição vazio."}, 400

        try:
            if "title" in data:
                evento.title = data["title"]
            if "descricao" in data:
                evento.descricao = data["descricao"]
            if "local" in data:
                evento.local = data["local"]
            if "data" in data:
                evento.data = data["data"] 
            
            db.commit()
            db.refresh(evento)
            return {
                "id": evento.id,
                "title": evento.title,
                "descricao": evento.descricao,
                "local": evento.local,
                "data": evento.data,
                "created_at": evento.created_at
            }
        except IntegrityError:
            db.rollback()
            return {"message": "Já existe um evento com este título."}, 409
        except Exception as e:
            db.rollback()
            return {"message": f"Erro ao atualizar evento: {str(e)}"}, 500

    def delete(self, evento_id):
        db = next(get_db())
        evento = db.query(Evento).filter(Evento.id == evento_id).first()
        if not evento:
            return {"message": "Evento não encontrado."}, 404
        
        db.delete(evento)
        db.commit()
        return {"message": "Evento deletado com sucesso."}, 204 # 204 No Content para deleção bem-sucedida
class InformacaoListResource(Resource):
    def get(self):
        db = next(get_db())
        informacoes = db.query(Informacao).order_by(Informacao.created_at.desc()).all()
        return jsonify([
            {
                "id": i.id,
                "title": i.title,
                "descricao": i.descricao,
                "created_at": i.created_at
            } for i in informacoes
        ])

    def post(self):
        db = next(get_db())
        data = request.get_json()
        if not data or not data.get("title") or not data.get("descricao"):
            return {"message": "Título e descrição são obrigatórios."}, 400

        try:
            new_informacao = Informacao(
                title=data["title"],
                descricao=data["descricao"],
                created_at=int(time.time() * 1000)
            )
            db.add(new_informacao)
            db.commit()
            db.refresh(new_informacao)
            return {
                "id": new_informacao.id,
                "title": new_informacao.title,
                "descricao": new_informacao.descricao,
                "created_at": new_informacao.created_at
            }, 201
        except IntegrityError:
            db.rollback()
            return {"message": "Já existe uma informação com este título."}, 409
        except Exception as e:
            db.rollback()
            return {"message": f"Erro ao adicionar informação: {str(e)}"}, 500

# --- Recursos para Usuários (Autenticação/Registro) ---
class UserRegisterResource(Resource):
    def post(self):
        db = next(get_db())
        data = request.get_json()
        if not data or not all(k in data for k in ["username", "password", "name", "cargo"]):
            return {"message": "Todos os campos (username, password, name, cargo) são obrigatórios."}, 400

        try:
            existing_user = db.query(User).filter(User.username == data["username"]).first()
            if existing_user:
                return {"message": "Usuário já existe."}, 409

            new_user = User(
                username=data["username"],
                password=data["password"], # Em produção, use hashing de senhas (ex: bcrypt)
                name=data["name"],
                cargo=data["cargo"]
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {
                "id": new_user.id,
                "username": new_user.username,
                "name": new_user.name,
                "cargo": new_user.cargo
            }, 201
        except Exception as e:
            db.rollback()
            return {"message": f"Erro ao registrar usuário: {str(e)}"}, 500

class UserLoginResource(Resource):
    def post(self):
        db = next(get_db())
        data = request.get_json()
        if not data or not all(k in data for k in ["username", "password"]):
            return {"message": "Usuário e senha são obrigatórios."}, 400

        user = db.query(User).filter(
            User.username == data["username"],
            User.password == data["password"] # Em produção, compare com senha hashed
        ).first()

        if user:
            return {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "cargo": user.cargo
            }, 200
        return {"message": "Credenciais inválidas."}, 401

# --- Mapeamento de Rotas da API ---
api.add_resource(ContatoListResource, '/api/contatos')
api.add_resource(ContatoResource, '/api/contatos/<int:contato_id>')

api.add_resource(DenunciaListResource, '/api/denuncias')

api.add_resource(EventoListResource, '/api/eventos')
api.add_resource(EventoResource, '/api/eventos/<int:evento_id>') 

api.add_resource(InformacaoListResource, '/api/informacoes')

api.add_resource(UserRegisterResource, '/api/register')
api.add_resource(UserLoginResource, '/api/login')


if __name__ == '__main__':
    # Para desenvolvimento, use debug=True. Em produção, use gunicorn ou uWSGI.
    # Ex: gunicorn -w 4 app:app
    app.run(debug=True, host='0.0.0.0', port=8080)