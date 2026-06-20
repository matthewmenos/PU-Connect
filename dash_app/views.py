from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

#===================================================2024-06-01: Added dashboard view and template rendering


def dashboard(request):
    """
    User Dashboard
    GET /dashboard/
    
    Displays:
    - User profile summary
    - Recent activity feed
    - Quick links to key features (post item, view messages, manage listings)
    - Personalized recommendations
    """
    context = {
        'page_title': 'Your Dashboard - PU-Marketplace',
        'page_description': 'Manage your account, view activity, and access key features.',
        # Add any additional context data needed for the dashboard here
    }
    return render(request, 'dash/dashboard.html', context)
    