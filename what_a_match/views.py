from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect



def index(request):
    """Public homepage for What-A-Match"""
    return render(request, 'what_a_match/index.html')
