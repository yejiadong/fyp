from django.shortcuts import render
from rest_framework import generics
from django.db.models import Count, Q, F
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from database.serializers import DatabaseSerializer, ClaimSerializer, EvidenceSerializer, ClaimEvidenceFinalLabelSerializer, ClaimEvidenceExcludeSerializer, AnnotationSerializer
from database.models import Database, Claim, Evidence, Annotation, Justification, ClaimParaphrases
from user.models import CustomUser
import bcrypt
from django.db.models import Count
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count, Case, When, FloatField
import requests
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import ExpressionWrapper
import json
import re
import numpy as np
from django.db.models import Prefetch
import ast


# Generate database's secure accesskey with a salt
def hash_new_password(password):
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    bytePwd = password.encode('utf-8')
    # Generate salt
    mySalt = bcrypt.gensalt()
    # Hash password
    hash = bcrypt.hashpw(bytePwd, mySalt)   
    return hash.decode('utf-8')

def is_correct_password(pw_hash, password):
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return bcrypt.checkpw(password.encode('utf-8'), pw_hash.encode('utf-8'))

# Check annotation password matches
class CheckAnnotationAPIView(APIView):
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    """This endpoint makes sure users specify a correct access-key."""
    def post(self, request):
            providedKey = request.data.get('accessKey')
            db = request.data.get('databaseId')
            try:
                obj = Database.objects.get(id = db)
            except Database.DoesNotExist:
                raise NotFound("Specified database id does not exist!")
            if (obj.is_active == False):
                raise NotFound("Specified database is not ready for annotation yet.!")
            correct_password = is_correct_password(obj.accesskey, providedKey) 
            return Response({"validated": correct_password})

# Database
class ListDatabaseAPIView(ListAPIView):
    """This endpoint list all of the available databases"""
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    def get_queryset(self):
        """
        Return a list of all the databases
        for the currently authenticated user.
        """
        user = self.request.user
        filtered_queryset = Database.objects.filter(owner=user).annotate(
            num_claims=Count('claim')
        )
        return filtered_queryset
        

class CreateDatabaseAPIView(APIView):
    """This endpoint allows for creation of a database if it does not exist, or just returns the database id if it exists"""
    def post(self, request):
        reqOwner = request.data.get('owner')
        reqName = request.data.get('name')
        reqDescription = request.data.get('description')
        pw_hash = hash_new_password(request.data.get('accesskey'))
        user = CustomUser.objects.get(id=reqOwner)

        obj, created = Database.objects.get_or_create(
        owner=user,
        name=reqName,
        defaults={'description': reqDescription, 'accesskey': pw_hash})
        return Response({"id": obj.id, "created": created})

class UpdateDatabaseAPIView(UpdateAPIView):
    """This endpoint allows for updating a specific database by passing in the id of the database to update"""
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer

class DeleteDatabaseAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific Database"""
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer

# Main function to add databases + claims + evidence + temporal arguments to reduce axios calls
class CreateDatabaseClaimEvidenceTemporalAPIView(APIView):
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        reqNew = request.data.get('new') == 'true'
        # Create database first
        if reqNew == True:
            reqOwner = request.data.get('owner')
            reqName = request.data.get('name')
            reqDescription = request.data.get('description')
            pw_hash = hash_new_password(request.data.get('accesskey'))
            user = CustomUser.objects.get(id=reqOwner)
            databaseObj, databaseCreated = Database.objects.get_or_create(
            owner=user,
            name=reqName,
            defaults={'description': reqDescription, 'accesskey': pw_hash})
        else:
            databaseObj = Database.objects.get(id = int(request.data.get('databaseId')))

        # Add claims and evidences
        data = request.FILES.get('file')

        if data is None:
            return Response({'error': 'No file found'}, status=400)
        try:
            file_data = json.loads(data.read().decode('utf-8'))
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON file'}, status=400)

        data.close()
        # Create a list to store claims
        claims = []

        # Iterate over each claim in the file data
        for claim_data in file_data:
            content = claim_data['claim']
            original_id = claim_data['id']
            claim = Claim(
                database=databaseObj,
                content=content,
                original_id=original_id
            )
            claims.append(claim)

        # Bulk create the claims and get their primary keys
        Claim.objects.bulk_create(claims)
         # Replace the current claims_pks query
        claims_pks = Claim.objects.filter(database=databaseObj, original_id__in=[claim['id'] for claim in file_data]).values_list('pk', flat=True)

        # Create a list to store evidences and a set for unique evidence keys
        evidences = []
        unique_evidence_keys = set()

        claims_map = {claim['id']: pk for claim, pk in zip(file_data, claims_pks)}

        # Iterate over the claims in file_data
        for claim_data in file_data:
            claim_pk = claims_map[claim_data['id']]
            # Iterate over each evidence for this claim
            for evidence_data in claim_data['evidence']:
                content = evidence_data[0]
                # Check if the evidence_key already exists
                evidence_key = (claim_pk, content)
                if evidence_key not in unique_evidence_keys:
                    if len(evidence_data) == 1:
                        # If the evidence_key doesn't exist, create a new instance
                        evidence = Evidence(
                            claim_id=claim_pk,
                            content=content
                        )
                        unique_evidence_keys.add(evidence_key)
                        evidences.append(evidence)
                    else:
                        print(evidence_data[4])
                        general_facts_label = evidence_data[4]
                        same_entity_label = evidence_data[7]
                        same_entity_justification = evidence_data[6]
                        general_facts_justification = evidence_data[3]
                        time_label = evidence_data[8]
                        time_justification = evidence_data[9]
                        topic = evidence_data[10]
                        claim_temporal = evidence_data[1]
                        evidence_temporal = evidence_data[2]
                        relevant_evidence = evidence_data[5]
                        model_label = evidence_data[11]

                        evidence = Evidence(
                            claim_id=claim_pk,
                            content=content,
                            same_entity_label=same_entity_label,
                            same_entity_justification=same_entity_justification,
                            general_facts_label=general_facts_label,
                            general_facts_justification=general_facts_justification,
                            time_label=time_label,
                            time_justification=time_justification,
                            topic=topic,
                            claim_temporal = ast.literal_eval(evidence_data[1]),
                            evidence_temporal = ast.literal_eval(evidence_data[2]),
                            relevant_evidence = ast.literal_eval(evidence_data[5]),
                            model_label=model_label
                        )
                        unique_evidence_keys.add(evidence_key)
                        evidences.append(evidence)

        # Create the Evidence instances 
        Evidence.objects.bulk_create(evidences)

        return Response({"databaseId": databaseObj.pk, "numClaim": len(claims), "numEvidence": len(evidences)})

# Claims
class CreateClaimAPIView(APIView):
    """This endpoint allows for creation of a claim if it does not exist, or just returns the claim id if it exists"""
    def post(self, request):
        reqDatabase = request.data.get('database')
        reqContent = request.data.get('content')
        reqOriginalId = request.data.get('original_id')

        claim = Claim(
            database=Database.objects.get(id=reqDatabase),
            content=reqContent,
            original_id=reqOriginalId
        )
        claim.save()

        return Response({"id": claim.id})

class ListClaimAPIView(ListAPIView):
    serializer_class = ClaimSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned claims to a given database,
        by filtering against a `databaseId` query parameter in the URL.
        """
        queryset = Claim.objects.all()
        databaseId = self.request.query_params.get('databaseId')
        databaseObj = Database.objects.get(id=databaseId)
        queryset = queryset.filter(database=databaseObj)
        return queryset

# Get single entry for annotation (instead of all for speed)
class ListClaimWithEvidenceAPIView(APIView):
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []

    serializer_class = ClaimEvidenceExcludeSerializer
    def post(self, request):
        """
        Restricts the returned claims to a given database,
        by filtering against a `databaseId` query parameter in the URL.
        Also ensures that returned results have not been previously annotated already.
        """
        database_id = request.data.get('databaseId')
        annotator_email = request.data.get('annotatorEmail')

        if not database_id:
            raise NotFound("Database ID must be provided!")

        if not annotator_email:
            raise NotFound("Annotator email was not provided!")

        database_obj = Database.objects.get(id=database_id)
        print(database_obj)
        queryset = Claim.objects.filter(database=database_obj).annotate(
            annotated_evidences_count=Count(
                'evidences__evidence_annotations',
                filter=Q(evidences__evidence_annotations__annotator_email=annotator_email),
                distinct=True
            ),
            total_evidences_count=Count('evidences'),
        ).filter(total_evidences_count__gt=F('annotated_evidences_count'))

        # Filter only unannotated evidences
        unannotated_evidences = Evidence.objects.filter(
            claim__in=queryset,
        ).exclude(
            evidence_annotations__annotator_email=annotator_email,
        ).exclude(
            manual_review=True
        )
        print("Filtered Claims:", queryset)
        # Serialize the first claim with unannotated evidences
        if unannotated_evidences.exists():
            first_claim = unannotated_evidences.first().claim
            output = ClaimEvidenceExcludeSerializer(first_claim, context={'annotator_email': annotator_email}, many=False)
        else:
            output = None

        return Response({
            "count": queryset.count(),
            "firstItem": output.data if output else None
        })


class DeleteClaimAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific Claim"""
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer


# Evidences
class CreateEvidenceAPIView(APIView):
    """This endpoint allows for creation of an evidence if it does not exist, or just returns the evidence id if it exists"""
    def post(self, request):
        reqClaim = request.data.get('claim')
        reqContent = request.data.get('content')
        getClaim = Claim.objects.get(id=reqClaim)
        obj, created = Evidence.objects.get_or_create(
        claim=getClaim,
        content=reqContent)
        return Response({"id": obj.id, "created": created})

class UpdateEvidenceAPIView(APIView):
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    def put(self, request, evidence_id):
        # Get the evidence instance
        try:
            evidence = Evidence.objects.get(pk=evidence_id)
        except Evidence.DoesNotExist:
            return Response({'error': f'Evidence with id {evidence_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Get the corresponding claim instance
        claim = evidence.claim

        # Prepare the claim and evidence JSON payload
        payload = {
            'claim': claim.content,
            'evidence': evidence.content,
        }

        # Send the request to the OpenAI endpoint
        try:
            response = requests.post('https://fyp-gpt-wr6verfzva-as.a.run.app', json=payload)
        except requests.exceptions.RequestException:
            return Response({'error': 'Failed to connect to OpenAI endpoint.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check if the request was successful
        if response.status_code != 200:
            return Response({'error': 'Failed to retrieve data from OpenAI endpoint.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Update the evidence instance with the new labels
        data = response.json()
        evidence.same_entity_label = data["same_entity_label"]
        evidence.same_entity_justification = data["same_entity_justification"]
        evidence.general_facts_label = data["general_facts_label"]
        evidence.general_facts_justification = data["general_facts_justification"]
        evidence.time_label = data["time_label"]
        evidence.time_justification = data["time_justification"]
        evidence.topic = data["topic"]
        evidence.claim_temporal = data["claim_temporal"]
        for i in range(len(evidence.claim_temporal)):
            # Remove single and double quotes
            evidence.claim_temporal[i] = re.sub(r"[\"']", "", evidence.claim_temporal[i])
            # Remove unnecessary whitespaces
            evidence.claim_temporal[i] = re.sub(r"\s+", " ", evidence.claim_temporal[i]).strip()
            # Remove spaces before punctuation
            evidence.claim_temporal[i] = re.sub(r"\s*([.,!?;:])", r"\1", evidence.claim_temporal[i])
        evidence.evidence_temporal = data["evidence_temporal"]
        for i in range(len(evidence.evidence_temporal)):
            # Remove single and double quotes
            evidence.evidence_temporal[i] = re.sub(r"[\"']", "", evidence.evidence_temporal[i])
            # Remove unnecessary whitespaces
            evidence.evidence_temporal[i] = re.sub(r"\s+", " ", evidence.evidence_temporal[i]).strip()
            # Remove spaces before punctuation
            evidence.evidence_temporal[i] = re.sub(r"\s*([.,!?;:])", r"\1", evidence.evidence_temporal[i])
        evidence.relevant_evidence = data["relevant_evidence"]
        for i in range(len(evidence.relevant_evidence)):
            # Remove single and double quotes
            evidence.relevant_evidence[i] = re.sub(r"[\"']", "", evidence.relevant_evidence[i])
            # Remove unnecessary whitespaces
            evidence.relevant_evidence[i] = re.sub(r"\s+", " ", evidence.relevant_evidence[i]).strip()
            # Remove spaces before punctuation
            evidence.relevant_evidence[i] = re.sub(r"\s*([.,!?;:])", r"\1", evidence.relevant_evidence[i])
        # Update model_label based on general_facts_label and time_label
        if evidence.general_facts_label == "REFUTES" or evidence.time_label == "REFUTES":
            evidence.model_label = "REFUTES"
        elif evidence.general_facts_label == "SUPPORTS" and evidence.time_label == "SUPPORTS":
            evidence.model_label = "SUPPORTS"
        else:
            evidence.model_label = "NOT ENOUGH INFO"
        evidence.save()

        # Return a response with the updated evidence data
        return Response({'claim_temporal': evidence.claim_temporal, 'evidence_temporal': evidence.evidence_temporal, 'evidence_relevant': evidence.relevant_evidence, 'topic': evidence.topic})

# Annotation
class CreateAnnotationAPIView(APIView):
    """This endpoint allows for creation of an annotation"""
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        claim = request.data.get('claimId')
        evidence = request.data.get('evidenceId')
        req_annotator_email = request.data.get('email')
        req_temporal_label = request.data.get('temporal_flag')
        req_general_label = request.data.get('general_flag')
        req_overall_label = request.data.get('overall_flag')
        getClaim = Claim.objects.get(id=claim)
        getEvidence = Evidence.objects.get(id=evidence)

        obj = Annotation(
        claim=getClaim,
        evidence=getEvidence,
        annotator_email=req_annotator_email,
        temporal_label=req_temporal_label,
        general_label=req_general_label,
        overall_label=req_overall_label
        )
        obj.save()
        # Get all annotations for the given evidence that are not ignored
        annotations = Annotation.objects.filter(evidence=getEvidence, ignore_flag=False)

        # Count the labels
        label_counts = annotations.values('overall_label').annotate(count=Count('overall_label'))

        label_counts_dict = {item['overall_label']: item['count'] for item in label_counts}

        # Iterate over the keys in the label count dictionary
        for key in label_counts_dict.keys():
            # Check if the key matches "NOT ENOUGH INFORMATION"
            if key == "NOT ENOUGH INFORMATION":
                # Update the dictionary with a new key "not enough info" and its corresponding value
                label_counts_dict["NOT ENOUGH INFO"] = label_counts_dict.pop(key)
                
        # Check majority label and update final_label if matches model_label, will update even if final label has been previously set.
        if getEvidence.model_label:
            if getEvidence.model_label in label_counts_dict:
                majority_label = [key for key, value in label_counts_dict.items() if value == max(label_counts_dict.values())]
                # In case there is a tie, do not update final label
                if len(majority_label) == 1 and majority_label[0] == getEvidence.model_label:
                    getEvidence.final_label = getEvidence.model_label
                    getEvidence.save()

        return Response({"id": obj.id})

class ListAnnotationAPIView(APIView):
    """This endpoint allows for listing of an annotation"""
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    serializer_class = AnnotationSerializer
    def get(self, request):
        databaseId = request.query_params.get('databaseId')
        databaseObj = Database.objects.get(id=databaseId)
        getClaims = Claim.objects.filter(database=databaseObj)
        annotations = Annotation.objects.filter(claim__in=getClaims)
        output = AnnotationSerializer(annotations, many=True)
        return JsonResponse(output.data, safe=False)

# Justification
class CreateJustificationAPIView(APIView):
    """This endpoint allows for creation of a justification"""
    # Disable administrator authentication and permission for annotation
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        req_annotation = request.data.get('annotation')
        req_temporal = request.data.get('temporal')
        req_claimPart = request.data.get('claimPart')
        req_justification = request.data.get('justification')
        getAnnotation = Annotation.objects.get(id=req_annotation)
        if (req_claimPart == False):   
            req_evidence = request.data.get('evidence')
            getEvidence = Evidence.objects.get(id=req_evidence)
            obj = Justification(
            annotation=getAnnotation,
            evidence=getEvidence, temporal=req_temporal,
            justification=req_justification
            )
            obj.save()
            return Response({"id": obj.id})
        else:
            obj = Justification(
            annotation=getAnnotation, temporal=req_temporal,
            justification=req_justification
            )
            obj.save()
            return Response({"id": obj.id})

class GetFirstReviewableAnnotation(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        databaseId = request.query_params.get('databaseId')
        database = get_object_or_404(Database, pk=databaseId)
        annotation = Annotation.objects.filter(
            Q(ignore_flag__isnull=True) | Q(ignore_flag=False),
            claim__database=database,
            evidence__final_label=None,
            evidence__manual_review=False,
        ).order_by("claim", "evidence").first()

        if annotation:
            claim = annotation.claim
            evidence = annotation.evidence
            claim_data = ClaimSerializer(claim).data
            evidence_data = EvidenceSerializer(evidence).data

            annotations_with_same_claim_evidence = Annotation.objects.filter(claim=claim, evidence=evidence, ignore_flag=False).annotate(
                total_count=Count("id", distinct=True),
                ignored_count=Count(Case(When(ignore_flag=True, then=1))),
                percentage_ignored=ExpressionWrapper(
                    100.0 * F("ignored_count") / F("total_count"), output_field=FloatField()
                ),
            )
            label_counts = annotations_with_same_claim_evidence.exclude(ignore_flag=True).values('overall_label').annotate(count=Count('overall_label')).order_by()
            label_counts_dict = {item['overall_label']: item['count'] for item in label_counts}

            for key in label_counts_dict.keys():
                if key == "NOT ENOUGH INFORMATION":
                    label_counts_dict["NOT ENOUGH INFO"] = label_counts_dict.pop(key)

            evidence_data["label_counts"] = label_counts_dict

            if evidence.model_label and evidence.final_label is None:
                majority_label = [key for key, value in label_counts_dict.items() if value == max(label_counts_dict.values())]
                if len(majority_label) == 1 and majority_label[0] == evidence.model_label:
                    evidence.final_label = evidence.model_label
                    evidence.save()
                else:
                    result = {
                        'claim': claim_data,
                        'evidence': evidence_data,
                        'annotations': list(annotations_with_same_claim_evidence.values())
                    }

                    return Response({'data': result})
            else:
                result = {
                    'claim': claim_data,
                    'evidence': evidence_data,
                    'annotations': list(annotations_with_same_claim_evidence.values())
                }

                return Response({'data': result})
        else:
            return Response({'data': None})

class IgnoreAnnotation(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        annotation_id = request.data.get('annotation_id')
        database_id = request.data.get('database_id')

        # Get the Annotation object using the provided primary key
        annotation = get_object_or_404(Annotation, pk=annotation_id)

        # Check if the annotation's claim belongs to the provided database
        if annotation.claim.database.id != database_id:
            return Response({'error': 'Invalid database_id'}, status=400)

        # Set the ignore_flag field to True
        annotation.ignore_flag = True
        annotation.save()

        return Response({'status': 'success'})

class IgnoreAnnotator(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        annotator_email = request.data.get('annotator_email')
        database_id = request.data.get('database_id')

        # Get the Database object using the provided primary key
        database = get_object_or_404(Database, pk=database_id)

        # Get the Claims related to this Database
        claims = Claim.objects.filter(database=database)

        # Filter Annotations with the provided annotator_email and related to the Claims within the Database
        annotations = Annotation.objects.filter(
            Q(claim__in=claims) & Q(annotator_email=annotator_email)
        )

        # Set the ignore_flag field to True for all filtered Annotations
        annotations.update(ignore_flag=True)

        return Response({'status': 'success'})

class UpdateFinalLabelView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        # Get the evidence_id and final_label from the POST request
        claim_id = request.data.get('claim_id')
        evidence_id = request.data.get('evidence_id')
        final_label = request.data.get('final_label')

        if not evidence_id or not final_label:
            return Response({'error': 'Both evidence_id and final_label are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the Evidence object using the provided evidence_id
        try:
            evidence = Evidence.objects.get(pk=evidence_id)
        except Evidence.DoesNotExist:
            return Response({'error': 'Evidence not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the final_label field in the Evidence model
        evidence.final_label = final_label.upper()
        evidence.manual_review = True

        # Validate and save the updated evidence object
        try:
            evidence.save()
            paraphrases = paraphrase(claim_id)
            if paraphrases == None:
                return Response({'error': 'Failed to get paraphrases.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'message': 'Final label updated successfully.', "paraphrases": paraphrases})
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def paraphrase(claimId):
    try:
        claim = Claim.objects.get(pk=claimId)
    except Claim.DoesNotExist:
        return Response({'error': f'Claimwith id {claimId} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if claim.is_paraphrased:
        paraphrases = claim.paraphrases.all().values_list('claim_content', flat=True)
        return list(paraphrases)

    # Prepare the claim and evidence JSON payload
    payload = {
        'sentence': claim.content
    }

    # Send the request to the OpenAI endpoint
    ### Fill in Google Cloud Function Endpoing here for Paraphrasing if required
    try:
        response = requests.post('', json=payload)
    except requests.exceptions.RequestException:
        return None
    # Check if the request was successful
    if response.status_code != 200:
        return None
    
    # Update the evidence instance with the new labels
    data = response.json()['generated_texts'][0]['content']
    removed_front = [sent[3:] for sent in data.split("\n")]
    # Loop through each paraphrase and create a ClaimParaphrases object
    for paraphrase in removed_front:
        ClaimParaphrases.objects.create(
            claim=claim,
            claim_content=paraphrase
        )

    claim.is_paraphrased = True
    claim.save()
    # Return paraphrases
    return removed_front

class ClaimEvidenceFinalLabelView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        claims_with_final_labels = (
            Claim.objects
            .annotate(evidence_with_final_label_count=Count('evidences', filter=Q(evidences__final_label__isnull=False)))
            .filter(evidence_with_final_label_count__gt=0)
        )

        serializer = ClaimEvidenceFinalLabelSerializer(claims_with_final_labels, many=True)
        return Response(serializer.data)


