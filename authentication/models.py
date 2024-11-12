from django.contrib.auth.models import User
from django.db import models




# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    # subscription_plan = models.ForeignKey(SubscriptionPlan, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

    # def user_has_access_to_course(self, course):
    #     """
    #     Determine if the user has access to a specific course based on:
    #     - Whether the course is free (platform courses or instructor-owned).
    #     - Whether the user has purchased the course if it is paid.
    #     - The user's subscription plan and whether the course is platform-owned.
    #     """
    #     if isinstance(course, PlatformCourse):
    #         # Platform courses can be accessed based on subscription plan (Premium/Pro) or if the course is free
    #         if not course.is_paid or Purchase.objects.filter(user=self.user, course=course).exists():
    #             return True
    #         if self.subscription_plan and self.subscription_plan.name in ["Premium", "Pro"]:
    #             return True
    #         return False
    #     elif isinstance(course, InstructorCourse):
    #         # Instructors courses are always paid and require a separate purchase
    #         return Purchase.objects.filter(user=self.user, course=course).exists()
    #     return False






