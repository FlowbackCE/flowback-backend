from flowback.polls.models import Poll, PollProposal, PollProposalIndex, PollProposalEvent, PollProposalEventIndex, \
    PollProposalComments, PollProposalThreads, PollProposalEventComments, PollProposalEventThreads
from flowback.polls.serializer import PollProposalEventGetSerializer, PollProposalGetSerializer, \
    PollProposalIndexCreateSerializer, PollProposalEventIndexCreateSerializer, \
    CreateCounterProposalCommentSerializer, CreateCounterProposalEventCommentSerializer, \
    GetPollCounterProposalDetailsSerializer, GetPollCounterProposalEventDetailsSerializer, \
    PollProposalCommentsGetSerializer, PollProposalEventCommentsGetSerializer



class PollAdapter:
    def __init__(self, poll: Poll):
        self.poll = poll

        self.proposal = PollProposal
        self.proposal_get_serializer = PollProposalGetSerializer
        self.proposal_detail_serializer = GetPollCounterProposalDetailsSerializer
        self.index = PollProposalIndex
        self.index_create_serializer = PollProposalIndexCreateSerializer
        self.comments = PollProposalComments
        self.comment_create_serializer = CreateCounterProposalCommentSerializer
        self.comments_get_serializer = PollProposalCommentsGetSerializer
        self.threads = PollProposalThreads

        if poll.type == Poll.Type.EVENT:
            self.proposal = PollProposalEvent
            self.proposal_get_serializer = PollProposalEventGetSerializer
            self.proposal_detail_serializer = GetPollCounterProposalEventDetailsSerializer
            self.index = PollProposalEventIndex
            self.index_create_serializer = PollProposalEventIndexCreateSerializer
            self.comments = PollProposalEventComments
            self.comments_get_serializer = PollProposalEventCommentsGetSerializer
            self.comment_create_serializer = CreateCounterProposalEventCommentSerializer
            self.threads = PollProposalEventThreads
