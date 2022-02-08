from django.shortcuts import get_object_or_404
from rest_framework import serializers

from flowback.polls.helper import PollAdapter
from flowback.polls.models import Poll, PollProposal


def create_poll_receipt(
        *,
        poll: int
):
    poll = get_object_or_404(Poll, id=poll)
    adapter = PollAdapter(poll)

    class VoteSerializer(serializers.ModelSerializer):
        score = serializers.IntegerField(source='priority')

        class Meta:
            model = adapter.index
            fields = ('user', 'score', 'is_positive', 'created_at')

    class ProposalSerializer(serializers.ModelSerializer):
        votes = serializers.SerializerMethodField()

        class Meta:
            model = PollProposal
            fields = (
                'id', 'title', 'description', 'final_score_positive',
                'final_score_negative', 'created_at', 'file', 'votes'
            )

        def get_votes(self, obj):
            data = adapter.index.objects.filter(proposal=obj).all()
            return VoteSerializer(data, many=True)

    class PollSerializer(serializers.ModelSerializer):
        proposals = serializers.SerializerMethodField()

        class Meta:
            model = Poll
            fields = (
                'id', 'title', 'description', 'total_participants', 'files',
                'votes_counted', 'success', 'top_proposal', 'created_at', 'proposals'
            )

        def get_proposals(self, obj):
            data = PollProposal.objects.filter(poll=obj).all()
            return ProposalSerializer(data, many=True)

    return PollSerializer(poll)
