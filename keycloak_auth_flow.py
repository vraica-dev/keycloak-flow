import jwt
import requests
from base64 import b64decode
import datetime
import time


class KLAuthClient:
    CLIENT_ID = "rbc_test"
    CLIENT_SECRET = "mSwqytawzeRUWFvQYulyjP3ABQFnGuOA"
    USERNAME = "__ur__username"
    PASSWORD = "__ur_password"
    URL = "http://localhost:8080/realms/master/protocol/openid-connect/token"

    ACCESS_TOKEN = None
    REFRESH_TOKEN = None

    @classmethod
    def _cache_info(cls, resp):
        cls.ACCESS_TOKEN = resp.json()["access_token"]
        cls.REFRESH_TOKEN = resp.json()["refresh_token"]

    @classmethod
    def auth(cls):
        print("Calling init auth.")
        try:
            resp = requests.post(
                url=cls.URL,
                data={
                    "client_id": cls.CLIENT_ID,
                    "client_secret": cls.CLIENT_SECRET,
                    "username": cls.USERNAME,
                    "password": cls.PASSWORD,
                    "grant_type": "password",
                },
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch the access token - {e}.")
        else:
            if resp.status_code == 200:
                cls._cache_info(resp)
            else:
                print(f"Failed to fetch the access token - {resp.status_code}.")

    @classmethod
    def refresh_token(cls):
        if cls.REFRESH_TOKEN and not cls.token_expired(cls.REFRESH_TOKEN):
            try:
                resp = requests.post(
                    url=cls.URL,
                    data={
                        "client_id": cls.CLIENT_ID,
                        "client_secret": cls.CLIENT_SECRET,
                        "username": cls.USERNAME,
                        "password": cls.PASSWORD,
                        "refresh_token": cls.REFRESH_TOKEN,
                        "grant_type": "refresh_token",
                    },
                )
                resp.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Failed to refresh the token - {e}.")
            else:
                if resp.status_code == 200:
                    cls._cache_info(resp)
                    print("Token refreshed.")
                else:
                    print(f"Failed to refresh the token - {resp.status_code}.")
        else:
            print("Refresh token also expired.")
            cls.auth()

    @classmethod
    def token_expired(cls, token):
        try:
            data = jwt.decode(
                token,
                b64decode(cls.CLIENT_SECRET),
                algorithms=["HsS256"],
                options={"verify_signature": False, "verify_expiring": True},
            )
        except jwt.ExpiredSignatureError:
            print("Error. Token has expired.")
            return True
        else:
            if datetime.datetime.now(datetime.UTC) > datetime.datetime.fromtimestamp(
                data["exp"], datetime.UTC
            ):
                print("Token has expired.")
                return True

    @classmethod
    def get_bearer(cls):
        if cls.ACCESS_TOKEN is None:
            cls.auth()
        elif cls.token_expired(cls.ACCESS_TOKEN):
            cls.refresh_token()

        return cls.ACCESS_TOKEN


class Client:

    def get_info(self):
        at = KLAuthClient.get_bearer()
        print(f"Calling get_info API with {at[:4]}.")


if __name__ == "__main__":

    c1 = Client()
    c2 = Client()
    c3 = Client()
    c4 = Client()
    c5 = Client()

    for x in range(1, 6):
        locals().get(f"c{x}").get_info()
        # simulating access token exp
        if x == 2:
            time.sleep(11)
        # simulating refresh token exp
        if x == 4:
            time.sleep(20)
