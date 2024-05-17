from django.shortcuts import render
from .models import Customer,Product,Order,OrderLine
import pandas as pd
  

data = 'C:\DE\data\Simona_data.csv'

def index(request):
    template = 'index.html'
    ###### import data cho product và customer ##########
    def import_data(model, csv_data, code_column, name_column, unit_price_column=None):
        df = pd.read_csv(csv_data)
        for idx, row in df.iterrows():
            defaults = {'name': row[name_column]}
            if unit_price_column and unit_price_column in row:
                defaults['unit_price'] = row[unit_price_column]
            
            obj, created = model.objects.get_or_create(
                code=row[code_column],
                defaults=defaults
            )
            if created:
                print('Created:', obj)
            else:
                print('Already exists:', obj)
        
        return model.objects.all()

    products = import_data(Product, data, 'Mã mặt hàng','Tên mặt hàng', unit_price_column='Đơn giá' )
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
# viết lại templates của customer_list,
# viết hàm trong view

def customer_detail(request, pk):
    template = 'record/customer_detail.html'

    # Lấy thông tin khách hàng dựa trên khóa chính pk
    customer = Customer.objects.get(pk=pk)

    # Lấy danh sách các đơn hàng liên kết với khách hàng này
    orders = Order.objects.filter(customer=customer)

    # Truyền dữ liệu vào context
    context = {
        'customer': customer,
        'orders': orders
    }
    return render(request, template, context)

#####################################################
######### order_detail ##############################

def order_detail(request, order_code):
    template = 'record/order_detail.html'

    # Lấy thông tin đơn hàng dựa trên order_code
    order = Order.objects.get(order_code=order_code)

    # Lấy danh sách các dòng đơn hàng liên kết với đơn hàng này
    order_lines = OrderLine.objects.filter(order=order)

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
                order_code = row['Mã đơn hàng'],  ## kiểm tra thông qua order_code
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

def order_line(request) :
    template = 'record/order_line.html'

    def import_ol_data(csv_data) :

        df = pd.read_csv(csv_data)

        for idx, row in df.iterrows():                                                 ## note lại chưa hiểu vì sao phải dùng idx để chạy được 
            product = Product.objects.filter(code=row['Mã mặt hàng']).last()
            order = Order.objects.filter(order_code=row['Mã đơn hàng']).last()

            defaults = {
                'order' : order,
                'product_id' : product,
                'sl' : row['SL']
            }
            obj, created = OrderLine.objects.get_or_create(
                order=order,
                product_id=product,
                defaults=defaults
            )
            if created:
                print('Created:', obj)
            else:
                print('Already exists:', obj)
                
        return OrderLine.objects.all()
    
    order_lines = import_ol_data(data)

    context = {
        'OrderLines' : order_lines
    }

    return render(request, template, context)


























'''
import được dữ liệu nhưng chưa có detail về order 
bấm vào orderid thì xem được các thông tin như tên khách, những sản phẩm, thành tiền = (thành tiền từ order line + lại)
bấm vào các khách hàng thì xem được các orderid 
'''