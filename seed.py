"""
Seed Script for Complaint Management System
Populates initial sample users and complaints for demonstration purposes.
"""
from datetime import datetime, timedelta
from app import app, db, User, Admin, Complaint

def seed_database():
    with app.app_context():
        db.create_all()

        # Check if users already exist
        if User.query.count() == 0:
            print("[INFO] Seeding sample users...")
            u1 = User(name='Rahul Sharma', email='rahul@gmail.com', mobile='9876543210')
            u1.set_password('user123')

            u2 = User(name='Priya Patel', email='priya@gmail.com', mobile='9876543211')
            u2.set_password('user123')

            db.session.add_all([u1, u2])
            db.session.commit()
            print("[INFO] Sample users created: rahul@gmail.com / user123, priya@gmail.com / user123")

            year = datetime.now().strftime("%Y")

            c1 = Complaint(
                complaint_number=f"CMP-{year}-0001",
                user_id=u1.id,
                title='Wi-Fi Connectivity Dropping in Central Library',
                category='Technical Issues',
                priority='High',
                description='The Wi-Fi network in the Central Library 2nd floor continuously drops every 10 minutes, making online research impossible.',
                status='In Progress',
                admin_remark='Network engineer assigned. Inspecting router access points on the 2nd floor.',
                created_date=datetime.utcnow() - timedelta(days=2)
            )

            c2 = Complaint(
                complaint_number=f"CMP-{year}-0002",
                user_id=u1.id,
                title='Library Book Reservation Delay',
                category='Service Issues',
                priority='Low',
                description='Requested a copy of Data Structures using C++ book 3 days ago. Status still shows pending in library catalog.',
                status='Pending',
                admin_remark=None,
                created_date=datetime.utcnow() - timedelta(days=1)
            )

            c3 = Complaint(
                complaint_number=f"CMP-{year}-0003",
                user_id=u2.id,
                title='Projector Not Working in Room 304',
                category='Infrastructure Issues',
                priority='Medium',
                description='HDMI input port on classroom projector is damaged. Display shows no signal during morning lectures.',
                status='Resolved',
                admin_remark='Replaced HDMI cable and updated display adapter driver. Projector tested working fine.',
                created_date=datetime.utcnow() - timedelta(days=4)
            )

            c4 = Complaint(
                complaint_number=f"CMP-{year}-0004",
                user_id=u2.id,
                title='Mid-Semester Exam Timetable Conflict',
                category='Academic Issues',
                priority='High',
                description='BCA 5th Semester Cloud Computing paper overlaps with Web Technologies practical exam on Friday afternoon.',
                status='Resolved',
                admin_remark='Examination committee rescheduled Web Technologies practical exam to Saturday morning.',
                created_date=datetime.utcnow() - timedelta(days=5)
            )

            db.session.add_all([c1, c2, c3, c4])
            db.session.commit()
            print("[INFO] Sample complaints seeded successfully!")
        else:
            print("[INFO] Database already seeded.")

if __name__ == '__main__':
    seed_database()
