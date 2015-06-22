from django.db import models

# Create your models here.
class Watershed(models.Model):
    name = models.CharField(max_length = 200)
    
class GageLocation(models.Model):
    watershed = models.ForeignKey(Watershed)
    identifier = models.CharField(max_length=200)
    
class GradedFlowTarget(models.Model):
    location = models.ForeignKey(GageLocation)
    name = models.CharField(max_length=200)
    
class GradedFlowTargetElement(models.Model):
    flow_target = models.ForeignKey(GradedFlowTarget)
    from_month = models.IntegerField()
    from_day = models.IntegerField()
    to_month = models.IntegerField()
    to_day = models.IntegerField()
    target_value = models.DecimalField(max_digits=8, decimal_places=2)