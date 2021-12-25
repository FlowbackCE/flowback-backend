
from django.contrib import admin

from flowback.polls.models import Post, PostComment, PollProposal, Poll

# all registered model will show in admin panel
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Poll)
admin.site.register(PollProposal)
