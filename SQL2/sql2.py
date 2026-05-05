"""Volume 1: SQL 2.
<Lane Lindstrom>
<Math 321>
<3/26/2026>
"""

import sqlite3 as sql


# Problem 1
def prob1(db_file="students.db"):
    """Query the database for the list of the names of students who have a
    'B' grade in any course. Return the list.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): a list of strings, each of which is a student name.
    """
    with sql.connect(db_file) as con:
        cur = con.cursor()
        data = cur.execute("""SELECT DISTINCT StudentInfo.StudentName from StudentInfo JOIN StudentGrades
                           ON StudentInfo.StudentID == StudentGrades.StudentID WHERE
                           StudentGrades.Grade == 'B'""").fetchall()
    return [row[0] for row in data]


# Problem 2
def prob2(db_file="students.db"):
    """Query the database for all tuples of the form (Name, MajorName, Grade)
    where 'Name' is a student's name and 'Grade' is their grade in Calculus.
    Only include results for students that are actually taking Calculus, but
    be careful not to exclude students who haven't declared a major.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    with sql.connect(db_file) as conn:
        cur = conn.cursor()
        return cur.execute("""SELECT StudentInfo.StudentName, MajorInfo.MajorName, StudentGrades.Grade
                           FROM StudentInfo JOIN StudentGrades ON StudentInfo.StudentID == StudentGrades.StudentID
                           JOIN CourseInfo ON StudentGrades.CourseID == CourseInfo.CourseID
                           LEFT JOIN MajorInfo on StudentInfo.MajorID == MajorInfo.MajorID
                           WHERE CourseInfo.CourseName == 'Calculus'""").fetchall()


# Problem 3
def prob3(db_file="students.db"):
    """Query the given database for tuples of the form (MajorName, N) where N
    is the number of students in the specified major. Sort the results in
    descending order by the counts N, then in alphabetic order by MajorName.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    with sql.connect(db_file) as conn:
        cur = conn.cursor()
        return cur.execute("""SELECT MajorInfo.MajorName, COUNT(StudentInfo.StudentID) AS N 
                            FROM StudentInfo LEFT JOIN MajorInfo ON StudentInfo.MajorID = MajorInfo.MajorID
                            GROUP BY MajorInfo.MajorName
                            ORDER BY N DESC, MajorInfo.MajorName ASC;""").fetchall()


# Problem 4
def prob4(db_file="students.db"):
    """Query the database for tuples of the form (StudentName, N, GPA) where N
    is the number of courses that the specified student is in and 'GPA' is the
    grade point average of the specified student according to the following
    point system.

        A+, A  = 4.0    B  = 3.0    C  = 2.0    D  = 1.0
            A- = 3.7    B- = 2.7    C- = 1.7    D- = 0.7
            B+ = 3.4    C+ = 2.4    D+ = 1.4

    Order the results from greatest GPA to least.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    with sql.connect(db_file) as conn:
        cur = conn.cursor()
        return cur.execute("""SELECT StudentInfo.StudentName AS StudentName,
                           COUNT(StudentGrades.CourseID) AS N,
                           AVG(CASE StudentGrades.Grade
                           WHEN 'A+' THEN 4.0
                           WHEN 'A' THEN 4.0
                           WHEN 'A-' THEN 3.7
                           WHEN 'B+' THEN 3.4
                           WHEN 'B' THEN 3.0
                           WHEN 'B-' THEN 2.7
                           WHEN 'C+' THEN 2.4
                           WHEN 'C' THEN 2.0
                           WHEN 'C-' THEN 1.7
                           WHEN 'D+' THEN 1.4
                           WHEN 'D' THEN 1.0
                           WHEN 'D-' THEN 0.7
                           ELSE 0 END) AS GPA
                           FROM StudentInfo JOIN StudentGrades
                           ON StudentInfo.StudentID = StudentGrades.StudentID
                           GROUP BY StudentInfo.StudentID
                           ORDER BY GPA DESC;""").fetchall()


# Problem 5
def prob5(db_file="mystery_database.db"):
    """Use what you've learned about SQL to identify the outlier in the mystery
    database.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): outlier's name, outlier's ID number, outlier's eye color, outlier's height
    """
    with sql.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA case_sensitive_like = FALSE;")
        row = cur.execute("""
            SELECT rowid
            FROM table_4
            WHERE home_world LIKE '%Earth%'
        """).fetchone()

        if row is None:
            raise ValueError("No outlier found with 'Earth' in description.")

        rowid = row[0]

        eye_color, height = cur.execute("""
            SELECT eye_color, height
            FROM table_3
            WHERE rowid = ?
        """, (rowid,)).fetchone()

        ID_number = cur.execute("""
            SELECT ID_number
            FROM table_2
            WHERE rowid = ?
        """, (rowid,)).fetchone()[0]

        name = cur.execute("""
            SELECT name
            FROM table_1
            WHERE rowid = ?
        """, (rowid,)).fetchone()[0]

        return [str(name), str(ID_number), str(eye_color), str(height)]

if __name__ == "__main__":
    """with sql.connect("mystery_database.db") as conn:
        cur = conn.cursor()
        for table in ["table_1", "table_2", "table_3", "table_4"]:
            cur.execute(f"SELECT * FROM {table} LIMIT 1;")
            columns = [d[0] for d in cur.description]
            print(columns)"""
    print(prob4())
            
