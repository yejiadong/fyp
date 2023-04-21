from uuid import uuid4
from django.utils import timezone
from django.db import models
from user.models import CustomUser

# Owner, name combi must be unique
class Database(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    accesskey = models.CharField(max_length=50)
    is_active= models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['owner', 'name', 'description', 'accesskey', 'is_active']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'name'], name="labeller_database_unique")
        ]

    def __str__(self):
        return self.name

# Database and Claim content combi must be unique, no same claim in same database
class Claim(models.Model):
    original_id = models.IntegerField()
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    is_paraphrased = models.BooleanField(default=False)
    # There can be multiple similar claims in the same database, but with different evidences stored

    def __str___(self):
            return self.name

# Claim and content must be unique
class Evidence(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="evidences")
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    same_entity_label = models.BooleanField(default=None, null=True)
    same_entity_justification = models.CharField(max_length=500, default=None, null=True)
    general_facts_label = models.CharField(max_length=20, choices=(("SUPPORTS", "Supports"), ("REFUTES", "Refutes"), ("NOT ENOUGH INFO", "Not Enough Info")), default=None, null=True)
    general_facts_justification = models.CharField(max_length=500, default=None, null=True)
    time_label = models.CharField(max_length=20, choices=(("SUPPORTS", "Supports"), ("REFUTES", "Refutes"), ("NOT ENOUGH INFO", "Not Enough Info")), default=None, null=True)
    time_justification = models.CharField(max_length=500, default=None, null=True)
    topic = models.CharField(max_length=100, default=None, null=True)
    claim_temporal = models.JSONField(default=None, null=True)
    evidence_temporal = models.JSONField(default=None, null=True)
    relevant_evidence = models.JSONField(default=None, null=True)
    final_label = models.CharField(max_length=20, choices=(("SUPPORTS", "Supports"), ("REFUTES", "Refutes"), ("NOT ENOUGH INFO", "Not Enough Info")), default=None, null=True)
    model_label = models.CharField(max_length=20, choices=(("SUPPORTS", "Supports"), ("REFUTES", "Refutes"), ("NOT ENOUGH INFO", "Not Enough Info")), default=None, null=True)
    manual_review = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['claim', 'content'], name="labeller_evidence_unique")
        ]

# Annotation
class Annotation(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="annotations")
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, related_name="evidence_annotations")
    annotator_email = models.CharField(max_length=100)
    temporal_label = models.CharField(max_length=30, blank=True, null=True)
    general_label = models.CharField(max_length=30, blank=True, null=True)
    overall_label = models.CharField(max_length=30, blank=True, null=True)
    annotated_at = models.DateTimeField(default=timezone.now)
    ignore_flag = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['claim', 'evidence', 'annotator_email'], name="annotation_unique")
        ]

# Justification
class Justification(models.Model):
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name="justifications")
    # True means temporal, False means general
    temporal = models.BooleanField()
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, blank=True, null=True)
    justification = models.CharField(max_length=100)


# Paraphrases
class ClaimParaphrases(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="paraphrases")
    claim_content = models.CharField(max_length=500)

