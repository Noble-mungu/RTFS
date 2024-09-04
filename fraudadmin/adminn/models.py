from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime    
from django.utils import timezone


class transaction(models.Model):
    key = models.CharField(max_length=255)
    index = models.IntegerField()
    phonenumber = models.CharField(max_length=20)
    time = models.DateTimeField(default=timezone.now)
    v1 = models.CharField(max_length=255, blank=True, null=True)
    v2 = models.CharField(max_length=255, blank=True, null=True)
    v3 = models.CharField(max_length=255, blank=True, null=True)
    v4 = models.CharField(max_length=255, blank=True, null=True)
    v5 = models.CharField(max_length=255, blank=True, null=True)
    v6 = models.CharField(max_length=255, blank=True, null=True)
    v7 = models.CharField(max_length=255, blank=True, null=True)
    v8 = models.CharField(max_length=255, blank=True, null=True)
    v9 = models.CharField(max_length=255, blank=True, null=True)
    v10 = models.CharField(max_length=255, blank=True, null=True)
    v11 = models.CharField(max_length=255, blank=True, null=True)
    v12 = models.CharField(max_length=255, blank=True, null=True)
    v13 = models.CharField(max_length=255, blank=True, null=True)
    v14 = models.CharField(max_length=255, blank=True, null=True)
    v15 = models.CharField(max_length=255, blank=True, null=True)
    v16 = models.CharField(max_length=255, blank=True, null=True)
    v17 = models.CharField(max_length=255, blank=True, null=True)
    v18 = models.CharField(max_length=255, blank=True, null=True)
    v19 = models.CharField(max_length=255, blank=True, null=True)
    v20 = models.CharField(max_length=255, blank=True, null=True)
    v21 = models.CharField(max_length=255, blank=True, null=True)
    v22 = models.CharField(max_length=255, blank=True, null=True)
    v23 = models.CharField(max_length=255, blank=True, null=True)
    v24 = models.CharField(max_length=255, blank=True, null=True)
    v25 = models.CharField(max_length=255, blank=True, null=True)
    v26 = models.CharField(max_length=255, blank=True, null=True)
    v27 = models.CharField(max_length=255, blank=True, null=True)
    v28 = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField(default=0)
    time_produced = models.DateTimeField(default=timezone.now)
    time_processed = models.DateTimeField(default=timezone.now)
    latency = models.IntegerField(default=0)
    prediction = models.IntegerField(default=0)
    reply = models.CharField(max_length=255, default='')
    is_fraud = models.BooleanField(default=False)
    

    def __str__(self):
        return f"Transaction {self.key} - Index {self.index}"

class feedback(models.Model):
    transaction = models.ForeignKey(transaction, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20)
    feedback_response = models.CharField(max_length=20)
    processed_by = models.CharField(max_length=50, null=True, blank=True)
    feedback_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction.transaction_id} - {self.feedback_type}"
