from django.contrib import admin

# Register your models here.
from .models import Database, Claim, Evidence, Annotation, Justification, ClaimParaphrases

admin.site.register(Database)
admin.site.register(Claim)
admin.site.register(Evidence)
admin.site.register(Annotation)
admin.site.register(Justification)
admin.site.register(ClaimParaphrases)