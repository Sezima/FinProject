from rest_framework import serializers
from rest_framework.decorators import action

from .models import *


class CodeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    class Meta:
        model = Department
        fields = ('id', 'title', 'category', 'created_at', 'description')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['category'] = CategorySerializer(instance.category).data
        representation['images'] = DepartmentImageSerializer(instance.images.all(), many=True).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        department = Department.objects.create(**validated_data)
        return department


class DepartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ('author',)

    def to_representation(self, instance):
        represintation = super().to_representation(instance)
        represintation['images'] = CodeImageSerializer(instance.comments.all(), many=True).data
        cation = self.context.get('action')
        if action == 'list':
            represintation['replies'] = instance.replies.count()
        else:
            represintation['replies'] = ReplySerializer(instance.replies.all(), many=True).data

        return represintation

    def create(self, validated_data):
        request = self.context.get('request')
        image_data = request.FILES
        author = request.user
        problem = Problem.objects.create(author=author, **validated_data)
        for image in image_data.getlist('images'):
            CodeImage.objects.create(image=image, problem=problem)
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image, problem=instance)
        return instance

    def to_representation(self, instance):
        represintation = super().to_representation(instance)
        represintation['images'] = CodeImageSerializer(instance.images.all(), many=True).data
        represintation['replies'] = instance.replies.count()
        return represintation


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(author=request.user, **validated_data)
        return reply

    def to_representation(self, instance):
        represintation = super().to_representation(instance)
        represintation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return represintation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(author=request.user, **validated_data)

        return comment
