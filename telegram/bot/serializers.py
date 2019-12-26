from rest_framework import serializers

from .models import *


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('invited_by', 'user_id', 'first_name', 'last_name', 'username', 'balance')


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('invited_by', 'first_name', 'last_name', 'username')


class InvitedBySerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username')


class TransactionSerializer(serializers.ModelSerializer):
    broker = ProfileSerializer()

    class Meta:
        model = Transaction
        fields = ('broker', 'card', 'type', 'verified', 'sum', 'image', 'pub_date')


class TransactionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('broker', 'card', 'type', 'sum', 'image', 'details', 'pub_date')


class VerifiedTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()

    class Meta:
        model = VerifiedTransaction
        fields = ('transaction', 'verified_sum', 'pub_date')


class VerifiedTransactionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerifiedTransaction
        fields = ('transaction', 'verified_sum')


