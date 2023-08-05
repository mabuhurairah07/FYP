from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from .models import *
from user_details.models import UserDetails
class AddProductView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        image = request.data['p_image']
        if serializer.is_valid():
            category_name = request.data['category']
            category = Category.objects.get(cat_name = category_name)
            sub_cat_name = request.data['sub_category']
            sub_cat = SubCategory.objects.get(sub_name = sub_cat_name)
            user = UserDetails.objects.get(id = request.data['user_data'], is_seller=True)
            product = Product.objects.create(
                    p_name = request.data['p_name'],
                    p_image = request.data['p_image'],
                    p_brand = request.data['p_brand'],
                    p_status = request.data['p_status'],
                    p_des = request.data['p_des'],
                    p_price = request.data['p_price'],
                    disc_price = request.data['disc_price'],
                    discount = request.data['discount'],
                    category = category,
                    sub_category = sub_cat,
                    user_data = user,
                    created_at = timezone.now(),
                    updated_at = timezone.now()
                )
            product.save()
            if category_name == 'Phones':  
                mobile = MobilePhones.objects.create(
                    category = category,
                    sub_category = sub_cat,
                    product = product,
                    processor = request.data['processor'],
                    battery = request.data['battery'],
                    memory = request.data['memory'],
                    display = request.data['display'],
                    camera = request.data['camera']
                )
                mobile.save()
            elif category_name == 'Laptops':
                laptops = Laptops.objects.create(
                    category = category,
                    sub_category = sub_cat,
                    product = product,
                    processor = request.data['processor'],
                    battery = request.data['battery'],
                    memory = request.data['memory'],
                    display = request.data['display'],
                    generation = request.data['generation']
                )
                laptops.save()
            elif category_name == 'LCD':
                lcd = LCD.objects.create(
                    category = category,
                    sub_category = sub_cat,
                    product = product,
                    display = request.data['display'],
                    power_consumption = request.data['power_consumption'],
                    audio = request.data['audio'],
                    chip = request.data['chip']
                )
                lcd.save()
            elif category_name == 'AC':
                ac = AC.objects.create(
                    category = category,
                    sub_category = sub_cat,
                    product = product,
                    capacity = request.data['capacity'],
                    type = request.data['type'],
                    inverter = request.data['inverter'],
                    warranty = request.data['warranty'],
                    energy_efficiency = request.data['energy_efficiency']
                )
                ac.save()
            variation = Variation.objects.create(
                product = product,
                size = request.data['size'],
                color = request.data['color'],
                quantity = request.data['quantity']
            )
            variation.save()
            return Response({
                'data' : serializer.data,
                'error' : False,
                'msg' : 'Product Added Successfully'
            })
        return Response({
            'error' : True,
            'msg' : 'Cannot Add Product',
            'data' : image
        })
class ProductView(APIView):

    def get(self, request):
        allProducts = self.get_allproducts()
        latest = self.get_latest()
        discounted = self.get_discounted()
        if allProducts is not None or latest is not None or discounted is not None:
            return Response({
                'allproducts' : allProducts,
                'latest' : latest,
                'special' : discounted,
                'error'  : False,
            })
        return Response({
            'error' : True,
            'msg' : 'There is an error Fetching data'
        })

    def get_allproducts(self):
        product = Product.objects.all()
        if product is not None:
            serializer = ProductSerializer(product, many=True)
            return serializer.data
        return []
  
    def get_latest(self):
        latest_products = Product.objects.all().order_by('created_at')[:5]
        if latest_products is not None:
            serializer = ProductSerializer(latest_products, many=True)
            return serializer.data
        return []

    def get_discounted(self):
        discounted_products = Product.objects.all().order_by('-disc_price')[:5]
        if discounted_products is not None:
            serializer = ProductSerializer(discounted_products, many=True)
            return serializer.data
        return []

class ProductDetailsView(APIView):

    def get(self, request, id):
        product = Product.objects.get(p_id=id)
        if product is not None:
            serializer = ProductSerializer(product)
            return Response({
                'data' : serializer.data,
                'error' : False,
            })
        return Response({
            'error' : True,
            'msg' : 'Product No Found'
        })
            

class WishlistView(APIView):


    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data['product_id']
            user_id = request.data['user_id']
            if not UserDetails.objects.get(id = user_id):
                return Response({'error' : True, 'data' : serializer.data, 'msg' : 'Related user or Product not Found. Login to Your Account'}, status.HTTP_204_NO_CONTENT)
            product_instance = Product.objects.get(p_id = product_id)
            product_serializer = ProductSerializer(product_instance)
            user_instance = UserDetails.objects.get(id=user_id)
            wishlist, created = Wishlist.objects.get_or_create(product = product_instance , user_data = user_instance)
            if created:
                return Response({'data' : product_serializer.data, 'error' : False, 'msg' : 'Product Added in Wishlist'}, status.HTTP_202_ACCEPTED)
            else:
                return Response({'data' : product_serializer.data, 'error' : True, 'msg' : 'Product Already in Wishlist'}, status.HTTP_207_MULTI_STATUS)
            
        return Response({'data' : serializer.data, 'error' : True, 'msg' : 'Cannot Add Products To Wishlist'}, status.HTTP_204_NO_CONTENT)
    
    def get(self,request,id):
        wishlist = Wishlist.objects.filter(user_data = id)
        if wishlist is not None:
            serializer = ShowWishlistSerializer(wishlist, many=True)
            for products in wishlist:
                p = products.product
                print(p.category.cat_name)
                if p.category.cat_name == 'Phones':
                    phone = MobilePhones.objects.get(product=p)
                    phone_serializer = MobileSerializer(phone)
                    print(phone_serializer.data)
                elif p.category.cat_name == 'LCD':
                    lcd = LCD.objects.get(product=p)
                    lcd_serializer = LCDSerializer(lcd)
                    print(lcd_serializer.data)
                elif p.category.cat_name == 'Laptops':
                    laptops = Laptops.objects.get(product=p)
                    laptop_serializer = LaptopSerializer(laptops)
                    print(laptop_serializer.data)
                elif p.category.cat_name == 'AC':
                    ac = AC.objects.get(product=p)
                    ac_serializer = ACSerializer(ac)
                    print(ac_serializer.data)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'error' : True,
            'msg' : 'There is no Product to Show'
        })

class DeleteWishlistView(APIView):
    def post(self, request):
        serializer = WishlistSerializer(data= request.data)
        if serializer.is_valid():
            product_id = request.data['product_id']
            user_id = request.data['user_id']
            wishlist = Wishlist.objects.get(product_id = product_id, user_data_id = user_id)
            wishlist.delete()
            return Response({
                'error' : False,
                'msg' : 'Product Deleted'
            })
        return Response({
            'error': True,
            'msg' : serializer.errors
        }) 

             
class AddCompareView(APIView):
    
    def post(self, request):
        serializer = AddCompareSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data['product_id']
            user_id = request.data['user_id']
            if not Product.objects.filter(p_id = product_id) or not UserDetails.objects.filter(id = user_id):
                return Response({'msg' : 'Related user or Product not Found', 'error' : True})
            existing = CompareProducts.objects.filter(user_data = user_id).first()
            print(CompareProducts.objects.filter(user_data = user_id).first())
            count = CompareProducts.objects.filter(user_data = user_id).count()
            product_instance1 = Product.objects.get(p_id = product_id)
            if count >= 2 :
                return Response({'msg' : 'Already Two Products In Comparing', 'error' : True})
            product_val = '' 
            if existing is not None:
                product_val = existing.product.p_id
                product_instance = Product.objects.get(p_id = product_val)
                cat_id = product_instance.category
                cat_id1 = product_instance1.category
                if cat_id != cat_id1:
                    return Response({'msg' : 'Products Category Must Be Same', 'error' : True})
            product_serializer = ProductSerializer(product_instance1)
            user_instance = UserDetails.objects.get(id=user_id)
            compare, created = CompareProducts.objects.get_or_create(product = product_instance1 , user_data = user_instance)
            if created:
                
                return Response({'data' : product_serializer.data, 'error' : False, 'msg' : 'Product Added in Compare'}, status.HTTP_202_ACCEPTED)
            elif compare:
                return Response({'data' : product_serializer.data, 'error' : True, 'msg' : 'Product Already in Compare'}, status.HTTP_207_MULTI_STATUS)
            
        return Response({ 'data' : serializer.errors ,'error' : True, 'msg' : 'Cannot Add Products To Compare'}, status.HTTP_204_NO_CONTENT)
    
    def get(self,request, id):
        compare = CompareProducts.objects.filter(user_data = id)
        if compare is not None:
            serializer = ShowCompareSerializer(compare, many=True)
            return Response({
                'data' : serializer.data,
                'error' : False
            })
        return Response({
            'error' : True,
            'msg' : 'There is no Product to Show'
        })

class DeleteCompareView(APIView):
    def post(self, request):
        serializer = AddCompareSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data['product_id']
            user_id = request.data['user_id']
            compare = CompareProducts.objects.get(product_id = product_id, user_data_id = user_id)
            compare.delete()
            return Response({
                'error' : False,
                'msg' : 'Product Deleted'
            })
        return Response({
            'error': True,
            'msg' : serializer.errors
        })

class AddCategoryView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        cat_image = request.data['cat_image']
        if serializer.is_valid():
            cat_name = request.data['cat_name']
            category = Category.objects.create(
                cat_name = cat_name,
                cat_image = cat_image
            )
            return Response({
                'error' : False,
                'data' : serializer.data,
                'msg' : 'Category Added'
            })
        return Response({
            'error' : True,
            'data' : serializer.errors,
            'msg' : 'Cannot Add Category'
        })
            