from django.contrib import admin
from .models import CustomUser, Schedule, Position, Reservation, Table, Order, Dish, Ingredient, News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'hidden')


admin.site.register(News, NewsAdmin)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(Reservation)
admin.site.register(Table)
admin.site.register(Position)
admin.site.register(Schedule)
