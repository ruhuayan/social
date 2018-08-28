from django.shortcuts import render, redirect

def gotopage(request):
    return redirect("/social/profile")