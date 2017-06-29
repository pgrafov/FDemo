from django.db.models import (BooleanField, CharField, DateTimeField,
                              ForeignKey, Model, URLField)


class Word(Model):
    title = CharField(unique=True, max_length=100)
    assigned = BooleanField(default=False)

    def __str__(self):
        return self.title


class Url(Model):
    link = URLField(verbose_name=u'URL')
    word = ForeignKey(Word, null=True)
    created = DateTimeField(auto_now_add=True)

    def delete(self):
        self.word.assigned = False
        self.word.save()
        super(Url, self).delete()
