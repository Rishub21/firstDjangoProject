from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import celeryResponse
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from rango.google_search import customsearch
from datetime import datetime
from rango.tasks import hello_message
import subprocess
import time

def index(request):
    my_messages =  []
    category_list = Category.objects.order_by('-likes')[:20]
    context_dict = {'boldmessage': "I am bold font from the context",
		    "categories" : category_list, "my_messages" : "" }
    other_dict = {}

    #numvisits = request.COOKIES.get("visits", "1" )) # if no value we default to one as that would be the first time they visit # this is less secure as this is a client side cookie
    numvisits = request.session.get("numvisits") # more secure way, request.session.get allows you to access cookies on the server side
    if not numvisits:
        numvisits = 1 # setting a default

    reset_last_visit_time  = False
    last_visit = request.session.get("last_visit")

    if last_visit: # if there was a last visit, meaning that this is not the first visit
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S") # formatting the last visit as according to date time format

        if (datetime.now()  - last_visit_time).seconds >0 : # if a full hour  has elapsed since the last visit and the current visit  then we will  consider the current visit to be an entirely new visit and thus not an extension of the old one
            numvisits = numvisits + 1
            reset_last_visit_time = True # this signals that we need to reset our numvisits cookie
            #context_dict["numvisits"] = numvisits

    else:
        # there was not last_visit in cookies meaning that this is the first visit
        reset_last_visit_time = True # we need to set the numvisits in cookies to be 1 now
        #context_dict["numvisits"] = numvisits # this will just help us render the number of total visits in the starting page, if we want to display it

        #response = render(request, "rango/index.html", context_dict)

    if reset_last_visit_time: # resetting the cookies or setting them for the first time
        request.session["last_visit"] = str(datetime.now())
        request.session["numvisits"] = numvisits

    if request.session.get("numvisits"):
        count = request.session.get("numvisits")
    else:
        count = 0

    context_dict["numvisits"] = numvisits

    tester = "tester"

    boolean  = False

    if request.method == "GET":
        totallikes = request.GET.get("wholelikes", 0);
        totallikes +=1;
        print totallikes


    if request.method == "POST":
        special_message = request.POST.get("special_message") # value of userinput
        time.sleep(30)
        hello_message.delay(special_message)
        my_messages = celeryResponse.objects.order_by("message") # order the messages alphabetically
        context_dict["my_messages"] = my_messages
        subprocess.call("python manage.py celeryd", shell = True)


        #context_dict["message"] = message.delay(message = "Rendering the index page")

    print len(my_messages)

    response = render(request, "rango/index.html", context_dict)
    return response # context dict gets rendered with templatex
    return render(request, "rango/nextindex.html", {"visits": count, "tester": test,})
    return HttpResponse(totallikes)

#def getcategory_list(max_result= 0, starts_with = " "  ):
#    if max_result = 0 :
#        cat_list = Category.objects.filter(starts_with = starts_with) # in the filter always define the variable


        #if cat_list.count(:max_result)

def likecategory(request):
    cat_id = None

    if request.method == "GET":
        cat_id = request.GET["category_id"] # this category_id is coming directly from the AJAX request parameters

    likes = 0  # default value
    if cat_id:
        cat = Category.objects.get(id= int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()

    print "testing this jquery"
    return HttpResponse(likes) # the http response will communicate with the jquery

def about(request):
	return render(request, "rango/nextindex.html")

def risebase(request):
    return render(request, "rango/risebase.html")

def search(request):

    results_list = []
    checkedlist =  []
    nextlist = []

    if request.method == "POST":
        query = request.POST.get("query")
        nextval  = request.POST.get("nextval")

        if nextval or len(nextlist) > 0:
            nextval = nextval.strip()
            print nextval
            nextlist.append(nextval)

            print (len(nextlist))

        if query:
            query = query.strip()
            results_list = customsearch(query)

        submitlist = request.POST.getlist("checks")
        if submitlist:
            return render(request, "rango/search.html", {"results_list" : results_list, "next_list" : nextlist, "submitlist" : submitlist})


        #display_type = request.POST.get["display_type", None] # every thing that has been checked

        #for i in results_list:
        #    if display_type in results_list[i]["title"]:
        #        print i

    return render(request, "rango/search.html", {"results_list" : results_list, "next_list" : nextlist})

def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug = category_name_slug)
        context_dict["category_name"] = category.name

        pages= Page.objects.filter(category = category)
        context_dict["pages"] = pages
        context_dict["category"] = category # category object
        context_dict["category_name_slug"] = category_name_slug

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)

def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request,category_name_slug): # must pass on whatever values to category function # must include the actual category name to add page
    try:
        cat = Category.objects.get(slug=category_name_slug) # this is the category that we will edit in terms of pages
    except Category.DoesNotExist:
                cat = None

    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
            else:
                print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}
    context_dict["category_name_slug"] = category_name_slug
    return render(request, 'rango/add_page.html', context_dict)


def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
        if request.method == "POST":
            #username and password will be collected from the form
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(username = username, password = password) # built in authenicate function will cross reference to see if such a user exists in the database

            if user: # user object is validated via the authenticate method
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect("/rango/") # redirect to home page
                else:
                    # inactive account
                    return HttpResponse("Your Rango Account is disabled")
            else:
                print "Invalid login {0},{1}".format(username, password)
                return HttpResponse("Invalid login details supplied")

        else:
            return render(request,"rango/login.html", {})

#@login_required # this decorator ensures that only users who are logged in can access this view
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/rango/")
