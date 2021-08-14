from rest_framework import serializers


from reviews.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Review
        fields = '__all__'