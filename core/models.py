from django.db import models


class ContactMessage(models.Model):
    INTEREST_CHOICES = [
        ('volunteer', 'Volunteer with YELA'),
        ('partner', 'Partner with us'),
        ('donate', 'Donate or fund a programme'),
        ('apply', 'Apply to a programme'),
        ('general', 'General enquiry'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.email} ({self.created_at.strftime('%d %b %Y')})"


class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=200)
    quote = models.TextField()
    initials = models.CharField(max_length=3, help_text='2-3 letters shown in avatar')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} — {self.role}"


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=200)
    initials = models.CharField(max_length=3)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🌟', help_text='Emoji icon')
    tag = models.CharField(max_length=60, help_text='Short label e.g. "6 months"')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    image = models.ImageField(upload_to='events/', blank=True)
    registration_link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['event_date', 'event_time', 'order']

    def __str__(self):
        return f"{self.title} — {self.event_date:%d %b %Y}"


class StudentProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='student_profile')
    phone = models.CharField(max_length=40)
    age = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=150, blank=True)
    school_or_organization = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ProgramApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('reviewing', 'Reviewing'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='program_applications')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='applications')
    motivation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'program']

    def __str__(self):
        return f"{self.user.username} — {self.program.title}"
