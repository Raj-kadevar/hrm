from dj_rest_auth.views import PasswordResetView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from knox.views import LoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, LeaveStatus, Device
from .serializers import AuthSerializer, RegisterSerializer, LeaveSerializer, DeviceSerializer
from .task import send_email_fun
from .utils import send_email


@login_required
def index(request):
    return render(request, "index.html")

@login_required
def leave(request):
    return render(request, "leave.html")

def verification(request, id):
    user = User.objects.get(id=urlsafe_base64_decode(id).decode())
    user.is_active = True
    user.save()
    return render(request, "login.html")


class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, *args, **kwargs):
        return Response(template_name="login.html")


class IndexAPI(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        user = request.user
        return Response({"username":user.username})


class RegisterAPI(PermissionRequiredMixin, CreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    permission_required = ('user.add_user',)
    serializer_class = RegisterSerializer
    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        user.groups.add(Group.objects.get(name=self.request.data.get('roles')))
        send_email(self.request, user)

    def post(self, request, *args, **kwargs):
        super().post(request,*args, **kwargs )
        return Response({"message":"registration successful"})


class LoginAPI(LoginView):
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)

class PasswordReset(PasswordResetView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        return Response(template_name="registration/password_reset_form.html")

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        return Response(template_name="registration/password_reset_done.html")


class GetDevice(ListAPIView):
    serializer_class = DeviceSerializer
    def get_queryset(self):
        queryset = Device.objects.all()
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = Device.objects.filter(name__icontains=search)
        return queryset

    # def get(self, request, *args, **kwargs):
    #     return Response({"data":"0 phone available"})


class AddLeaveAPI(CreateAPIView):
    queryset = LeaveStatus.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LeaveSerializer

    def perform_create(self, serializer):
        leave = serializer.save()
        leave.user = self.request.user
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        send_email_fun.delay(request)
        return Response({"message": "Leave added"})