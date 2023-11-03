from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from api.utils import load_data_from_dataframe
from api.serializers import UploadFileSerializer
from openpyxl import load_workbook
from io import BytesIO
from django.utils import timezone
from api.models import TourURL
from django.core.files.storage import default_storage
from score_review.tasks import process_file_upload


class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_serializer = UploadFileSerializer(data=request.data)

        if file_serializer.is_valid():
            file = file_serializer.validated_data['file']
            file_path = default_storage.save('uploads/myfile.xlsx', file)
            print(file_path)
            process_file_upload.delay(file_path)
            return Response(status=201)

        else:
            return Response(file_serializer.errors, status=400)
