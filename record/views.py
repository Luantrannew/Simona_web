from django.shortcuts import render,redirect
from .models import Customer,Product,Order,OrderLine
import pandas as pd
import time


data = 'C:\DE\data\Simona_data.csv'   # dữ liệu csv record của cửa hàng

def index(request):
  template = 'index.html'
  ###### import data cho product và customer ##########
  def import_data(model, csv_data, code_column, name_column, unit_price_column=None):
      df = pd.read_csv(csv_data)
      for idx,row in df.iterrows():             # hàm iterrows() trả về một tuples chứa giá trị là index và row 
          defaults = {'name': row[name_column]} # ghi cột name của cả 2 model từ các biến truyền vào

          if unit_price_column and unit_price_column in row:
              defaults['unit_price'] = row[unit_price_column]   # ghi đơn giá vào cho model sản phẩm
          
          obj, created = model.objects.get_or_create(   
              code=row[code_column],       # điều kiện để tìm kiếm đối tượng 
              defaults=defaults            # ghi các giá trị mặc định vào nếu không tìm thấy
          )
          if created:
              print('Created:', obj)
          else:
              print('Already exists:', obj)
      
      return model.objects.all()

  products = import_data(Product, data, 'Mã mặt hàng','Tên mặt hàng', unit_price_column= 'Đơn giá' )    # gọi hàm 
  customers = import_data(Customer, data, 'Mã khách hàng', 'Tên khách hàng')          

  context = {
      'customers': customers,
      'products': products
  }
  return render(request, template, context)


##############################
######## list custumer ######
def customer_list(request):
  template = 'record/customer_list.html'
  customer_objects = Customer.objects.all()

  customers = [{
    'pk':obj.pk,
    'name':obj.name,
} for obj in customer_objects]


  context = {
      'customers': customers
  }
  return render(request, template, context)


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
###############################################
########### order_from_customer ###################

def order_from_customer(request) :
  template = 'record/order_from_customer.html'

  def import_data(csv_data) :
      df = pd.read_csv(csv_data)
      for idx, row in df.iterrows():
          customer = Customer.objects.filter(code=row['Mã khách hàng']).last()
          defaults = {
              'order_code': row['Mã đơn hàng'],
              'time' : row['Thời gian tạo đơn'],
              'customer' : customer
                      }
          obj, created = Order.objects.get_or_create(
              order_code = row['Mã đơn hàng'],                          ## kiểm tra thông qua order_code
              defaults=defaults
          )
          if created:
              print('Created:', obj)
          else:
              print('Already exists:', obj)
              
      return Order.objects.all()

  orders = import_data(data)

  context = {
      'orders' : orders
  }
  return render(request, template, context)
  

############################################################
########## order_line ######################################

# data = 'C:\DE\data\Simona_data.csv'   # Path to your CSV data

def order_line(request):
  template = 'record/order_line.html'

  start_time = time.time()

  def import_ol_data(csv_data):
      df = pd.read_csv(csv_data)

      for idx, row in df.iterrows():
          product_code = row['Mã mặt hàng']
          order_code = row['Mã đơn hàng']

          product = Product.objects.filter(code=product_code).last()
          order = Order.objects.filter(order_code=order_code).last()

          if product is None:
              print(f'Product not found for code {product_code}')         # in ra các product bị sai / không hoạt động 
              continue

          defaults = {
              'order': order,
              'product': product,
              'quantity': row['SL']
          }
          # print(product.product_id)
          obj, created = OrderLine.objects.get_or_create(
              order=order,
              product=product,

              # product_id = product => sai vì product_id không tồn tại, product là một object phải gán với một object
              # có thể dùng thêm một cách là product__id = product.id
              
              defaults=defaults
          )
          if created:
              print('Created:', obj)
          else:
              print('Already exists:', obj)

      return OrderLine.objects.all()

  order_lines = import_ol_data(data)
  end_time = time.time()  # Record end time

  print("Data loading time:", end_time - start_time, "seconds")

  context = {
      'OrderLines': order_lines
  }

  return render(request, template, context)


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


def form(request):
    template = 'form_bootstraps.html'

    products = Product.objects.all()
    customers = Customer.objects.all()
    current_time = datetime.now()  # Lấy thời gian hiện tại



    if request.method == 'POST':
        print(request.POST)

        # Lấy dữ liệu từ request.POST   
        order_id = request.POST.get('order_id')  
        customer_code = request.POST.get('customer')
        order_time = current_time    

        # Tạo đối tượng Order
        order = Order.objects.create(
            order_code=order_id,
            time=order_time,
            customer_id=customer_code
        )

        i = 1
        while f'product{i}' in request.POST:
            product_code = request.POST.get(f'product{i}')
            quantity = request.POST.get(f'quantity{i}')
            product = Product.objects.get(code=product_code)
            orderline = OrderLine.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
            i += 1

        # Redirect hoặc xử lý tiếp theo
        return redirect('order_success')

    context = {
        'products': products,
        'customers': customers,
        'current_time': current_time, 
    }
    return render(request, template, context)



def order_success(request):
  template = 'record/order_success.html'
  context = {}
  return render(request, template, context)

def create_customer(request):
    template = 'record/customer_form.html'
    context = {}

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        customer_code = request.POST.get('customerCode')
        customer_name = request.POST.get('customerName')

        # Tạo đối tượng Customer và lưu vào cơ sở dữ liệu
        customer = Customer.objects.create(
           code=customer_code, 
           name=customer_name)
        
        return redirect('form')
    else:
        return render(request, template, context)

  


def create_product(request):
    template = 'record/product_form.html'
    
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        product_code = request.POST.get('code')
        product_name = request.POST.get('name')
        unit_price = request.POST.get('unit_price')

        # Tạo đối tượng Product và lưu vào cơ sở dữ liệu
        product = Product.objects.create(
           code=product_code, 
           name=product_name, 
           unit_price=unit_price)
        
        return redirect('form')
    else:
        context = {}  
        return render(request, template, context)