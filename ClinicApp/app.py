from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 1. الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# 2. صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# 3. صفحة إنشاء حساب
@app.route('/signup')
def signup():
    return render_template('signup.html')

# 4. لوحة التحكم
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# 5. بروفايل الدكتور
@app.route('/doctor-profile')
def doctor_profile():
    return render_template('doctor-profile.html')

# 6. صفحة الحجز
@app.route('/booking')
def booking():
    return render_template('booking.html')

# 7. صفحة المواعيد
@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

# 8. التقييم
@app.route('/rating')
def rating():
    return render_template('rating.html')

# 9. تعديل البروفايل
@app.route('/edit-profile')
def edit_profile():
    return render_template('edit-profile.html')

if __name__ == '__main__':
    app.run(debug=True)