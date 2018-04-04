""" This file contains the unit tests for HW09 and HW10. """

import unittest
import os
import sys
from prettytable import PrettyTable
from collections import defaultdict
from HW09KyleRozanitis import Student, Instructor, Repository

class HW09Test(unittest.TestCase):
    def repository_error(self):
        directory_path = "/Users/Rozanitis/Documents/Stevens/SSW-810/DataRepository/fil"
        self.assertEqual(Repository(directory_path), "/Users/Rozanitis/Documents/Stevens/SSW-810/DataRepository/fil could not be found.")      
    
    def student_test(self):
        directory_path = "/Users/Rozanitis/Documents/Stevens/SSW-810/DataRepository/files"
        repo = Repository(directory_path)
        s1 = repo.student_data["10103"]
        self.assertEqual(s1.scwid, "10103")
        self.assertEqual(s1.name, "10103")        
        self.assertEqual(s1.major, "10103")

        self.assertEqual(s1.remaining_required(), ['SSW 540', 'SSW 555'])
        self.assertEqual(s1.remaining_electives(), None)

    def instructor_test(self):
        directory_path = "/Users/Rozanitis/Documents/Stevens/SSW-810/DataRepository/files"
        repo = Repository(directory_path)
        i1 = repo.instructor_data["98765"]
        self.assertEqual(i1.cwid, "98765")
        self.assertEqual(i1.name, "Einstein, A")
        self.assertEqual(i1.department, "SFEN")


if __name__ == '__main__':
    # Note there is no main() This program contains only test cases.
    unittest.main(exit=False, verbosity=2)