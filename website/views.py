from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import SignUpForm, AddRecordForm
from .models import Record 


# Create homepage view (implement logic for user already logger in or not)
def home(request):
    
    records = Record.objects.all()   # grab all records in DB table and save into records var

    # check to see if logging in 
    if request.method == "POST": 
        # get username and password from form 
        username = request.POST['username']
        password = request.POST['password']

        # login authentication
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            messages.success(request, "You have been loggen in!") 
            return redirect('home')
        else:
            messages.error(request, "Wrong credentials. Please try again.")
            return redirect('home')
    else:
        return render(request, "home.html", {'records': records})  # Display all Records when user is logged in 


# Create user logout view
def logout_user(request): 
    logout(request)
    messages.success(request, "You have been logged out.") 
    return redirect("home")


# Create user register view
def register_user(request):
    if request.method == "POST": 
        form = SignUpForm(request.POST)
        # registration data validation
        if form.is_valid(): 
            form.save()  # save the form 
            # after registration, authenticate user and log him in 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! You are now logged in.")
            return redirect("home")
        else: 
            return render(request, "register.html", {'form':form})
    else: 
        form = SignUpForm()
        return render(request, "register.html", {'form':form})
    

# Create display customer record view
def customer_record(request, pk): 
    # only see records if logger in 
    if request.user.is_authenticated: 
        # look-up record 
        customer_record = Record.objects.get(id=pk)   # get Record based on id 
        return render(request, "record.html", {'customer_record':customer_record})
    else: 
        messages.warning(request, "You must be logged in to Display Records.")
        return redirect("home")


# Create record deletion view
def delete_record(request, pk): 
    if request.user.is_authenticated: 
        delete_it = Record.objects.get(id=pk)  # get record which needs to be deleted
        delete_it.delete()  # delete record
        messages.success(request, f"Record with ID={pk} [{delete_it.first_name} {delete_it.last_name}] successfully deleted!")
        return redirect("home")
    else: 
        messages.warning(request, "You must be logged in to Delete Records.")
        return redirect("home")
    

# Create record addition view
def add_record(request): 
    form = AddRecordForm(request.POST or None)  

    if request.user.is_authenticated: 
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, f"New Record was successfully added!")
                return redirect("home")
        else: 
            return render(request, 'add_record.html', {'form':form})
    else: 
        messages.warning(request, "You must be logged in to Add Records.")
        return redirect("home")
    

# Create update record view 
def update_record(request, pk): 
    
    if request.user.is_authenticated: 
        update_it = Record.objects.get(id=pk)  # get record which needs to be updated
        form = AddRecordForm(request.POST or None, instance=update_it)

        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, f"Record has been updated successfully!")
                return redirect("home")
            else: 
                return render(request, 'update_record.html', {'form':form})   
        else: 
            return render(request, 'update_record.html', {'form':form})   
    else: 
        messages.warning(request, "You must be logged in to Update Records.")
        return redirect("home")