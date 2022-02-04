from itertools import groupby

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from flowback.polls.helper import PollAdapter
from flowback.polls.models import Poll, PollProposal

# Save data as json
# Poll (id, title, description, total_participants, votes_counted, success, top_proposal, date)
# Proposal (id, title, description, final_score_positive, final_score_negative)
# Vote (user{id, proposal_id, proposal_date}, score, is_positive)

def create_poll_reciept(
        *,
        poll: int
):
    poll = get_object_or_404(Poll, id=poll)
    proposals = PollProposal.objects.filter(poll=poll)

    adapter = PollAdapter(poll)
    indexes = adapter.index.objects.filter(proposal__poll=poll).all()
    indexes = groupby(indexes, lambda x: x.proposal.id)

    final_result = dict(
        poll=poll.id,
        title=poll.title,
        description=poll.description,
        total_participants=poll.total_participants,
        votes_counted=poll.votes_counted,
        success=poll.success,
        top_proposal=poll.top_proposal,
        date=poll.created_at,
        proposals=dict()
    )

    # Poll (id, title, description, total_participants, votes_counted, success, top_proposal, date)
    class PollSerializer(serializers.ModelSerializer):
        class Meta:
            model = Poll
            fields = (
                'id', 'title', 'description', 'total_participants',
                'votes_counted', 'success', 'top_proposal', 'created_at'
            )

    # Proposal (id, title, description, final_score_positive, final_score_negative)
    class ProposalSerializer(serializers.ModelSerializer):
        class Meta:
            model = PollProposal
            fields = ('id', 'title', 'description', 'final_score_positive', 'final_score_negative', 'created_at')

    # Vote (user{id, proposal_id, proposal_date}, score, is_positive)
    class VoteSerializer(serializers.ModelSerializer):
        class Meta:
            model = adapter.index
            fields = ('user', 'score', 'is_positive', 'created_at')

    for proposal in proposals:
        proposal =