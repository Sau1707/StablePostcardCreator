import random

epic_adjectives = ["majestic", "magnificent", "stunning", "breathtaking", "impressive", "awe-inspiring", "spectacular", "grand", "imposing", "towering", "mammoth", "colossal", "gigantic", "monstrous", "enormous", "gargantuan", "towering", "monumental"]
epic_nouns = ["sunset", "mountain", "waterfall", "ocean view", "forest", "desert", "canyon", "valley", "mesa", "beach", "lake", "river", "swamp", "rainforest", "jungle", "tundra", "glacier", "iceberg", "canyon", "geyser", "volcano", "earthquake", "hurricane", "tornado", "blizzard"]

def generateDescription():
    # adjective = random.choice(epic_adjectives)
    noun = random.choice(epic_nouns)
    description = f"An epic image of a {noun}, high-detail, true-color, 4K "
    return description