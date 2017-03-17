"""ACM_General URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views


app_name = 'payments'
urlpatterns = [
    url(
      r'membership/',
      views.MembershipPayment.as_view(),
      name='acm-memberships',
    ),
    url(
        r'productHandler/(?P<pk>[0-9a-z-]+)/',
        views.ProductHandler.as_view(),
        name='product-handler',
    ),
]
