import random
import string

from django.conf import settings




EVENT_CODE_LEN = getattr(settings, 'EVENT_CODE_LEN', 12)



def code_generator(size=EVENT_CODE_LEN, chars=string.ascii_lowercase + string.digits):
    new_code = ''
    for _ in range(size):
        new_code += random.choice(chars)
    return new_code



def create_event_code(instance, size=EVENT_CODE_LEN):
    new_code = code_generator(size)
    event_model = instance.__class__
    is_exist = event_model.objects.filter(event_code=new_code).exists()
    if is_exist:
        return create_event_code(instance, size=size)
    return new_code
