from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Tambahkan is_admin ke payload JWT
        token['is_admin'] = user.is_admin
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # (opsional) tetap tambahkan ke response juga
        data['is_admin'] = self.user.is_admin
        data['username'] = self.user.username
        return data
