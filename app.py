from flask import Flask, render_template, request, redirect, url_for,session, flash
from controllers.user_controller import UserController
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from controllers.notification_controller import NotificationController
from controllers.auth_utils import login_required, patient_required, refresh_session_user
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    if 'user' in session:
        return handle_dashboard()
    return render_template('index.html')

def handle_login():
    return redirect(url_for('login'))

def handle_dashboard():
    return redirect(url_for('dashboard'))

def get_login_page():
    return render_template('login.html')

def get_signup_page():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        result = UserController.login(email, password)
        if result['success']:
            user = result['user']
            session['user'] = {
                'id': user.user_id,
                'name': user.get_full_name(),
                'role': user.role,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            return handle_dashboard()
        else:
            flash(result['message'], 'error')
            
    return get_login_page()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'patient')
                
        result = UserController.register(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=role
        )
        
        if result['success']:
            flash('Registration successful! Please login.', 'success')
            return handle_login()
        else:
            flash(result['message'], 'error')
            
    return get_signup_page()

@app.route('/logout')
def logout():
    session.pop('user', None)
    UserController.logout()
    return handle_login()

@app.route('/dashboard')
@login_required
def dashboard():
    user = session['user']
    role = user.get('role', 'patient')
    
    if role == 'patient':
        appointments_result = PatientController.get_appointments(user['id'])
        appointments = appointments_result['appointments'] if appointments_result['success'] else []
        return render_template('dashboard.html', user=user, appointments=appointments)
    elif role == 'doctor':
        appointments_result = DoctorController.get_todays_appointments(user['id'])
        appointments = appointments_result['appointments'] if appointments_result['success'] else []
        return render_template('dashboard.html', user=user, appointments=appointments)
    
    return render_template('dashboard.html', user=user, appointments=[])

@app.route('/doctor-profile', defaults={'doctor_id': None})
@app.route('/doctor-profile/<doctor_id>')
@login_required
def doctor_profile(doctor_id):
    if not doctor_id:
        if session['user']['role'] == 'doctor':
            doctor_id = session['user']['id']
        else:
            return handle_dashboard()

    result = DoctorController.get_doctor(doctor_id)
    if result['success']:
        doctor = result['doctor']
        feedback = DoctorController.get_feedback(doctor_id)['feedback']
        return render_template('doctor-profile.html', doctor=doctor, feedback=feedback)
    
    return handle_dashboard()

@app.route('/booking', methods=['GET', 'POST'])
@patient_required
def booking():
    doctors = DoctorController.get_all_doctors()['doctors']
    
    # Auto-select the only doctor if there's only one
    if not doctors or len(doctors) == 0:
        flash('No doctors available', 'error')
        return handle_dashboard()
    
    # Always use the first (and only) doctor
    selected_doctor = doctors[0]
        
    if request.method == 'POST':
        # Auto-select doctor if not provided (shouldn't happen, but safety check)
        doctor_id = request.form.get('doctor_id') or selected_doctor.user_id
        date = request.form.get('date')
        time = request.form.get('time')
        reason = request.form.get('reason')
        
        result = PatientController.book_appointment(
            patient_id=session['user']['id'],
            doctor_id=doctor_id,
            appointment_date=date,
            appointment_time=time,
            reason=reason
        )
        
        if result['success']:
            flash('Appointment booked successfully!', 'success')
            return  handle_dashboard()
        else:
            flash(result['message'], 'error')

    # Get first doctor's info and feedback for display
    doctor = selected_doctor
    feedback_result = DoctorController.get_feedback(doctor.user_id)
    feedback = feedback_result.get('feedback', []) if feedback_result['success'] else []
    
    return render_template('booking.html', doctors=doctors, doctor=doctor, feedback=feedback)

@app.route('/appointments')
@login_required
def appointments():
        
    user_id = session['user']['id']
    if session['user']['role'] == 'patient':
        result = PatientController.get_appointments(user_id)
    else:
        result = DoctorController.get_appointments(user_id)
        
    return render_template('appointments.html', appointments=result['appointments'])

@app.route('/rating', methods=['GET', 'POST'])
@patient_required
def rating():
    doctors = DoctorController.get_all_doctors()['doctors']
    
    # Auto-select the only doctor if there's only one
    if not doctors or len(doctors) == 0:
        flash('No doctors available to rate', 'error')
        return handle_dashboard()
    
    # Always use the first (and only) doctor
    selected_doctor = doctors[0]
    doctor_id = selected_doctor.user_id
        
    if request.method == 'POST':
        # Auto-select doctor if not provided (shouldn't happen, but safety check)
        doctor_id = request.form.get('doctor_id') or selected_doctor.user_id
        rating_value = request.form.get('rating')
        comment = request.form.get('comment', '')
        
        # Validate rating is provided
        if not rating_value:
            flash('Please select a rating', 'error')
            return render_template('rating.html', doctors=doctors, doctor_id=doctor_id, success=False)
        
        try:
            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                flash('Rating must be between 1 and 5', 'error')
                return render_template('rating.html', doctors=doctors, doctor_id=doctor_id, success=False)
        except (ValueError, TypeError):
            flash('Invalid rating value', 'error')
            return render_template('rating.html', doctors=doctors, doctor_id=doctor_id, success=False)
        
        result = PatientController.submit_feedback(
            patient_id=session['user']['id'],
            doctor_id=doctor_id,
            rating=rating_value,
            comment=comment
        )
        
        if result['success']:
            flash('Thank you for your feedback!', 'success')
            # Stay on the rating page to show the success message
            return render_template('rating.html', doctors=doctors, doctor_id=doctor_id, success=True)
        else:
            flash(result.get('message', 'Failed to submit feedback. Please try again.'), 'error')
            return render_template('rating.html', doctors=doctors, doctor_id=doctor_id, success=False)
            
    # GET request - use auto-selected doctor
    return render_template('rating.html', doctors=doctors, doctor_id=doctor_id, success=False)

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        updates = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'date_of_birth': request.form.get('date_of_birth')
        }
        
        # Remove empty values
        updates = {k: v for k, v in updates.items() if v}
        
        # Update profile via controller with ownership validation
        result = UserController.update_profile(
            user_id=session['user']['id'],
            requesting_user_id=session['user']['id'],  # Ownership check
            **updates
        )
        
        if result['success']:
            # Refresh session data to show updated info
            refresh_session_user(session['user']['id'])
            flash('Profile updated successfully', 'success')
        else:
            flash(result.get('message', 'Failed to update profile'), 'error')
        
        return handle_dashboard()
        
    user = UserController.get_profile(session['user']['id'])['user']
    return render_template('edit-profile.html', user=user)

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/reset-password')
def reset_password():
    return render_template('reset-password.html')

@app.route('/cancel-appointment', methods=['POST'])
@login_required
def cancel_appointment():
    appointment_id = request.form.get('appointment_id')
    user_role = session['user']['role']
    user_id = session['user']['id']
    
    if not appointment_id:
        flash('No appointment specified', 'error')
        return redirect(url_for('appointments'))
    
    # Use appropriate controller based on user role
    if user_role == 'patient':
        result = PatientController.cancel_appointment(appointment_id)
    elif user_role == 'doctor':
        result = DoctorController.cancel_appointment(appointment_id)
    else:
        flash('Unauthorized action', 'error')
        return redirect(url_for('appointments'))
    
    if result['success']:
        flash('Appointment cancelled successfully', 'success')
    else:
        flash(result.get('message', 'Failed to cancel appointment'), 'error')
    
    return redirect(url_for('appointments'))

if __name__ == '__main__':
    app.run(debug=True)



