from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.http.response import HttpResponseRedirect
from django.conf import settings

from accounts.models import User

from accounts.serializers.main_serializers import UserRegisterSerializer
from accounts.services import AuthorizationService

from application_info.services import LogService


class Authorization(viewsets.GenericViewSet):
    queryset = User.objects.all()
    service = AuthorizationService

    @action(methods=('post',), detail=False)
    def registration(self, request):
        serializer = UserRegisterSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance
        self.service.send_register_confirm_link(user)
        return Response({'detail': f'На почту {user.email} было выслано письмо для подтверждения вашей личности. '
                                   f'Перейдите по ссылке из письма для окончания регистрации'})

    @action(methods=('post',), detail=False)
    def registration_confirm(self, request):
        user = self.service.registration_confirm(request.query_params.get('tk'))
        LogService.log('new_user-register', f'Новый пользователь. Пользователь: {user.__str__()}; Email: {user.email};',
                       'accounts', user)
        return HttpResponseRedirect(settings.ROOT_APP_ADDR)

    @action(methods=('post',), detail=False)
    def authorization(self, request):
        email = request.data.get("login")
        password = request.data.get("password")
        return Response(self.service.authorize_user(email, password, request))

    @action(methods=('post',), detail=False)
    def password_reset(self, request):
        self.service.password_reset(request.query_params.get('tk'))
        return Response({'detail': 'Письмо с новым паролем отправлено на почту'})

    @action(methods=('post',), detail=False)
    def password_reset_confirm(self, request):
        self.service.password_reset(request.query_params.get('tk'))
        return Response({'detail': 'Письмо с новым паролем было выслано на вашу почту'})

    @action(methods=('get',), detail=False, permission_classes=(IsAuthenticated,))
    def get_profile(self, request):
        return Response(self.service.get_profile(request.user))
