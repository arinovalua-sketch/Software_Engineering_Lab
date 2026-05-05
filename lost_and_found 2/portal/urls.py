from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    home,
    items_page,
    lost_items,
    register,
    dashboard,
    add_item,
    claim_item,
    get_items_api,
    create_item_api,
    update_item_api,
    delete_item_api,
    profile,
)

urlpatterns = [
    path('', home),
    path('found/', items_page),
    path('lost/', lost_items),
    path('register/', register),
    path('dashboard/', dashboard),
    path('add/', add_item),
    path('claim/<int:item_id>/', claim_item),

    # API
    path('api/items/', get_items_api),
    path('api/items/create/', create_item_api),
    path('api/items/update/<int:item_id>/', update_item_api),
    path('api/items/delete/<int:item_id>/', delete_item_api),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', profile, name='profile'),
]
