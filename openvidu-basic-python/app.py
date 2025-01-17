import os
import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

OPENVIDU_URL = os.environ.get("OPENVIDU_URL")
OPENVIDU_SECRET = os.environ.get("OPENVIDU_SECRET")


@app.route("/sessions", methods=['POST'])
def initializeSession():
    try:
        body = request.json if request.data else {}
        response = requests.post(
            OPENVIDU_URL + "openvidu/api/sessions",
            verify=False,
            auth=("OPENVIDUAPP", OPENVIDU_SECRET),
            headers={'Content-type': 'application/json'},
            json=body
        )
        response.raise_for_status()
        return response.json()["sessionId"]
    except requests.exceptions.HTTPError as err:
        if (err.response.status_code == 409):
            # Session already exists in OpenVidu
            return request.json["customSessionId"]
        else:
            return err


@app.route("/sessions/<sessionId>/connections", methods=['POST'])
def createConnection(sessionId):
    body = request.json if request.data else {}
    return requests.post(
        OPENVIDU_URL + "openvidu/api/sessions/" + sessionId + "/connection",
        verify=False,
        auth=("OPENVIDUAPP", OPENVIDU_SECRET),
        headers={'Content-type': 'application/json'},
        json=body
    ).json()["token"]


if __name__ == "__main__":
    app.run(debug=True, ssl_context=("cert/cert.pem", "cert/key.pem"))
