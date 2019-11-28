from application import app
import os

app.secret_key = os.urandom(21)
app.run(debug=True)