from django.shortcuts import render, redirect




def main(request):
    if checkCookies():
        return render(request, 'tutorPage.html')
    else:
        return redirect('/about')
def about_page(request):
    return render(request, 'about.html')

def login_page(request):
    return render(request, 'login.html')


def checkCookies():
    return False


