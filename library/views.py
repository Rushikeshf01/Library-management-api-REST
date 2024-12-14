from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response  
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated ,IsAuthenticatedOrReadOnly,IsAdminUser,SAFE_METHODS
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime,date

from .permissions import IsAdminOrReadOnly,IsOwnerOrAdmin
from .models import Book, Member, Loan
from .serializers import BooksSerializer, MemberSerializer, LoanSerializer, BookReturnSerializer,MyTokenObtainPairSerializer
from .utils import calculate_fine


# Create your views here.
class MyCustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsOwnerOrAdmin]

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author', 'genere']
    

class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAdminUser]

class BookReturnView(UpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = BookReturnSerializer
    permission_classes = [IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        message = "Book returned succefully"
        due_date = instance.due_date
        return_date = request.data.get('return_date')

        # setting up the date to current date if not provided
        if return_date:
            return_date = datetime.strptime(request.data.get('return_date'), "%Y-%m-%d").date() 
        else:
            return_date =  date.today()
            request.data.update({'return_date': return_date})

        if return_date > due_date:
            instance.fine,message = calculate_fine(due_date, return_date)

        # incrementing available_copies on returning book

        # another way - instead of incrementing/decrementng here, may be we can do this using django's
        #               signal(like triggring it on post_save event)
        
        instance.book.available_copies += 1
        instance.book.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"data": serializer.data, "message": message}, status=status.HTTP_200_OK)


# class BooksList(ListCreateAPIView):
#     # queryset = Book.objects.all()
#     queryset = get_list_or_404(Book)
#     serializer_class = BooksSerializer

# class BookDetail(RetrieveUpdateDestroyAPIView):
#     # queryset = get_list_or_404(Book)
#     queryset = Book.objects.all()
#     serializer_class = BooksSerializer
    
    # def get(self, request, id):
    #     book = get_object_or_404(Book, pk=id)
    #     serializer = BooksSerializer(book)
    #     return Response(serializer.data, status = status.HTTP_200_OK)
    
    # def put(self, request, id):
    #     book = get_object_or_404(Book, pk=id)
    #     serializer = BooksSerializer(book, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status = status.HTTP_200_OK)
    
    # def delete(self, request, id):
    #     book = get_object_or_404(Book, pk=id)
    #     book.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'DELETE'])
# def books_detail(request, id):
#     book = get_object_or_404(Book, pk=id)
#     if request.method == 'GET':
#         serializer = BooksSerializer(book)
#         return Response(serializer.data, status = status.HTTP_200_OK)
#     elif request.method == 'PUT':
#         serializer = BooksSerializer(book, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status = status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
