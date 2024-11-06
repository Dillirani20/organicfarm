from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Categories,Cart,Product,SellerProduct,Payment, Tracking,Profile
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import random


# Create your views here.



def index(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})

@login_required
def base_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)  # Get the user's profile

    return render(request, "base.html", {'user': user, 'profile': profile})



def register(request):
  
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = email)
        
        if user.exists():
            messages.info(request, "Email already taken")
            return redirect('/register/')
        
        user =User.objects.create(
            username = email,
            email=email,
        )
        user.set_password(password)
        Profile.objects.create(user=user)
        user.save()
        login(request, user)
        # return redirect("index")
        messages.info(request,'Enter Information')
        return redirect("profileset")
    return render(request, 'user_register.html')
        
    
  
def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=email).exists():
            messages.info(request, "Invalid Username")
            return redirect('login')
        
        user = authenticate(username = email,password = password )
        
        if user is None:
            messages.info(request, "Invalid Password")
            return redirect('login')
        
        else:
            login(request,user)
            return redirect('index')
    
    return render(request,'user_login.html')

@login_required
def logout_page(request):
    logout(request)
    return redirect('/')



@login_required
def profileset(request):
    user = request.user  # Get the logged-in user directly

    if request.method == 'POST':
        mob_no = request.POST.get('moblienumber')
        gender = request.POST.get('gender')
        image = request.FILES.get('profilepic')

        # Use update_or_create to handle both updating and creating the profile
        profile, created = Profile.objects.update_or_create(
            user=user,
            defaults={
                'mob_no': mob_no,
                'gender': gender,
                'image': image
            }
        )

        # Provide feedback to the user
        if created:
            messages.success(request, 'Profile Created Successfully.')
        else:
            messages.success(request, 'Profile Updated Successfully.')

        return redirect("index")

    # If the request method is GET, render the profile form
    return render(request, "profile-details.html", {'user': user})


@login_required
def product_detail(request,id):
    prod_detail =  Product.objects.get(id=id)
    return render(request,'product_detail.html',{'prod_detail':prod_detail})


#Seller Views

def seller_register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = email)
        
        if user.exists():
            messages.info(request, "Email already taken")
            return redirect('seller_register')
        
        user =User.objects.create(
            username = email,
            email=email,
            is_staff=True
        )
        user.set_password(password)
        # Profile.objects.create(user=user)
        user.save()
        login(request, user)
        return redirect("seller_dashboard")
        # messages.info(request,'Enter Information')
        # return redirect("profileset")
    return render(request, 'seller/seller_register.html')
        
    
  
def seller_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=email).exists():
            messages.info(request, "Invalid Username")
            return redirect('seller_login')
        
        user = authenticate(username = email,password = password )
        
        if user is None:
            messages.info(request, "Invalid Password")
            return redirect('seller_login')
        
        else:
            login(request,user)
            return redirect('seller_dashboard')
    
    return render(request,'seller/seller_login.html')


def seller_dashboard(request):
    products = Product.objects.filter(user=request.user)
    return render(request,'seller/seller_dashboard.html',{'products':products})

@login_required
def seller_dashboard(request):
    # Fetch products for the logged-in seller based on approval status
    approved_products = SellerProduct.objects.filter(user=request.user, approval_status='approved')
    pending_products = SellerProduct.objects.filter(user=request.user, approval_status='pending')
    rejected_products = SellerProduct.objects.filter(user=request.user, approval_status='rejected')
    
    context = {
        'approved_products': approved_products,
        'pending_products': pending_products,
        'rejected_products': rejected_products,
    }
    return render(request, 'seller/seller_dashboard.html', context)


def add_product(request):
    categories = Categories.objects.all()
    return render(request,'seller/add_seller_product.html',{'categories':categories})


def delete_product(request,id):
    del_product = Product.objects.get(id=id)
    del_product.delete()
    return redirect('seller_dashboard') 



@login_required
def add_seller_product(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image') 
        
        # Assuming category exists, you may need to handle errors if it doesn't
        category = Categories.objects.get(id=category_id)
        
        seller_product = SellerProduct(
            user=request.user,  # Current logged-in user
            category=category,
            name=name,
            price=price,
            image=image,
            description=description,
            accept=False  # Default to not accepted
        )
        seller_product.save()
        return redirect('product_list')  # Redirect after saving
    
    categories = Categories.objects.all()  # Pass categories to template for selection
    return render(request, 'seller/add_seller_product.html', {'categories': categories})


# View for displaying pending seller products for approval
@staff_member_required
def pending_seller_products(request):
    # Fetch all products where approval_status='pending'
    pending_products = SellerProduct.objects.filter(approval_status='pending')
    context = {
        'pending_products': pending_products
    }
    return render(request, 'pending_seller_products.html', context)

# View to approve a seller's product
@staff_member_required
def approve_seller_product(request, product_id):
    product = get_object_or_404(SellerProduct, id=product_id)
    if request.method == 'POST':
        product.approval_status = 'approved'  # Update approval status
        product.save()
        return redirect('pending_seller_products')  # Redirect back to pending list after approval
    
    return render(request, 'approve_seller_product.html', {'product': product})

# View to reject a seller's product
@staff_member_required
def reject_seller_product(request, product_id):
    product = get_object_or_404(SellerProduct, id=product_id)
    if request.method == 'POST':
        product.approval_status = 'rejected'  # Update approval status
        product.save()
        return redirect('pending_seller_products')  # Redirect back to pending list after rejection

    return render(request, 'reject_seller_product.html', {'product': product})



def delete_seller_product(request,id):
    prod=SellerProduct.objects.get(id=id)
    prod.delete()
    return redirect('product_list') 

def product_list(request):
    seller_product = SellerProduct.objects.filter(user=request.user)
    return render(request,'seller/product_list.html',{'seller_product':seller_product})

#Admin Views

def admin(request):
    return redirect('/admin/')

def admin_request(request):
    seller_product = SellerProduct.objects.filter(user=request.user)
    return render(request,'admin_request.html',{'seller_product':seller_product})

@staff_member_required  # Ensure only admin/staff can access this view
def admin_request(request):
    # Fetch all seller products where approval_status is 'pending'
    pending_products = SellerProduct.objects.filter(approval_status='pending')
    return render(request, 'admin_request.html', {'pending_products': pending_products})



def approve_product(request,id):
    seller_product = SellerProduct.objects.get(id=id)
    
    Product.objects.create(
            user=seller_product.user,
            category=seller_product.category,
            name=seller_product.name,
            price=seller_product.price,
            image=seller_product.image,
            description=seller_product.description
        )
        
    seller_product.delete()
    return redirect('admin_request')  
   



def error_page(request):
    return render(request,'error_page.html')

def shop_page(request):
    products = Product.objects.all() 
    categories=Categories.objects.all()
    return render(request,'shop.html',{'products':products,'categories':categories})

def category(request):
    categories = Categories.objects.all()
    products = Product.objects.all()  # Get all products by default

    # Check if a category is selected
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category=category_id)  # Filter products by selected category

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request,'shop.html',context)


def search(request):
    q=request.GET['query']
    results = Product.objects.filter(name__icontains=q) 
    categories=Categories.objects.all()
    return render(request,'search_results.html',{'products':results,'categories':categories})


@login_required 
def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    # Check if the item already exists in the user's cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,  # Associate the cart item with the logged-in user
        product=product
    )

    if not created:
        # If the item already exists in the cart, increase the quantity
        cart_item.quantity += 1
    else:
        # If the item is new, default quantity is 1 (handled in model)
        cart_item.quantity = 1

 
    cart_item.save()

    return redirect('cart_view')  


@login_required
def cart_view(request):
    # Filter cart items by the current logged-in user
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})



@login_required
def delete(request,id):
    object=Cart.objects.get(id=id)
    object.delete()
    return redirect("cart_view")



@login_required
def payment(request):
    amount = request.GET.get('rs')
    if request.method == "POST":
        total = request.POST.get('amount')
        user = request.POST.get('user')
        email = request.POST.get('email')
        add = request.POST.get('add')
        place = request.POST.get('place')
        paytype = request.POST.get('paytype')

        # Save payment details
        payment_record = Payment.objects.create(
            amount=total,
            username=user,
            email=email,
            address=add,
            place=place,
            paytype=paytype
        )

        # Generate a random tracking number
        tracking_number = f"TRK{random.randint(100000, 999999)}"

        # Save tracking details
        tracking_record = Tracking.objects.create(
            payment=payment_record,
            tracking_number=tracking_number,
            status="Processing"  # Default status is "Processing"
        )

        # Generate tracking URL
        tracking_url = request.build_absolute_uri(reverse('tracking', args=[payment_record.id]))

        # Send confirmation email with tracking details
        subject = 'Payment Confirmation and Tracking Details'
        message = f"""
        Dear {user},

        Thank you for your payment of {total}. Your order is being processed.

        Your tracking number is: {tracking_record.tracking_number}

        You can track your order using the following link:
        {tracking_url}

        We will notify you once the status of your order changes.

        Thank you for shopping with us!

        Best regards,
        Farm Fresh
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Redirect to success or home page after sending the email
        return render(request, 'success.html')

    return render(request, 'payment.html', {'amount': amount})


@login_required
def tracking_view(request,id):
    # Fetch the payment and associated tracking information
    payment = get_object_or_404(Payment, id=id)
    tracking = get_object_or_404(Tracking, payment=payment)

    context = {
        'payment': payment,
        'tracking': tracking
    }
    return render(request, 'tracking_details.html', context)

