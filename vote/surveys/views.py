from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Survey
from .serializers import SurveySerializer, SurveyImageSerializer

# Create your views here.


class SurveyViewSet(viewsets.ModelViewSet):
    """Manage Survey in the databse."""
    serializer_class = SurveySerializer

    def get_queryset(self):
        return Survey.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'upload_image':
            return SurveyImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create new survey."""
        serializer.save()

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a survey."""
        survey = self.get_object()
        serializer = self.get_serializer(
            survey,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
