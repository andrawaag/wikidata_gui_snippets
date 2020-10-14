from wikidataintegrator import wdi_core, wdi_login, wdi_helpers
from flask import Flask, request, render_template, session
from flask_session import Session
import secrets
import os
import pprint

secret = secrets.token_urlsafe(32)
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config['SECRET_KEY'] = secret
app.config.from_object(__name__)
Session(app)

if "WDUSER" in os.environ and "WDPASS" in os.environ:
    WDUSER = os.environ['WDUSER']
    WDPASS = os.environ['WDPASS']
else:
    raise ValueError("WDUSER and WDPASS must be specified in local.py or as environment variables")

login = wdi_login.WDLogin(WDUSER, WDPASS)


#print(wdi_helpers.PublicationHelper("12432931", id_type="pmid",source="europepmc").get_or_create(login))

#print(wdi_helpers.PublicationHelper("10.2307/2399146", id_type="doi", source="crossref").get_or_create(login))

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/getqid", methods=['POST'])
def getqid():
    print(request.form.get("buttom"))
    pprint.pprint(request.form)
    if request.form.get("button") == "PMID":
        qid = wdi_helpers.PublicationHelper(request.form.get("refid"), id_type="pmid",source="europepmc").get_or_create(login)
    elif request.form.get("button") == "DOI":
        qid = wdi_helpers.PublicationHelper(request.form.get("refid"), id_type="doi", source="crossref").get_or_create(login)
    return render_template("resolve.html", wdid=qid)

if __name__ == "__main__":

    app.secret_key = secret

    app.run(host='0.0.0.0', port=1973, debug=True)