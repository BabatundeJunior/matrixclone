from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from authentication.models import UserProfile


# Create your models here.

# core/models.py

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class PlatformCourse(Course):
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title


class InstructorCourse(Course):
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    # videos = models
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Quiz(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.module.title} - Quiz: {self.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Enrollment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='platform_course_enrollments')
    course = models.ForeignKey(PlatformCourse, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.user.username} enrolled in {self.course.title}"


class Progress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.lesson.title} progress"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('core.Course', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.course.title} on {self.purchase_date}"


class Feature(models.Model):
    """To help me define each feature available in the system."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, help_text="Description of the feature.")

    def __str__(self):
        return self.name


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)  # "Free", "Premium", "Pro" plans
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(help_text="Duration of the plan in days", null=True, blank=True)
    features = models.ManyToManyField('Feature', blank=True, related_name='subscription_plans')
    order_priority = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['order_priority']

    def __str__(self):
        return self.name




class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('expired', 'Expired')], default='active')

    def __str__(self):
        return f"{self.user.user.username} - {self.plan.name if self.plan else 'Subscription'}"

    def is_active(self):
        """Returns True if the subscription is currently active."""
        return (self.end_date is None or self.end_date >= timezone.now()) and self.status == 'active'

    def save(self, *args, **kwargs):
        # Automatically set end date based on the subscription plan's duration when saving
        if not self.end_date and self.plan:
            self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_days)

        super().save(*args, **kwargs)
        # Update the user profile's subscription_plan upon save
        self.user.subscription_plan = self.plan
        self.user.save()


class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    trade_date = models.DateTimeField()
    pair = models.CharField(max_length=6, help_text="Enter currency pair, e.g., GBPUSD")
    entry_price = models.DecimalField(max_digits=10, decimal_places=5)
    exit_price = models.DecimalField(max_digits=10, decimal_places=5)
    position_size = models.DecimalField(max_digits=10, decimal_places=2)
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2)
    trade_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.trade_type.capitalize()} {self.pair} on {self.trade_date.date()}"

    def calculate_return_percentage(self):
        if self.trade_type == 'buy':
            return ((self.exit_price - self.entry_price) / self.entry_price) * 100
        else:
            return ((self.entry_price - self.exit_price) / self.entry_price) * 100


class TradePerformance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trade_performance')
    total_trades = models.PositiveIntegerField(default=0)
    total_profit_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    win_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # As a percentage
    avg_return_per_trade = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Avg % return
    top_pairs = models.JSONField(default=list, blank=True)  # Will store list of pairs with the best performance

    def update_performance(self):
        """Update performance metrics based on user's trades."""
        trades = self.user.trades.all()
        total_trades = trades.count()
        winning_trades = trades.filter(profit_loss__gt=0).count()
        total_profit_loss = trades.aggregate(models.Sum('profit_loss'))['profit_loss__sum'] or 0.00
        avg_return = trades.aggregate(models.Avg('profit_loss'))['profit_loss__avg'] or 0.00
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0.00

        # Update fields
        self.total_trades = total_trades
        self.total_profit_loss = total_profit_loss
        self.avg_return_per_trade = avg_return
        self.win_rate = win_rate

        # Track top performing pairs
        top_pairs = self.get_top_pairs()
        self.top_pairs = top_pairs

        self.save()

    def get_top_pairs(self):
        """Return a list of pairs where the user has the best performance."""
        # Aggregate trades by currency pair
        pairs = self.user.trades.values('pair').annotate(
            total_profit=models.Sum('profit_loss'),
            total_trades=models.Count('id')
        ).order_by('-total_profit')

        # Filter pairs where the user made a profit
        top_pairs = [
            pair['pair'] for pair in pairs if pair['total_profit'] > 0
        ]

        return top_pairs

    def __str__(self):
        return f"Performance for {self.user.username}"
