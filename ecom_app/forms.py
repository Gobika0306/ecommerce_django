# # ecom_app/forms.py
# from django import forms
# from .models import CustomUser, Profile

# class CreateUserForm(forms.ModelForm):
#     user_type = forms.ChoiceField(choices=[('admin', 'Admin'), ('manager', 'Manager'), ('staff', 'Staff')])

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#         profile = Profile.objects.create(user=user, user_type=self.cleaned_data['user_type'])
#         return user


from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image','stock']  # Add other fields as needed
