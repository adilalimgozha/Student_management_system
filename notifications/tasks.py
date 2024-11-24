# notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from students.models import Student
from grades.models import Grades
from attendance.models import Attendance
from django.utils import timezone

@shared_task
def send_attendance_reminder(username, email):
        # send email or notification to mark attendance
        subject = 'Attendance Reminder'
        message = f'Dear {username}, please mark your attendance.'
        from_email = 'admin@school.com'
        recipient_list = [email]
        
        send_mail(subject, message, from_email, recipient_list)
        print(f'Will send email to: {email}')

@shared_task
def send_grade_notification(username, email, course):
        # send email or notification to mark attendance
        subject = 'Grade added notification'
        message = f'Dear {username}, added grade of the course {course}'
        from_email = 'admin@school.com'
        recipient_list = [email]
        
        send_mail(subject, message, from_email, recipient_list)
        print(f'Will send email to: {email}')

@shared_task
def send_grade_updated_notification(username, email, course):
        # send email or notification to mark attendance
        subject = 'Grade updated notification'
        message = f'Dear {username}, updated grade of the course {course}'
        from_email = 'admin@school.com'
        recipient_list = [email]
        
        send_mail(subject, message, from_email, recipient_list)
        print(f'Will send email to: {email}')




@shared_task
def generate_daily_report():
    # Logic to summarize attendance and grades
    attendance_summary = Attendance.objects.all()  # Example logic
    grades_summary = Grades.objects.all()  # Example logic
    # Here, you could generate a PDF or email the summary
    send_mail(
        'Daily Attendance and Grades Report',
        f'Attendance: {attendance_summary}\nGrades: {grades_summary}',
        'from@example.com',
        ['admin@example.com'],
    )

@shared_task
def send_weekly_performance_update():
    # Logic to send email updates summarizing performance
    students = Student.objects.all()
    for student in students:
        performance_summary = f'Performance for {student.student.username}: ...'  # Example logic
        send_mail(
            'Weekly Performance Update',
            performance_summary,
            'from@example.com',
            [student.student.email],
        )
