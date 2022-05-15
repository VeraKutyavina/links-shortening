from random import choice

from string import ascii_letters, digits

# Max url size
URL_SIZE = 10
AVAIABLE_CHARS = ascii_letters + digits


# Creates a random string with url size length

def create_random_string():
    return "".join(
        [choice(AVAIABLE_CHARS) for _ in range(URL_SIZE)]
    )


# Generate short link for url

def generate_short_url(model_instance):
    random_string = create_random_string()

    model_class = model_instance.__class__

    # Call method again if string have already exist
    if model_class.objects.filter(short_link=random_string).exists():
        return generate_short_url(model_instance)

    return random_string
