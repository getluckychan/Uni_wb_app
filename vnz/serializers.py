from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class UserStudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class UserEducatorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Educator
        fields = '__all__'


class SpecialityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'


class ListOfSubjectsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'


class MarksModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = '__all__'


class RankModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'


class DepartmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class GroupsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'




class ListOfUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class StudentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTest
        fields = '__all__'


class SpecialityInDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialityInDepartment
        fields = '__all__'


class SubjectForSpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectForSpeciality
        fields = '__all__'


class UnistuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unistuff
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Email",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
