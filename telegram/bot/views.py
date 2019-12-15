from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class VerifiedTransactionsView(APIView):
    """
    GET:
    Get all the Verified Transactions
    """

    def get(self, request):
        v_t = VerifiedTransaction.objects.all()
        serializer = VerifiedTransactionSerializer(v_t, many=True)
        return Response({'data': serializer.data})

    """
    POST:
    Creator class
    ###Fileds should be sent:
        {
            'transaction': 123,     #Foreign Key to transaction.id
            'verified_sum': 40,
        }
    """

    def post(self, request):
        p = VerifiedTransactionCreateSerializer(data=request.data)
        if p.is_valid():
            p.save()
            return Response({'status': 'Added'})
        else:
            return Response(p.errors)


class TransactionsVerifiedView(APIView):
    """
    GET:
    Get all the Transactions (verified = True)
    """

    def get(self, request):
        t = Transaction.objects.filter(verified=True)
        serializer = TransactionSerializer(t, many=True)
        return Response({'data': serializer.data})


class TransactionsNotVerifiedView(APIView):
    """
    GET:
    Get all the Transactions (verified = False)
    """

    def get(self, request):
        t = Transaction.objects.filter(verified=False)
        serializer = TransactionSerializer(t, many=True)
        return Response({'data': serializer.data})

    """
    POST:
    Creator class
    ###Fileds should be sent:
        {
            'broker': 123,     #Foreign Key to user_id
            'type': 'P' or 'V',
            'sum': 40,
        }
    + image - ***Optional***
    + card - ***Optional***
    """

    def post(self, request):
        p = TransactionCreateSerializer(data=request.data)
        if p.is_valid():
            p.save()
            return Response({'status': 'Added'})
        else:
            return Response(p.errors)


class ProfilesView(APIView):
    """
    GET:
    Get all the Profiles
    """

    def get(self, request):
        t = Profile.objects.all()
        serializer = ProfileSerializer(t, many=True)
        return Response({'data': serializer.data})

    """
    POST:
    Creator class
    ###Fileds should be sent:
        {
            'user_id': 123,     #Foreign Key to user_id
        }
    + invited_by - ***Optional***
    + first_name - ***Optional***
    + last_name - ***Optional***
    + username - ***Optional***
    """

    def post(self, request):
        p = ProfileSerializer(data=request.data)
        if p.is_valid():
            p.save()
            return Response({'status': 'Added'})
        else:
            return Response({'status': 'Error'})
