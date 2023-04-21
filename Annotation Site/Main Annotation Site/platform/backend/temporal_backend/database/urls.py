from django.urls import path
from database import views

urlpatterns = [
    path("",views.ListDatabaseAPIView.as_view(),name="database_list"),
    path("newdb/", views.CreateDatabaseClaimEvidenceTemporalAPIView.as_view(),name="create_new_db"),
    path("create/", views.CreateDatabaseAPIView.as_view(),name="database_create"),
    path("update/<int:pk>/",views.UpdateDatabaseAPIView.as_view(),name="update_database"),
    path("delete/<int:pk>/",views.DeleteDatabaseAPIView.as_view(),name="delete_database"),
    path("claims/create/", views.CreateClaimAPIView.as_view(),name="claim_create"),
    path("claims/list/", views.ListClaimAPIView.as_view(),name="claim_list_by_database"),
    path("claims/delete/<int:pk>/",views.DeleteClaimAPIView.as_view(),name="delete_claim"),
    path("evidence/create/", views.CreateEvidenceAPIView.as_view(),name="evidence_create"),
    path("evidence/updateGPT/<int:evidence_id>/", views.UpdateEvidenceAPIView.as_view(),name="evidence_update_gpt"),
    path("evidence/updateFinal/", views.UpdateFinalLabelView.as_view(),name="evidence_update_final"),
    path("annotation/check/", views.CheckAnnotationAPIView.as_view(),name="check_annotation"),
    path("annotation/get/", views.ListClaimWithEvidenceAPIView.as_view(),name="get_annotation"),
    path("annotation/add/", views.CreateAnnotationAPIView.as_view(),name="add_annotation"),
    path("annotation/add/justification/", views.CreateJustificationAPIView.as_view(),name="add_justification"),
    path("annotation/list/", views.ListAnnotationAPIView.as_view(),name="list_annotation"),
    path("annotation/list/review/", views.GetFirstReviewableAnnotation.as_view(),name="list_first_review_annotation"),
    path("annotation/ignore/", views.IgnoreAnnotation.as_view(),name="ignore_annotation"),
    path("annotation/ignoreall/", views.IgnoreAnnotator.as_view(),name="ignore_annotator"),
    path("annotation/final/", views.ClaimEvidenceFinalLabelView.as_view(),name="get_final_labels"),
]