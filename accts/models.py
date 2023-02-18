from django.db import models

from django.contrib.auth.models import User


class ProgrammingLanguage(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
class BankAccount(models.Model):
    bank=models.CharField(max_length=50)
    acctName=models.CharField(max_length=100)
    acctNo=models.CharField(max_length=15)
    
    def __str__(self):
        return self.acctName
        

    

class Person(User):
    phone = models.IntegerField()
    state=models.CharField(max_length=50)
    lga=models.CharField(max_length=50)
    programmingLanguage= models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='person_programming_language')
    programmingLanguageYearsOfExperience=models.IntegerField()
    github = models.URLField(max_length=200)
    bankDetail=models.ForeignKey(BankAccount,on_delete=models.CASCADE, related_name='person_bankdetails')
    
    def __str__(self):
        return self.username


        
class ProgrammingTask(models.Model):
    programmingLanguage=models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='task_programming_language')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    def __str__(self):
        return self.title
    
class ProgrammingTaskDone(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    task =models.ForeignKey(ProgrammingTask, on_delete=models.CASCADE, related_name='programming_task_done')
    taskIsDone=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.task.title} {self.taskIsDone}'
    
        
class Invitee(models.Model):
    fullname=models.CharField(max_length=200)
    email=models.EmailField()
    phone = models.IntegerField()
    programmingLanguage=models.ForeignKey(ProgrammingLanguage,on_delete=models.CASCADE, related_name='invitee_programming_language')
    def __str__(self):
        return self.fullname
        
class DigitalLiteracyTask(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    def __str__(self):
        return self.title
    
class DigitalLiteracyTaskDone(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    task =models.ForeignKey(DigitalLiteracyTask, on_delete=models.CASCADE, related_name='digital_literacy_task_done')
    invite =models.ForeignKey(Invitee, on_delete=models.CASCADE, related_name='digital_literacy_invitee')
    taskIsDone=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.task.title} {self.taskIsDone}'
    

class Point(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_point')
    programingTaskDone=models.ForeignKey(ProgrammingTaskDone,on_delete=models.CASCADE, related_name='programming_task_done_point')
    digitalLiteracyTaskDone=models.ForeignKey(ProgrammingTaskDone,on_delete=models.CASCADE, related_name='digital_literacy_task_done_point')
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
        return f'{self.person} Budget({self.currentBudget}'

       
class Withdrawal(models.Model):
    person =models.ForeignKey(Person,on_delete=models.CASCADE,related_name='person_withdrawal')
    currentBudget =models.IntegerField(default=0)
    withdrawalPurpose=models.CharField(max_length=200)
    bank = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='withdrawal_bank')
    withdrawal=models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.currentBudget.__le__(self.withdrawal):
            return None
        self.currentBudget -= self.withdrawal
        super().save(self, *args, **kwargs)
    
    def __str__(self):
        return f'{self.person} Budget({self.currentBudget})'
