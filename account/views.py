from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.models import User
###################################################
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact
###################################################
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm , UserRegistrationForm , UserEditForm , ProfileEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from actions.models import Action
# Create your views here.

# Building an AJAX view to follow users
@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})






# User List
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,'user/list.html',{'section': 'people' , 'users':users})


@login_required
def user_detail(request,username):
    user = get_object_or_404(User , username=username , is_active=True)
    return render(request , 'user/detail.html' , {'section':'people' , 'user':user})


#Sign UP Page
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile=Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request , 'editregister/register_done.html' , {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request , 'editregister/register.html' , {'user_form':user_form})

#Profile Page
@login_required
def edit(request):
    profile = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST,instance=request.user)
        profile_form = ProfileEditForm(request.POST , request.FILES , instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
        return redirect('/account/')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request , 'user_profile/edit.html' , {'user_form':user_form , 'profile_form':profile_form})






@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    return render(request,'dashboard.html',{'section':'dashboard','actions': actions})





















#### Didint Use it now we make another one new ########
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
