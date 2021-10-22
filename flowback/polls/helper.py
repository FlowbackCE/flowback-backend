from flowback.polls.models import Poll, PollProposal, PollProposalIndex, PollProposalEvent, PollProposalEventIndex
from flowback.polls.serializer import PollProposalEventGetSerializer, PollProposalGetSerializer, \
    PollProposalIndexCreateSerializer, PollProposalEventIndexCreateSerializer


class PollAdapter:
    def __init__(self, poll: Poll):
        self.poll = poll

        self.proposal = PollProposal
        self.proposal_get_serializer = PollProposalGetSerializer
        self.index = PollProposalIndex
        self.index_create_serializer = PollProposalIndexCreateSerializer

        if poll.type == Poll.Type.EVENT:
            self.proposal = PollProposalEvent
            self.proposal_get_serializer = PollProposalEventGetSerializer
            self.index = PollProposalEventIndex
            self.index_create_serializer = PollProposalEventIndexCreateSerializer
