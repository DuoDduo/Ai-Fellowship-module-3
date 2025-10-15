##classwork
# create a simple class names Pet.

class Pet: 
    def __init__(self, name, species,age):
        print("Pet Profile")
        self.name = name,
        self.species = species,
        self.age = age
        
        print(f"My pet's name is {name}, It's breed is {species} and she is presently {age} year's old")
        
    # Write a function to celebarate the pet's birthday
    def birthday(self):
        from datetime import datetime
        return f"{datetime(2025, 6,10).strftime("%m/%d/%Y")}"  
        
shelby = Pet("Shelby", "Caucasian","3")
print(f"My pet {shelby.name}'s birthday date is {shelby.birthday()}")



            
 
        
# This class should have features name, species and age.
# Include a function to display the class information.
