from .serializers import MenuSerializer, RestauranteSerializer, RestauranteMenuSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from apps.restaurantes.models import Menu, Restaurante, RestauranteMenu

class MenuViewset(viewsets.ModelViewSet):
    queryset = Menu.objects.activos() #que son consultas se van a poder hacer(conjunto de datos)
    serializer_class = MenuSerializer #como los va a convertir
    
    def create(self, request, *args, **kwargs):                
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)  
        self.perform_create(serializer)  

        return Response({
            "message": "Menu creado.",
            "created_data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs): 
        partial = kwargs.pop('partial', False)
        instance = self.get_object()   
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Los datos han sido actualizados",
            "updated_data": serializer.data 
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        usuario.estado = False
        usuario.is_active = False  
        usuario.save()

        return Response({
            'status': 'success',
            'message': 'El Menu ha sido Eliminado.'
        }, status=status.HTTP_204_NO_CONTENT)
    

class RestauranteViewset(viewsets.ModelViewSet):
    queryset = Restaurante.objects.activos() #que son consultas se van a poder hacer(conjunto de datos)
    serializer_class = RestauranteSerializer #como los va a convertir
    
    def create(self, request, *args, **kwargs):                
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)  
        self.perform_create(serializer)  

        return Response({
            "message": "Restaurante creado.",
            "created_data": serializer.data
        }, status=status.HTTP_201_CREATED)  

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Los datos han sido actualizados",
            "updated_data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        usuario.estado = False
        usuario.is_active = False  
        usuario.save()

        return Response({
            'status': 'success',
            'message': 'El Restaurante ha sido Eliminado.'
        }, status=status.HTTP_204_NO_CONTENT)

class RestauranteMenuViewset(viewsets.ModelViewSet):
    queryset = RestauranteMenu.objects.all()
    serializer_class = RestauranteMenuSerializer #como los va a convertir
    