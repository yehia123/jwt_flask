from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import request 
# parser = reqparse.RequestParser()
# parser.add_argument('username', help='This field cannot be blank', required=True)
# parser.add_argument('password', help='This field cannot be blank', required=True)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}

        new_user = UserModel(
            username= data['username'],
            password =  UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = request.get_json()

        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} does not exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Loggin in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        @jwt_required
        def post(self):
            jti = get_raw_jwt()['jti']
            try:
                revoked_token = RevokedTokenModel(jti = jti)
                revoked_token.add()
                return {'message': 'Access token has been revoked'}
            except:
                return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        print(jti)
        try: 
            revoked_token = RevokedTokenModel(jti= jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revokved'}
        except:
            return {'message': 'something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }

class VideoRecognition(Resource):
    def get(self):
        cascPath = "./haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)

        cap = cv2.VideoCapture(0)
        face_locations = []

        while True:
            ret, frame = cap.read()

            # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rgb_frame = frame[:, :, ::-1]

            #find all locations
            facelocations = face_recognition.face_locations(rgb_frame)

            for top, right, bottom, left in facelocations:
                cv2.rectangle(frame, (left, top), (right,bottom), (0,0,255), 2)

            cv2.imshow('video', frame)

            k = cv2.waitKey(30) & 0xff
            if k==27:
                break


        cap.release()
        cv2.destroyAllWindows()
        return {"done": 0}
