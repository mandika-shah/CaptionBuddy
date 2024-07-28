from django.shortcuts import get_object_or_404, render , redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from .models import Photo,Caption
import uuid
from django.core.mail import send_mail
from django.conf import settings
import re ,json ,requests
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from .generate_caption1 import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def validate_password(password):
    # Use Django's built-in validators for minimum length, common passwords, and numeric passwords
    min_length_validator = MinimumLengthValidator()
    common_password_validator = CommonPasswordValidator()
    numeric_password_validator = NumericPasswordValidator()

    # Validate minimum length
    min_length_validator.validate(password)

    # Validate against common passwords
    common_password_validator.validate(password)

    # Validate against numeric passwords
    numeric_password_validator.validate(password)

    # Custom validation for at least one lowercase, one uppercase, and one special character
    if not any(char.islower() for char in password):
        raise ValidationError("The password must contain at least one lowercase letter.")
    if not any(char.isupper() for char in password):
        raise ValidationError("The password must contain at least one uppercase letter.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("The password must contain at least one digit.")
    if not any(char.isascii() and not char.isalnum() for char in password):
        raise ValidationError("The password must contain at least one special character.")

def validate_username(username):
    # Validate minimum length
    if len(username) < 6:
        raise ValidationError("Username must be at least 6 characters long.")

    # Validate against invalid characters
    if not re.match("^[a-zA-Z0-9_]*$", username):
        raise ValidationError("Username can only contain letters, numbers, and underscores.")

def home(request):
    return render(request, 'header.html')


def index(request):
    uploaded_image = None
    caption = None

    if request.method == 'POST':
        image_file = request.FILES.get('image12')
        if image_file:
          if request.user.is_authenticated:
            user = request.user
          else:
            user = None
          image = Photo.objects.create(user=user,image=image_file)
          image.save()
          caption = generate_caption1(image_file)
          cap = Caption.objects.create(captiontext=caption,image=image)
          cap.save()
          return redirect('show_popup', pk=image.pk)
        else:
         messages.error(request,"Please upload an image.")
    return render(request, 'index.html', {'caption': caption , 'uploaded_image':uploaded_image})

def generate_caption1(image):
    caption=generate_caption(image)
    return caption
def show_popup(request, pk):
    image_instance = Photo.objects.get(pk=pk)
    caption_instance = Caption.objects.get(image=image_instance)
    return render(request, 'popup.html', {'image_instance': image_instance, 'caption_instance': caption_instance})


@login_required
def user_dashboard(request):
    # Retrieve images and captions associated with the logged-in user
    user_images = Photo.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user_images': user_images})

#  for login 
def login1(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(request, username=username, password=password)
       if user is not None :
            if user.is_active :
                    if user.is_superuser:
                        messages.error(request,"Sorry, Use other login credential or create new one.")
                        return redirect('login')
                    else:    
                      login(request, user)
                       # Store user ID in session data
                      request.session['user_id'] = user.id
                      messages.success(request, "User logged in successfully.")
                      return redirect('index')  
            else:
                messages.error(request, 'Please verify your email before logging in.')
       else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'login.html')

# for signup
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm')
        clientKey = request.POST['g-recaptcha-response']
        secretKey = 'put your generated secret key'
        captchaData={
            'secret':secretKey,
            'response':clientKey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=captchaData)
        response = json.loads(r.text)
        verify =response['success']
        # check username and password validation
        try:
            validate_username(username)
            validate_password(password1)
        except ValidationError as e:
            return render(request, 'signup.html', {'error': str(e)})
        if password1!=password2:
            messages.error(request,"Both password should match.")
            return render(request,'signup.html')
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username is already taken'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email is already in use'})
        if verify:
          new_user = User.objects.create_user(username=username, email=email, password=password1)
          new_user.set_password(password1)
          new_user.is_active = False
          new_user.save()
          send_verification_email(request, new_user)
          messages.success(request, "Please check your email to activate your account.")
          return redirect('login')
        else:
            messages.error(request,'Please verify using I am not robot.')
            return render(request,'signup.html')
    return render(request, 'signup.html')

# for logout
def logout1(request):
    logout(request)
    return redirect('home')

# it will send mail for verification.
def send_verification_email(request, user):
     uid = urlsafe_base64_encode(force_bytes(user.pk))
     token = default_token_generator.make_token(user)

    # Build verification URL
     verification_url = request.build_absolute_uri(
            f'/verify/{uid}/{token}/'
        )

    # Compose email subject and body
     subject = 'Verify your email'
     message = render_to_string('verification_email.txt', {
            'user': user,
            'verification_url': verification_url,
        })

    # Send email
     send_mail(subject, message, 'your mail', [user.email])
     
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if user and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Email verified successfully. You can now log in.')
                return redirect('login')  # Redirect to your login page
            else:
                messages.error(request, 'Email verification failed.')
        except User.DoesNotExist:
            messages.error(request, 'Email verification failed. User not found.')
        return redirect('login')          # Redirect to your login page
    

@login_required
def view_saved_data(request):
    captions_with_images = Caption.objects.filter(image__user=request.user).select_related('image')
    return render(request, 'saved_data.html', {'captions_with_images': captions_with_images})

def handler404(request, exception):
    return render(request, 'error.html', status=404)

def handler500(request):
    return render(request, 'error.html', status=500)
        
def handle(request):
    return render(request,'error.html')