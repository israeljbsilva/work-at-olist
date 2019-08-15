from djchoices import DjangoChoices, ChoiceItem


class CallRecordType(DjangoChoices):
    start = ChoiceItem('START')
    end = ChoiceItem('END')
