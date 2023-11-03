from rest_framework import serializers
from authentication.models import User
from .models import Tour, TourURL, TourOperator, Country, State, City
from django.db.models import Avg


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'user_type']


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        name = validated_data.pop('name', None)
        role = validated_data.pop('role', 3)
        user_type = validated_data.pop('user_type', None)

        user = User(username=username,
                    email=username,
                    name=name,
                    role=role,
                    user_type=user_type,
                    )
        user.set_password(password)
        user.save()
        return user


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'user_type']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.user_type = validated_data.get('user_type', instance.user_type)

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'user_type', 'created_by']
        extra_kwargs = {'created_by': {'read_only': True}}


class UserCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'user_type', 'created_by']
        extra_kwargs = {'password': {'write_only': True}}
        extra_kwargs = {'created_by': {'read_only': True}}

    def create(self, validated_data):
        username = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        name = validated_data.pop('name', None)
        role = validated_data.pop('role', 3)
        user_type = validated_data.pop('user_type', None)
        created_by = validated_data.pop('created_by', None)

        user = User(username=username,
                    email=username,
                    name=name,
                    role=role,
                    user_type=user_type,
                    created_by=created_by
                    )
        user.set_password(password)

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'user_type', 'created_by']
        extra_kwargs = {'created_by': {'read_only': True}}

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.user_type = validated_data.get('user_type', instance.user_type)

        instance.save()
        return instance

class TourURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourURL
        fields = ['url', 'stream']

class TourOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOperator
        fields = ['name', 'id']

class TourSerializer(serializers.ModelSerializer):
    # tour_operator = TourOperatorSerializer(read_only=True)
    tour_urls = TourURLSerializer(many=True)

    class Meta:
        model = Tour
        fields = ['id', 'date_created', 'tour_operator', 'country', 'state', 'city', 'rating', 'n_reviews', 'email', 'website', 'tour_urls']
    
    def create(self, validated_data):
        tour_urls_data = validated_data.pop('tour_urls')
        print(validated_data)
        # validated_data['tour_operator'] = validated_data['tour_operator'].id
        tour = Tour.objects.create(**validated_data)
        for tour_url_data in tour_urls_data:
            TourURL.objects.create(tour=tour, **tour_url_data)
        return tour
    
    def update(self, instance, validated_data):
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        # instance.category = validated_data.get('category', instance.category)
        instance.email = validated_data.get('email', instance.email)
        instance.website = validated_data.get('website', instance.website)
        
        # Handle tour_urls
        instance.tour_urls.all().delete()
        tour_urls_data = validated_data.pop('tour_urls')
        for tour_url_data in tour_urls_data:
            TourURL.objects.create(tour=instance, **tour_url_data)
        
        instance.save()
        return instance


    def to_representation(self, instance):
        representation = super(TourSerializer, self).to_representation(instance)
        representation['tour_operator_name'] = instance.tour_operator.name
        # representation['category_name'] = dict(Tour.CATEGORIES)[instance.category]
        representation['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return representation

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'