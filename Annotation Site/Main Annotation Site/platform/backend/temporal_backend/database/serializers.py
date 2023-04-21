from rest_framework import serializers
from .models import Database, Claim, Evidence, Annotation, Justification, ClaimParaphrases

class DatabaseSerializer(serializers.ModelSerializer):
    num_claims = serializers.SerializerMethodField()

    def get_num_claims(self, obj):
        try:
            return obj.num_claims
        except:
            return None

    class Meta:
        model = Database
        fields = "__all__"

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"

class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = "__all__"

class ClaimEvidenceSerializer(serializers.ModelSerializer):
    evidences = EvidenceSerializer(many=True)

    class Meta:
        model = Claim
        fields = '__all__'

class ClaimEvidenceExcludeSerializer(serializers.ModelSerializer):
    evidences = serializers.SerializerMethodField()

    class Meta:
        model = Claim
        fields = ('id', 'original_id', 'content', 'database', 'created_at', 'evidences')

    def get_evidences(self, obj):
        annotator_email = self.context.get('annotator_email')
        annotated_evidences = obj.evidences.filter(evidence_annotations__annotator_email=annotator_email)
        unannotated_evidences = obj.evidences.exclude(evidence_annotations__annotator_email=annotator_email)
        if annotated_evidences.exists():
            # exclude annotated evidences
            unannotated_evidences = unannotated_evidences.exclude(id__in=annotated_evidences.values_list('id', flat=True))
        return EvidenceSerializer(unannotated_evidences, many=True).data



class JusstificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justification
        fields = '__all__'

class AnnotationSerializer(serializers.ModelSerializer):
    claim = ClaimEvidenceSerializer(many=False)
    justifications = JusstificationSerializer(many=True)
    class Meta:
        model = Annotation
        fields = '__all__'

class ParaphraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimParaphrases
        fields = ('claim_content',)

class ClaimEvidenceFinalLabelSerializer(serializers.ModelSerializer):
    evidence = serializers.SerializerMethodField()
    paraphrases = ParaphraseSerializer(many=True, read_only=True)

    class Meta:
        model = Claim
        fields = ('original_id', 'content', 'evidence', 'paraphrases')

    def get_evidence(self, obj):
        final_label_evidences = obj.evidences.filter(final_label__isnull=False)
        return [{'content': evidence.content, 'final_label': evidence.final_label} for evidence in final_label_evidences]