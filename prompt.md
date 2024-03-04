## Promot - 01

- Result below:

```python
import random

class GameLogic:
    @staticmethod
    def roll_dice(num_dice):
        if not isinstance(num_dice, int) or num_dice < 1:
            raise ValueError("Number of dice must be a positive integer")
        
        return tuple(random.randint(1, 6) for _ in range(num_dice))

# Example usage:
num_dice = 3
result = GameLogic.roll_dice(num_dice)
print(f"Rolling {num_dice} dice: {result}")
```

## Prompt - 2

- Results below:

```python
class GameLogic:
    @staticmethod
    def calculate_score(dice_roll):
        if not isinstance(dice_roll, tuple):
            raise TypeError("Input must be a tuple of integers representing a dice roll")

        score = 0
        # Count occurrences of each number in the dice roll
        counts = {i: dice_roll.count(i) for i in range(1, 7)}

        # Calculate score according to game rules
        for num, count in counts.items():
            if count >= 3:
                if num == 1:
                    score += 1000
                else:
                    score += num * 100
                count -= 3

            if num == 1:
                score += count * 100
            elif num == 5:
                score += count * 50

        return score

# Example usage:
dice_roll = (1, 3, 3, 4, 5)
score = GameLogic.calculate_score(dice_roll)
print(f"Score for the roll {dice_roll}: {score}")
```

## Prompt -3

I'm still getting this error and I checked mostly everything where it has the attribute error.this is what happend when I ran python -m pytest tests/version_1/test_roll_dice.py

- Result below:

Dealing with AttributeError
Check for Duplicate Class Definitions: Ensure that there is only one GameLogic class definition in your entire project. It's possible to accidentally define a class more than once, especially in large projects or when refactoring code. Use your IDE's search feature to look for multiple definitions.

Verify Correct File and Class Naming: Double-check that the file name and class name exactly match what's being imported. Python is case-sensitive, so ensure there are no discrepancies in case or spelling.

Python Path Issue: The error might be due to Python not being able to find your module. Ensure your project structure is correct and that you're running pytest from the root directory of your project. Sometimes, running pytest with the module's path can help, e.g., python -m pytest path/to/your/tests/.

Virtual Environment: Since you're using a virtual environment (as indicated by the prompt), make sure it's activated and that you've installed all necessary dependencies. Sometimes, deactivating and reactivating the virtual environment can help resolve path issues.

Initialization File: Confirm that each package directory (any directory containing Python files you're importing) has an __init__.py file. Even an empty file is sufficient for Python to recognize the directory as a package.

## Prompt -4

Is these tests referring to the last one the test all FAILED tests/version_1/test_calculate_score.py::test_all[test_input4-2000] - assert 400 == 2000
FAILED tests/version_1/test_calculate_score.py::test_all[test_input5-3000] - assert 600 == 3000
FAILED tests/version_1/test_calculate_score.py::test_all[test_input16-600] - assert 400 == 600

- Result below: 

Yes, the failed tests you've listed are indeed referring to the test_all function you've set up with parameterized inputs using @pytest.mark.parametrize. These failures indicate that for each of these test cases, the calculate_score method's actual output does not match the expected output defined in your test cases.

The pattern in the failures (assert actual == expected) suggests that your calculate_score method may not be correctly handling certain scoring rules or combinations of dice. The discrepancies between the actual and expected scores imply that either:

The scoring logic within calculate_score may not accurately account for all game rules or specific dice combinations you've tested against.
The expected values in your test cases might be incorrect or based on a misunderstanding of the scoring rules.

## Prompt -5 

Here is what the test wants @pytest.mark.parametrize(
    "test_input,expected",
    [
        (tuple(), 0),
        ((1,), 100),
        ((1, 1), 200),
        ((1, 1, 1), 1000),
}

- Result below:

Here's an adjusted approach for calculate_score to handle these scenarios, focusing on the rules as described:


```python
from collections import Counter

class GameLogic:
    @staticmethod
    def calculate_score(dice_roll):
        score = 0
        # Count the occurrences of each die roll
        counts = Counter(dice_roll)

        # Check for a straight
        if sorted(dice_roll) == list(range(1, 7)):
            return 1500

        # Check for three pairs
        if len(dice_roll) == 6 and all(count == 2 for count in counts.values()):
            return 1500

        for num, count in counts.items():
            # Handle triples and beyond
            if count >= 3:
                if num == 1:
                    score += 1000 * (2 ** (count - 3))  # Double for each additional 1 beyond three
                else:
                    score += num * 100 * (2 ** (count - 3))  # Double for each additional number beyond three
                count -= 3

            # Score singles for 1s and 5s not part of a triple
            if num == 1:
                score += count * 100
            elif num == 5:
                score += count * 50

        return score

```
## Prompt -6 

This is the requirment of the game Handle calculating score for dice roll
Add calculate_score static method to GameLogic class.
The input to calculate_score is a tuple of integers that represent a dice roll.
The output from calculate_score is an integer representing the roll’s score according to rules of game.

- Result below: 

Based on the requirement you've provided for the GameLogic class to have a calculate_score static method, the method should indeed be implemented as a @staticmethod within the GameLogic class. The method's purpose is to calculate and return an integer score for a given tuple of integers that represent a dice roll, according to the game's scoring rules.

Here's an implementation of the GameLogic class with the calculate_score static method, designed to meet the outlined requirements. This implementation assumes a set of common scoring rules for dice games but note that you should adjust the logic to fit the specific rules of your game.

```python
import random
from collections import Counter

class GameLogic:
    @staticmethod
    def roll_dice(num_dice):
        """Roll the dice a specified number of times and return a tuple of the results."""
        return tuple(random.randint(1, 6) for _in range(num_dice))

    @staticmethod
    def calculate_score(dice_roll):
        """Calculate and return the score for a given dice roll."""
        score = 0
        counts = Counter(dice_roll)

        # Scoring rules
        scoring_rules = {
            1: {1: 100, 2: 200, 3: 1000, 4: 2000, 5: 3000, 6: 4000},
            2: {3: 200, 4: 400, 5: 600, 6: 800},
            3: {3: 300, 4: 600, 5: 900, 6: 1200},
            4: {3: 400, 4: 800, 5: 1200, 6: 1600},
            5: {1: 50, 2: 100, 3: 500, 4: 1000, 5: 1500, 6: 2000},
            6: {3: 600, 4: 1200, 5: 1800, 6: 2400},
        }

        # Check for a straight (1-2-3-4-5-6)
        if sorted(dice_roll) == list(range(1, 7)):
            return 1500

        # Calculate points for each die value
        for die, count in counts.items():
            if count >= 3:
                score += scoring_rules[die][3]  # Score for a triple
                count -= 3
            # Score remaining 1s and 5s
            if die in scoring_rules and count in scoring_rules[die]:
                score += scoring_rules[die][count]

        return score

# Example usage

dice_roll = (1, 1, 1, 5, 5)
score = GameLogic.calculate_score(dice_roll)
print(f"Score for the roll {dice_roll}: {score}")
```

## Prompt -7 

It sounds like I have a persistent issue where tests 4 and 5 should be less than 100 and test 28 and 29 should be less than a 50 

Result: same answer as before, asked for TA help



