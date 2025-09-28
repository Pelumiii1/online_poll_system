from rest_framework import serializers
from .models import Poll, Option, Vote
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name='MCQ Poll Example',
            summary='Multiple Choice Question Poll',
            description='Example of creating a multiple choice poll with options',
            value={
                'question': 'What is your favorite programming language?',
                'poll_type': 'mcq',
                'duration': 24,
                'result_visibility': 'public',
                'options': [
                    {'text': 'Python'},
                    {'text': 'JavaScript'},
                    {'text': 'Java'}
                ]
            }
        ),
        OpenApiExample(
            name='True/False Poll Example',
            summary='True/False Poll',
            description='Example of creating a true/false poll',
            value={
                'question': 'Is Django a Python web framework?',
                'poll_type': 'tf',
                'duration': 48,
                'result_visibility': 'private'
            }
        ),
        OpenApiExample(
            name='Comment Poll Example',
            summary='Comment-based Poll',
            description='Example of creating a comment-based poll',
            value={
                'question': 'What features would you like to see?',
                'poll_type': 'comment',
                'duration': 72,
                'result_visibility': 'public'
            }
        )
    ]
)
        
class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    created_by = serializers.ReadOnlyField(source='created_by.email')
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = Poll
        fields = ['id', 'question', 'poll_type', 'duration', 'created_by', 'created_at', 'result_visibility', 'options', "is_active", "is_expired"]
        read_only_fields = ['created_at', 'is_expired', 'created_by']
        
    def validate(self, data):
        poll_type = data.get('poll_type')
        options = self.initial_data.get("options",[])
        
        if(poll_type) == 'mcq' and len(options) < 2:
            raise serializers.ValidationError("MCQ Poll must have at least 2 options.")
        
        if poll_type == 'tf' and len(options) != 2:
            raise serializers.ValidationError('True/False polls must have exactly 2 options.')
        
        if poll_type == 'comment' and options:
            raise serializers.ValidationError('Comment polls cannot have options.')
        
        return data
    
    def create(self, validated_data):
        options_data = validated_data.pop("options")
        poll = Poll.objects.create(**validated_data)
        
        if poll.poll_type == 'tf':
            Option.objects.create(poll=poll, text="True")
            Option.objects.create(poll=poll, text="False")
            
        elif poll.poll_type == 'mcq':
            for option_data in options_data:
                Option.objects.create(poll=poll, **option_data)
                
        return poll
    
    def update(self, instance, validated_data):
       options_data = validated_data.pop('options',None)
       instance = super().update(instance, validated_data)
       
       if options_data is not None and instance.poll_type == 'mcq':
           instance.options.all().delete()
           for option_data in options_data:
               Option.objects.create(poll=instance, **option_data)
       return instance

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'poll', 'option', 'comment', 'voted_at']
        read_only_fields = ['voted_at']
    
    def validate(self, data):
        poll = data['poll']
        option = data.get('option')
        comment = data.get('comment')
        
        # Validate based on poll type
        if poll.poll_type == 'mcq' or poll.poll_type == 'tf':
            if not option:
                raise serializers.ValidationError("Option is required for this poll type.")
            if comment:
                raise serializers.ValidationError("Comments are not allowed for this poll type.")
            if option.poll != poll:
                raise serializers.ValidationError("Selected option does not belong to this poll.")
        
        if poll.poll_type == 'comment':
            if option:
                raise serializers.ValidationError("Options are not allowed for comment polls.")
            if not comment:
                raise serializers.ValidationError("Comment is required for this poll type.")
        
        # Check if user already voted
        if Vote.objects.filter(user=self.context['request'].user, poll=poll).exists():
            raise serializers.ValidationError("You have already voted on this poll.")
        
        # Check if poll is expired
        if poll.is_expired:
            raise serializers.ValidationError("This poll has expired.")
        
        return data


class PollResultSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()
    
    class Meta:
        model = Poll
        fields = ['id', 'question', 'poll_type', 'total_votes', 'options']
    
    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_options(self, obj):
        if obj.poll_type == 'comment':
            return []
        
        options = obj.options.all()
        results = []
        for option in options:
            vote_count = Vote.objects.filter(poll=obj, option=option).count()
            results.append({
                'id': option.id,
                'text': option.text,
                'vote_count': vote_count
            })
        return results
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_total_votes(self, obj):
        return Vote.objects.filter(poll=obj).count()
        