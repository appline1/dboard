from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from django.contrib.auth.models import User


class Person(User):
    phone = models.IntegerField()
    state=models.CharField(max_length=50)
    lga=models.CharField(max_length=50)
    # programmingLanguage= models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='person_programming_language')
    github = models.URLField(max_length=200)
    # bankDetail=models.ForeignKey(BankAccount,on_delete=models.CASCADE, related_name='person_bankdetails')
    
    def __str__(self):
        return self.username
        
class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Programming(models.Model):
    person=models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_programming_language')
    programmingLanguage=models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='person_programminglanguage')
    # name=models.CharField(max_length=50)
    programmingLanguageYearsOfExperience=models.IntegerField()
    
    def __str__(self):
        return self.programmingLanguage.name
        
class BankAccount(models.Model):
    person=models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_bankaccount')
    bank=models.CharField(max_length=50)
    nameOnAcct=models.CharField(max_length=100)
    acctNo=models.CharField(max_length=15)
    
    def __str__(self):
        return self.acctName


        
class ProgrammingTask(models.Model):
    person=models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_programming_languageTask')
    programmingLanguage= ChainedForeignKey(Programming,
        chained_field="person",
        chained_model_field="person",
        show_all=False, 
        auto_choose=True, 
        sort=True
        )
    # programmingLanguage=models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='task_programming_language')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    def __str__(self):
        return self.title
    
class ProgrammingTaskDone(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE, related_name='person_programming_languageTaskDone')
    programmingLanguage= ChainedForeignKey(Programming,
        chained_field="person",
        chained_model_field="person",
        show_all=False, 
        auto_choose=True, 
        sort=True
        )
    task= ChainedForeignKey(ProgrammingTask,
        chained_field="person",
        chained_model_field="person",
        show_all=False, 
        auto_choose=True, 
        sort=True
        )
    # task =models.ForeignKey(ProgrammingTask, on_delete=models.CASCADE, related_name='programming_task_done')
    taskIsDone=models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.task.title} {self.taskIsDone}'
    
        
class Invitee(models.Model):
    invited_by = models.ForeignKey(Person, on_delete = models.CASCADE,related_name='invited_by')
    fullname=models.CharField(max_length=200)
    email=models.EmailField()
    phone = models.IntegerField()
    
    programmingLanguage=models.ForeignKey(ProgrammingLanguage,on_delete=models.CASCADE, related_name='invitee_programming_language')
    def __str__(self):
        return self.fullname
        
class DigitalLiteracyTask(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE, related_name='personDigitalLiteracyTask')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    def __str__(self):
        return self.title
    
class DigitalLiteracyTaskDone(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    task= ChainedForeignKey(DigitalLiteracyTask,
        chained_field="person",
        chained_model_field="person",
        show_all=False, 
        auto_choose=True, 
        sort=True
        )
    # task =models.ForeignKey(DigitalLiteracyTask, on_delete=models.CASCADE, related_name='digital_literacy_task_done')
    invitee= ChainedForeignKey(Invitee,
        chained_field="person",
        chained_model_field="invited_by",
        show_all=False, 
        auto_choose=True, 
        sort=True
        )
    # invite =models.ForeignKey(Invitee, on_delete=models.CASCADE, related_name='digital_literacy_invitee')
    taskIsDone=models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.task.title} {self.taskIsDone}'
    

class Point(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_point')
    
    programingTaskDone= ChainedForeignKey(ProgrammingTaskDone,
        chained_field="person",
        chained_model_field="person",
        show_all=False, 
        auto_choose=True, 
        sort=True, null=False
        )
    # programingTaskDone=models.ForeignKey(ProgrammingTaskDone,on_delete=models.CASCADE, related_name='programming_task_done_point')
    digitalLiteracyTaskDone= ChainedForeignKey(DigitalLiteracyTaskDone,
        chained_field="person",
        chained_model_field="person",
        show_all=False, 
        auto_choose=True, 
        sort=True
        )
    # digitalLiteracyTaskDone=models.ForeignKey(ProgrammingTaskDone,on_delete=models.CASCADE, related_name='digital_literacy_task_done_point')
    point=models.IntegerField()
    
    def save(self, *args, **kwargs):
        import datetime
        if datetime.date.today().__gt__(self.digitalLiteracyTaskDone.task.expiry_date):
            # task expired
            return None
        if self.digitalLiteracyTaskDone.taskIsDone==False:
            self.point -= 10
            return self.point
        self.point +=10
        
        if datetime.date.today().__gt__(self.programingTaskDone.task.expiry_date):
            return None
        if self.programingTaskDone.taskIsDone==False:
            self.point -= 10
            return self.point
        self.point +=10
        super().save(self,*args, *kwargs)
        
    def __str__(self):
        return f'Person: {self.person} ({self.point} points)'
        
class Budget(models.Model):
    person =models.ForeignKey(Person,on_delete=models.CASCADE,related_name='person_budget')
    currentBudget =models.IntegerField(default=0)
    allocatedBudget=models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.currentBudget += self.allocatedBudget
        super().save(self, *args, **kwargs)
    
    def __str__(self):
        return f'{self.person} Budget ({self.currentBudget})'

       
class Withdrawal(models.Model):
    person =models.ForeignKey(Person,on_delete=models.CASCADE,related_name='person_withdrawal')
    bank_acct= ChainedForeignKey(BankAccount,
        chained_field="person",
        chained_model_field="person",
        show_all=False, 
        auto_choose=True, 
        sort=True
        )
    currentBudget= ChainedForeignKey(Budget,
        chained_field="person",
        chained_model_field="person",
        show_all=False, 
        auto_choose=True, 
        sort=True
        )

    #currentBudget =models.IntegerField(default=0)
    withdrawalPurpose=models.CharField(max_length=200)
    # bank = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='withdrawal_bank')
    withdrawal=models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.currentBudget.__le__(self.withdrawal):
            return None
        self.currentBudget -= self.withdrawal
        super().save(self, *args, **kwargs)
    
    def __str__(self):
        return f'{self.person} Budget({self.currentBudget})'
