# code to print marks of a student from the record  
student_name_1 = 'Itika'  
student_name_2 = 'Parker'  
  
  
# Creating a dictionary of records of the students  
records = {'Itika': 90, 'Arshia': 92, 'Peter': 46}  
def marks( student_name ):  
    for a_student in records: # for loop will iterate over the keys of the dictionary  
        if a_student == student_name:  
            return records[ a_student ]  
            break  
    else:  
        return f'There is no student of name {student_name} in the records'   
          
# giving the function marks() name of two students  
print( f"Marks of {student_name_1} are: ", marks( student_name_1 ) )  
print( f"Marks of {student_name_2} are: ", marks( student_name_2 ) )  