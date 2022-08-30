from rest_framework import response, status


def return_code_400(message):
    data = {
        "message": message
    }
    
    return response.Response(data=data, status=status.HTTP_400_BAD_REQUEST)


def exception_stripe_message(e):
    print(e)
    message = str(e)[(str(e).find(":", 0, len(str(e))))+2: len(str(e))]
    return message