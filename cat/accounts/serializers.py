from rest_framework import serializers
from .models import Accounts


class AccountsSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Accounts
        fields = (
            "id",
            "name",
            "surname",
            "email",
            "createdAt",
            "updatedAt",
        )

        read_only_fields = [
            "id",
            "createdAt",
            "updatedAt",
        ]
