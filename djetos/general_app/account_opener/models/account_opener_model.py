from django.db import models
from django.core.exceptions import ValidationError

class Email(models.Model):
    email = models.EmailField(primary_key=True, max_length=250, unique=True)
    activation_key = models.CharField(max_length=255, null=True, blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    verification = models.BooleanField(default=False)

    class Meta:
        db_table = "emails"


class Mobile(models.Model):
    mobile = models.CharField(primary_key=True, max_length=15, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    verification = models.BooleanField(default=False)

    class Meta:
        db_table = "mobiles"


class Activation(models.Model):
    activationnum = models.AutoField(primary_key=True)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)

    class Meta:
        db_table = "activations"


class UserType(models.Model):
    usertype = models.AutoField(primary_key=True)
    customer = models.BooleanField(default=False)
    investor = models.ForeignKey('Investor', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "user_types"


class Investor(models.Model):
    class InvestorType(models.TextChoices):
        COMPANY = 'company', 'Company'
        INDIVIDUAL = 'individual', 'Individual'
    investor = models.AutoField(primary_key=True)
    investor_type = models.CharField(max_length=10, choices=InvestorType.choices, default=InvestorType.INDIVIDUAL)
    company_registration_number = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "investors"
    
    def clean(self):
        if self.investor_type == self.InvestorType.COMPANY:
            if not self.company_registration_number:
                raise ValidationError('Company registration number is mandatory for company investors.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ETOSCustomer(models.Model):
    cust_id = models.AutoField(primary_key=True, db_column="account_application_id")
    name = models.CharField(max_length=255, null=True, blank=True)
    user_title = models.CharField(max_length=10, null=True, blank=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, db_column="user_type")
    email_id = models.ForeignKey(Email, on_delete=models.CASCADE, db_column="email_id")
    mobile_number = models.ForeignKey(Mobile, on_delete=models.CASCADE, db_column="mobile_number", null=True, blank=True)
    activation = models.ForeignKey(Activation, on_delete=models.CASCADE, db_column="activation", null=True, blank=True)
    app_passcode = models.CharField(max_length=255, null=True, blank=True)
    bank_opening_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    etos_customer_id = models.IntegerField(default=None, null=True)
    investor_type = models.ForeignKey(Investor, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "ETOS_customers"

    def save(self, *args, **kwargs):
        if self.email_id.verification and (self.mobile_number is None or self.mobile_number.verification):
            self.is_active = True
        super(ETOSCustomer, self).save(*args, **kwargs)
