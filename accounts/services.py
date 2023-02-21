import smtplib
import random
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .exceptions import InvalidUniqueToken
from .exceptions import WrongLoginOrPassword
from .models import User
from .models import UserUniqueToken
from .serializers.main_serializers import UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import user_logged_in


class AuthorizationService:
    @staticmethod
    def send_register_confirm_link(user: User):
        tk = UserUniqueToken.generate(user, 'register')
        link = settings.ROOT_APP_ADDR + '/authorization/registration_confirm/?tk=' + tk.token
        msg = MIMEMultipart()
        msg["Subject"] = "Подтверждение регистрации ASIST"
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = user.email
        text = "Для завершения регистрации перейдите по ссылке из этого письма.\n" + link
        msg.attach(MIMEText(text))
        s = smtplib.SMTP(settings.SMTP_ADDR, settings.SMTP_PORT)
        s.starttls()
        s.login(settings.SMTP_LOGIN, settings.SMTP_PASSWD)
        s.sendmail(settings.SMTP_EMAIL, [user.email], msg.as_string())
        s.quit()

    @staticmethod
    def registration_confirm(tk: str):
        try:
            token = UserUniqueToken.objects.get(token=tk, action='register')
            user = token.user
            if token.expire < timezone.localtime(timezone.now()):
                raise InvalidUniqueToken('Время действия данного токена истекло')
            user.is_active = True
            user.save()
            token.delete()
            return user
        except UserUniqueToken.DoesNotExist:
            raise InvalidUniqueToken

    @staticmethod
    def authorize_user(email: str, passwd: str, request):
        try:
            user = User.objects.get(email=email, is_active=True)
            if user.check_password(passwd):
                user_data = UserProfileSerializer(user).data
                token = str(RefreshToken.for_user(user).access_token)
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return {'token': token, 'user': user_data}
            else:
                raise Exception
        except User.DoesNotExist:
            raise WrongLoginOrPassword

    @staticmethod
    def send_password_reset_confirm_link(email: str):
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise WrongLoginOrPassword('Пользователь с данным Email не существует')
        tk = UserUniqueToken.generate(user, 'pass_reset')
        link = settings.ROOT_APP_ADDR + '/authorization/password_reset_confirm/?tk=' + tk.token
        msg = MIMEMultipart()
        msg["Subject"] = "Подтверждение сброса пароля ASIST"
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = user.email
        text = "Для подтверждения действия перейдите по ссылке из этого письма.\n" + link
        msg.attach(MIMEText(text))
        s = smtplib.SMTP(settings.SMTP_ADDR, settings.SMTP_PORT)
        s.starttls()
        s.login(settings.SMTP_LOGIN, settings.SMTP_PASSWD)
        s.sendmail(settings.SMTP_EMAIL, [user.email], msg.as_string())
        s.quit()

    @staticmethod
    def password_reset(tk: str):
        try:
            token = UserUniqueToken.objects.get(token=tk, action='pass_reset')
            if token.expire < timezone.localtime(timezone.now()):
                raise InvalidUniqueToken('Время действия данного токена истекло')
            s = 'QWERYIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
            new_pass = ''.join([random.choice(s) for _ in range(8)])
            token.user.set_password(new_pass)
            token.user.save()
            msg = MIMEMultipart()
            msg["Subject"] = "Новый пароль"
            msg["From"] = settings.SMTP_EMAIL
            msg["To"] = token.user.email
            msg.attach(MIMEText("Ваш новый пароль: " + new_pass))
            s = smtplib.SMTP(settings.SMTP_ADDR, settings.SMTP_PORT)
            s.starttls()
            s.login(settings.SMTP_LOGIN, settings.SMTP_PASSWD)
            s.sendmail(settings.SMTP_EMAIL, [token.user.email], msg.as_string())
            s.quit()
            token.delete()
        except UserUniqueToken.DoesNotExist:
            raise InvalidUniqueToken

    @staticmethod
    def get_user_by_token(token: str):
        access_token_obj = AccessToken(token)
        user_id = access_token_obj['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = AnonymousUser()
        return user

    @staticmethod
    def get_profile(user):
        return UserProfileSerializer(user).data
