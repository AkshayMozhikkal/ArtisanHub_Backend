from rest_framework.generics import *
from .serializers import *
from .models import *

# Create your views here.

class Banner_List_Create(ListCreateAPIView):
    serializer_class = Banner_Serializer
    queryset = Banner.objects.all().order_by('index')
    

class Banner_Edit_Delete(RetrieveUpdateDestroyAPIView):
    lookup_field ='id'
    serializer_class = Banner_Serializer
    queryset = Banner.objects.all().order_by('id')    
