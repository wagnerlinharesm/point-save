import jwt


class JwtUtil:
    def __init__(self, jwt_token):
        self._decoded_token = JwtUtil.__decode(jwt_token)

    @staticmethod
    def __decode(jwt_token):
        try:
            return jwt.decode(
                jwt_token,
                algorithms=["RS256"],
                options={"verify_signature": False}
            )
        except Exception as e:
            print("Error connecting to database.", e)
            raise Exception("Error decoding jwt token.", e)

    def get_required_attribute(self, name):
        value = self._decoded_token.get(name)

        if value is None:
            raise Exception("jwt token attribute '", name, "' is missing.")

        return value
