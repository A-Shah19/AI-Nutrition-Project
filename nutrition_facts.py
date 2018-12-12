# based on a 2000 calorie diet
# suggested diet = 40 % carbs, 40% protein, 20% fat ,1500 mg of sodium (American Heart Association), 300 mg cholesterol
class Food:
    food_facts = {}
    def __init__(self, name, calories, fat, cholesterol, sodium, carbohydrates, protein):
        self.name = name
        self.calories = calories
        self.fat = fat
        self.cholesterol = cholesterol
        self.sodium = sodium
        self.carbohydrates = carbohydrates
        self.protein = protein
        self.food_facts[name] = [self.calories, self.fat, self.cholesterol, self.sodium, self.carbohydrates, self.protein]

def main():
    waffles = Food('waffles', 218, 11, 52, 383, 25, 5.9)
    sushi = Food('sushi', 349, 19, 17, 537, 38, 7.8)
    pizza = Food('pizza', 285, 10, 18, 640, 36, 12)
    pho = Food('pho', 638, 14, 86, 3268, 78, 47)
    club_sandwich = Food('club_sandwich', 817, 46, 203, 1867, 42, 56)
    french_fries= Food('french_fries', 365, 17, 0, 246, 48, 4)
    chicken_wings = Food('chicken_wings', 216, 14, 120, 83, 0, 20)
    caesar_salad = Food('caesar_salad', 481, 40, 36, 1152, 23, 10)
    suggested_diet = Food('suggested', 2000, 400, 300, 1500, 800,800 )

if __name__ == '__main__':
    main()

