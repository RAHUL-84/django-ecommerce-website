from django.db.models import Q
from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.contrib import messages
from django.views import View

from .models import OrderDetail
from .models.product import Product
from .models.category import Category
from .models.customer import Customer

from .models.cart import Cart
from .models.order import OrderDetail

from django.db.models import Q
from django.http import JsonResponse


#===============HOMEPAGE===============#
def home(request):
    if not request.session.has_key('phone'):
        return redirect('login')

    phone = request.session.get('phone')

    category = Category.get_all_categories()
    customer = Customer.objects.filter(phone=phone)
    totalitem = len(Cart.objects.filter(phone=phone))

    name = ""
    for c in customer:
        name = c.name

    categoryID = request.GET.get('category')

    if categoryID:
        products = Product.get_all_product_by_category_id(categoryID)
    else:
        products = Product.objects.all()

    data = {
        'name': name,
        'products': products,
        'category': category,
        'totalitem': totalitem
    }

    return render(request, 'home.html', data)



class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')
    def post(self, request):
        postData = request.POST
        name = postData.get('name')
        phone = postData.get('phone')

        error_message = None

        value = {
            'name':name,
            'phone':phone
        }

        customer = Customer(name=name,
                            phone=phone)

        if(not name):
            error_message = "Name is required."
        elif not phone:
            error_message = "Phone number is required."

        elif len(phone) < 10:
            error_message = "Phone number must be 10 digits."

        elif customer.isExist():
            error_message = "This phone number already exists."

        if not error_message:
            messages.success(request, 'Congratulation !! Register successful.')
            customer.register()
            return redirect('signup')
        else:
            data = {
                'error': error_message,
                'value': value
            }
            return render(request, 'signup.html', data)





class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        phone = request.POST.get('phone')
        error_message = None

        value = {
            'phone': phone
        }
        customer = Customer.objects.filter(phone=request.POST['phone'])
        if customer:
            request.session['phone']=phone
            return redirect('homepage')
        else:
            error_message = "Phone number is invalid."
            data = {
                'error': error_message,
                'value': value
            }

        return render(request, 'login.html', data)




#===============PRODUCT===============#
def productdetail(request,pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.session.has_key('phone'):
        phone = request.session['phone']
        totalitem = len(Cart.objects.filter(phone=phone))
        item_already_in_cart = Cart.objects.filter(Q(product=product) & Q(phone=phone)).exists()
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name


        data = {
            'product':product,
            'item_already_in_cart':item_already_in_cart,
            'name':name,
            'totalitem':totalitem
        }

        return render(request, 'productdetail.html', data)



#===============LOGOUT===============#
def logout(request):
    if request.session.has_key('phone'):
        del request.session['phone']
        return redirect('login')
    else:
        return redirect('login')


def add_to_cart(request):
    phone = request.session['phone']
    product_id = request.GET.get('prod_id')
    product_name = Product.objects.get(id=product_id)
    product = Product.objects.filter(id=product_id)
    for p in product:
        image=p.image
        price=p.price
        Cart(phone=phone,product=product_name,image=image,price=price).save()
        return redirect(f"/product-detail/{product_id}")



#===============CART===============#
def show_cart(request):
    totalitem = 0
    if request.session.has_key('phone'):
        phone = request.session['phone']
        totalitem = len(Cart.objects.filter(phone=phone))

        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name

            cart = Cart.objects.filter(phone=phone)
            data = {
               'name':name,
               'totalitem':totalitem,
               'cart':cart
            }

            if cart:
                return render(request,'show_cart.html', data)
            else:
                return render(request,'empty_cart.html', data)


#===============PLUS BUTTON===============
def plus_cart(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        product_id = request.GET['prod_id']
        cart = Cart.objects.filter(product=product_id, phone=phone).first()
        cart.quantity+=1
        cart.save()

        data = {
            'quantity' :cart.quantity
        }
        return JsonResponse(data)



#===============MINUS BUTTON===============
def minus_cart(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        product_id = request.GET['prod_id']
        cart = Cart.objects.filter(product=product_id, phone=phone).first()
        cart.quantity-=1
        cart.save()

        data = {
            'quantity' :cart.quantity
        }
        return JsonResponse(data)



#===============REMOVE BUTTON===============
def remove_cart(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        product_id = request.GET['prod_id']
        cart = Cart.objects.filter(product=product_id, phone=phone).first()

        cart.delete()

        return JsonResponse()



#===============CHECKOUT===============
def checkout(request):
    totalitem = 0
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')


        cart_product = Cart.objects.filter(phone=phone)
        for c in cart_product:
            qty = c.quantity
            price = c.price
            product_name = c.product
            image = c.image

            OrderDetail(user=phone, product_name=product_name, image=image, qty=qty, price=price).save()
            cart_product.delete()

            totalitem = len(Cart.objects.filter(phone=phone))

            customer = Customer.objects.filter(phone=phone)
            for c in customer:
                name = c.name

            data = {
                'name':name,
                'totalitem':totalitem
            }

            return render(request, 'empty_cart.html', data)

    else:
        return render('login')




#===============ORDER===============
def order(request):
    totalitem = 0
    if request.session.has_key('phone'):
        phone = request.session["phone"]

        totalitem = len(OrderDetail.objects.filter(user=phone))
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name
            order = OrderDetail.objects.filter(user=phone)

            data = {
                'order':order,
                'name':name,
                'totalitem':totalitem
            }

            if order:
                return render(request, 'order.html', data)
            else:
                return render(request, 'emptyorder.html', data)
    else:
        return redirect('login')



#===============SEARCH===============
def search(request):
    totalitem = 0
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        query = request.GET.get('query')
        search = Product.objects.filter(name__contains=query)
        category = Category.get_all_categories()

        totalitem = len(OrderDetail.objects.filter(user=phone))
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name


        data = {
            'name':name,
            'totalitem':totalitem,
            'category':category,
            'search':search,
            'query':query
        }



        return render(request,'search.html', data)
    else:
        return redirect('login')