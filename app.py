import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from config import Config
from models import db, User, Admin, Complaint

app = Flask(__name__)
app.config.from_object(Config)

# Ensure instance folder exists for SQLite db
os.makedirs(os.path.join(app.config['BASE_DIR'], 'instance'), exist_ok=True)
db.init_app(app)

# ---------------------------------------------------------
# Helper Functions & Decorators
# ---------------------------------------------------------

def generate_complaint_id():
    """Generates unique formatted complaint ID like CMP-2026-0001."""
    year = datetime.now().strftime("%Y")
    last_complaint = Complaint.query.order_by(Complaint.id.desc()).first()
    next_id = (last_complaint.id + 1) if last_complaint else 1
    return f"CMP-{year}-{next_id:04d}"


def login_required(f):
    """Decorator to protect user routes requiring active session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to protect admin panel routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin authentication required.', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ---------------------------------------------------------
# Database Initialization & Default Admin/Sample Seed
# ---------------------------------------------------------
with app.app_context():
    db.create_all()
    # Seed default admin account if none exists
    if not Admin.query.filter_by(username='admin').first():
        default_admin = Admin(
            username='admin',
            name='System Administrator',
            email='admin@cms.com'
        )
        default_admin.set_password('admin123')
        db.session.add(default_admin)
        db.session.commit()
        print("[INFO] Default admin account created: admin / admin123")

    # Auto seed initial sample users & complaints if empty
    if User.query.count() == 0:
        u1 = User(name='Rahul Sharma', email='rahul@gmail.com', mobile='9876543210')
        u1.set_password('user123')
        u2 = User(name='Priya Patel', email='priya@gmail.com', mobile='9876543211')
        u2.set_password('user123')
        db.session.add_all([u1, u2])
        db.session.commit()

        c1 = Complaint(
            complaint_number="CMP-2026-0001",
            user_id=u1.id,
            title='Wi-Fi Connectivity Dropping in Central Library',
            category='Technical Issues',
            priority='High',
            description='The Wi-Fi network in the Central Library 2nd floor continuously drops every 10 minutes, making online research impossible.',
            status='In Progress',
            admin_remark='Network engineer assigned. Inspecting router access points on the 2nd floor.'
        )
        c2 = Complaint(
            complaint_number="CMP-2026-0002",
            user_id=u1.id,
            title='Library Book Reservation Delay',
            category='Service Issues',
            priority='Low',
            description='Requested a copy of Data Structures using C++ book 3 days ago. Status still shows pending in library catalog.',
            status='Pending',
            admin_remark=None
        )
        c3 = Complaint(
            complaint_number="CMP-2026-0003",
            user_id=u2.id,
            title='Projector Not Working in Room 304',
            category='Infrastructure Issues',
            priority='Medium',
            description='HDMI input port on classroom projector is damaged. Display shows no signal during morning lectures.',
            status='Resolved',
            admin_remark='Replaced HDMI cable and updated display adapter driver. Projector tested working fine.'
        )
        db.session.add_all([c1, c2, c3])
        db.session.commit()
        print("[INFO] Sample database records initialized.")


# ---------------------------------------------------------
# Public Routes
# ---------------------------------------------------------

@app.route('/')
def index():
    """Landing Page displaying system overview and stats."""
    total_complaints = Complaint.query.count()
    resolved_complaints = Complaint.query.filter_by(status='Resolved').count()
    pending_complaints = Complaint.query.filter_by(status='Pending').count()
    registered_users = User.query.count()
    return render_template('index.html',
                           total_complaints=total_complaints,
                           resolved_complaints=resolved_complaints,
                           pending_complaints=pending_complaints,
                           registered_users=registered_users)


# ---------------------------------------------------------
# User Authentication Routes
# ---------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration Route."""
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basic validations
        if not name or not email or not mobile or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'warning')
            return render_template('register.html')

        # Create user
        new_user = User(name=name, email=email, mobile=mobile)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User Login Route."""
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email address or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """User Logout Route."""
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


# ---------------------------------------------------------
# User Portal Routes
# ---------------------------------------------------------

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    """User Dashboard showing personal stats & recent complaints."""
    user = User.query.get(session['user_id'])
    user_complaints = Complaint.query.filter_by(user_id=user.id).order_by(Complaint.created_date.desc()).all()

    total = len(user_complaints)
    pending = sum(1 for c in user_complaints if c.status == 'Pending')
    in_progress = sum(1 for c in user_complaints if c.status == 'In Progress')
    resolved = sum(1 for c in user_complaints if c.status == 'Resolved')
    rejected = sum(1 for c in user_complaints if c.status == 'Rejected')

    recent_complaints = user_complaints[:5]

    return render_template('user_dashboard.html',
                           user=user,
                           total=total,
                           pending=pending,
                           in_progress=in_progress,
                           resolved=resolved,
                           rejected=rejected,
                           recent_complaints=recent_complaints)


@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and Edit User Profile."""
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not name or not mobile:
            flash('Name and Mobile number cannot be empty.', 'danger')
            return render_template('profile.html', user=user)

        if new_password:
            if new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
                return render_template('profile.html', user=user)
            user.set_password(new_password)

        user.name = name
        user.mobile = mobile
        session['user_name'] = user.name
        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)


@app.route('/user/add-complaint', methods=['GET', 'POST'])
@login_required
def add_complaint():
    """Submit New Complaint."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        priority = request.form.get('priority', 'Medium').strip()
        description = request.form.get('description', '').strip()

        if not title or not category or not description:
            flash('Please fill out all required fields.', 'danger')
            return render_template('add_complaint.html')

        complaint_code = generate_complaint_id()
        new_complaint = Complaint(
            complaint_number=complaint_code,
            user_id=session['user_id'],
            title=title,
            category=category,
            priority=priority,
            description=description,
            status='Pending'
        )

        db.session.add(new_complaint)
        db.session.commit()

        flash(f'Complaint submitted successfully! Your Ticket ID is {complaint_code}', 'success')
        return redirect(url_for('my_complaints'))

    return render_template('add_complaint.html')


@app.route('/user/my-complaints')
@login_required
def my_complaints():
    """View, track, filter, and search user's complaints."""
    category_filter = request.args.get('category', '').strip()
    status_filter = request.args.get('status', '').strip()
    search_query = request.args.get('search', '').strip()

    query = Complaint.query.filter_by(user_id=session['user_id'])

    if category_filter:
        query = query.filter(Complaint.category == category_filter)
    if status_filter:
        query = query.filter(Complaint.status == status_filter)
    if search_query:
        query = query.filter(
            (Complaint.title.ilike(f'%{search_query}%')) |
            (Complaint.complaint_number.ilike(f'%{search_query}%')) |
            (Complaint.description.ilike(f'%{search_query}%'))
        )

    complaints = query.order_by(Complaint.created_date.desc()).all()
    categories = ['Technical Issues', 'Academic Issues', 'Infrastructure Issues', 'Service Issues', 'Other']
    statuses = ['Pending', 'In Progress', 'Resolved', 'Rejected']

    return render_template('my_complaints.html',
                           complaints=complaints,
                           categories=categories,
                           statuses=statuses,
                           selected_category=category_filter,
                           selected_status=status_filter,
                           search_query=search_query)


# ---------------------------------------------------------
# Admin Portal Routes
# ---------------------------------------------------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin Portal Login."""
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_name'] = admin.name
            session['admin_username'] = admin.username
            flash(f'Welcome Admin, {admin.name}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid administrator credentials.', 'danger')

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin Logout Route."""
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    session.pop('admin_username', None)
    flash('Admin logged out successfully.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin Dashboard with statistics & analytics graphs."""
    total_complaints = Complaint.query.count()
    pending_complaints = Complaint.query.filter_by(status='Pending').count()
    in_progress_complaints = Complaint.query.filter_by(status='In Progress').count()
    resolved_complaints = Complaint.query.filter_by(status='Resolved').count()
    rejected_complaints = Complaint.query.filter_by(status='Rejected').count()
    total_users = User.query.count()

    recent_complaints = Complaint.query.order_by(Complaint.created_date.desc()).limit(5).all()

    return render_template('admin_dashboard.html',
                           total=total_complaints,
                           pending=pending_complaints,
                           in_progress=in_progress_complaints,
                           resolved=resolved_complaints,
                           rejected=rejected_complaints,
                           total_users=total_users,
                           recent_complaints=recent_complaints)


@app.route('/admin/api/analytics')
@admin_required
def admin_analytics_api():
    """JSON API endpoint returning data for Chart.js charts."""
    # Status Counts
    statuses = ['Pending', 'In Progress', 'Resolved', 'Rejected']
    status_counts = [Complaint.query.filter_by(status=s).count() for s in statuses]

    # Category Counts
    categories = ['Technical Issues', 'Academic Issues', 'Infrastructure Issues', 'Service Issues', 'Other']
    category_counts = [Complaint.query.filter_by(category=c).count() for c in categories]

    # Priority Counts
    priorities = ['Low', 'Medium', 'High']
    priority_counts = [Complaint.query.filter_by(priority=p).count() for p in priorities]

    return jsonify({
        'status_labels': statuses,
        'status_data': status_counts,
        'category_labels': categories,
        'category_data': category_counts,
        'priority_labels': priorities,
        'priority_data': priority_counts
    })


@app.route('/admin/manage-complaints')
@admin_required
def manage_complaints():
    """Manage All Complaints (Search, Filter, View Details, Update Status)."""
    category_filter = request.args.get('category', '').strip()
    status_filter = request.args.get('status', '').strip()
    priority_filter = request.args.get('priority', '').strip()
    search_query = request.args.get('search', '').strip()

    query = Complaint.query

    if category_filter:
        query = query.filter(Complaint.category == category_filter)
    if status_filter:
        query = query.filter(Complaint.status == status_filter)
    if priority_filter:
        query = query.filter(Complaint.priority == priority_filter)
    if search_query:
        query = query.join(User).filter(
            (Complaint.title.ilike(f'%{search_query}%')) |
            (Complaint.complaint_number.ilike(f'%{search_query}%')) |
            (Complaint.description.ilike(f'%{search_query}%')) |
            (User.name.ilike(f'%{search_query}%')) |
            (User.email.ilike(f'%{search_query}%'))
        )

    complaints = query.order_by(Complaint.created_date.desc()).all()
    categories = ['Technical Issues', 'Academic Issues', 'Infrastructure Issues', 'Service Issues', 'Other']
    statuses = ['Pending', 'In Progress', 'Resolved', 'Rejected']
    priorities = ['Low', 'Medium', 'High']

    return render_template('manage_complaints.html',
                           complaints=complaints,
                           categories=categories,
                           statuses=statuses,
                           priorities=priorities,
                           selected_category=category_filter,
                           selected_status=status_filter,
                           selected_priority=priority_filter,
                           search_query=search_query)


@app.route('/admin/complaint/update/<int:complaint_id>', methods=['POST'])
@admin_required
def update_complaint_status(complaint_id):
    """Update status and add resolution remarks to a complaint."""
    complaint = Complaint.query.get_or_404(complaint_id)

    new_status = request.form.get('status', '').strip()
    admin_remark = request.form.get('admin_remark', '').strip()

    if new_status in ['Pending', 'In Progress', 'Resolved', 'Rejected']:
        complaint.status = new_status
        complaint.admin_remark = admin_remark
        complaint.updated_date = datetime.utcnow()
        db.session.commit()
        flash(f'Complaint {complaint.complaint_number} status updated to {new_status}!', 'success')
    else:
        flash('Invalid status selected.', 'danger')

    return redirect(request.referrer or url_for('manage_complaints'))


@app.route('/admin/complaint/delete/<int:complaint_id>', methods=['POST'])
@admin_required
def delete_complaint(complaint_id):
    """Delete a complaint record."""
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint_num = complaint.complaint_number
    db.session.delete(complaint)
    db.session.commit()
    flash(f'Complaint {complaint_num} has been permanently deleted.', 'info')
    return redirect(request.referrer or url_for('manage_complaints'))


@app.route('/admin/manage-users')
@admin_required
def manage_users():
    """View and Manage User accounts."""
    search_query = request.args.get('search', '').strip()

    query = User.query
    if search_query:
        query = query.filter(
            (User.name.ilike(f'%{search_query}%')) |
            (User.email.ilike(f'%{search_query}%')) |
            (User.mobile.ilike(f'%{search_query}%'))
        )

    users = query.order_by(User.created_at.desc()).all()
    return render_template('manage_users.html', users=users, search_query=search_query)


@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user account and associated complaints."""
    user = User.query.get_or_404(user_id)
    user_name = user.name
    db.session.delete(user)
    db.session.commit()
    flash(f'User account for {user_name} and associated complaints deleted.', 'info')
    return redirect(url_for('manage_users'))


# ---------------------------------------------------------
# Custom Error Handlers
# ---------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', error_message="404 - Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html', error_message="500 - Internal Server Error"), 500


if __name__ == '__main__':
    # Run application on port 5000 in debug mode for development
    app.run(host='0.0.0.0', port=5000, debug=True)
