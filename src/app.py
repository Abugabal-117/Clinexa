from flask import Flask, render_template, request, redirect, url_for,session, flash
from controllers.user_controller import UserController
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController

from controllers.auth_utils import login_required, patient_required, refresh_session_user
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
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
            return redirect(url_for('dashboard'))
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
    session.clear()
    UserController.logout()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = session['user']
    role = user.get('role', 'patient')
    
    if role == 'patient':
        appointments_result = PatientController.get_appointments(user['id'])
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
            doctors = DoctorController.get_all_doctors()['doctors']
            if doctors and len(doctors) > 0:
                doctor_id = doctors[0].user_id
            else:
                flash('No doctors available', 'error')
                return redirect(url_for('dashboard'))

    result = DoctorController.get_doctor(doctor_id)
    if result['success']:
        doctor = result['doctor']
        feedback_result = DoctorController.get_feedback(doctor_id)
        feedback = feedback_result.get('feedback', []) if feedback_result['success'] else []
        return render_template('doctor-profile.html', doctor=doctor, feedback=feedback)
    
    flash('Doctor not found', 'error')
    return redirect(url_for('dashboard'))

@app.route('/about-doctor', defaults={'doctor_id': None})
@app.route('/about-doctor/<doctor_id>')
def about_doctor(doctor_id):
    if not doctor_id:
        doctors = DoctorController.get_all_doctors()['doctors']
        if doctors and len(doctors) > 0:
            doctor_id = doctors[0].user_id
        else:
            flash('No doctors available', 'error')
            if 'user' in session:
                return redirect(url_for('dashboard'))
            return redirect(url_for('home'))

    result = DoctorController.get_doctor(doctor_id)
    if result['success']:
        doctor = result['doctor']
        feedback_result = DoctorController.get_feedback(doctor_id)
        feedback = feedback_result.get('feedback', []) if feedback_result['success'] else []
        avg_rating = 0.0
        if feedback and len(feedback) > 0:
            total_rating = sum(item.rating for item in feedback)
            avg_rating = round(total_rating / len(feedback), 1)
        return render_template('about-doctor.html', doctor=doctor, feedback=feedback, avg_rating=avg_rating)
    
    flash('Doctor not found', 'error')
    return redirect(url_for('dashboard'))

@app.route('/booking', methods=['GET', 'POST'])
@patient_required
def booking():
    doctors = DoctorController.get_all_doctors()['doctors']
    
    if not doctors or len(doctors) == 0:
        flash('No doctors available', 'error')
        return redirect(url_for('dashboard'))
    
    selected_doctor = doctors[0]
        
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id') or selected_doctor.user_id
        date = request.form.get('date')
        time = request.form.get('time')
        reason = request.form.get('reason')
        
        # Validate that the selected time is in the doctor's available times
        doctor_result = DoctorController.get_available_times(doctor_id)
        available_times = doctor_result.get('available_times', []) if doctor_result['success'] else []
        
        selected_slot = {'date': date, 'time': time}
        if selected_slot not in available_times:
            flash('Selected time is not available. Please choose from available time slots.', 'error')
        else:
            result = PatientController.book_appointment(
                patient_id=session['user']['id'],
                doctor_id=doctor_id,
                appointment_date=date,
                appointment_time=time,
                reason=reason
            )
            
            if result['success']:
                flash('Appointment booked successfully!', 'success')
                return redirect(url_for('appointments'))
            else:
                flash(result['message'], 'error')

    doctor = selected_doctor
    feedback_result = DoctorController.get_feedback(doctor.user_id)
    feedback = feedback_result.get('feedback', []) if feedback_result['success'] else []
    
    # Get available times for the selected doctor
    available_times_result = DoctorController.get_available_times(doctor.user_id)
    available_times = available_times_result.get('available_times', []) if available_times_result['success'] else []
    
    return render_template('booking.html', doctors=doctors, doctor=doctor, feedback=feedback, available_times=available_times)

@app.route('/appointments')
@login_required
def appointments():
        
    user_id = session['user']['id']
    if session['user']['role'] == 'patient':
        result = PatientController.get_appointments(user_id)
        return render_template('appointments.html', appointments=result['appointments'], user_role='patient')
    elif session['user']['role'] == 'doctor':
        # Get doctor's patients
        doctor_result = DoctorController.get_doctor(user_id)
        doctor = doctor_result.get('doctor') if doctor_result['success'] else None
        patients = doctor.patients if doctor else []
        return render_template('appointments.html', appointments=[], patients=patients, user_role='doctor')
    
    return render_template('appointments.html', appointments=[])

@app.route('/rating', methods=['GET', 'POST'])
@patient_required
def rating():
    doctors = DoctorController.get_all_doctors()['doctors']
    
    if not doctors or len(doctors) == 0:
        flash('No doctors available to rate', 'error')
        return redirect(url_for('dashboard'))
    
    selected_doctor = doctors[0]
    doctor_id = selected_doctor.user_id
        
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id') or selected_doctor.user_id
        rating_value = request.form.get('rating')
        comment = request.form.get('comment', '')
        
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
            return render_template('rating.html', doctors=doctors, doctor_id=doctor_id, success=True)
        else:
            flash(result.get('message', 'Failed to submit feedback. Please try again.'), 'error')
            return render_template('rating.html', doctors=doctors, doctor_id=doctor_id, success=False)
            
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
        
        updates = {k: v for k, v in updates.items() if v}
        
        result = UserController.update_profile(
            user_id=session['user']['id'],
            requesting_user_id=session['user']['id'],
            **updates
        )
        
        if result['success']:
            refresh_session_user(session['user']['id'])
            flash('Profile updated successfully', 'success')
        else:
            flash(result.get('message', 'Failed to update profile'), 'error')
        
        return redirect(url_for('edit_profile'))
        
    user = UserController.get_profile(session['user']['id'])['user']
    return render_template('edit-profile.html', user=user)

@app.route('/patient-report', methods=['GET', 'POST'])
@login_required
def patient_report():
    return render_template('patient-report.html')

@app.route('/schedule-management', methods=['GET', 'POST'])
@login_required
def schedule_management():
    if session['user']['role'] != 'doctor':
        flash('Unauthorized action', 'error')
        return redirect(url_for('dashboard'))
    
    doctor_id = session['user']['id']
    result = DoctorController.get_available_times(doctor_id)
    available_times = result.get('available_times', []) if result['success'] else []
    
    if request.method == 'POST':
        action = request.form.get('action')
        date = request.form.get('date')
        time = request.form.get('time')
        
        if action == 'add':
            add_result = DoctorController.add_available_time(doctor_id, date, time)
            if add_result['success']:
                flash('Time slot added successfully', 'success')
            else:
                flash(add_result.get('message', 'Failed to add time slot'), 'error')
        elif action == 'remove':
            remove_result = DoctorController.remove_available_time(doctor_id, date, time)
            if remove_result['success']:
                flash('Time slot removed successfully', 'success')
            else:
                flash(remove_result.get('message', 'Failed to remove time slot'), 'error')
        
        return redirect(url_for('schedule_management'))
    
    return render_template('schedule-management.html', available_times=available_times)

@app.route('/remove-patient/<patient_id>', methods=['POST'])
@login_required
def remove_patient(patient_id):
    if session['user']['role'] != 'doctor':
        flash('Unauthorized action', 'error')
        return redirect(url_for('dashboard'))
    
    doctor_id = session['user']['id']
    result = DoctorController.remove_patient(doctor_id, patient_id)
    
    if result['success']:
        flash('Patient removed successfully', 'success')
    else:
        flash(result.get('message', 'Failed to remove patient'), 'error')
    
    return redirect(url_for('appointments'))



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
    
    if user_role == 'patient':
        result = PatientController.cancel_appointment(appointment_id)
    else:
        flash('Unauthorized action', 'error')
        return redirect(url_for('appointments'))
    
    if result['success']:
        flash('Appointment cancelled successfully', 'success')
    else:
        flash(result.get('message', 'Failed to cancel appointment'), 'error')
    
    if user_role == 'patient':
        return redirect(url_for('appointments'))
    else:
        return redirect(url_for('appointments'))

if __name__ == '__main__':
    app.run(debug=True)
