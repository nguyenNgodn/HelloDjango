from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

@shared_task
def send_thank_you_email(user_email, username):
    print(f"Sending thank you email to {user_email} for user {username}")
    subject = 'Cảm ơn bạn đã đăng ký!'
    message = f'Chào {username}, cảm ơn bạn đã đăng ký tài khoản trên hệ thống của chúng tôi.'
    from_email = 'ngonguyen295@gmail.com'
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)

@shared_task
def check_new_users_and_notify():
    User = get_user_model()
    now = timezone.now()
    ten_minutes_ago = now - timedelta(minutes=10)

    new_users = User.objects.filter(date_joined__gte=ten_minutes_ago)

    if new_users.exists():
        message = "\n".join([
            f"- {user.username} ({user.email}) - đăng ký lúc {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}"
            for user in new_users
        ])

        send_mail(
            subject="🔔 Thông báo: Có người dùng mới",
            message=f"Có {new_users.count()} người dùng mới trong 10 phút qua:\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["nngo6449@gmail.com"],
        )
    else:
        send_mail(
            subject="🔔 Thông báo: Không có người dùng mới",
            message=f"Không có người dùng mới trong khoảng thời gian từ {ten_minutes_ago.strftime('%H:%M:%S')} đến {now.strftime('%H:%M:%S')}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["nngo6449@gmail.com"],
        )