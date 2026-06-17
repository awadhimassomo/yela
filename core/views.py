from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import ContactForm, ProgramApplicationForm, StudentLoginForm, StudentRegistrationForm
from .models import Event, ProgramApplication, Testimonial, TeamMember, Program


def home(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    team = TeamMember.objects.filter(is_active=True)
    programs = Program.objects.filter(is_active=True)

    # Seed defaults if DB is empty (first run)
    if not testimonials.exists():
        _seed_testimonials()
        testimonials = Testimonial.objects.filter(is_active=True)
    if not team.exists():
        _seed_team()
        team = TeamMember.objects.filter(is_active=True)
    if not programs.exists():
        _seed_programs()
        programs = Program.objects.filter(is_active=True)

    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            # Send notification email (works when EMAIL_BACKEND is configured)
            try:
                send_mail(
                    subject=f'[YELA] New message from {contact.first_name} {contact.last_name}',
                    message=(
                        f'Name: {contact.first_name} {contact.last_name}\n'
                        f'Email: {contact.email}\n'
                        f'Interest: {contact.get_interest_display()}\n\n'
                        f'Message:\n{contact.message}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@yela.or.tz',
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, 'Thank you! We will be in touch within 48 hours.')
            return redirect('home')

    context = {
        'testimonials': testimonials,
        'team': team,
        'programs': programs,
        'form': form,
    }
    return render(request, 'core/home.html', context)


def events(request):
    events_qs = Event.objects.filter(is_active=True)
    if not events_qs.exists():
        _seed_events()
        events_qs = Event.objects.filter(is_active=True)
    return render(request, 'core/events.html', {'events': events_qs})


def student_register(request):
    if request.user.is_authenticated:
        return redirect('program_apply')

    form = StudentRegistrationForm()
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your student account has been created. You can now apply for a program.')
            return redirect('program_apply')

    return render(request, 'core/register.html', {'form': form})


def student_login(request):
    if request.user.is_authenticated:
        return redirect('program_apply')

    form = StudentLoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Welcome back. You are signed in.')
        return redirect(request.GET.get('next') or 'program_apply')

    return render(request, 'core/login.html', {'form': form})


def student_logout(request):
    logout(request)
    messages.success(request, 'You have been signed out.')
    return redirect('home')


@login_required(login_url='student_login')
def program_apply(request):
    programs = Program.objects.filter(is_active=True)
    form = ProgramApplicationForm()
    form.fields['program'].queryset = programs

    if request.method == 'POST':
        form = ProgramApplicationForm(request.POST)
        form.fields['program'].queryset = programs
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            try:
                application.save()
                messages.success(request, 'Your program application has been submitted.')
                return redirect('program_apply')
            except IntegrityError:
                form.add_error('program', 'You have already applied for this program.')

    applications = ProgramApplication.objects.filter(user=request.user).select_related('program')
    return render(request, 'core/apply.html', {
        'form': form,
        'applications': applications,
    })


# ── Seed helpers (run once on empty DB) ─────────────────────────────────────

def _seed_testimonials():
    data = [
        {'name': 'Amina Mtui', 'role': 'Youth Leadership Academy, Class of 2023',
         'initials': 'AM', 'order': 1,
         'quote': 'YELA didn\'t just teach me skills — it showed me who I could become. The leadership programme changed my entire outlook on life and my role in this community.'},
        {'name': 'James Kibet', 'role': 'Digital Skills Hub Graduate',
         'initials': 'JK', 'order': 2,
         'quote': 'The Digital Skills Hub gave me the tools to start my own freelance design business. I now earn a living doing what I love, and I am training other youth in my village.'},
        {'name': 'Sarah Ndago', 'role': 'YELA Mentor, Arusha Chapter',
         'initials': 'SN', 'order': 3,
         'quote': 'As a mentor with YELA, I get more than I give. Watching these young people grow their confidence and pursue their dreams is the most fulfilling work I have ever done.'},
    ]
    for d in data:
        Testimonial.objects.get_or_create(name=d['name'], defaults=d)


def _seed_team():
    data = [
        {'name': 'Emmanuel Kariuki', 'role': 'Executive Director', 'initials': 'EK', 'order': 1},
        {'name': 'Fatuma Masoud', 'role': 'Programs Manager', 'initials': 'FM', 'order': 2},
        {'name': 'Daniel Odhiambo', 'role': 'Head of Digital Skills', 'initials': 'DO', 'order': 3},
        {'name': 'Grace Njeri', 'role': 'Community & Outreach', 'initials': 'GN', 'order': 4},
    ]
    for d in data:
        TeamMember.objects.get_or_create(name=d['name'], defaults=d)


def _seed_programs():
    data = [
        {'title': 'Youth Leadership Academy', 'icon': '🌟', 'tag': '6 months', 'order': 1,
         'description': 'A six-month intensive programme developing the next generation of community leaders through workshops, projects, and peer learning.'},
        {'title': 'Digital Skills Hub', 'icon': '💻', 'tag': 'Ongoing cohorts', 'order': 2,
         'description': 'Equipping young people with practical tech skills — from digital literacy to coding, design, and online entrepreneurship.'},
        {'title': 'Youth Entrepreneurship', 'icon': '🚀', 'tag': 'Funding available', 'order': 3,
         'description': 'Helping young entrepreneurs turn ideas into viable businesses through training, seed funding, and expert mentorship.'},
        {'title': 'Creative Arts Initiative', 'icon': '🎨', 'tag': 'Year-round', 'order': 4,
         'description': 'Using art, music, and performance as tools for self-expression, healing, and social advocacy among young people.'},
        {'title': 'Civic Engagement', 'icon': '🗳️', 'tag': 'Community based', 'order': 5,
         'description': 'Training young citizens to actively participate in governance, advocate for their rights, and engage with local leadership.'},
        {'title': 'Mentorship Network', 'icon': '🤝', 'tag': '1-on-1 matching', 'order': 6,
         'description': 'Connecting youth with experienced professionals and leaders who guide them through career and personal development journeys.'},
    ]
    for d in data:
        Program.objects.get_or_create(title=d['title'], defaults=d)


def _seed_events():
    data = [
        {
            'title': 'Youth Leadership Workshop',
            'description': 'A practical session helping students build confidence, communication skills, and community leadership habits.',
            'venue': 'Arusha Community Hall',
            'event_date': '2026-07-12',
            'event_time': '10:00',
            'order': 1,
        },
        {
            'title': 'Digital Skills Open Day',
            'description': 'An introduction to digital literacy, online safety, design tools, and pathways into technology careers.',
            'venue': 'YELA Digital Hub',
            'event_date': '2026-08-03',
            'event_time': '09:30',
            'order': 2,
        },
        {
            'title': 'Mentorship & Career Forum',
            'description': 'Youth meet mentors, ask career questions, and learn how to prepare for school, work, and entrepreneurship opportunities.',
            'venue': 'Dar es Salaam Youth Center',
            'event_date': '2026-08-24',
            'event_time': '14:00',
            'order': 3,
        },
    ]
    for d in data:
        Event.objects.get_or_create(title=d['title'], defaults=d)
