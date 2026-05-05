Python 3.14.2 (v3.14.2:df793163d58, Dec  5 2025, 12:18:06) [Clang 16.0.0 (clang-1600.0.26.6)] on darwin
Enter "help" below or click "Help" above for more information.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import json

from .models import Item, ItemImage, Claim


# ================= AUTH =================
def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/login/')
    return render(request, 'register.html', {'form': form})


# ================= PAGES =================
def items_page(request):
    category = request.GET.get('category')
    items = Item.objects.filter(item_type='found')
    if category:
        items = items.filter(category=category)

    return render(request, 'items_list.html', {
        'items': items,
        'page_title': 'Found Items'
    })

def home(request):
    return render(request, 'home.html')


def lost_items(request):
    category = request.GET.get('category')
    items = Item.objects.filter(item_type='lost')
    if category:
        items = items.filter(category=category)

    return render(request, 'items_list.html', {
        'items': items,
        'page_title': 'Lost Items'
    })


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'items_count': Item.objects.count(),
        'claims_count': Claim.objects.count(),
    })

# test1
@login_required
def add_item(request):
    print("STEP 1 → Enter add_item view")

    item_type = request.GET.get('type', 'found')
    print("STEP 2 → item_type:", item_type)

    if request.method == 'POST':
        print("STEP 3 → POST request received")

        print("STEP 4 → POST DATA:", request.POST)
        print("STEP 5 → FILES:", request.FILES)

        title = request.POST.get('title')
        print("STEP 6 → title:", title)

        item = Item.objects.create(
            title=title,
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            item_type=request.POST.get('item_type'),
            category=request.POST.get('category'),
            created_by=request.user
        )

        print("STEP 7 → item created with ID:", item.id)

        for img in request.FILES.getlist('images'):
            print("STEP 8 → saving image:", img)
            ItemImage.objects.create(item=item, image=img)

        print("STEP 9 → redirecting to home")

        return redirect('/')

    print("STEP 10 → GET request, rendering page")
    return render(request, 'add_item.html', {
        'item_type': item_type
    })

@login_required
def claim_item(request, item_id):
    item = Item.objects.get(id=item_id)

    if request.method == 'POST':
        Claim.objects.create(
            user=request.user,
            item=item,
            message=request.POST['message']
        )
        return redirect('/')

    return render(request, 'claim.html', {'item': item})


# ================= API =================
def get_items_api(request):
    items = list(Item.objects.values())
    return JsonResponse(items, safe=False)

# test2
@csrf_exempt
def create_item_api(request):
    print("API STEP 1 → create_item_api called")

    if request.method == 'POST':
        print("API STEP 2 → POST request")

        data = json.loads(request.body)
        print("API STEP 3 → data received:", data)

        item = Item.objects.create(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            item_type=data['item_type'],
            category=data['category'],
            created_by=request.user if request.user.is_authenticated else None
        )

        print("API STEP 4 → item created ID:", item.id)

        return JsonResponse({
            'status': 'created',
            'item_id': item.id
        })

    print("API STEP ERROR → wrong method")
    return JsonResponse({'error': 'Only POST allowed'}, status=405)
# test3
@csrf_exempt
def update_item_api(request, item_id):
    print("UPDATE STEP 1 → called with ID:", item_id)

    if request.method not in ['PUT', 'PATCH']:
        print("UPDATE STEP ERROR → wrong method")
        return JsonResponse({'error': 'PUT or PATCH only'}, status=405)

    data = json.loads(request.body)
...     print("UPDATE STEP 2 → data:", data)
... 
...     try:
...         item = Item.objects.get(id=item_id)
...         print("UPDATE STEP 3 → item found:", item)
...     except Item.DoesNotExist:
...         print("UPDATE STEP ERROR → item not found")
...         return JsonResponse({'error': 'Item not found'}, status=404)
... 
...     item.title = data.get('title', item.title)
...     item.location = data.get('location', item.location)
... 
...     item.save()
...     print("UPDATE STEP 4 → item updated")
... 
...     return JsonResponse({'status': 'updated'})
... # test4
... @csrf_exempt
... def delete_item_api(request, item_id):
...     print("DELETE STEP 1 → called with ID:", item_id)
... 
...     if request.method == 'DELETE':
...         deleted = Item.objects.filter(id=item_id).delete()
...         print("DELETE STEP 2 → deleted:", deleted)
... 
...         return JsonResponse({'status': 'deleted'})
... 
...     print("DELETE STEP ERROR → wrong method")
...     return JsonResponse({'error': 'DELETE only'}, status=405)
... 
... @login_required
... def profile(request):
...     user_items = Item.objects.filter(created_by=request.user)
...     user_claims = Claim.objects.filter(user=request.user)
... 
...     return render(request, 'profile.html', {
...         'user_items': user_items,
...         'user_claims': user_claims
...     })
