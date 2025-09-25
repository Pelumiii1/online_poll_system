from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializer import PollSerializer,VoteSerializer
from .models import Poll
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsOwnerOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

class PollListCreateView(generics.ListCreateAPIView):
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Poll.objects.filter(is_active=True).select_related('created_by')
    
    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)
        
class UserPollListView(generics.ListAPIView):
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Poll.objects.filter(created_by=self.request.user)
    
class PollDeleteView(generics.DestroyAPIView):
    queryset = Poll.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        
class PollDetailsView(generics.RetrieveUpdateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsOwnerOrReadOnly]

        
@extend_schema(
    request=None,
    responses={
        200: OpenApiResponse(
            description="Visibility toggled successfully",
            examples=[{"result_visibility": "private"}]
        ),
        403: OpenApiResponse(description="Not authorized"),
        404: OpenApiResponse(description="Poll not found"),
    },
    description="Toggle poll result visibility between public and private"
)        
@api_view(["PATCH"])
@permission_classes([IsOwnerOrReadOnly])
def toogle_poll_visibility(request,pk):
    poll = get_object_or_404(Poll, pk=pk)
    
    if poll.created_by != request.user:
        return Response(
            {"error":"You do not have permission to modify this poll."},
            status=status.HTTP_403_FORBIDDEN
        )
    poll.result_visibility == 'private' if poll.result_visibility == 'public' else 'public'
    poll.save()
    return Response({"result_visibility":poll.result_visibility}, status=status.HTTP_200_OK)


class PollResultView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    
    def retrieve(self, request, *args, **kwargs):
        poll = self.get_object()
        
        if poll.result_visibility == 'private' and poll.created_by != request.user:
            return Response(
                {'error': "Results are not public"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not poll.is_expired and poll.result_visiblity == "public":
            return Response(
                {'error':'Results are not available until the poll expires'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = self.get_serializer(poll)
        return Response(serializer.data)
    
class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)