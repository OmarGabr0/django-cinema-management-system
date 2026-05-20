from rest_framework import serializers
from guests.models import Guest

class GuestSerializer(serializers.ModelSerializer):
    # Custom field requirement
    is_vip_guest = serializers.SerializerMethodField()

    class Meta:
        model = Guest
        fields = ['guest_id', 'name', 'email', 'is_vip_guest']
    #vip is based on the email domain 
    def get_is_vip_guest(self, obj):
        
        return obj.email.endswith('@cinema-vip.com')