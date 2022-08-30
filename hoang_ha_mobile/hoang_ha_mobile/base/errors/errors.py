from rest_framework import response, status

from comments.models import Comment
from variants.models import Variant
from django.db.models import Q

from .bases import return_code_400



def check_valid_item(items):
    if(len(items) < 1): 
        message = "Invalid data"
        return_code_400(message)
        # return response.Response(data={"Error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        
    for item in items:        
        if not (int(item.get('quantity')) > 0): 
            message = "Invalid quantity"
            return_code_400(message)
            # return response.Response(data={"Error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
            
        variant = Variant.objects.filter(id = item.get('variant'), status=True, deleted_by=None)
        if not(variant.exists()): 
            message = "Invalid data"
            return_code_400(message)
            # return response.Response(data={"Error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


def check_valid_comment(parent_id, variant_id):
    comment_instance = Comment.objects.filter(variant = variant_id, id = parent_id)
    if not(comment_instance.exists()):
        message = "Comment failed,Error: Different variant or comment parent, Can't create new instance"
        return_code_400(message)
        # return response.Response(data={"Error": "Comment failed,Error: Different variant or comment parent, Can't create new instance"}, status=status.HTTP_400_BAD_REQUEST)


def check_rating_exist(user_id, variant_id):
    rate = Comment.objects.filter(~Q(rating=0), created_by=user_id, variant=variant_id)
    if(rate.exists()):
        message = "Rating existed, Can't create new instance"
        return_code_400(message)
        # return response.Response(data={"Error": "Rating existed, Can't create new instance"}, status=status.HTTP_400_BAD_REQUEST)