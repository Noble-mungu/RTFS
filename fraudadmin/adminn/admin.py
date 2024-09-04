from django.contrib import admin
from .models import transaction , feedback
from django.http import HttpResponse
import csv

class FraudTransactionAdmin(admin.ModelAdmin):
    list_display = ('key', 'amount', 'is_fraud_display', 'reply', 'phonenumber', 'time_processed', 'prediction')
    list_filter = ('is_fraud', 'prediction', 'reply')
    search_fields = ('key', 'amount', 'is_fraud', 'reply', 'phonenumber', 'time_processed', 'prediction')

    def is_fraud_display(self, obj):
        return obj.is_fraud  # This will call the property if you used Option 2

    is_fraud_display.boolean = True
    is_fraud_display.short_description = 'Is Fraud'
    
    def get_queryset(self, request):
        qs = super(FraudTransactionAdmin, self).get_queryset(request)
        return qs.filter(is_fraud=True)

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fraud_transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(['key', 'amount', 'is_fraud', 'reply', 'phonenumber', 'time_processed', 'prediction'])

        for obj in queryset:
            writer.writerow([obj.key, obj.amount, obj.is_fraud, obj.reply, obj.phonenumber, obj.time_processed, obj.prediction])

        return response

    export_csv.short_description = 'Export selected fraud transactions to CSV'

    actions = [export_csv]

admin.site.register(transaction, FraudTransactionAdmin)
admin.site.register(feedback)
