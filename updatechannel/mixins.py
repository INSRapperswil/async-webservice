from updatechannel.consumers import UpdateChannelConsumer


class CreateModelNotifyMixin:

    """ A mixin for views to announce creation of objects. """

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        model = self.get_serializer().Meta.model
        UpdateChannelConsumer.send_update_message({
            'event': 'model-created',
            'model': model.__name__,
            'data': response.data
        })
        return response


class DestroyModelNotifyMixin:

    """ A mixin for views to announce deletion of objects. """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = super().destroy(request, *args, **kwargs)
        UpdateChannelConsumer.send_update_message({
            'event': 'model-deleted',
            'model': instance.__class__.__name__,
            'data': serializer.data
        })
        return response


class UpdateModelNotifyMixin:

    """ A mixin for views to announce changes of objects. """

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        model = self.get_serializer().Meta.model
        UpdateChannelConsumer.send_update_message({
            'event': 'model-updated',
            'model': model.__name__,
            'data': response.data
        })
        return response


class NotifyMixin(CreateModelNotifyMixin, DestroyModelNotifyMixin, UpdateModelNotifyMixin):

    pass
