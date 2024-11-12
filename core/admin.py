from django.contrib import admin

from .models import Course, Module, Lesson, Quiz, Question, Choice, Enrollment, Progress, Subscription, \
    SubscriptionPlan, Feature, Purchase, TradePerformance, Trade, PlatformCourse, InstructorCourse


# Register your models here.


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days', 'access_to_paid_courses']
    filter_horizontal = ('features',)

    def access_to_paid_courses(self, obj):
        """
        Determine whether the subscription plan grants access to paid courses.
        Modify this logic based on your actual access conditions.
        """
        if obj.name in ["Premium", "Pro"]:  # Example condition: these plans have access to paid courses
            return "Yes"
        return "No"

    access_to_paid_courses.short_description = 'Access to Paid Courses'

admin.site.register(Course)
admin.site.register(PlatformCourse)
admin.site.register(InstructorCourse)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(Subscription)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Purchase)
admin.site.register(Trade)
admin.site.register(TradePerformance)