from rest_framework import serializers
from general_app.account_opener.models import Email, Mobile, Activation, UserType, Investor, ETOSCustomer

class AccountOpeningSerializer(serializers.Serializer):
    user_title = serializers.CharField(required=False)
    user_name = serializers.CharField(required=False)
    email_id = serializers.EmailField(required=True)
    user_type = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=False)
    otp = serializers.IntegerField(required=False)
    investor_type = serializers.CharField(required=False)
    company_registration_number = serializers.CharField(required=False)
    type_of_options = serializers.CharField(required=True)

    def validate(self, data):
        type_of_options = data.get('type_of_options')
        
        if type_of_options == 'email_validation':
            required_fields = ['user_title','user_name','email_id','user_type']
            for field in required_fields:
                if field not in data or not data[field]:
                    raise serializers.ValidationError(f"{field.replace('_', ' ').capitalize()} is required for updating details.")
            data['user_title'] = data.get('user_title', None)

        elif type_of_options == 'update_details':
            required_fields = ['mobile_number', 'otp']
            for field in required_fields:
                if field not in data or not data[field]:
                    raise serializers.ValidationError(f"{field.replace('_', ' ').capitalize()} is required for updating details.")
        
        return data


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email', 'activation_key', 'expiry', 'verification']

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ['mobile', 'otp', 'expiry', 'verification']

class OTPVerificationSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

class AccountOpeningSerializer(serializers.Serializer):
    email = serializers.EmailField()
    mobile = serializers.CharField(max_length=15)
    usertype = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=10)
    investor_type = serializers.CharField(max_length=255, required=False, allow_blank=True)
    company_registration_number = serializers.CharField(max_length=50, required=False, allow_blank=True)

class ETOSCustSerializer(serializers.ModelSerializer):
    class Meta:
        model = ETOSCustomer
        fields = ['name', 'user_title', 'email_id']