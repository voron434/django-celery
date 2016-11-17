from date_range_filter import DateRangeFilter
from django.contrib import admin

from elk.admin.filters import BooleanFilter
from market.admin.components import ClassesLeftInline, ClassesPassedInline, ProductContainerAdmin
from market.models import Subscription


class IsFinishedFilter(BooleanFilter):
    title = 'Is fully used'
    parameter_name = 'is_fully_used'

    def t(self, request, queryset):
        return queryset.filter(is_fully_used=True)

    def f(self, request, queryset):
        return queryset.filter(is_fully_used=False)


class IsActiveFilter(BooleanFilter):
    title = 'Is active'
    parameter_name = 'is_active'

    def t(self, request, queryset):
        return queryset.filter(active=1)

    def f(self, request, queryset):
        return queryset.filter(active=0)


@admin.register(Subscription)
class SubscriptionAdmin(ProductContainerAdmin):
    list_display = ('customer', '__str__', 'lesson_usage', 'planned_lessons', 'purchase_date',)
    list_filter = (IsActiveFilter, ('buy_date', DateRangeFilter), IsFinishedFilter)
    readonly_fields = ('lesson_usage', 'purchase_date', 'planned_lessons')
    inlines = (ClassesLeftInline, ClassesPassedInline)
    search_fields = ('customer__user__first_name', 'customer__user__last_name')
    fieldsets = (
        (None, {
            'fields': ('purchase_date', 'lesson_usage', 'customer', 'buy_price', 'product_type',)
        }),
    )

    def lesson_usage(self, instance):
        total = instance.classes
        finished = total.filter(is_fully_used=True)

        return '%d/%d' % (finished.count(), total.count())

    def planned_lessons(self, instance):
        """
        Lessons, that are planned, but not finished yet
        """
        scheduled = instance.classes.exclude(is_fully_used=True) \
            .filter(timeline__isnull=False).count()

        if not scheduled:
            return '—'
        else:
            return scheduled
