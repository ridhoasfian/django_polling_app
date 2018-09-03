from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    pub_date = models.DateField()
    def __str__(self):
        return self.text

    def user_bisa_voting(self, user):
        pilihan_user = user.vote_set.all() #data dari class Vote
        qs = pilihan_user.filter(poll=self)
        if qs.exists():
            return False
        return True

    def jumlah_pemilih(self):
        return self.vote_set.count()

    def get_hasil_dict(self):
        hasil = []
        for choice in self.choice_set.all():
            dict = {}
            dict['choice_text'] = choice.choice_text
            dict['jumlah_voting'] = choice.jumlah_voting()
            if self.jumlah_pemilih() :
                dict['persentase'] = choice.jumlah_voting() / self.jumlah_pemilih() * 100
            else :
                dict['persentase'] = 0
            hasil.append(dict)
        return hasil

"""#############################################################################"""

class Choice(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text

    def jumlah_voting(self):
        return self.vote_set.count()

"""#############################################################################"""

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)
