from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task, Benefactor, Charity
from charities.serializers import (
    TaskSerializer,
    CharitySerializer,
    BenefactorSerializer,
)


class BenefactorRegistration(APIView):
    queryset = Benefactor.objects.all()
    serializer_class = BenefactorSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def save(self, **kwargs):
    #     """
    #     kwargs should contain `user` object
    #     it should be evaluated from AuthToken
    #     """
    #     user = kwargs.get('user')
    #     assert user is not None, "`user` is None"
    #     return super().save(user=user)


class CharityRegistration(APIView):
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Tasks(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def post(self, request, *args, **kwargs):
        data = {**request.data, "charity_id": request.user.charity.id}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [
                IsAuthenticated,
            ]
        else:
            self.permission_classes = [
                IsCharityOwner,
            ]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)


class TaskRequest(APIView):
    permission_classes = [
        IsBenefactor,
    ]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if task.state != Task.TaskStatus.PENDING:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "This task is not pending."},
            )
        task.assign_to_benefactor(request.user.benefactor)
        return Response(status=status.HTTP_200_OK, data={"detail": "Request sent."})


class TaskResponse(APIView):
    permission_classes = [
        IsCharityOwner,
    ]

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        response_task = request.POST.get('response')
        
        if response_task not in ['A', 'R']:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'detail': 'Required field ("A" for accepted / "R" for rejected)'},
            )
        if task.state != Task.TaskStatus.WAITING:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'detail': 'This task is not waiting.'},
            )
            
        task.response_to_benefactor_request(response_task)
        return Response(
                status=status.HTTP_200_OK,
                data={'detail': 'Response sent.'},
            ) 


class DoneTask(APIView):
    pass
