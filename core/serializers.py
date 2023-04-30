from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Graphics, HomePageSlider, HomePageSmallPicture, Logo

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'user': self.user.username})
        data.update({'email': self.user.email})
        data.update({'first_name': self.user.first_name})
        data.update({'last_name': self.user.last_name})
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data




class HomePageSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageSlider
        fields = ['id', 'subtitle', 'image', 'link']

class HomePageSmallPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageSmallPicture
        fields = ['id', 'title', 'subtitle', 'image', 'link']

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = ['id', 'image']

class GraphicsSerializer(serializers.ModelSerializer):
    home_page_slider = HomePageSliderSerializer(many=True, read_only=True)
    home_page_small_picture = HomePageSmallPictureSerializer(many=True, read_only=True)
    logo = LogoSerializer(read_only=True)

    class Meta:
        model = Graphics
        fields = ['home_page_slider', 'home_page_small_picture', 'logo']