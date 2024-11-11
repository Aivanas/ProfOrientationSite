from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from StudyPlatform.models import *


class TestViewSet(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestsSerializer
    permission_classes = (IsAuthenticated,)


class UsersViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated,)


class TestQuestionsViewSet(generics.ListAPIView):
    serializer_class = TestQuestionsSerializer
    def get_queryset(self):
        test_id = self.kwargs['test_id']
        return Question.objects.filter(test_id=test_id)
    permission_classes = (IsAuthenticated,)

