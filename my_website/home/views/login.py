# from django.shortcuts import render , redirect , HttpResponseRedirect
# from django.contrib.auth.hashers import check_password
# from home.models.customer import Customer
# from django.views import View
#
#
# class Login(View):
#     return_url = None
#
#     def get(self, request):
#         Login.return_url = request.GET.get ('return_url')
#         return render (request, 'login.html')
#
#     def post(self, request):
#         email = request.POST.get ('email')
#         password = request.POST.get ('password')
#
#         customer = Customer.get_customer_by_email(email)
#
#         error_message = None
#         if customer:
#             flag = check_password(password, customer.password)
#             # flag = True
#             if flag:
#                 request.session['customer'] = customer.id
#
#                 if Login.return_url:
#                     return HttpResponseRedirect (Login.return_url)
#                 else:
#                     Login.return_url = None
#                     return redirect ('store')
#             else:
#                 error_message = 'Invalid !!'
#         else:
#             error_message = 'Invalid !!'
#
#         print (email, password)
#         return render (request, 'login.html', {'error': error_message})
#
# def logout(request):
#     request.session.clear()
#     return redirect('login')

from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.hashers import check_password
from django.views import View

from home.models.customer import Customer


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render(request, 'login.html')
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        customer = Customer.get_customer_by_email(email)
        print(email)
        print(customer)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponse (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Invalid !! 1'
        else:
            error_message = 'Invalid !! 2'

        return render(request, 'login.html',{'error':error_message})
def logout(request):
    request.session.clear()
    return  redirect('login')