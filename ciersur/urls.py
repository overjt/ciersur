from django.urls import include, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
	re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^password_change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    re_path(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'^admin/', admin.site.urls),
    # re_path(r'^markdown/', include("django_markdown2.urls")), # django_markdown2 does not have urls
    re_path(r'^', include('app.urls')),
]
