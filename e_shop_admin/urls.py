from django.urls import path
from . import views

urlpatterns = [
        path('login-admin/', views.auth_login, name='loginn'),
        path('admin-panel/', views.index, name="index-page"),
        path('add-category/', views.add_catrgory, name="add-category"),
        path('add-product/', views.add_product, name="add-product"),
        path('all-categories/', views.showcategory, name="show-cat"),
        path('del-cat/<str:slug>', views.del_cat, name="del-cat"),
        path('del-pro/<str:slug>', views.del_product, name="del-pro"),
        path('edit-cat/<str:slug>', views.edit_cat, name="edit-cat"),
        path('all-products/', views.show_product, name="show-pro"),
        path('edit-products/<str:slug>', views.edit_product, name="edit-pro"),
        path('del-img/<int:pk>/<str:slug>', views.delete_img_gallery, name="del-img"),
        path('auth-logout/', views.auth_logout, name="auth-logout"),
        path('crousal/', views.img_crousal, name="img-crousal"),
        path('crousal-del/<int:pk>', views.del_crousal, name="del-crousal"),
        path('crousal-list/', views.show_crousal, name="all-crousal"),
        path('message-list/', views.show_messages, name="message-list"),
        path('det-message/<int:pk>', views.del_mess, name="det-message"),
        
        



]