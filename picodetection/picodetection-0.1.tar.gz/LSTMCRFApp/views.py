from django.shortcuts import render
# Create your views here.
from rest_framework import views,status
from rest_framework.response import Response
from .serializers import OutPutSerializer
import os
import json
from django.views.decorators.csrf import csrf_exempt
from lstm_crf.predict import main


class AllPredictionView(views.APIView):
    def __init__(self):
        # #print("intt........")
        pass

    def post(self, request):

        try:
            text = request.POST.get('text', False)
            if text == "" or text == False:
                jsonr = {'Output': "couldn't fetch  text"}
                return Response(OutPutSerializer(jsonr).data, status=status.HTTP_204_NO_CONTENT)                
        except Exception as e:

            jsonr = {'Output': "couldn't fetch any text"+str(e)}

            return Response(OutPutSerializer(jsonr).data, status=status.HTTP_400_BAD_REQUEST)

        try:
            prediction = main(text)
            jsonr = {"Output": prediction}
        except Exception as e:
            jsonr = {'Output': "Internal error==>"+str(e)}
            return Response(OutPutSerializer(jsonr).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(prediction, status=status.HTTP_200_OK)
    


