from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document,DocumentFile
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

@login_required(login_url='/')
def uploadDocument(request):
    default_document = Document.objects.filter(is_default = True)
    if request.method == 'POST':
        for document in default_document:
            uploaded_file = request.FILES[str(document.id)]
            documentRef = Document.objects.get(pk=document.id)
            print(documentRef)

            document_file = DocumentFile.objects.create(
                document=documentRef,
                user=request.user,
                file=uploaded_file
            )
            document_file.save()
        return redirect('/login')
            

    return render(request, 'documents/documentform.html',{"default_document":default_document})





@login_required(login_url='/')
def ListDocument(request):
    all_document = DocumentFile.objects.filter(user=request.user)
    
    return render(request, 'documents/documentlist.html',{"all_document":all_document})


@login_required(login_url='/')
def allUsers(request):
    if not request.user.is_superuser:
        return redirect('/documents-list')
   
    all_users = User.objects.all()
    temp = []
    for i in all_users:
        if not i.is_superuser:
            temp.append(i)

    return render(request, 'documents/alluser.html', {'all_users': temp})



def check_is_present(document,all_document):
    for i in all_document:
        print(i)
        if i.document_name == document.document_name:
            return True
    return False
    

@login_required(login_url='/')
def userdetails(request, id):
    user = User.objects.get(id=id)
    all_document = DocumentFile.objects.filter(user=user)
    all_document = list(all_document)
    for i in range(0,len(all_document)):
        all_document[i].document_name = all_document[i].document.document_name
        all_document[i].is_submit = True
        all_document[i].id = all_document[i].document.id
    all_document_copy = [*all_document]

    all_added_docuemnt  = Document.objects.all()
    for i in all_added_docuemnt:
        if not check_is_present(i,all_document_copy):
            all_document.append({
                "is_submit": False,
                "document_name": i.document_name,
                "user": user,
                "id": i.id
            })
    
   

    # Pass the user object to the template context
    return render(request, 'documents/userdocument.html',{'all_document':all_document})

@login_required(login_url='/')
def sendmail(request, document_id,user_id):
    if not request.user.is_superuser:
        return HttpResponse('Only admin can send email')
    
    # Retrieve the document and user objects using the IDs
    document = get_object_or_404(Document, id=document_id)
    user = get_object_or_404(User, id=user_id)

    original_url = request.build_absolute_uri('/')[:-1]
    url = f"{original_url}/upoload-document/{document_id}"
    
    subject = f"Please Submit your {document.document_name}."
    message = f"click on this link {url} to submit your document"
    from_email = settings.EMAIL_HOST_USER  # Sender's email address
    recipient_list = [user.email]  # List of recipient email addresses

    send_mail(subject, message, from_email, recipient_list)

    return render(request,'documents/message.html',{"message":'Email sent successfully!'})


    # return render(request, 'documents/alluser.html')




@login_required(login_url='/')
def getOneDoucment(request, document_id):
    # Retrieve the document and user objects using the IDs
    document_from_db = get_object_or_404(Document, id=document_id)
    default_document = [document_from_db]

    if request.method == 'POST':
        for document in default_document:
            uploaded_file = request.FILES[str(document.id)]
            documentRef = Document.objects.get(pk=document.id)

            document_file = DocumentFile.objects.create(
                document=documentRef,
                user=request.user,
                file=uploaded_file
            )
            document_file.save()

    
        return render(request,'documents/message.html',{"message":'Document Submit successfully!'})
    
    return render(request, 'documents/documentform.html',{"default_document":default_document})