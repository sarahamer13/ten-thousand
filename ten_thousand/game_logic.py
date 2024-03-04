import random
from collections import Counter

class GameLogic:
    @staticmethod
    def roll_dice(num_dice):
        """Roll the dice a specified number of times and return a tuple of the results."""
        """" Generating  random numbers between 1 and 6 using list comprehension and using the function of 
        random.randint then the numbers are converted to a tuple and returned
        """

        return tuple(random.randint(1, 6) for _ in range(num_dice))



    def calculate_score(dice_roll):
        score = 0
        counts = Counter(dice_roll)

        """ First going to check if the sorted dice roll is equal to 6 then second condition will check if sorted dice roll
        has numbers from 1 to 6, it will score 1500. If not the next condition will check two things, first if there are 3 identical
        numbers, second it will checks if all the counts of the numbers in the dice_roll are equal to 2,
        meaning each number appears twice. This condition ensures that each of the three pairs has a count of 2. 
        If both are true, score is 1500
        """
        if len(dice_roll) == 6:
            if sorted(dice_roll) == list(range(1, 7)):    
                return 1500  
            elif len(set(dice_roll)) == 3 and all(count == 2 for count in counts.values()):
                return 1500  
            
        if len (dice_roll) == 5:
            for num, count in counts.items():
                 if count == 5:
                   if num == 1:
                    score += 3000
                    return score
              
                   elif num == 5:
                        score+= 1500
                        return score
                   
        if len (dice_roll) == 4:
            for num, count in counts.items():
                 if count == 4:
                   if num == 1:
                    score += 2000
                    return score
              
                   elif num == 4:
                        score+= 800
                        return score
                   elif num == 5:  
                        score += 1000
                        return score

        """
        Line below calculate additional score points based on how many times we see 1 and 5 in dice roll.
        When 1 is divided by 3, we are finding out how many 1s are left from a set of 3. Then we multiply
        the reminder by 100. Next step is similar to the first but with 5, then we multiply the reminder by 50. 

        """
        score += (counts[1] % 3) * 100 + (counts[5] % 3) * 50


        # Scoring for triples and beyond
        for num, count in counts.items():
         
            if count >= 3:
                if num == 1:
                    score += 1000  #  If the current number is 1 and occurs three or more times, it adds 1000 points to the score. This represents the score for a triple of ones.
                    if count > 3:
                        score += (count - 3) * 1000  # For each additional occurrence of 1 beyond the triple, it adds 1000 points to the score. This represents the score for each additional one beyond the triple.

        ## if the current number is not 1, meaning 2-6. Scoring will be simpler
                else:
                    score += num * 100  # for example 3 is found 3 times, it will add 300 points
                    if count > 3:
                        score += (count - 3) * num * 100  # adding 100 points to the score, this represents a linear increase in scoring for additional matching dice beyond the triple.

        return score

