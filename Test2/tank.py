import unittest


class ArmorType():
    """
    Description d'une armure de tank avec en particulier le bonus d'armure qu'elle donne
    """
    name: str = None
    bonus: int = 0

    def __init__(self, name: str, bonus: int):
        self.name = name
        self.bonus = bonus


class Tank():
    """
    Description d'un tank avec son nom, la pénétration de son canon, son armure et son type d'armure
    """
    name: str = ''
    penetration: int = 0
    armor: int = 0
    armor_type: ArmorType = None

    def __init__(self, name: str, penetration: int, armor: int, armor_type: ArmorType):
        self.armor = armor
        self.penetration = penetration
        self.armor_type = armor_type
        self.name = name

    def is_vulnerable_to_tank(self, tank: 'Tank'):
        return self.armor + self.armor_type.bonus <= tank.penetration

    def swap_armor(self, othertank):
        (self.armor, othertank.armor) = (othertank.armor, self.armor)

    def __repr__(self):
        return self.name.lower().replace(' ', '-')

class TestTank(unittest.TestCase):
    armorChobham: ArmorType = ArmorType('chobham', 100)
    armorComposite: ArmorType = ArmorType('composite', 50)
    armorCeramic: ArmorType = ArmorType('ceramic', 50)
    armorSteel: ArmorType = ArmorType('steel', 10)
    
    def test_penetration_simple(self):
        tank1: Tank = Tank('Tank1', 670, 600, self.armorChobham)

        tank2: Tank = Tank('Tank2', 670, 620, self.armorChobham)
        self.assertEqual(tank1.is_vulnerable_to_tank(tank2), False)

        tank2: Tank = Tank('Tank2', 1000, 620, self.armorChobham)
        self.assertEqual(tank1.is_vulnerable_to_tank(tank2), True)

    def test_penetration_accurate(self):
        shooter: Tank = Tank('Tank1', 450, 0, self.armorChobham)

        tanks: list[Tank] = []
        tanks.append(Tank('Tank 1', 0, 400, self.armorSteel))
        tanks.append(Tank('Tank 2', 0, 430, self.armorSteel))
        tanks.append(Tank('Tank 3', 0, 440, self.armorSteel))
        tanks.append(Tank('Tank 4', 0, 450, self.armorSteel))
        tanks.append(Tank('Tank 5', 0, 500, self.armorSteel))

        self.assertEqual(tanks[0].is_vulnerable_to_tank(shooter), True)
        self.assertEqual(tanks[1].is_vulnerable_to_tank(shooter), True)
        self.assertEqual(tanks[2].is_vulnerable_to_tank(shooter), True)
        self.assertEqual(tanks[3].is_vulnerable_to_tank(shooter), False)
        self.assertEqual(tanks[4].is_vulnerable_to_tank(shooter), False)

    def test_swap_armor(self):
        tank1: Tank = Tank('Tank1', 670, 600, self.armorChobham)
        tank2: Tank = Tank('Tank2', 670, 620, self.armorChobham)

        tank1.swap_armor(tank2)
        self.assertEqual(tank1.armor, 620)
        self.assertEqual(tank2.armor, 600)

unittest.main()
