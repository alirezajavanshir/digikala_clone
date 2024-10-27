from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from attribute.models import AttrProduct
from .serializers import (
    CommentSerializer,
    RateCommentSerializer,
    CommentAffectSerializer,
)
from comment.models import Comment, RateComment
from product.models import Product


class CommentCreateAPIViewSet(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class RateCommentAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = RateCommentSerializer
    queryset = RateComment.objects.all()

    def post(self, request, format=None):
        serializer = RateCommentSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(Product, id=request.data["product_id"])
            attr = get_object_or_404(
                AttrProduct, slug=request.data["attribute_slug"], product=product
            )

            # Create and save RateComment instance
            rate_comment = RateComment(attribute=attr, rate=int(request.data["rate"]))
            rate_comment.save()

            # Update average rating
            all_rate_comment = RateComment.objects.filter(attribute=attr).aggregate(
                avarage=Avg("rate")
            )
            avg = all_rate_comment["avarage"] or 0
            attr.rate = int(avg)
            attr.save()

            return Response(data="امتیاز ثبت شد", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AffectiveCommentAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentAffectSerializer
    queryset = Comment.objects.all()

    def post(self, request, format=None):
        serializer = CommentAffectSerializer(data=request.data)
        if serializer.is_valid():
            comment = get_object_or_404(Comment, id=request.data["comment_id"])

            if comment.notaffective.filter(id=request.user.id).exists():
                comment.notaffective.remove(request.user.id)
                comment.notaffective_count -= 1

            if not comment.affective.filter(id=request.user.id).exists():
                comment.affective.add(request.user.id)
                comment.affective_count += 1

            comment.save()
            return Response(data="این نظر مفید بوده است", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotAffectiveCommentAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentAffectSerializer
    queryset = Comment.objects.all()

    def post(self, request, format=None):
        serializer = CommentAffectSerializer(data=request.data)
        if serializer.is_valid():
            comment = get_object_or_404(Comment, id=request.data["comment_id"])

            if comment.affective.filter(id=request.user.id).exists():
                comment.affective.remove(request.user.id)
                comment.affective_count -= 1

            if not comment.notaffective.filter(id=request.user.id).exists():
                comment.notaffective.add(request.user.id)
                comment.notaffective_count += 1

            comment.save()
            return Response(data="این نظر مفید نبوده است", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
