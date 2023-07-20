from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthenticatedOrIsEmployee
from .serializers import MovieOrderSerializer, MovieSerializer
from django.shortcuts import get_object_or_404
from .models import Movie


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrIsEmployee]

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        get_movies = Movie.objects.all()
        result_page = self.paginate_queryset(get_movies, request)
        movies_result = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(movies_result.data)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrIsEmployee]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)
        print(MovieSerializer(movie).data)

        return Response(MovieSerializer(movie).data, status=status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)
        order = MovieOrderSerializer(data=request.data)
        order.is_valid(raise_exception=True)
        order.save(user=request.user, movie=movie)

        return Response(order.data, status=status.HTTP_201_CREATED)
