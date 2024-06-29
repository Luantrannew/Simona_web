from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Customer, Product, Order, OrderLine, CustomerSegments, Category
import pandas as pd
import time


def index(request):
    template = 'index.html'
    
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()

    context = {
        'total_products': total_products,
        'total_customers': total_customers,
    }
    return render(request, template, context)

#############################################
from io import StringIO
def upload_csv(request):
    if request.method == 'POST':
        start_time = time.time()
        csv_file = request.FILES['csv_file']
        csv_data = csv_file.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))
        
        expected_header = ["Thời gian tạo đơn", "Mã đơn hàng", "Mã khách hàng", "Tên khách hàng", "Mã PKKH", "Mô tả Phân Khúc Khách hàng", "Mã nhóm hàng", "Tên nhóm hàng", "Mã mặt hàng", "Tên mặt hàng", "SL", "Đơn giá", "Thành tiền"]
        
        if list(df.columns) != expected_header:
            return JsonResponse({"error": "Sai định dạng file CSV"}, status=400)
        
        # Tách dữ liệu theo từng model
        df_categories = df[["Mã nhóm hàng", "Tên nhóm hàng"]].drop_duplicates(subset=["Mã nhóm hàng"])
        df_segments = df[["Mã PKKH", "Mô tả Phân Khúc Khách hàng"]].drop_duplicates(subset=["Mã PKKH"])
        df_customers = df[["Mã khách hàng", "Tên khách hàng", "Mã PKKH"]].drop_duplicates(subset=["Mã khách hàng"])
        df_products = df[["Mã mặt hàng", "Tên mặt hàng", "Đơn giá", "Mã nhóm hàng"]].drop_duplicates(subset=["Mã mặt hàng"])
        df_orders = df[["Mã đơn hàng", "Thời gian tạo đơn", "Mã khách hàng"]].drop_duplicates(subset=["Mã đơn hàng"])
        df_order_lines = df[["Mã đơn hàng", "Mã mặt hàng", "SL"]]
        
        # Prepare data for bulk_create
        categories = []
        for _, row in df_categories.iterrows():
            categories.append(Category(cat_code=row["Mã nhóm hàng"], cat_name=row["Tên nhóm hàng"]))
        
        Category.objects.bulk_create(categories, ignore_conflicts=True)

        segments = []
        for _, row in df_segments.iterrows():
            segments.append(CustomerSegments(seg_code=row["Mã PKKH"], seg_name=row["Mô tả Phân Khúc Khách hàng"]))

        CustomerSegments.objects.bulk_create(segments, ignore_conflicts=True)

        customers = []
        for _, row in df_customers.iterrows():
            seg = CustomerSegments.objects.get(seg_code=row["Mã PKKH"])
            customers.append(Customer(code=row["Mã khách hàng"], name=row["Tên khách hàng"], seg=seg))

        Customer.objects.bulk_create(customers, ignore_conflicts=True)

        products = []
        for _, row in df_products.iterrows():
            cat = Category.objects.get(cat_code=row["Mã nhóm hàng"])
            products.append(Product(code=row["Mã mặt hàng"], name=row["Tên mặt hàng"], unit_price=row["Đơn giá"], cat=cat))

        Product.objects.bulk_create(products, ignore_conflicts=True)

        orders = []
        for _, row in df_orders.iterrows():
            customer = Customer.objects.get(code=row["Mã khách hàng"])
            orders.append(Order(order_code=row["Mã đơn hàng"], time=row["Thời gian tạo đơn"], customer=customer))

        Order.objects.bulk_create(orders, ignore_conflicts=True)

        order_lines = []
        for _, row in df_order_lines.iterrows():
            order = Order.objects.get(order_code=row["Mã đơn hàng"])
            product = Product.objects.get(code=row["Mã mặt hàng"])
            order_lines.append(OrderLine(order=order, product=product, quantity=row["SL"]))

        OrderLine.objects.bulk_create(order_lines, ignore_conflicts=True)

        end_time = time.time()
        print("Data loading time:", end_time - start_time, "seconds")
        
        return JsonResponse({"message": "Tệp CSV đã được tải lên và xử lý thành công"}, status=200)
    return JsonResponse({"error": "Yêu cầu không hợp lệ"}, status=400)

##############################
######## list custumer ######

from django.db.models import Max
def customer_list(request):
  template = 'record/customer_list.html'
#   customer_objects = Customer.objects.all().annotate(last_order_time=Order.Max('order__time')).order_by('-last_order_time')
  customer_objects = Customer.objects.annotate(last_order_time=Max('order__time')).order_by('-last_order_time')

  customers = [{
    'pk':obj.pk,
    'name':obj.name,
    'seg' :obj.seg
} for obj in customer_objects]


  context = {
      'customers': customers
  }
  return render(request, template, context)

def customer_delete(request, pk):
    customer = Customer.objects.filter(pk=pk).last()
    customer.delete()
    return redirect('customer_list')


##################################################
######### customer_detail ########################


def customer_detail(request, pk):
  template = 'record/customer_detail.html'

  # Lấy thông tin khách hàng dựa trên pk
  customer = Customer.objects.filter(pk=pk).last()

  orders = Order.objects.filter(customer=customer)                     # filter các oject Order thông qua các customer

  context = {
      'customer': customer,
      'orders': orders
  }
  return render(request, template, context)

#####################################################
######### order_detail ##############################

def order_detail(request, order_code):
  template = 'record/order_detail.html'
  order = Order.objects.filter(order_code=order_code).last()
  order_lines = OrderLine.objects.filter(order=order)                   # filter order line thông qua các order 

  context = {
      'order': order,
      'order_lines': order_lines
  }
  return render(request, template, context)



##############################
######## list product ######
def product_list (request):
  template = 'record/product_list.html'
  products = Product.objects.all()
  context = {
      'Products': products
  }
  return render(request, template, context)


def product_detail (request,pk):
    template = 'record/product_detail.html'
    product = Product.objects.filter(pk=pk).last()
    context = {
        'product': product
    }

    return render(request, template, context)

def product_delete(request, pk):
    product = Product.objects.filter(pk=pk).last()
    product.delete()
    return redirect('product_list')




###############################################
########### order_from_customer ###################

from django.db.models import Sum, F

def order_from_customer(request):
    template = 'record/order_from_customer.html'
    order_objects = Order.objects.all().order_by('-time')

    orders = []
    for obj in order_objects:
        # Tính tổng total_amount cho mỗi đơn hàng
        total_amount = OrderLine.objects.filter(order=obj).aggregate(
            total=Sum(F('quantity') * F('product__unit_price'))
        )['total'] or 0

        orders.append({
            'code': obj.pk,
            'time': obj.time,
            'customer': obj.customer,
            'total_amount': total_amount
        })

    context = {
        'orders': orders,
    }
    return render(request, template, context)

def order_delete(request, pk):
    order = Order.objects.filter(pk=pk).last()
    order.delete()
    return redirect('order_from_customer')

####################################
## Form làm từ Django###############
'''
from .forms import OrderForm, OrderLineForm, CustomerForm, ProductForm, OrderLineFormSet
from django.forms import formset_factory

def create_order(request):
  template = 'form.html'

  print(request.POST)
  print(request.POST.get('order_code'))
  print(request.POST.get('order_code'))


  order_form = OrderForm(request.POST or None)

  # Dynamically create an order line formset instance
  OrderLineFormSet = formset_factory(OrderLineForm)
  orderline_formset = OrderLineFormSet(request.POST or None, prefix='orderline')

  if request.method == 'POST':
      if order_form.is_valid() and orderline_formset.is_valid():
          order = order_form.save()

          for form in orderline_formset:
              orderline = form.save(commit=False)
              orderline.order = order

              # Retrieve product name from form data
              product_name = form.cleaned_data.get('product_name')

              if product_name:
                  product = Product.objects.filter(name=product_name).first()
                  if product:
                      orderline.product = product

              orderline.save()

          # Check which button was clicked
          if request.POST.get("submit") == "finish":
              return redirect('order_success')
          # else:
          #     # Redirect to add_order_line view
          #     return redirect('add_order_line')
  
  products = Product.objects.all()
  context = {
      'order_form': order_form,
      'orderline_formset': orderline_formset,
      'products' : products
  }
  return render(request, template, context)

'''

#################################################
####### form điền thông tin về order ############

from django.utils import timezone
from datetime import datetime

def generate_order_code():
    # Lấy mã đơn hàng mới dựa trên số lượng đơn hàng hiện tại + 1
    last_order = Order.objects.last()
    if last_order:
        last_order_number = int(last_order.order_code.split('ORD')[1])
        new_order_number = last_order_number + 1
    else:
        new_order_number = 1
    return f'ORD{new_order_number:07d}'


def form(request):
    template = 'form_bootstraps.html'

    segments_objects = CustomerSegments.objects.all()
    segments = [{   
        'seg_name': obj.seg_name ,  
        'seg_code': obj.seg_code,
    } for obj in segments_objects]

    cato__objects = Category.objects.all()
    cat = [{   
        'cat_name': obj.cat_name ,  
        'cat_code': obj.cat_code,
    } for obj in cato__objects]
    
    products_objects = Product.objects.all()
    products = [{
        'pk': obj.pk,
        'code': obj.code,
        'name': obj.name,
        'unit_price' : obj.unit_price,
        'cat_name': obj.cat.cat_name ,  
        'cat_code': obj.cat.cat_code,
    } for obj in products_objects]
 
    customers_objects = Customer.objects.all()
    customers = [{
        'pk': obj.pk,
        'code': obj.code,
        'name': obj.name,
        'seg_name': obj.seg.seg_name ,  
        'seg_code': obj.seg.seg_code ,
    } for obj in customers_objects]
    
    current_time = datetime.now()

    if request.method == 'POST':
        print(request.POST)

        # Extract data from POST request
        order_id = generate_order_code()  
        customer_code = request.POST.get('customer')
        order_time = current_time    

        # Create Order object
        order = Order.objects.create(
            order_code=order_id,
            time=order_time,
            customer_id=customer_code
        )

        i = 1
        while f'product{i}' in request.POST:
            product_code = request.POST.get(f'product{i}')
            print(product_code)
            quantity = request.POST.get(f'quantity{i}')
            print(quantity)
            if product_code and quantity:
                product = Product.objects.get(code=product_code)
                OrderLine.objects.create(
                    order=order,
                    product=product,
                    quantity=int(quantity)
                )

            i += 1  
        # Return success response
        return JsonResponse({'message': 'Order created successfully'})

    context = {
        'products': products,
        'customers': customers,
        'current_time': current_time,
        'segments': segments,
        'cat' : cat,
    }
    return render(request, template, context)

def generate_customer_code():
    last_customer = Customer.objects.order_by('-code').first()
    if last_customer:
        last_code = int(last_customer.code[3:])  # Extract numeric part
        new_customer_number = last_code + 1
    else:
        new_customer_number = 1
    return f'CUZ{new_customer_number:05d}'

def create_customer(request):
    if request.method == 'POST':
        customer_code = request.POST.get('customerCode')
        customer_name = request.POST.get('customerName')
        seg_code = request.POST.get('seg')

        segment = CustomerSegments.objects.get(seg_code=seg_code)

        customer = Customer.objects.create(
            code=generate_customer_code(),
            name=customer_name,
            seg=segment
        )

        response_data = {
            'message': 'Tạo thành công khách hàng',
            'customer': {
                'code': customer.code,
                'name': customer.name,
                'seg_name': segment.seg_name,
                'seg_code': segment.seg_code,
            }
        }
        
        return JsonResponse(response_data)
    
    segments = CustomerSegments.objects.all()
    context = {'segments': segments}
    return render(request, 'record/customer_form.html', context)

def generate_product_code(cat_code):
    # Lấy sản phẩm cuối cùng theo nhóm hàng
    last_product = Product.objects.filter(cat__cat_code=cat_code).order_by('-code').first()
    if last_product:
        last_product_number = int(last_product.code.replace(cat_code, ''))
        new_product_number = last_product_number + 1
    else:
        new_product_number = 1
    return f'{cat_code}{new_product_number:02d}'

def create_product(request):
    if request.method == 'POST':
        # product_code = request.POST.get('code')
        product_name = request.POST.get('name')
        unit_price = request.POST.get('unit_price')
        cat_code = request.POST.get('cat')

        category = Category.objects.get(cat_code=cat_code)

        product = Product.objects.create(
            code=generate_product_code(cat_code),
            name=product_name,
            unit_price=unit_price,
            cat=category
        )
    
        # Prepare data to return as JSON response
        response_data = {
            'message': 'Đã tạo thành công sản phẩm mới',
            'product': {
                'code': product.code,
                'name': product.name,
                'unit_price': product.unit_price,
            }
        }
        return JsonResponse(response_data)
    
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'record/product_form.html', context)

################################################
################################################
def segment_list(request):
  template = 'record/segment_list.html'
  segments = CustomerSegments.objects.all()  # Lấy tất cả các nhóm khách hàng

  context = {
      'segments': segments,
  }
  return render(request,template, context)
    
from django.http import JsonResponse

def create_segment(request):
    if request.method == 'POST':
        seg_code = request.POST.get('seg_code')
        seg_name = request.POST.get('seg_name')
        
        segment = CustomerSegments.objects.create(
            seg_code=seg_code,
            seg_name=seg_name
        )
        
        # Construct your response data
        response_data = {
            'message': 'Tạo thành công nhóm khách hàng',
            'segment_id': segment.pk,
            'segment_code': segment.seg_code,
            'segment_name': segment.seg_name,
        }
        
        return JsonResponse(response_data)
    
    template = 'record/segment_form.html'
    context = {}
    return render(request, template, context)

def delete_segment(request, segment_id):
    template = 'record/segment_list.html'
    segment= CustomerSegments.objects.filter(pk=segment_id).last()
    
    if request.method == 'POST':
        segment.delete()
        return redirect('segment_list')
    
    context = {}
    return render(request, template, context)