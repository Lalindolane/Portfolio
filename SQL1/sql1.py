# sql1.py
import csv
import numpy as np
import sqlite3 as sql
from matplotlib import pyplot as plt


# Problems 1, 2, and 4
def student_db(db_file="students.db", student_info="student_info.csv",
                                      student_grades="student_grades.csv"):
    """Connect to the database db_file (or create it if it doesn’t exist).
    Drop the tables MajorInfo, CourseInfo, StudentInfo, and StudentGrades from
    the database (if they exist). Recreate the following (empty) tables in the
    database with the specified columns.

        - MajorInfo: MajorID (integers) and MajorName (strings).
        - CourseInfo: CourseID (integers) and CourseName (strings).
        - StudentInfo: StudentID (integers), StudentName (strings), and
            MajorID (integers).
        - StudentGrades: StudentID (integers), CourseID (integers), and
            Grade (strings).

    Next, populate the new tables with the following data and the data in
    the specified 'student_info' 'student_grades' files.

                MajorInfo                         CourseInfo
            MajorID | MajorName               CourseID | CourseName
            -------------------               ---------------------
                1   | Math                        1    | Calculus
                2   | Science                     2    | English
                3   | Writing                     3    | Pottery
                4   | Art                         4    | History

    Finally, in the StudentInfo table, replace values of −1 in the MajorID
    column with NULL values.

    Parameters:
        db_file (str): The name of the database file.
        student_info (str): The name of a csv file containing data for the
            StudentInfo table.
        student_grades (str): The name of a csv file containing data for the
            StudentGrades table.
    """
    with sql.connect(db_file) as conn:
        conn.execute("DROP TABLE IF EXISTS MajorInfo")
        conn.execute("DROP TABLE IF EXISTS CourseInfo")
        conn.execute("DROP TABLE IF EXISTS StudentInfo")
        conn.execute("DROP TABLE IF EXISTS StudentGrades")
        conn.execute("CREATE TABLE MajorInfo (MajorID INTEGER, MajorName TEXT)")
        conn.execute("CREATE TABLE CourseInfo (CourseID INTEGER, CourseName TEXT)")
        conn.execute("CREATE TABLE StudentInfo (StudentID INTEGER, StudentName TEXT, MajorID INTEGER)")
        conn.execute("CREATE TABLE StudentGrades (StudentID INTEGER, CourseID INTEGER, Grade TEXT)")
        cur = conn.cursor()
        Majorinfo = [(1, "Math"), (2, "Science"), (3, "Writing"), (4, "Art")]
        Courseinfo = [(1, "Calculus"), (2, "English"), (3, "Pottery"), (4, "History")]
        with open(student_info, "r") as file:
            Studentinfo = list(csv.reader(file))
        with open(student_grades, "r") as file:
            Studentgrades = list(csv.reader(file))
        Studentinfo = [(int(sid), name, int(mid)) for sid, name, mid in Studentinfo]
        Studentgrades = [(int(sid), int(cid), grade) for sid, cid, grade in Studentgrades]
        cur.executemany("INSERT INTO MajorInfo VALUES(?,?);", Majorinfo)
        cur.executemany("INSERT INTO CourseInfo VALUES(?,?);", Courseinfo)
        cur.executemany("INSERT INTO StudentGrades VALUES(?,?,?);", Studentgrades)
        cur.executemany("INSERT INTO StudentInfo VALUES(?,?,?);", Studentinfo)
        cur.execute("UPDATE StudentInfo SET MajorID = NULL WHERE MajorID == -1")


# Problems 3 and 4
def earthquakes_db(db_file="earthquakes.db", data_file="us_earthquakes.csv"):
    """Connect to the database db_file (or create it if it doesn’t exist).
    Drop the USEarthquakes table if it already exists, then create a new
    USEarthquakes table with schema
    (Year, Month, Day, Hour, Minute, Second, Latitude, Longitude, Magnitude).
    Populate the table with the data from 'data_file'.

    For the Minute, Hour, Second, and Day columns in the USEarthquakes table,
    change all zero values to NULL. These are values where the data originally
    was not provided.

    Parameters:
        db_file (str): The name of the database file.
        data_file (str): The name of a csv file containing data for the
            USEarthquakes table.
    """
    with sql.connect(db_file) as conn:
        conn.execute("DROP TABLE IF EXISTS USEarthquakes")
        conn.execute("CREATE TABLE USEarthquakes (Year INTEGER, Month INTEGER, Day INTEGER, Hour INTEGER, Minute INTEGER, Second INTEGER, Latitude REAL, Longitude REAL, Magnitude REAL)")
        with open(data_file, "r") as file:
            cleaned = []
            info = list(csv.reader(file))
            for row in info:
                row[0] = int(row[0])
                row[1] = int(row[1])
                row[2] = int(row[2])
                row[3] = int(row[3])
                row[4] = int(row[4])
                row[5] = int(row[5])
                row[6] = float(row[6])
                row[7] = float(row[7])
                row[8] = float(row[8])
                cleaned.append(row)
        cur = conn.cursor()
        cur.executemany("INSERT INTO USEarthquakes VALUES(?,?,?,?,?,?,?,?,?);", cleaned)
        cur.execute("DELETE FROM USEarthquakes WHERE Magnitude == 0")
        cur.execute("UPDATE USEarthquakes SET Day = NULL WHERE Day == 0")
        cur.execute("UPDATE USEarthquakes SET Hour = NULL WHERE Hour == 0")
        cur.execute("UPDATE USEarthquakes SET Minute = NULL WHERE Minute == 0")
        cur.execute("UPDATE USEarthquakes SET Second = NULL WHERE Second == 0")


# Problem 5
def prob5(db_file="students.db"):
    """Query the database for all tuples of the form (StudentName, CourseName)
    where that student has an 'A' or 'A+'' grade in that course. Return the
    list of tuples.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    with sql.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT SI.StudentName, CI.CourseName
                    FROM StudentInfo AS SI, StudentGrades AS SG, CourseInfo AS CI
                    WHERE SI.StudentID == SG.StudentID AND SG.CourseID == CI.CourseID
                    AND (SG.Grade == 'A' or SG.Grade == 'A+')""")
        return cur.fetchall()


# Problem 6
def prob6(db_file="earthquakes.db"):
    """Create a single figure with two subplots: a histogram of the magnitudes
    of the earthquakes from 1800-1900, and a histogram of the magnitudes of the
    earthquakes from 1900-2000. Also calculate and return the average magnitude
    of all of the earthquakes in the database.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (float): The average magnitude of all earthquakes in the database.
    """
    with sql.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT Magnitude, Year from USEarthquakes""")
        tups = cur.fetchall()
    total = 0
    count = 0
    prenineteen = []
    postnineteen = []
    for mag, year in tups:
        count += 1
        total += mag
        if 1800 <= year <= 1899:
            prenineteen.append(mag)
        elif 1900 <= year <= 1999:
            postnineteen.append(mag)
    avg = total/count
    plt.subplot(1, 2, 1)
    plt.xlabel("Magnitude")
    plt.ylabel("Occurrences")
    plt.hist(prenineteen)
    plt.title("1800-1899")
    plt.subplot(1, 2, 2)
    plt.xlabel("Magnitude")
    plt.ylabel("Occurrences")
    plt.title("1900-1999")
    plt.hist(postnineteen)
    plt.savefig("histograms_of_earthquakes.png")
    plt.show()
    return avg


if __name__ == "__main__":
    student_db()
    with sql.connect("students.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM StudentInfo;")
        print([d[0] for d in cur.description])
    with sql.connect("students.db") as conn:
        cur = conn.cursor()
        for row in cur.execute("SELECT * FROM MajorInfo;"):
            print(row)
    earthquakes_db()
    prob6()