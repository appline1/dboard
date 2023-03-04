

rest_framework import serializers

from .models import *

class PersonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Person
        fields= '__all__'

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ProgrammingLanguage
        fields= '__all__'


class ProgrammingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Programming
        fields= '__all__'
class ProgrammingTaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ProgrammingTask
        fields= '__all__'
        
class ProgrammingTaskDoneSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ProgrammingTaskDone
        fields= '__all__'

class BankAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=BankAccount
        fields= '__all__'

class InviteeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Invitee
        fields= '__all__'
        
class DigitalLiteracyTaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=DigitalLiteracyTask
        fields= '__all__'

class DigitalLiteracyTaskDoneSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=DigitalLiteracyTaskDone
        fields= '__all__'

class PointSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Point
        fields= '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Budget
        fields= '__all__'

class WithdrawalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Withdrawal
        fields= '__all__'