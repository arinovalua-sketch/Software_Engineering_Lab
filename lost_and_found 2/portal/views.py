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


@login_required
def add_item(request):
    item_type = request.GET.get('type', 'found')

    if request.method == 'POST':
        item = Item.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            item_type=request.POST['item_type'],
            category=request.POST['category'],
            created_by=request.user
        )

        for img in request.FILES.getlist('images'):
            ItemImage.objects.create(item=item, image=img)

        return redirect('/')

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


@csrf_exempt
def create_item_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        item = Item.objects.create(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            item_type=data['item_type'],
            category=data['category'],
            created_by=request.user if request.user.is_authenticated else None
        )

        return JsonResponse({
            'status': 'created',
            'item_id': item.id
        })

    return JsonResponse(
        {'error': 'Only POST method allowed'},
        status=405
    )


@csrf_exempt
def update_item_api(request, item_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'PUT or PATCH only'}, status=405)

    data = json.loads(request.body)

    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

    item.title = data.get('title', item.title)
    item.description = data.get('description', item.description)
    item.location = data.get('location', item.location)
    item.item_type = data.get('item_type', item.item_type)
    item.category = data.get('category', item.category)

    item.save()

    return JsonResponse({'status': 'updated'})


@csrf_exempt
def delete_item_api(request, item_id):
    if request.method == 'DELETE':
        Item.objects.filter(id=item_id).delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'DELETE only'}, status=405)
@login_required
def profile(request):
    user_items = Item.objects.filter(created_by=request.user)
    user_claims = Claim.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'user_items': user_items,
        'user_claims': user_claims
    })
