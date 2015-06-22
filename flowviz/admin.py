from django.contrib import admin

# Register your models here.
from models import GageLocation, Watershed, GradedFlowTarget, GradedFlowTargetElement

admin.site.register(GageLocation)
admin.site.register(Watershed)
admin.site.register(GradedFlowTarget)
admin.site.register(GradedFlowTargetElement)
