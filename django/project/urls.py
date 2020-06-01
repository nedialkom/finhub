from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from finhub.api.views import CompanyList

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/company/', CompanyList.as_view()),
    path('finhub/', include('finhub.urls')),
    path('', views.base, name='base'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
            template_name='login/password_reset.html',
            subject_template_name='login/password_reset_subject.txt',
            email_template_name='login/password_reset_email.html',
            ),
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='login/password_reset_done.html'
            ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='login/password_reset_confirm.html'
            ),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name='login/password_reset_complete.html'
            ),
          name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)