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
    past_events = [
        {
            'title': 'YELA Football Cup',
            'kicker': 'Continuing Youth Engagement Program',
            'badge': 'Annual Program',
            'description': (
                'The YELA Football Cup is an ongoing annual program that uses sports, '
                'especially football, as a powerful platform to engage young people and '
                'raise awareness on key issues affecting their lives. It is part of '
                'YELA\'s long-term strategy to empower youth and build stronger, healthier, '
                'and more informed communities across Tanzania.'
            ),
            'venue': 'Kijitonyama, Dar es Salaam and expanding districts',
            'image': 'images/football.jpeg',
            'images': [
                'images/football.jpeg',
                'images/football2.jpeg',
                'images/Football3.jpeg',
            ],
            'objectives': [
                'Promote youth participation in civic education and leadership',
                'Provide sexual and reproductive health and mental health education',
                'Raise awareness on gender-based violence and advocate for gender equality',
                'Inspire entrepreneurship and economic empowerment',
                'Strengthen community unity, peace, and inclusion through sport',
            ],
            'continuity': [
                'Held annually and expanding to reach more districts and regions',
                'Creates a sustainable platform for community mobilization and education',
                'Engages local stakeholders and private sector sponsors to support youth causes',
                'Builds lasting opportunities for talent development, life skills, and behavior change',
            ],
        },
        {
            'title': 'Direction Hub Program',
            'kicker': 'Practical Business & Life Skills Training',
            'badge': '2-Day Training',
            'description': (
                'Direction Hub is one of YELA\'s flagship empowerment programs, designed '
                'to equip young entrepreneurs, especially municipal loan recipients, with '
                'the knowledge and skills needed to run sustainable businesses and make '
                'informed life choices.'
            ),
            'venue': 'Most recent session: Kibaha District, Pwani Region',
            'image': 'images/training2.jpeg',
            'images': [
                'images/training2.jpeg',
                'images/training.jpeg',
                'images/training3.jpeg',
                'images/training 5.jpeg',
                'images/trainnng4.jpeg',
                'images/tranning6.jpeg',
            ],
            'objectives': [
                'Train 300 young boys and girls from diverse backgrounds',
                'Support proper use of municipal and youth loans',
                'Build marketing, sales, and customer engagement skills',
                'Strengthen basic business management and financial literacy',
                'Develop leadership and accountability in entrepreneurship',
            ],
            'continuity_heading': 'Program Focus',
            'continuity': [
                'Understanding the effects of mixing love and business',
                'Building professional boundaries in youth-led ventures',
                'Using real-life examples, guided dialogue, and mentorship',
                'Helping participants grow profitable businesses and take charge of their futures',
            ],
            'note': (
                'The most recent Direction Hub session was successfully conducted in Kibaha '
                'District, reaching young people with practical, hands-on coaching.'
            ),
        },
        {
            'title': '20 Partners Project',
            'kicker': 'SRH & Relationship Education',
            'badge': '40 Youth Reached',
            'description': (
                'The 20 Partners Project promotes sexual and reproductive health education '
                'among young people in informal relationships. It creates a structured space '
                'for youth to learn, ask questions, and make safer, more informed decisions.'
            ),
            'venue': 'Selected participants from different communities',
            'image': 'images/relations4.jpeg',
            'images': [
                'images/relations4.jpeg',
                'images/relations5.jpeg',
                'images/relation.jpeg',
                'images/relation3.jpeg',
            ],
            'objectives': [
                'Engage 20 boys and 20 girls from different communities',
                'Educate young people in informal partnerships through structured sessions',
                'Promote safe relationships, consent, and SRH rights',
                'Strengthen knowledge on family planning and STI prevention',
                'Improve communication and respectful decision-making in relationships',
            ],
            'continuity_heading': 'Program Goal',
            'continuity': [
                'Reduce sexual and reproductive health risks among young people',
                'Empower youth to make informed relationship and health decisions',
                'Promote respectful, informed, and accountable youth relationships',
                'Create space for honest dialogue on consent, rights, and responsibility',
            ],
            'note': (
                'Through SRH education and relationship dialogue, the project supports young '
                'people to build healthier partnerships and protect their futures.'
            ),
        },
        {
            'title': 'Going Beyond Project',
            'kicker': 'Digital, Entrepreneurial & Life Skills',
            'badge': 'Youth Skills',
            'description': (
                'Going Beyond Project aimed to equip youth with digital, entrepreneurial, '
                'and life skills to help them thrive in today\'s changing economy. It '
                'specifically targeted underserved youth, especially young women, preparing '
                'them for success in the digital and entrepreneurial world.'
            ),
            'venue': 'YELA host organization and local community outreach spaces',
            'image': 'images/training 5.jpeg',
            'images': [
                'images/training 5.jpeg',
                'images/training2.jpeg',
                'images/WhatsApp Image 2026-06-17 at 1.07.18 PM.jpeg',
            ],
            'objectives': [
                'Provide a safe and inclusive space for program delivery',
                'Support outreach and youth mobilization in local communities',
                'Facilitate mentorship and coaching sessions',
                'Help track progress and impact among participating youth',
            ],
            'continuity_heading': 'Focus Areas',
            'continuity': [
                'Digital literacy and technology for business',
                'Entrepreneurship and innovation',
                'Financial literacy and saving culture',
                'Confidence and leadership building for young women',
            ],
            'note': (
                'As the host organization, YELA helped create the structure, mentorship, '
                'and community connection needed for underserved youth to build practical skills.'
            ),
        },
        {
            'title': 'Climate Action Project',
            'kicker': 'Environmental Conservation & Sustainability',
            'badge': 'Climate Action',
            'description': (
                'The Climate Action Project engages young people in practical environmental '
                'stewardship, connecting climate education with hands-on community action. '
                'Through tree planting, awareness sessions, and local mobilization, youth '
                'learn how their choices can protect the environment and strengthen community resilience.'
            ),
            'venue': 'Community green spaces and local learning sites',
            'image': 'images/env.jpeg',
            'images': [
                'images/env.jpeg',
                'images/env2.jpg',
                'images/evn3.jpg',
            ],
            'objectives': [
                'Promote youth participation in climate action and environmental stewardship',
                'Support tree planting and community greening activities',
                'Raise awareness on waste management and sustainable daily practices',
                'Build responsibility for protecting shared community spaces',
                'Encourage youth-led environmental leadership and advocacy',
            ],
            'continuity_heading': 'Program Focus',
            'continuity': [
                'Climate education linked to practical action',
                'Tree planting and care for green spaces',
                'Community mobilization around sustainability',
                'Youth leadership in environmental protection',
            ],
            'note': (
                'The project helps young people turn climate awareness into visible community '
                'action, building greener and more resilient neighborhoods.'
            ),
        },
    ]
    return render(request, 'core/events.html', {'past_events': past_events})


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
        {'name': 'Sarah Ndago', 'role': 'YELA Mentor, Dar es Salaam Chapter',
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
        {'title': 'Youth Empowerment', 'icon': '🌟', 'tag': 'Skills & opportunity', 'order': 1,
         'description': 'We empower young people through skills development, entrepreneurship, employability initiatives, civic engagement, and access to opportunities that enable them to become active contributors to their communities and society.'},
        {'title': 'Leadership Skills Development', 'icon': '🧭', 'tag': 'Training & mentorship', 'order': 2,
         'description': 'We nurture ethical, responsible, and visionary leaders by providing leadership training, mentorship, civic education, and opportunities for meaningful participation in decision-making processes.'},
        {'title': 'Health Awareness', 'icon': '💚', 'tag': 'Well-being', 'order': 3,
         'description': 'We promote healthy lifestyles by raising awareness on physical and mental health, sexual and reproductive health, nutrition, disease prevention, and overall well-being among young people and communities.'},
        {'title': 'Women and Gender Equality', 'icon': '♀️', 'tag': 'Empowerment', 'order': 4,
         'description': 'We advocate for gender equality and the empowerment of women and girls through education, capacity-building, leadership opportunities, and initiatives that address gender-based discrimination and violence.'},
        {'title': 'Environmental Conservation and Sustainability', 'icon': '🌱', 'tag': 'Climate action', 'order': 5,
         'description': 'We promote environmental stewardship through climate action, tree planting, waste management, environmental education, and sustainable practices that contribute to a greener future.'},
        {'title': 'Digital Awareness', 'icon': '💻', 'tag': 'Digital safety & skills', 'order': 6,
         'description': 'We equip young people with digital skills and knowledge to safely and effectively navigate the digital world, including digital literacy, online safety, emerging technologies, artificial intelligence, and digital career opportunities.'},
        {'title': 'Education and Innovation', 'icon': '🔬', 'tag': 'STEM & creativity', 'order': 7,
         'description': 'We foster quality education, creativity, innovation, STEM learning, research, and technology-driven solutions that empower young people to address community challenges and thrive in a rapidly changing world.'},
    ]
    for d in data:
        defaults = d.copy()
        title = defaults.pop('title')
        Program.objects.update_or_create(title=title, defaults=defaults)


def _seed_events():
    data = [
        {
            'title': 'Youth Leadership Workshop',
            'description': 'A practical session helping students build confidence, communication skills, and community leadership habits.',
            'venue': 'Dar es Salaam Community Hall',
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
