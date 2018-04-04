""" This program takes student, instructor, course, and grade data, which are
stored in text files in a specified directory, adds them to a repository, 
and then prints a student summary table containing student cwid, name,
completed courses, remaining required courses, and remaining elective courses
and an instructor summary table containing instructor cwid, name, department,
course, and number of students. """

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
        self.required_coures = defaultdict(list)    # key = major, value = list of courses
        self.elective_courses = defaultdict(list)  # key = major, value = list of courses
        self.directory_path = directory_path
        if os.path.exists(directory_path):
            self.directory_path = directory_path
        else:
            print(directory_path, "could not be found.")
        self.get_student_data()
        self.get_instructor_data()
        self.get_grades()
        self.get_major_courses()

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

    def get_major_courses(self):
        """ This method attempts to open the file majors.txt in the specified
        directory and prints an error if not. Once the file is open, the line
        is split and based on the tflag, the the course is added to a required
        or elective default dictionary where the major is the key. If the course
        does not have an appropriate tflag, an error message is printed out. """
        filename = os.path.join(self.directory_path, "majors.txt")
        try:
            fp = open(filename, "r")
        except FileNotFoundError:
            print(filename, "could not be found.")
        else:
            with fp:
                for line in fp:
                    major, tflag, course = line.strip().split("\t")
                    if tflag == "R":
                        self.required_coures[major].append(course)
                    elif tflag == "E":
                        self.elective_courses[major].append(course)
                    else:
                        print("Error:", course, "is neither a required course or elective.")

    def check_student_courses(self):
        """ This method generates a list of student scwids and for each scwid,
        creates an instance of that student, calls a student method to get a
        set of courses the student has passed, and checks the set against the
        list of required and elective courses. Based on the difference of the
        required courses and courses passed sets, the remaining courses to be
        completed will be added to the student's remaining courses' dictionary.
        Based on the intersection of the elective courses and courses passed
        sets, the student's elective courses' dictionary will be converted to
        None if the student has passed at least one elective or will show a
        list of potential electives to take. """
        student_lst = self.student_data.keys()
        for item in student_lst:
            s1 = self.student_data[item]
            courses_passed = s1.retrieve_courses(item)
            required_courses_remaining = set(self.required_coures[s1.major]).difference(courses_passed)
            s1.add_remaining_required(required_courses_remaining)

            elective_courses_taken = set(self.elective_courses[s1.major]).intersection(courses_passed)
            if len(elective_courses_taken) > 0:
                s1.electives_complete()
            else:
                s1.add_remaining_elective(self.elective_courses[s1.major])

    def major_table(self):
        """ This method creates a prettytable which iterates through the
        required_courses dictioanry keys and adds a row with the department,
        a list of required courses, and a list of elective courses. """
        pt = PrettyTable(field_names=["Department", "Required", "Electives"])
        lst = self.required_coures.keys()
        for item in lst:
            pt.add_row([item, self.required_coures[item], self.elective_courses[item]])
        print(pt)

    def student_table(self):
        """ This method creates a prettytable which iterates through the
        student_data dictionary and adds "CWID", "Name", and "Completed Courses"
        information to the table. The table is printed out at the end. """
        pt = PrettyTable(field_names=["CWID", "Name", "Completed Courses", "Remaining Required", "Remaining Electives"])
        lst = self.student_data.keys()
        for item in lst:
            s1 = self.student_data[item]
            pt.add_row([item, s1.name, s1.retrieve_grades(item), s1.retrieve_remaining_required(item), s1.retrieve_remaining_electives(item)])
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
        self.remaining_required = []
        self.remaining_electives = []
    
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

    def retrieve_courses(self, scwid):
        """ This method creates a set, adds the courses completed and passed
        by a student to the set, and returns the set. """
        courses_set = []
        for key in self.grades_data.keys():
            if self.grades_data[key] in ("A", "A-", "B+", "B", "B-", "C+", "C"):
                courses_set.append(key)
        return courses_set

    def add_remaining_required(self, rem_req):
        """ This method adds the remaining required courses calculated from
        the check_student_courses method of class Repository to the class
        Student dictionary list remaining_required. """
        for item in rem_req:
            self.remaining_required.append(item)

    def add_remaining_elective(self, rem_ele):
        """ This method adds the class Repository's elective_courses dictionary
        values to the class Student's remaining_electives list if the student
        has not taken or completed any electives. """
        for item in rem_ele:
            self.remaining_electives.append(item)

    def electives_complete(self):
        """ This method changes the class Student's remaining_electives list
        to None if the student has taken and passed at least one elective. """
        self.remaining_electives = None
    
    def retrieve_remaining_required(self, scwid):
        """ This method returns the class Student's remaining_required list
        for the prettytable. """
        return self.remaining_required

    def retrieve_remaining_electives(self, scwid):
        """ This method returns the class Student's remaining_electives list
        for the prettytable. """
        return self.remaining_electives


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
    repo1.check_student_courses()
    repo1.major_table()
    repo1.student_table()
    repo1.instructor_table()
    sys.exit()

main()