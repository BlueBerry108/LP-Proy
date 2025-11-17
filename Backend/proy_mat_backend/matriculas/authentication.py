from rest_framework_simplejwt.authentication import JWTAuthentication

class AlumnoJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # Creamos un usuario falso basado en el token
        class FakeUserObj:
            def __init__(self, user_id):
                self.id = user_id
                self.is_active = True
            
            @property
            def is_authenticated(self):
                return True

        user_id = validated_token.get("user_id")
        return FakeUserObj(user_id)