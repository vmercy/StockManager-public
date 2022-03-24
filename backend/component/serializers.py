from rest_framework import serializers
from rest_framework_recaptcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
import bleach
from .models import Category, Component, Compartment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "get_thumbnail",
            "get_nb_ref",
            "get_nb_units"
        ]
    def validate_name(self, value):
      return bleach.clean(value)

class CompartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compartment
        fields = [
            "id",
            "get_nb_ref",
            "get_nb_units",
            "get_filling_rate"
        ]

class ComponentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    category_slug = serializers.CharField(source='category.slug')
    class Meta:
        model = Component
        fields = [
            "id",
            "category",
            "category_name",
            "category_slug",
            "title",
            "ref",
            "desc",
            "get_image",
            "get_thumbnail",
            "get_absolute_url",
            "date_added",
            "date_updated",
            "quantity",
            "compartment",
            "datasheet_url",
        ]

class ComponentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = [
            "id",
            "category",
            "title",
            "ref",
            "desc",
            "image",
            "get_image",
            "get_thumbnail",
            "get_absolute_url",
            "date_added",
            "date_updated",
            "quantity",
            "compartment",
            "datasheet_url",
        ]
    def validate_title(self, value):
      return bleach.clean(value)
    def validate_ref(self, value):
      return bleach.clean(value)
    def validate_desc(self, value):
      return bleach.clean(value)

class RegisterSerializer(serializers.ModelSerializer):
    recaptcha = ReCaptchaField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
          "username",
          "password",
          "password2",
          "recaptcha",
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe saisis sont différents"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user