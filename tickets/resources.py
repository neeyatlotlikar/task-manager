from import_export import resources

from .models import SupportTicket


class SupportTicketResource(resources.ModelResource):
    start_date = None
    end_date = None

    class Meta:
        model = SupportTicket
        fields = (
            "id",
            "title",
            "status",
            "description",
            "assigned_to",
            "created_at",
        )

    def __init__(self, start_date=None, end_date=None, **kwargs):
        super().__init__(**kwargs)
        self.start_date = start_date
        self.end_date = end_date

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.start_date:
            queryset = queryset.filter(created_at__date__gte=self.start_date)

        if self.end_date:
            queryset = queryset.filter(created_at__date__lte=self.end_date)

        return queryset
