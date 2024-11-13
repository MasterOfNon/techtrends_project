from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as userlogin, logout as userlogout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from techtrends_fn.models import Product,Review, Ratings
from django.shortcuts import get_object_or_404
from .Rating_review_form import ReviewForm, RatingForm


def signup(request):
    user=None
    error=None
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(f"username:{username} and password:{password}")

        if username and password:
            try:
                user= User.objects.create_user(username=username, password=password)
                return redirect('login')
            except Exception as e:
                error= str(e)
                print("Error:", e)
    else:
            error="Please fill both fields"

    return render(request, 'users/signup.html', {'user':user, 'error':error})



def login (request):

    error=None
    if request.method=='POST':
        username= request.POST.get("username")
        password= request.POST.get('password')

        user= authenticate(request, username=username, password=password) #checks if there is user in db
        if user is not None:
            userlogin(request, user) # If the user is valid, this function from django.contrib.auth logs the user in and starts a session.
            #It links the user to the current session and stores the session data server-side.
            return redirect('home')
        else:
            error="Invalid username or password!!"
        
    return render(request, 'users/login.html', {'error':error})


def logout(request):

    userlogout(request)
    return redirect('login')

@login_required
def rate_and_review(request, product_slug):
    product= get_object_or_404(Product, slug=product_slug) 
    reviews= Review.objects.filter(product=product).order_by('created_at')
    reviewform= ReviewForm()
    ratingform= RatingForm()

    if request.method=='POST':
        if 'rate'in request.POST: # rate contained in django form
            ratingform=RatingForm(request.POST)
            if ratingform.is_valid():
                score=ratingform.cleaned_data['score']
                Ratings.objects.update_or_create(
                    user=request.user, product=product,
                    defaults={'score':score}
                )# save in the tabel
                return redirect('rating_and_review', product_slug=product.slug)
        elif 'review' in request.POST:
            reviewform=ReviewForm(request.POST)
            if reviewform.is_valid():
                content=reviewform.cleaned_data['content']
                Review.objects.create(
                    user=request.user, product=product,
                    content=content
                )# save in the tabel
                return redirect('rating_and_review', product_slug=product.slug)# urls product_slug
            
    context={
        'product':product,
        'reviews':reviews,
        'ratingform':ratingform,
        'reviewform':reviewform
    }
    return render (request,'users/rating_and_review.html', context)
            









    

    



