import django
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Follow
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

from django.contrib import messages
from Listings_app.models import Listing
import json



# Create your views here.

@never_cache

@login_required(login_url='auth:auth_view')
def profile(request):
    """
    User Profile Page
    GET /profile/
    
    Displays:
    - User profile information
    - Avatar and basic details
    - Reputation and ratings
    - Activity history
    - Link to profile settings
    """
    context = {
        'page_title': 'My Profile - PU-Marketplace',
        'page_description': 'View and manage your profile information.',
        # Add any additional context data needed for the profile page here
    }
    return render(request, 'profile/profile.html', context)

@login_required(login_url='auth:auth_view')
def settings(request):
    """
    Profile Settings Page
    GET /profile/settings/
    
    Displays:
    - Account settings
    - Privacy settings
    - Notification preferences
    - Security settings
    """
    context = {
        'page_title': 'Settings - PU-Marketplace',
        'page_description': 'Manage your account settings.',
    }
    return render(request, 'profile/settings.html', context)





@login_required(login_url='auth:auth_view')
@never_cache
def get_my_profile(request):
    """Sends DB data to the frontend on load."""
    from Listings_app.models import Listing

    profile, _ = Profile.objects.get_or_create(user=request.user)
    user = request.user

    listing_qs = Listing.objects.filter(user=user)
    active_listings = list(
        listing_qs.filter(status__in=['active', 'boosted'])
        .order_by('-created_at')[:12]
        .values('id', 'title', 'price', 'image_url', 'listing_type', 'status', 'contact_for_price')
    )
    # Serialise Decimal -> str for JSON
    for l in active_listings:
        l['price'] = str(l['price'])

    return JsonResponse({
        'username': user.username,
        'name': user.get_full_name() or user.username,
        'email': user.email,
        'bio': profile.bio or "",
        'faculty': profile.faculty or "",
        'location': profile.location or "",
        'phone': profile.phone or "",
        'avatarSrc': profile.avatar_url or "",
        'joined': user.date_joined.strftime('%B %Y'),
        'listing_count': listing_qs.count(),
        'sold_count': listing_qs.filter(status='sold').count(),
        'followers_count': user.followers_set.count(),
        'following_count': user.following_set.count(),
        'active_listings': active_listings,
    })
  

# Profile_app/views.py
from .forms import PhoneForm

@login_required(login_url='auth:auth_view')
def complete_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # If already set, redirect to main site or profile
    if profile.phone:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, "Please enter a valid phone number.")
    else:
        form = PhoneForm(instance=profile)
        
    return render(request, 'profile/complete.html', {'form': form})









@login_required(login_url='auth:auth_view')
@require_POST
def update_profile_api(request):
    """Receives data and R2 links to save in DB."""
    try:
        data = json.loads(request.body)
        user = request.user
        p, _ = Profile.objects.get_or_create(user=user)
        
        # 1. Update User model (Username & Full Name)
        new_un = data.get('username', '').strip().replace('@','')
        if new_un and new_un != user.username:
            from django.contrib.auth.models import User
            if User.objects.filter(username=new_un).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already taken'}, status=400)
            user.username = new_un
            
        full_name = data.get('name', '').strip()
        if full_name:
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
        
        user.save()

        # 2. Update Profile model
        p.bio = data.get('bio', '')
        p.faculty = data.get('faculty', '')
        p.location = data.get('location', '')
        p.phone = data.get('phone', '')
        if data.get('avatarSrc'):
            p.avatar_url = data.get('avatarSrc')
        p.save()
        
        return JsonResponse({'status': 'success', 'username': user.username})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Ensure your Listing model is imported


def public_profile_page(request, username):
    """Renders the public profile page for any user."""
    target = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'profile/public_profile.html', {'target_username': username})


@never_cache
def public_profile_api(request, username):
    """JSON data for a public profile."""
    target = get_object_or_404(User, username=username, is_active=True)
    try:
        p = target.profile
    except Exception:
        p = None

    listing_qs = Listing.objects.filter(user=target, status__in=['active', 'boosted']).order_by('-created_at')
    active_listings = list(
        listing_qs[:12].values('id', 'title', 'price', 'image_url', 'listing_type', 'status', 'contact_for_price')
    )
    for l in active_listings:
        l['price'] = str(l['price'])

    is_following = False
    follows_you  = False
    is_own       = False
    if request.user.is_authenticated:
        is_own       = request.user == target
        is_following = Follow.objects.filter(follower=request.user, following=target).exists()
        follows_you  = Follow.objects.filter(follower=target, following=request.user).exists()

    return JsonResponse({
        'username':        target.username,
        'name':            target.get_full_name() or target.username,
        'bio':             (p.bio if p else '') or '',
        'faculty':         (p.faculty if p else '') or '',
        'location':        (p.location if p else '') or '',
        'avatarSrc':       (p.avatar_url if p else '') or '',
        'joined':          target.date_joined.strftime('%B %Y'),
        'posts_count':     listing_qs.count(),
        'followers_count': target.followers_set.count(),
        'following_count': target.following_set.count(),
        'is_following':    is_following,
        'follows_you':     follows_you,
        'is_own':          is_own,
        'active_listings': active_listings,
    })


@login_required(login_url='auth:auth_view')
@require_POST
def toggle_follow(request, username):
    """Toggle follow/unfollow. Returns new state."""
    target = get_object_or_404(User, username=username, is_active=True)
    if target == request.user:
        return JsonResponse({'status': 'error', 'message': 'Cannot follow yourself'}, status=400)

    follow_obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow_obj.delete()
        is_following = False
    else:
        is_following = True

    return JsonResponse({
        'following':       is_following,
        'followers_count': target.followers_set.count(),
    })


def logout_view(request):
    logout(request)
    return redirect('auth:auth_view') # Standard redirect works for logout

@login_required
@require_POST
def deactivate_account(request):
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def delete_account(request):
    user = request.user
    user.delete()
    return JsonResponse({'status': 'success'})

