from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Username: {username}, Password: {password}")  # Prints to terminal
    return render_template('connexion.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

'''
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

if bcrypt.checkpw(password, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")
'''