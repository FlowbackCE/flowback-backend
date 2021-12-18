# FlowBack was created and project lead by Loke Hagberg. The design was
# made by Lina Forsberg. Emilio Müller helped constructing Flowback.
# Astroneatech created the code. It was primarily financed by David
# Madsen. It is a decision making platform.
# Copyright (C) 2021  Astroneatech AB
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

import datetime

from rest_framework import serializers

from flowback.users.models import User, Group, OnboardUser, GroupRequest
from flowback.polls.models import Poll, PollDocs, PollVotes, PollComments, PollBookmark, PollProposal,\
    PollProposalIndex, PollProposalEventIndex, \
    PollProposalEvent, PollProposalComments, PollProposalThreads, PollProposalEventComments, PollProposalEventThreads, PollUserDelegate
from flowback.users.serializer import SimpleUserSerializer, PollCommentUserSerializer


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class GroupPollCreateSerializer(serializers.ModelSerializer):
    type = ChoiceField(choices=Poll.Type.choices)

    def to_internal_value(self, data):
        if data.get('type', None) == '':
            data['type'] = 'poll'
        return super(GroupPollCreateSerializer, self).to_internal_value(data)

    class Meta:
        model = Poll
        fields = ('group', 'title', 'description', 'type', 'end_time')


class GroupPollUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('title', 'description', 'end_time')


class GroupPollDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollDocs
        fields = ('id', 'file')


class GroupDetailPollListSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'title', 'image', 'user_type')

    def get_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user

    def get_user_type(self, obj):
        user = self.get_user()
        if user in obj.owners.all():
            return "Owner"
        elif user in obj.admins.all():
            return "Admin"
        elif user in obj.moderators.all():
            return "Moderator"
        elif user in obj.members.all():
            return "Member"
        elif user in obj.delegators.all():
            return "Delegator"
        else:
            return ""


class GetGroupPollsListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    files = GroupPollDocsSerializer(read_only=True, many=True)
    group = serializers.SerializerMethodField('get_group_details')
    # group = GroupDetailPollListSerializer()
    created_by = SimpleUserSerializer(read_only=True)
    comments_details = serializers.SerializerMethodField()
    discussion = serializers.SerializerMethodField()
    voting_status = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ('id', 'group', 'title', 'description', 'tags', 'files', 'accepted', 'accepted_at',
                  'end_time', 'created_at', 'created_by', 'comments_details', 'discussion', 'voting_status')

    def get_group_details(self, obj):
        grp_serializers = GroupDetailPollListSerializer(obj.group, context={'request': self.context.get("request")})
        return grp_serializers.data

    def get_comments_details(self, obj):
        poll_comments = PollComments.objects.filter(poll=obj).order_by('-created_at')
        serializer = GetPollCommentsSerializer(poll_comments, many=True, context={'request': self.context.get("request")})
        data = dict()
        data['comments'] = serializer.data
        data['total_comments'] = len(poll_comments)
        return data

    def get_tags(self, obj):
        return obj.tag.names()

    def get_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user

    def get_discussion(self, obj):
        if obj.end_time > datetime.datetime.now():
            return "In progress"
        return "Finished"

    def get_voting_status(self, obj):
        user = self.get_user()
        if user.id is None:
            return ""
        vote = PollVotes.objects.filter(poll=obj, user=user).first()
        if vote:
            return vote.vote_type
        return ""


class DelegatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollUserDelegate
        fields = ('user_id', 'group_id', 'delegate_user_id')


class SearchPollSerializer(serializers.ModelSerializer):
    # group = GroupDetailPollListSerializer()
    group = serializers.SerializerMethodField('get_group_details')

    class Meta:
        model = Poll
        fields = ('id', 'title', 'description', 'group', 'created_at')

    def get_group_details(self, obj):
        grp_serializers = GroupDetailPollListSerializer(obj.group, context={'request': self.context.get("request")})
        return grp_serializers.data


class GetBookmarkPollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollBookmark
        fields = ('id', 'poll')
        depth = 1


class GroupPollDetailsSerializer(serializers.ModelSerializer):
    vote_details = serializers.SerializerMethodField()
    files = GroupPollDocsSerializer(read_only=True, many=True)
    tags = serializers.SerializerMethodField()
    voting_status = serializers.SerializerMethodField()
    created_by = SimpleUserSerializer()
    modified_by = SimpleUserSerializer()
    discussion = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    comments_details = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField('get_group_details')


    class Meta:
        model = Poll
        fields = ('id', 'group', 'user_type', 'title', 'description', 'tags', 'files', 'accepted', 'accepted_at', 'end_time',
                  'created_at', 'modified_at', 'created_by', 'modified_by', 'vote_details', "voting_status", "discussion",
                  'comments_details')

    def get_group_details(self, obj):
        grp_serializers = GroupDetailPollListSerializer(obj.group, context={'request': self.context.get("request")})
        return grp_serializers.data

    def get_discussion(self, obj):
        if obj.end_time > datetime.datetime.now():
            return "In progress"
        return "Finished"

    def get_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user

    def get_user_type(self, obj):
        user = self.get_user()
        if user in obj.group.owners.all():
            return "Owner"
        elif user in obj.group.admins.all():
            return "Admin"
        elif user in obj.group.moderators.all():
            return "Moderator"
        elif user in obj.group.members.all():
            return "Member"
        elif user in obj.group.delegators.all():
            return "Delegator"
        else:
            return ""

    def get_tags(self, obj):
        return obj.tag.names()

    def get_vote_details(self, obj):
        poll_votes = PollVotes.objects.filter(poll=obj)
        total_vote_done = len(poll_votes)
        total_yes = total_no = total_voters = 0
        if total_vote_done:
            total_yes = len(poll_votes.filter(vote_type='upvote'))
            total_no = len(poll_votes.filter(vote_type='downvote'))
        total_voters = len(obj.group.owners.all()) + len(obj.group.admins.all()) + len(obj.group.moderators.all()) + \
                           len(obj.group.members.all())
        total_yes_percentage = total_no_percentage = reached_yes_percentage = reached_no_percentage = 0
        if total_vote_done:
            total_yes_percentage = (total_yes * 100) / total_vote_done
            total_no_percentage = (total_no * 100) / total_vote_done
            reached_yes_percentage = (total_yes * 100) / total_voters
            reached_no_percentage = (total_no * 100) / total_voters

        vote_details = {
            "yes": total_yes,
            "no": total_no,
            "total_voters": total_voters,
            "yes_percentage": total_yes_percentage,
            "no_percentage": total_no_percentage,
            "reached_yes_percentage": reached_yes_percentage,
            "reached_no_percentage": reached_no_percentage,
            "reached": total_vote_done,
        }
        return vote_details

    def get_voting_status(self, obj):
        user = self.get_user()
        vote = PollVotes.objects.filter(poll=obj, user=user).first()
        if vote:
            return vote.vote_type
        return ""

    def get_comments_details(self, obj):
        poll_comments = PollComments.objects.filter(poll=obj).order_by('-created_at')
        serializer = GetPollCommentsSerializer(poll_comments, many=True, context={'request': self.context.get("request")})
        data = dict()
        data['comments'] = serializer.data
        data['total_comments'] = len(poll_comments)
        return data


class GetPendingPollListSerializer(serializers.ModelSerializer):
    discussion = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ('id', 'group', 'title', 'description', 'accepted', 'accepted_at', 'start_time', 'end_time', 'created_by',
                  'modified_by', 'discussion', 'voting_status')

    def get_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user

    def get_discussion(self, obj):
        if obj.end_time > datetime.datetime.now():
            return "In progress"
        return "Finished"

    def get_voting_status(self, obj):
        user = self.get_user()
        vote = PollVotes.objects.filter(poll=obj, user=user).first()
        if vote:
            return vote.vote_type
        return ""


class CreatePollCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollComments
        fields = ('comment', 'poll', 'reply_to')


class GetPollCommentsSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    created_by = PollCommentUserSerializer()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = PollComments
        fields = ('id', 'comment', 'poll', 'reply_to', 'edited', 'likes', 'created_by', 'modified_by', 'created_at',
                  'modified_at', 'likes_count', 'liked')

    def get_likes_count(self, obj):
        return len(obj.likes.all())

    def get_liked(self, obj):
        request = self.context.get("request")
        if request.user in obj.likes.all():
            return True
        return False


# Poll Proposals
class PollProposalCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollProposal
        fields = ('poll', 'proposal', 'file')


class PollProposalEventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollProposalEvent
        fields = ('poll', 'proposal', 'date')

    def validate_poll(self, obj):
        if not obj.type == Poll.Type.EVENT:
            raise serializers.ValidationError(detail='Poll is not an Event.')

        return obj

    def validate_date(self, obj):
        if not (obj.minute % 5 == 0 and obj.second == 0 and obj.microsecond == 0):
            raise serializers.ValidationError(detail='Date needs to be in 5 minute increments.')

        return obj


class PollProposalGetSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    comments_details = serializers.SerializerMethodField()

    class Meta:
        model = PollProposal
        fields = ('id', 'poll', 'proposal', 'user', 'file', 'final_score', 'created_at', 'comments_details')

    def get_comments_details(self, obj):
        proposal_comments = PollProposalComments.objects.filter(counter_proposal=obj).order_by(
            '-created_at')
        serializer = PollProposalCommentsGetSerializer(proposal_comments, many=True,
                                                       context={'request': self.context.get("request")})
        data = dict()
        data['comments'] = serializer.data
        data['total_comments'] = len(proposal_comments)
        return data


class PollProposalEventGetSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    comments_details = serializers.SerializerMethodField()

    class Meta:
        model = PollProposalEvent
        fields = ('id', 'poll', 'proposal', 'date', 'user', 'final_score', 'created_at', 'comments_details')

    # TODO Add Comment Support For Events
    def get_comments_details(self, obj):
        proposal_comments = PollProposalComments.objects.filter(counter_proposal=obj).order_by(
            '-created_at')
        serializer = PollProposalCommentsGetSerializer(proposal_comments, many=True,
                                                       context={'request': self.context.get("request")})
        data = dict()
        data['comments'] = serializer.data
        data['total_comments'] = len(proposal_comments)
        return data

# TODO Check if user is in proposal group
class PollProposalIndexCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollProposalIndex
        fields = ('proposal', 'user', 'priority', 'is_positive')

    def get_unique_together_validators(self):
        return []


class PollProposalEventIndexCreateSerializer(serializers.ModelSerializer):
    poll = GroupPollDetailsSerializer(read_only=True)

    class Meta:
        model = PollProposalEventIndex
        fields = ('proposal', 'user', 'priority', 'is_positive')

    def get_unique_together_validators(self):
        return []


class PollProposalCommentsGetSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    created_by = PollCommentUserSerializer()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = PollProposalComments
        fields = ('id', 'comment', 'counter_proposal', 'reply_to', 'edited', 'likes', 'created_by', 'modified_by', 'created_at',
                  'modified_at', 'likes_count', 'liked')

    def get_likes_count(self, obj):
        return len(obj.likes.all())

    def get_liked(self, obj):
        request = self.context.get("request")
        if request.user in obj.likes.all():
            return True
        return False


class PollProposalEventCommentsGetSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    created_by = PollCommentUserSerializer()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = PollProposalEventComments
        fields = ('id', 'comment', 'counter_proposal', 'reply_to', 'edited', 'likes', 'created_by', 'modified_by', 'created_at',
                  'modified_at', 'likes_count', 'liked')

    def get_likes_count(self, obj):
        return len(obj.likes.all())

    def get_liked(self, obj):
        request = self.context.get("request")
        if request.user in obj.likes.all():
            return True
        return False



class GetPollCounterProposalDetailsSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    comments_details = serializers.SerializerMethodField()

    class Meta:
        model = PollProposal
        fields = ('id', 'poll', 'proposal', 'user', 'file', 'final_score', 'created_at', 'comments_details')

    def get_comments_details(self, obj):
        counter_proposal_comments = PollProposalComments.objects.filter(counter_proposal=obj).order_by('-created_at')
        serializer = PollProposalCommentsGetSerializer(counter_proposal_comments, many=True, context={'request': self.context.get("request")})
        data = dict()
        data['comments'] = serializer.data
        data['total_comments'] = len(counter_proposal_comments)
        return data


class GetPollCounterProposalEventDetailsSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    comments_details = serializers.SerializerMethodField()

    class Meta:
        model = PollProposalEvent
        fields = ('id', 'poll', 'proposal', 'date', 'user', 'file', 'final_score', 'created_at', 'comments_details')

    def get_comments_details(self, obj):
        counter_proposal_comments = PollProposalComments.objects.filter(counter_proposal=obj).order_by('-created_at')
        serializer = PollProposalCommentsGetSerializer(counter_proposal_comments, many=True, context={'request': self.context.get("request")})
        data = dict()
        data['comments'] = serializer.data
        data['total_comments'] = len(counter_proposal_comments)
        return data


class CreateCounterProposalCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollProposalComments
        fields = ('comment', 'counter_proposal', 'reply_to')


class CreateCounterProposalEventCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollProposalEventComments
        fields = ('comment', 'counter_proposal', 'reply_to')
