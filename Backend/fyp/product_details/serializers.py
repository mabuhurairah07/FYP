from rest_framework import serializers
from .models import Product,Category,SubCategory,Wishlist,Variation,CompareProducts,MobilePhones,Laptops,LCD,AC
from user_details.models import UserDetails

class AddProductSerializer(serializers.Serializer):
    p_image = serializers.ImageField(required=True)
    p_brand = serializers.CharField(max_length=250)
    p_status = serializers.IntegerField()
    p_des = serializers.CharField(max_length=5000)
    p_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    disc_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.IntegerField()
    category = serializers.CharField(max_length=250)
    sub_category = serializers.CharField(max_length=250)
    user_data = serializers.CharField(max_length=250)
    if category == 'Phones':
            processor = serializers.CharField(max_length=500)
            battery = serializers.CharField(max_length=500)
            memory = serializers.CharField(max_length=500)
            display = serializers.CharField(max_length=500)
            camera = serializers.CharField(max_length=500)
    elif category == 'Laptops':
            processor = serializers.CharField(max_length=500)
            battery = serializers.CharField(max_length=500)
            memory = serializers.CharField(max_length=500)
            display = serializers.CharField(max_length=500)
            generation = serializers.IntegerField()
    elif category == 'AC':
            capacity = serializers.CharField(max_length=500)
            type = serializers.CharField(max_length=500)
            inverter = serializers.BooleanField(default=True)
            warranty = serializers.IntegerField()
            energy_efficiency = serializers.IntegerField()
    elif category =='LCD':
            display = serializers.CharField(max_length=500)
            power_consumption = serializers.CharField(max_length=500)
            audio = serializers.CharField(max_length=500)
            chip = serializers.CharField(max_length=500)
    size = serializers.CharField(max_length=250)
    color = serializers.CharField(max_length=250)
    quantity = serializers.IntegerField()   


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    sub_category = SubCategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'

class MobileSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    sub_category = SubCategorySerializer
    product = ProductSerializer
    class Meta:
        model=MobilePhones
        fields = '__all__'

class LaptopSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    sub_category = SubCategorySerializer
    product = ProductSerializer
    class Meta:
        model=Laptops
        fields = '__all__'

class LCDSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    sub_category = SubCategorySerializer
    product = ProductSerializer
    class Meta:
        model=LCD
        fields = '__all__'

class ACSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    sub_category = SubCategorySerializer
    product = ProductSerializer
    class Meta:
        model=AC
        fields = '__all__'

class WishlistSerializer(serializers.Serializer):
    # product = ProductSerializer()
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        product_id = data.get("product_id", "")
        user_id = data.get("user_id", "")
        if not user_id or not product_id:
            raise serializers.ValidationError("Both User and Product ID's  are required")
        return data

class ShowWishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Wishlist
        fields = '__all__'

class AddCompareSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        product_id = data.get("product_id", "")
        user_id = data.get("user_id", "")
        if not user_id or not product_id:
            raise serializers.ValidationError("Both User and Product ID's  are required")
        return data

class ShowCompareSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CompareProducts
        fields = '__all__'

class VariationSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Variation
        fields = '__all__'