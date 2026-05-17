from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework import generics, mixins

from guests.models import Guest
from guests.serializers import GuestSerializer

####### WEB UI (FBV) ######
def list_guests(request):
    guests_list = Guest.objects.all()
    return render(request, 'guests/guests_list.html', {'guests': guests_list})

def add_guest(request):
    if request.method == 'POST':
        Guest.objects.create(
            name=request.POST['name'],
            email=request.POST['email']
        )
        return redirect('guests:guests_list')
    return render(request, 'guests/add_guest.html')

def edit_guest(request, id):
    guest = get_object_or_404(Guest, pk=id)
    if request.method == 'POST':
        guest.name = request.POST['name']
        guest.email = request.POST['email']
        guest.save()
        return redirect('guests:guests_list')
    return render(request, 'guests/edit_guest.html', {'guest': guest})

def delete_guest(request, id):
    guest = get_object_or_404(Guest, pk=id)
    if request.method == 'POST':
        guest.delete()
        return redirect('guests:guests_list')
    return render(request, 'guests/delete_guest.html', {'guest': guest})


##### API Views  #####

# api/v1: FBV 
@api_view(['GET', 'POST'])
def guest_api_list(request):
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def guest_api_detail(request, id):
    guest = get_object_or_404(Guest, pk=id)
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guest.delete()
        return Response({'message': 'Guest deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# api/v2: CBV
# Removes if-statements for request methods; maps them to class functions instead.
class GuestListCBV(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GuestDetailCBV(APIView):
    def get(self, request, id):
        guest = get_object_or_404(Guest, pk=id)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, id):
        guest = get_object_or_404(Guest, pk=id)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        guest = get_object_or_404(Guest, pk=id)
        guest.delete()
        return Response({'message': 'Guest deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# api/v3: Mixins 
class GuestListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class GuestDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
     # pk = id 
    lookup_field = 'id' 

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# api/v4 Generic Views 
class GuestListGenerics(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class GuestDetailGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_field = 'id'