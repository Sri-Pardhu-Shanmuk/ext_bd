from rest_framework.decorators import api_view

from rest_framework.response import Response

from django.contrib.auth.models import User

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import permission_classes

from rest_framework.permissions import IsAuthenticated

from .models import Transactions



@api_view(['POST'])
def register_user(req):

    username = req.data.get('username')

    password = req.data.get('password')



    if not username or not password:

        return Response(

            {
                "error":
                "Username and password required"
            },

            status=400
        )



    check_user = User.objects.filter(
        username=username
    ).exists()



    if check_user:

        return Response(

            {
                'error':
                'Username already exists'
            },

            status=400
        )



    user = User.objects.create_user(

        username=username,

        password=password
    )



    return Response(

        {
            'message':
            'User registered successfully'
        },

        status=201
    )







@api_view(['POST'])
def login_user(req):

    username = req.data.get('username')

    password = req.data.get('password')



    if not username or not password:

        return Response(

            {
                "error":
                "Username and password required"
            },

            status=400
        )



    user = authenticate(

        username=username,

        password=password
    )



    if user:

        refresh = RefreshToken.for_user(user)



        return Response(

            {

                "message":
                "Login successful",

                "refresh":
                str(refresh),

                "access":
                str(refresh.access_token),

                "username": username

            },

            status=200
        )



    return Response(

        {
            "message":
            "Invalid credentials"
        },

        status=401
    )








@api_view(['POST'])

@permission_classes([IsAuthenticated])

def add_transaction(req):

    try:

        title = req.data.get('title')

        category = req.data.get('category')

        date = req.data.get('date')

        amount = req.data.get('amount')

        type = req.data.get('type')



        if not title or not amount:

            return Response(

                {
                    "error":
                    "Required fields missing"
                },

                status=400
            )



        transaction = Transactions.objects.create(

            user=req.user,

            title=title,

            category=category,

            date=date,

            amount=amount,

            type=type
        )



        return Response(

            {
                "message":
                "Transaction added successfully",

                "id":
                transaction.id
            },

            status=201
        )



    except Exception as e:

        return Response(

            {
                "error":
                str(e)
            },

            status=500
        )









@api_view(['GET'])

@permission_classes([IsAuthenticated])

def get_transactions(req):

    transactions = Transactions.objects.filter(

        user=req.user

    ).order_by('-date')



    data = []



    for transaction in transactions:

        data.append({

            "id": transaction.id,

            "title": transaction.title,

            "category": transaction.category,

            "date": transaction.date,

            "amount": str(transaction.amount),

            "type": transaction.type

        })



    return Response(data)








@api_view(['DELETE'])

@permission_classes([IsAuthenticated])

def delete_transaction(req, id):

    try:

        transaction = Transactions.objects.get(

            id=id,

            user=req.user
        )



        transaction.delete()



        return Response(

            {
                "message":
                "Deleted successfully"
            }
        )



    except Transactions.DoesNotExist:

        return Response(

            {
                "error":
                "Transaction not found"
            },

            status=404
        )








@api_view(['PUT'])

@permission_classes([IsAuthenticated])

def update_transaction(req, id):

    try:

        transaction = Transactions.objects.get(

            id=id,

            user=req.user
        )



        title = req.data.get('title')

        category = req.data.get('category')

        date = req.data.get('date')

        amount = req.data.get('amount')

        type = req.data.get('type')



        transaction.title = title

        transaction.category = category

        transaction.date = date

        transaction.amount = amount

        transaction.type = type



        transaction.save()



        return Response(

            {
                "message":
                "Transaction updated successfully"
            },

            status=200
        )



    except Transactions.DoesNotExist:

        return Response(

            {
                "error":
                "Transaction not found"
            },

            status=404
        )



    except Exception as e:

        return Response(

            {
                "error":
                str(e)
            },

            status=500
        )