
from django.db import transaction
import requests
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime,timedelta, timezone
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.crypto import get_random_string

from common_files.common_functions import validate_uk_mobile_number, validate_email, validate_mobile_number
from general_app.account_opener.models import Email, Mobile, Activation, UserType, Investor, ETOSCustomer
from general_app.account_opener.serializers import *
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import os
import logging
import uuid
import traceback

FIRETEXT_API_KEY = 'f2VAUOqmxlOK3EFXT9qItT8829Bmmw'
FIRETEXT_SENDER_NAME = 'ETOS-Bank'

otp_storage = {}
otp_expiration_time = 180  # OTP validity in seconds (3 minutes)
logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
            ),
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
            ),
            'email': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User\'s email address'
            ),
            'mobile': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User\'s Mobile Number'
            ),
            'user_type': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=['Customer', 'Investor']
            ),
            'type_of_options': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Type of operation to perform',
                enum=['email_validation', 'mobile_no_validation', 'account_opening', 'otp_verified']
            ),
        },
        required=['user_title','user_name','email', 'user_type','type_of_options']
    ),
    responses={
        200: openapi.Response(
            description='OK',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Confirmation message'
                    )
                }
            )
        ),
        400: openapi.Response(
            description='Bad request',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Error message'
                    )
                }
            )
        )
    }
)

@api_view(http_method_names=['POST'])
@authentication_classes((OAuth2Authentication,))
@permission_classes((permissions.AllowAny,))
def account_opener_view(request):
    logger.debug('Request data: %s', request.data)
    type_of_options = request.data.get('type_of_options')
    name = request.data.get('name')
    title = request.data.get('title')

    if type_of_options == "email_validation":
        email = request.data.get('email')
        name = request.data.get('name')
        title = request.data.get('title')
        return handle_email_validation(email, name, title)

    elif type_of_options == "mobile_no_validation":
        mobile = request.data.get('mobile')
        return handle_mobile_validation(mobile)

    elif type_of_options == "otp_verified":
        serializer = OTPVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error('Invalid data for OTP validation: %s', serializer.errors)
            return JsonResponse(data={'message': 'Invalid request', 'errors': serializer.errors}, status=400)
        validated_data = serializer.validated_data
        return handle_otp_verification(validated_data)

    elif type_of_options == "account_opening":
        serializer = AccountOpeningSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error('Invalid data for account opening: %s', serializer.errors)
            return JsonResponse(data={'message': 'Invalid request', 'errors': serializer.errors}, status=400)
        validated_data = serializer.validated_data
        return handle_account_creation(validated_data)

    else:
        return JsonResponse(data={'message': 'Invalid type_of_options'}, status=400)

def handle_email_validation(email_id, name, title):
    activation_key = generate_activation_key()
    expiry = datetime.now() + timedelta(minutes=30)

    email_obj, created = Email.objects.get_or_create(email=email_id)
    if email_obj.verification:
        return JsonResponse({'message': 'Email already activated/ Try login'}, status=400)
    
    email_obj.activation_key = activation_key
    email_obj.expiry = expiry
    email_obj.save()

    send_activation_email(email_id, activation_key, name, title)
    return JsonResponse({'message': 'Activation link sent successfully'}, status=200)

def generate_otp_code():
    return get_random_string(length=6, allowed_chars='0123456789')

def generate_activation_key():
    return str(uuid.uuid4())

def generate_customer_id():
    return get_random_string(length=8, allowed_chars='0123456789')

def send_activation_email(email, activation_key, name, title):
    activation_link = f"{settings.BASE_URL}account_opener/activate_email/{activation_key}"
    subject = 'Action Required: Activate your account'
    template_path = os.path.join(settings.BASE_DIR, 'general_app', 'account_opener', 'templates', 'registration', 'activation_email.html')
    message = render_to_string(template_path,  {
        'name': name,
        'activation_key': activation_key,
        'title': title,
        'activation_link': activation_link,
    })
               
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    msg = EmailMultiAlternatives(subject, message, email_from, recipient_list)
    msg.attach_alternative(message, "text/html")
    msg.send()

    
def handle_mobile_validation(mobile):
    otp = generate_otp_code()
    expiry = datetime.now() + timedelta(minutes=3)

    mobile_obj, created = Mobile.objects.get_or_create(mobile=mobile)

    if mobile_obj.verification:
        return JsonResponse({'message': 'Mobile number already activated/ Try login'}, status=400)
    
    mobile_obj.otp = otp
    mobile_obj.expiry = expiry
    mobile_obj.save()
    send_otp(mobile, otp)
    return JsonResponse({'message': 'OTP Sent to mobile number'}, status=200)

def handle_otp_verification(validated_data):
    mobile = validated_data['mobile']
    otp = validated_data['otp']
    mobile_obj = get_object_or_404(Mobile, mobile=mobile, otp=otp)

    if mobile_obj.expiry < datetime.now(timezone.utc):
        return JsonResponse({'message': 'OTP expired'}, status=400)

    mobile_obj.verification = True
    mobile_obj.save()
    return JsonResponse({'message': 'OTP verification successful'}, status=200)

def handle_account_creation(validated_data):
    try:
        email_id = validated_data.get('email')
        mobile_number = validated_data.get('mobile')
        usertype = validated_data.get('usertype')
        name = validated_data.get('name')
        title = validated_data.get('title')
        etos_customer_id = generate_customer_id()

        email_obj = get_object_or_404(Email, email=email_id, verification=True)
        mobile_obj = get_object_or_404(Mobile, mobile=mobile_number, verification=True)

        activation, created = Activation.objects.get_or_create(mobile=mobile_obj, email=email_obj)
        
        if usertype.lower() == 'customer':
            user_type_obj, created = UserType.objects.get_or_create(customer=True)
        elif usertype.lower() == 'investor':
            investor_type = validated_data.get('investor_type')
            company_registration_number = validated_data.get('company_registration_number', None)
            investor_obj, created = Investor.objects.get_or_create(investor_type=investor_type, company_registration_number=company_registration_number)
            user_type_obj, created = UserType.objects.get_or_create(investor=investor_obj)
        else:
            return JsonResponse({'message': 'Invalid user type'}, status=400)

        try:
            etos_cust = ETOSCustomer.objects.get(email_id=email_obj)
        except ETOSCustomer.DoesNotExist:
            etos_cust = ETOSCustomer(email_id=email_obj)
            etos_cust.name = name
            etos_cust.user_title = title
            etos_cust.etos_customer_id = etos_customer_id
            etos_cust.user_type = user_type_obj
            etos_cust.mobile_number = mobile_obj
            etos_cust.activation = activation
            etos_cust.is_active = True
            etos_cust.investor_type_id = investor_obj.investor if usertype.lower() == 'investor' else None
            etos_cust.created_on = datetime.now()
            etos_cust.save()

        return JsonResponse({'message': 'Details updated successfully'}, status=200)
        
    except Email.DoesNotExist:
        return JsonResponse({'message': 'Email not verified'}, status=400)
    except Mobile.DoesNotExist:
        return JsonResponse({'message': 'Mobile number not verified'}, status=400)
    except ETOSCustomer.DoesNotExist:
        return JsonResponse({'message': 'Customer does not exist'}, status=400)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'message': 'An error occurred while updating details', 'error': str(e)}, status=500)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('activation_key', openapi.IN_PATH, description="Activation key for email verification", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(description="Email address successfully verified."),
        400: openapi.Response(description="Activation link has expired. Please request a new activation email."),
        404: openapi.Response(description="Invalid activation key."),
        500: openapi.Response(description="An error occurred during email verification."),
    }
)

@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def activate_email(request, activation_key):
    email_obj = get_object_or_404(Email, activation_key=activation_key)

    if email_obj.expiry < datetime.now(timezone.utc):
        return JsonResponse({'message': 'Activation key expired'}, status=400)

    email_obj.verification = True
    email_obj.save()
    return JsonResponse({'message': 'Email Activated successfully'}, status=200)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email_id': openapi.Schema(description="Email address to verify", type=openapi.TYPE_STRING),
        },
        # required=['email', 'activation_key']
    ),
    responses={
        200: openapi.Response(description="Email verification status retrieved successfully."),
        400: openapi.Response(description="Invalid activation key or email."),
        500: openapi.Response(description="An error occurred while retrieving email verification status."),
    }
)
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def verify_email_status(request):
    try:
        email = request.data.get('email')
        data = get_object_or_404(Email, email=email)

        if data.verification:
            return JsonResponse({'message': 'verified'}, status=200)

        if data.expiry < datetime.now(timezone.utc):
            return JsonResponse({'message': 'expired'}, status=400)

        return JsonResponse({'message': 'not verified'}, status=400)

    except AccountOpeningModel.DoesNotExist:
        return JsonResponse({'message': 'Invalid activation key or email.'}, status=400)
    except Exception as e:
        return JsonResponse({'message': 'An error occurred while retrieving email verification status.', 'error': str(e)}, status=500)

def send_otp(mobile_number, otp):
    
    message_body = f"Your Verification code is: {otp}. This code will expire in 3 minutes. Please do not share this code with anyone."
    
    api_url = f"https://www.firetext.co.uk/api/sendsms?apiKey={FIRETEXT_API_KEY}&message={message_body}&from={FIRETEXT_SENDER_NAME}&to={mobile_number}&reference=otp"

    try:
        response = requests.get(api_url)
        response_text = response.text

        if response_text.startswith("0:"):
            logger.info('SMS successfully queued')
            return True
        else:
            logger.error('Failed to send OTP via FireText: %s', response_text)
            raise Exception(response_text)
    except Exception as e:
        logger.error('Failed to send OTP via FireText: %s', str(e))
        raise