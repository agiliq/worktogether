from django.db import models


class Team(models.Model):

    name = models.CharField(max_length=150)
    email = models.EmailField()

    def __unicode__(self):
        return self.name


class Work(models.Model):

    person = models.ForeignKey(Team)
    date = models.DateField(auto_now_add=True)
    work = models.TextField()

    def __unicode__(self):
        return "%s, %s" % (self.person, self.date.ctime()[:10])
