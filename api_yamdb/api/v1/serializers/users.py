from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Имя me выбирать не стоит')
        elif username is None or username == "":
            raise serializers.ValidationError('Заполните поле имя')
        return username

    def validate_email(self, email):
        if email is None or email == "":
            raise serializers.ValidationError('Заполните поле email')
        return email


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                f'Никнейм {value} уже зарегистрирован в БД.'
            )

        if value == 'me':
            raise serializers.ValidationError('Имя me запрещено.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                f'Адрес почты {value} уже зарегистрирован в БД.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=100, required=True)
