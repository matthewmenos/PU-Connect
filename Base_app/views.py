"""
Base App Views - Homepage, About, Help, Terms, Privacy, Safety
"""

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import boto3
import uuid
import os


def home(request):
    """
    Homepage / Landing Page
    GET /
    
    Displays:
    - Hero section with call-to-action
    - Features overview
    - How it works
    - Categories
    - Statistics
    """
    context = {
        'page_title': 'PU-Marketplace - Campus Commerce, Reimagined',
        'page_description': 'Buy, sell, and trade on campus. Exclusively for university students.',
    }
    return render(request, 'base/index.html', context)


def about(request):
    """
    About Page
    GET /about/
    
    Displays:
    - Company mission and vision
    - Team information
    - History and milestones
    - Values
    """
    context = {
        'page_title': 'About PU-Marketplace',
        'page_description': 'Learn about our mission to revolutionize campus commerce.',
    }
    return render(request, 'base/about.html', context)


def help_page(request):
    """
    Help & Support Center
    GET /help/
    
    Displays:
    - FAQs
    - Getting started guide
    - Troubleshooting
    - Contact support
    """
    context = {
        'page_title': 'Help & Support - PU-Marketplace',
        'page_description': 'Find answers to common questions and get support.',
        'faqs': [
            {
                'question': 'How do I verify my student status?',
                'answer': 'Sign up with your university email address. Our system automatically verifies your status when you use your @student.pu.edu.gh email.'
            },
            {
                'question': 'Is it safe to buy and sell here?',
                'answer': 'Yes! All users are verified students. We also provide in-app messaging, secure payment options, and a rating system to ensure safe transactions.'
            },
            {
                'question': 'How do I create a listing?',
                'answer': 'Go to your Dashboard, click "New Listing", upload photos, add a description and price. Your listing goes live immediately!'
            },
            {
                'question': 'Can I meet buyers outside campus?',
                'answer': 'We recommend meeting at designated campus locations for safety. You can arrange meetups through our in-app messaging.'
            },
            {
                'question': 'What payment methods do you support?',
                'answer': 'We support Mobile Money (Vodafone Cash, MTN Mobile Money), bank transfers, and our secure escrow system.'
            },
            {
                'question': 'How do ratings work?',
                'answer': 'After each transaction, both parties can rate each other from 1-5 stars and leave comments. This builds trust in our community.'
            },
        ]
    }
    return render(request, 'base/help.html', context)


def terms(request):
    """
    Terms & Conditions Page
    GET /terms/
    
    Displays:
    - User agreement
    - Rights and responsibilities
    - Prohibited items
    - Dispute resolution
    """
    context = {
        'page_title': 'Terms & Conditions - PU-Marketplace',
        'page_description': 'Read our terms of service and user agreement.',
    }
    return render(request, 'base/terms.html', context)


def privacy(request):
    """
    Privacy Policy Page
    GET /privacy/
    
    Displays:
    - Data collection practices
    - How data is used
    - User rights
    - Cookies and tracking
    """
    context = {
        'page_title': 'Privacy Policy - PU-Marketplace',
        'page_description': 'Learn how we protect your privacy.',
    }
    return render(request, 'base/privacy.html', context)


def safety(request):
    """
    Safety Guidelines Page
    GET /safety/
    
    Displays:
    - Safe trading tips
    - Scam warnings
    - What to avoid
    - Emergency contacts
    """
    context = {
        'page_title': 'Safety Guidelines - PU-Marketplace',
        'page_description': 'Stay safe while buying and selling on campus.',
        'safety_tips': [
            {
                'title': 'Meet in Public Places',
                'description': 'Always meet at well-known campus locations like the library, student center, or cafeteria. Never meet strangers outside campus.'
            },
            {
                'title': 'Verify Before You Trade',
                'description': 'Check the seller\'s profile, reviews, and ratings. Ask questions and request additional photos if needed.'
            },
            {
                'title': 'Use In-App Messaging',
                'description': 'Communicate through our platform, not personal phone numbers. This keeps your privacy protected.'
            },
            {
                'title': 'Inspect Items Carefully',
                'description': 'Before handing over money, thoroughly inspect the item. Check for damage, missing parts, or wear.'
            },
            {
                'title': 'Trust Your Gut',
                'description': 'If something feels wrong, walk away. There are plenty of other sellers and buyers on PU-Marketplace.'
            },
            {
                'title': 'Report Suspicious Activity',
                'description': 'See scams or harassment? Report them immediately. Our team reviews all reports and takes action.'
            },
        ]
    }
    return render(request, 'base/safety.html', context)


def browse_categories(request, category=None):
    """
    Browse by Category
    GET /categories/
    GET /categories/<category>/
    
    Displays:
    - All available categories
    - Filtered listings by category
    """
    categories = [
        {'slug': 'textbooks', 'name': 'Textbooks', 'icon': 'book-open', 'count': 245},
        {'slug': 'electronics', 'name': 'Electronics', 'icon': 'laptop', 'count': 189},
        {'slug': 'services', 'name': 'Services', 'icon': 'palette', 'count': 156},
        {'slug': 'fashion', 'name': 'Fashion', 'icon': 'shirt', 'count': 423},
        {'slug': 'furniture', 'name': 'Furniture', 'icon': 'armchair', 'count': 234},
        {'slug': 'food', 'name': 'Food & Snacks', 'icon': 'utensils', 'count': 178},
    ]
    
    context = {
        'page_title': 'Browse by Category - PU-Marketplace',
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'base/categories.html', context)


def contact(request):
    """
    Contact Us Page
    GET /contact/
    POST /contact/
    
    Displays:
    - Contact form
    - Support email
    - Response time info
    """
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # TODO: Send email and save to database
        
        context = {
            'success': True,
            'message': 'Thank you for your message. We\'ll get back to you soon!'
        }
    else:
        context = {
            'page_title': 'Contact Us - PU-Marketplace',
            'page_description': 'Get in touch with our support team.',
        }
    
    return render(request, 'base/contact.html', context)


ALLOWED_CONTENT_TYPES = {
    'image': ['image/jpeg', 'image/png', 'image/webp', 'image/gif'],
    'video': ['video/mp4', 'video/webm', 'video/quicktime'],
}
MAX_FILE_SIZES = {'image': 10 * 1024 * 1024, 'video': 100 * 1024 * 1024}  # 10 MB / 100 MB


@login_required(login_url='auth:auth_view')
def r2_presign(request):
    """
    POST /api/r2-presign/
    Body: { "filename": "photo.jpg", "content_type": "image/jpeg", "resource_type": "image" }
    Returns: { "upload_url": "...", "public_url": "..." }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    import json
    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    filename = body.get('filename', '')
    content_type = body.get('content_type', '')
    resource_type = body.get('resource_type', 'image')

    if resource_type not in ALLOWED_CONTENT_TYPES:
        return JsonResponse({'error': 'Invalid resource type'}, status=400)
    if content_type not in ALLOWED_CONTENT_TYPES[resource_type]:
        return JsonResponse({'error': 'File type not allowed'}, status=400)

    ext = os.path.splitext(filename)[1].lower() or '.bin'
    key = f"media/{resource_type}s/{uuid.uuid4().hex}{ext}"

    s3 = boto3.client(
        's3',
        endpoint_url=f"https://{settings.CF_R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.CF_R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.CF_R2_SECRET_ACCESS_KEY,
        region_name='auto',
    )

    upload_url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': settings.CF_R2_BUCKET_NAME,
            'Key': key,
            'ContentType': content_type,
        },
        ExpiresIn=300,
    )

    public_url = f"{settings.CF_R2_PUBLIC_URL.rstrip('/')}/{key}"
    return JsonResponse({'upload_url': upload_url, 'public_url': public_url})


def serve_sw(request):
    """Serve sw.js from /sw.js so the service worker scope covers the whole origin."""
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    try:
        with open(sw_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse('// sw not found', content_type='application/javascript', status=404)


def serve_offline(request):
    """Minimal offline fallback page served by the service worker."""
    html = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<meta name="theme-color" content="#0d0e11"/>
<title>Offline — PU-Connect</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d0e11;color:#e8e6e0;font-family:'DM Sans',sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:2rem;text-align:center}
.wrap{max-width:340px}
.icon{margin:0 auto 1.5rem;width:64px;height:64px;opacity:.5}
h1{font-size:1.4rem;font-weight:700;margin-bottom:.75rem}
p{font-size:.9rem;color:#7a7e8a;line-height:1.6;margin-bottom:1.5rem}
button{background:#e8c96a;color:#0d0e11;border:none;border-radius:10px;padding:.75rem 2rem;font-size:.9rem;font-weight:600;cursor:pointer}
</style>
</head>
<body>
<div class="wrap">
  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <line x1="1" y1="1" x2="23" y2="23"/><path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"/><path d="M5 12.55a10.94 10.94 0 0 1 5.17-2.39"/><path d="M10.71 5.05A16 16 0 0 1 22.56 9"/><path d="M1.42 9a15.91 15.91 0 0 1 4.7-2.88"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>
  </svg>
  <h1>You're offline</h1>
  <p>No internet connection. Check your network and try again.</p>
  <button onclick="location.reload()">Try again</button>
</div>
</body>
</html>"""
    return HttpResponse(html, content_type='text/html')
