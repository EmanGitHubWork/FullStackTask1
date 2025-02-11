from django.shortcuts import render, redirect
from ecommerceapp.models import Contact, Product, Orders, OrderUpdate
from django.contrib import messages
from math import ceil

def index(request):
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nslides), nslides])

    params = {'allprods': allprods}
    return render(request, "index.html", params)

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        pnumber = request.POST.get("pnumber")

        if pnumber:  # Ensure phone number is provided
            myquery = Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
            myquery.save()
            messages.success(request, "Your message was sent successfully!")
            return redirect('/contact')  # Redirect to avoid form resubmission
        else:
            messages.error(request, "Phone number is required.")

    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # Validate amount is provided and is a number
        if not amount.isdigit():
            messages.error(request, "Invalid amount. Please enter a valid number.")
            return render(request, "checkout.html")

        # Convert amount to integer
        amount = int(amount)

        # Print received data for debugging
        print(f"Received order data: {name}, {email}, {amount}, {address1}, {address2}, {city}, {state}, {zip_code}, {phone}")

        # Save the order to the database
        order = Orders(items_json=items_json, name=name, amount=amount, email=email, address1=address1, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        print(f"Order saved with ID: {order.order_id}")

        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        print(f"OrderUpdate saved with ID: {update.update_id}")

        thank = True
        return render(request, "checkout.html", {'thank': thank, 'id': order.order_id})
    else:
        return render(request, "checkout.html")


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')
    
    currentuser=request.user.username
    items=Orders.objects.filter(email=currentuser)
    myid=""
    for i in items:
        myid=i.order_id
        print(myid)
    status=OrderUpdate.objects.filter(order_id=int(myid))
    for j in status:
        print(j.update_desc)

    context={"items":items,"status":status}
    print(currentuser)

    return render(request,"profile.html",context)
# # # PAYMENT INTEGRATION

#         id = Order.order_id
#         oid=str(id)+"ShopyCart"
#         param_dict = {

#             'MID':keys.MID,
#             'ORDER_ID': oid,
#             'TXN_AMOUNT': str(amount),
#             'CUST_ID': email,
#             'INDUSTRY_TYPE_ID': 'Retail',
#             'WEBSITE': 'WEBSTAGING',
#             'CHANNEL_ID': 'WEB',
#             'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

#         }
#         param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
#         return render(request, 'paytm.html', {'param_dict': param_dict})

#     return render(request, 'checkout.html')


# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]

#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#             a=response_dict['ORDERID']
#             b=response_dict['TXNAMOUNT']
#             rid=a.replace("ShopyCart","")
           
#             print(rid)
#             filter2= Orders.objects.filter(order_id=rid)
#             print(filter2)
#             print(a,b)
#             for post1 in filter2:

#                 post1.oid=a
#                 post1.amountpaid=b
#                 post1.paymentstatus="PAID"
#                 post1.save()
#             print("run agede function")
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'paymentstatus.html', {'response': response_dict})


# def profile(request):
#     if not request.user.is_authenticated:
#         messages.warning(request,"Login & Try Again")
#         return redirect('/auth/login')
#     currentuser=request.user.username
#     items=Orders.objects.filter(email=currentuser)
#     rid=""
#     for i in items:
#         print(i.oid)
#         # print(i.order_id)
#         myid=i.oid
#         rid=myid.replace("ShopyCart","")
#         print(rid)
#     status=OrderUpdate.objects.filter(order_id=int(rid))
#     for j in status:
#         print(j.update_desc)

   
#     context ={"items":items,"status":status}
#     # print(currentuser)
#     return render(request,"profile.html",context)