""" This program takes student, instructor, and grade data, which are
stored in text files in a specified directory, adds them to a repository, 
and then prints a student summary table containing student cwid, name, and
completed courses, and an instructor summary table containing instructor cwid,
name, department, course, and number of students. """

import os
import sys
from prettytable import PrettyTable
from collections import defaultdict

class Repository:
    """ This class is a container for the data structures housing student
    and instructor data. The class also has methods for parsing and storing
    the data and methods to generate a prettytable for the student data and the
    instructor data. """
    def __init__(self, directory_path):
        """ Initializes the Repository class and creates the dictionaries
        that will house the student and instructor data. This method also
        ensures that the directory path exists and returns a "<<file_name>>
        could not be found error" if not. """
        self.student_data = dict()  # key = scwid, value = instance of a student
        self.instructor_data = dict()   # key = icwid, value = instance of an instructor
        self.directory_path = directory_path
        if os.path.exists(directory_path):
            self.directory_path = directory_path
        else:
            print(directory_path, "could not be found.")
        self.get_student_data()
        self.get_instructor_data()
        self.get_grades()
    
    def get_student_data(self):
        """ This method attempts to open the file students.txt in the specified
        directory and prints an error if not. Once the file is open, the method
        reads through the file, creates instances of students with the info
        from the file, and stores them in the student_data dictionary. """
        filename = os.path.join(self.directory_path, "students.txt")
        try:
            fp = open(filename, "r")
        except FileNotFoundError:
            print(filename, "could not be found.")
        else:
            with fp:
                for line in fp:
                    scwid, name, major = line.strip().split("\t")
                    s1 = Student(scwid, name, major)
                    self.student_data[scwid] = s1

    def get_instructor_data(self):
        """ This method attempts to open the file instructors.txt in the specified
        directory and prints an error if not. Once the file is open, the method
        reads through the file, creates instances of instructors with the info
        from the file, and stores them in the instructor_data dictionary. """
        filename = os.path.join(self.directory_path, "instructors.txt")
        try:
            fp = open(filename, "r")
        except FileNotFoundError:
            print(filename, "could not be found.")
        else:
            with fp:
                for line in fp:
                    icwid, name, department = line.strip().split("\t")
                    i1 = Instructor(icwid, name, department)
                    self.instructor_data[icwid] = i1

    def get_grades(self):
        """ This method attempts to open the file grades.txt in the specified
        directory and prints an error if not. Once the file is open, the method
        reads through the file, creates instances of both student and instructor,
        adds the course and grade to the grades_data dictionary of that instance,
        and adds the additional student to student_count defaultdict. """
        filename = os.path.join(self.directory_path, "grades.txt")
        try:
            fp = open(filename, "r")
        except FileNotFoundError:
            print(filename, "could not be found.")
        else:
            with fp:
                for line in fp:
                    scwid, course, grade, icwid = line.strip().split("\t")
                    self.student_data[scwid].add_grades(course, grade)
                    self.instructor_data[icwid].add_student_count(course)

    def student_table(self):
        """ This method creates a prettytable which iterates through the
        student_data dictionary and adds "CWID", "Name", and "Completed Courses"
        information to the table. The table is printed out at the end. """
        pt = PrettyTable(field_names=["CWID", "Name", "Completed Courses"])
        lst = self.student_data.keys()
        for item in lst:
            s1 = self.student_data[item]
            pt.add_row([item, s1.name, s1.retrieve_grades(item)])
        print(pt)
 
    def instructor_table(self):
        """ This method creates a prettytable which iterates through the
        instructor_data dictionary and adds "CWID", "Name", and "Department",
        "Course", and number of students information to the table. The table
        is printed out at the end. """
        pt = PrettyTable(field_names=["CWID", "Name", "Department", "Course", "Students"])
        lst = self.instructor_data.keys()
        for item in lst:
            i1 = self.instructor_data[item]
            lst = []
            for key in i1.student_count.keys():
                lst.append(key)
            for course in lst:
                pt.add_row([item, i1.name, i1.department, course, i1.retrieve_student_count(course)])
        print(pt)


class Student:
    """ This class uses student cwid, name, and major to create an instance
    of a student. The class also contains methods to add grades to a grades_data
    dictionary and retrieve the courses for the prettytable. """
    def __init__(self, scwid, name, major):
        """ This method initializes the Student instance and creates a grades_data
        dictionary to house the course and grades. """
        self.scwid = scwid
        self.name = name
        self.major = major
        self.grades_data = dict()   # key = course, value = grade
    
    def add_grades(self, course, grade):
        """This method adds courses as keys and grades as values to
        the grades_data dictionary. """
        self.grades_data[course] = grade

    def retrieve_grades(self, scwid):
        """ This method creates a list, adds the courses completed by a student
        to the list, and returns the list for the prettytable. """
        lst = []
        for key in self.grades_data.keys():
            lst.append(key)
        return sorted(lst)


class Instructor:
    """ This class uses instructor cwid, name, and major to create an instance
    of an instructor. The class also contains methods to increment the count of
    students in each course and retrieve the number of students for each course
    for the prettytable. """
    def __init__(self, icwid, name, department):
        """ This method initializes the Instructor instance and creates a
        student_count default dictionary to house the courses and number of
        students. """
        self.icwid = icwid
        self.name = name
        self.department = department
        self.student_count = defaultdict(int)   # key = course, value = # of students

    def add_student_count(self, course):
        """ This method incrememts the number of students in a specific course
        or creates a new item with the course as the key and value as 0. """
        self.student_count[course] += 1

    def retrieve_student_count(self, course):
        """ This method returns the number of students in a specific course. """
        return self.student_count[course]


def main():
    """ This is the main function of the program. This program creates a new
    repository and prints a summary student table and summary instructor table. """
    repo1 = Repository("/Users/Rozanitis/Documents/Stevens/SSW-810/DataRepository/files")
    repo1.student_table()
    repo1.instructor_table()
    sys.exit()