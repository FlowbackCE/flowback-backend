from django.urls import path, include

from flowback.notifications.views import (
    NotificationListApi,
    NotificationSubscriptionsApi,
    NotificationSubscribedApi,
    NotificationUpdateApi,
    NotificationSubscribeApi,
    NotificationUnsubscribeApi
)

notification_patterns = [
    path('', NotificationListApi.as_view(), name='list'),
    path('subscriptions/', NotificationSubscriptionsApi.as_view(), name='subscriptions'),
    path('subscribed/', NotificationSubscribedApi.as_view(), name='subscribed'),
    path('<int:notification_id>/update/', NotificationUpdateApi.as_view(), name='update'),
    path('subscribe/', NotificationSubscribeApi.as_view(), name='subscribe'),
    path('unsubscribe', NotificationUnsubscribeApi.as_view(), name='unsubscribe')
]

urlpatterns = [
    path('notifications/', include((notification_patterns, 'notifications')))
]
