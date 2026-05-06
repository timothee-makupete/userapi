from rest_framework import serializers
from .models import User, Address, Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'catch_phrase', 'bs']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'suite', 'city', 'zipcode', 'lat', 'lng']

class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    company = CompanySerializer()
    
    class Meta:
        model = User
        fields = [
            'id', 'external_id', 'name', 'username', 'email',
            'phone', 'website', 'address', 'company', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        company_data = validated_data.pop('company')
        
        # Get or create address to avoid duplicates
        address, _ = Address.objects.get_or_create(**address_data)
        company, _ = Company.objects.get_or_create(
            name=company_data['name'],
            defaults={
                'catch_phrase': company_data.get('catch_phrase', ''),
                'bs': company_data.get('bs', '')
            }
        )
        
        user = User.objects.create(
            address=address,
            company=company,
            **validated_data
        )
        return user
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        company_data = validated_data.pop('company', None)
        
        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()
        
        if company_data:
            for attr, value in company_data.items():
                setattr(instance.company, attr, value)
            instance.company.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance