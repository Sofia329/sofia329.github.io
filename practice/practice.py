
class Student:
    def __init__ (self, name, house):
        if not name:
            raise ValueError ("Missing Name")
        self.name = name
        self.house = house

def get_student():
    name = input ("Name: ")
    house = input ("House: ")
    student = Student(name, house)
    return student

def main():
    try:
        student = get_student()`
        print(f"{student.name} from {student.house}")
    except ValueError as e:
        print(f"Error: {e}")
        print("No student object was created")

main()

