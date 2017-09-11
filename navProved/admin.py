from django.contrib import admin
from .models import Product, Ticker, Price, Predict, DeclineRate, NavProvedResult


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name',)


class TickerAdmin(admin.ModelAdmin):
	list_display = ('name', 'prod_taxes', 'tax_rate', 'deferred', 'op_cost_esc', 'dda', 'def_after_5yrs', 'capex', 'op_cost')


class PriceAdmin(admin.ModelAdmin):
	list_display = ('prod', 'ticker', 'year', 'price')


class PredictAdmin(admin.ModelAdmin):
	list_display = ('prod', 'ticker', 'prod_esc', 'prod_diff', 'prod_pred_opd')


class DeclineRateAdmin(admin.ModelAdmin):
	list_display = ('prod', 'ticker', 'decline_rate')


class NavProvedResultAdmin(admin.ModelAdmin):
	list_display = ('ticker', 'pv', 'pv_boe', 'pv_mcfe')


admin.site.register(Product, ProductAdmin)
admin.site.register(Ticker, TickerAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Predict, PredictAdmin)
admin.site.register(DeclineRate, DeclineRateAdmin)
admin.site.register(NavProvedResult, NavProvedResultAdmin)