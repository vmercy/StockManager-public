from django.db.models import Q
from django.http import Http404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import generics

from .models import Component, Category, Compartment
from .serializers import CategorySerializer, ComponentSerializer, CompartmentSerializer, ComponentAddSerializer, RegisterSerializer

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class LastUpdatedComponentsList(APIView):
  def get(self, request, format=None):
    components = Component.objects.all()[0:10]
    serializer = ComponentSerializer(components, many=True)
    return Response(serializer.data)

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class AllComponents(APIView):
  def get(self, request, format=None):
    components = Component.objects.all()
    serializer = ComponentSerializer(components, many=True)
    return Response(serializer.data)

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
class AddComponent(APIView):        
  def post(self, request, format=None):
    parser_classes = [MultiPartParser, FormParser]
    serializer = ComponentAddSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class CategoriesList(APIView):
  def get(self, request, format=None):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class CompartmentsList(APIView):
  def get(self, request, format=None):
    compartments = Compartment.objects.all()
    serializer = CompartmentSerializer(compartments, many=True)
    return Response(serializer.data)

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class CompartmentDetail(APIView):
  def get_compartment(self, compartment_id):
    try:
      return Compartment.objects.get(id=compartment_id)
    except Compartment.DoesNotExist:
      raise Http404
  
  def get(self, request, compartment_id, format=None):
    compartment = self.get_compartment(compartment_id)
    serializer = CompartmentSerializer(compartment)
    return Response(serializer.data)

  """ def post(self, request, compartment_id, format=None):
    serializer = CompartmentSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class ComponentDetail(APIView):
  def get_object(self, component_id):
    try:
      return Component.objects.get(id=component_id)
    except Component.DoesNotExist:
      raise Http404
  
  def get(self, request, component_id, format=None):
    component = self.get_object(component_id)
    serializer = ComponentSerializer(component)
    return Response(serializer.data)

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
class DeleteComponent(APIView):
  def delete(self, request, component_id, format=None):
    try:
      component = Component.objects.get(id=component_id)
      component.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except Component.DoesNotExist:
      raise Http404

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class CategoryDetail(APIView):
  def get_category(self, category_slug):
    try:
      return Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
      raise Http404
  def get(self, request, category_slug, format=None):
      category = self.get_category(category_slug)
      serializer = CategorySerializer(category)
      return Response(serializer.data)
  
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class ComponentsOfCategory(APIView):
  def get_category(self, category_slug):
    try:
      return Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
      raise Http404

  def get_objects(self, category):
    try:
      return Component.objects.filter(category=category).all()
    except Component.DoesNotExist:
      raise Http404
  
  def get(self, request, category_slug, format=None):
    category = self.get_category(category_slug).id
    components = self.get_objects(category)
    serializer = ComponentSerializer(components, many=True)
    return Response(serializer.data)

@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
class ComponentsInCompartment(APIView):
  def get_objects(self, compartment_id):
    try:
      return Component.objects.filter(compartment=compartment_id).all()
    except Component.DoesNotExist:
      raise Http404
  
  def get(self, request, compartment_id, format=None):
    components = self.get_objects(compartment_id)
    serializer = ComponentSerializer(components, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def searchComponent(request):
  search_query = request.data.get('query', '')
  if(search_query):
    components = Component.objects.filter(Q(ref__icontains=search_query) |Q(title__icontains=search_query) | Q(desc__icontains=search_query))
    serializer = ComponentSerializer(components, many=True)
    return Response(serializer.data)
  else:
    return Response([])

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
