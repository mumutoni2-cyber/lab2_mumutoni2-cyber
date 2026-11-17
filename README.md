# Lab 2 Transcript Generator



## Files
- grades.csv : grade data (assignment,group,score,weight).
- grade-evaluator.py : validates the grades and reports the result.
- organizer.sh :archives the current grades in the archive folder and resets the workspace.

## grade-evaluator.py
Run: python3 grade-evaluator.py, then enter the CSV filename (example : grades.csv).

It:
1. Checks every score is between 0 and 100.
2. Checks weights total 100 (Summative = 40, Formative = 60).
3. Calculates the total grade and GPA = (Total Grade / 100) * 5.0.
4. Prints PASSED only if both Formative and Summative are at least 50%, otherwise FAILED.
5. Lists failed Formative assignments (score < 50) with the highest weight as eligible for resubmission (all of them if tied).

## organizer.sh
Run: ./organizer.sh (after chmod +x organizer.sh if needed).

It:
1. Creates an archive/ folder if missing.
2. Moves grades.csv to archive/grades_<YYYYMMDD-HHMMSS>.csv.
3. Creates a new empty grades.csv.
4. Appends the timestamp, original name and archived name to organizer.log.

Run the evaluator first: the organizer leaves grades.csv empty.
