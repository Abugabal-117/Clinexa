from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/doctor-profile')
def doctor_profile():
    return render_template('doctor-profile.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

@app.route('/rating')
def rating():
    return render_template('rating.html')

@app.route('/edit-profile')
def edit_profile():
    return render_template('edit-profile.html')

if __name__ == '__main__':
    app.run(debug=True)
