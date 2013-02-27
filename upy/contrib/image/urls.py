"""
It includes urlpatterns necessary for upy.contrib.images
"""
from django.conf.urls import *
urlpatterns = patterns('',
        (r'^img_preview$','upy.contrib.image.views.img_preview'),
)
