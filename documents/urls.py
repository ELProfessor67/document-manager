
from django.urls import path,include
from .views import uploadDocument, ListDocument, allUsers, userdetails , sendmail, getOneDoucment

urlpatterns = [
    path('documents-uploads/',uploadDocument,name="upload document"),
    path('documents-lists/',ListDocument,name="upload lists"),
    path('all-users/',allUsers,name="upload lists"),
    path('all-users/<int:id>',userdetails,name="upload lists"),
    path('send-mail/<int:document_id>/<int:user_id>/',sendmail,name="upload lists"),
    path('upoload-document/<int:document_id>',getOneDoucment,name="upload lists"),
]