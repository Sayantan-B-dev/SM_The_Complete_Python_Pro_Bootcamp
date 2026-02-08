import random

FACTS = [
    "Commercial airplanes are struck by lightning about once per year on average.",
    "The Boeing 747 contains nearly six million individual parts.",
    "Airplane black boxes are painted orange for easier crash recovery.",
    "Jet lag is caused by disruption of the circadian rhythm.",
    "Planes fly more efficiently at higher altitudes due to thinner air."
]

def random_aviation_fact() -> str:
    return random.choice(FACTS)
