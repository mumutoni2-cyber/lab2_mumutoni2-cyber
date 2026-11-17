import csv
import sys
import os

required_columns = ['assignment', 'group', 'score', 'weight']



def fail(message):
    print(f"Error: {message}")
    sys.exit(1)

def load_csv_data():
  
    filename = input("Enter the name of the CSV file to process (example: grades.csv): ").strip()

    if not filename:
        fail("There was no  filename entered. Please type an existing  file name such as grades.csv.")
    if not os.path.exists(filename):
        fail(f"The file '{filename}' was not found. Check the spelling of if the file exists .")

    assignments = []

    try:
        file = open(filename, 'r')
    except:
        fail("Could not open '" + filename + "'.")

    reader = csv.DictReader(file)


    if reader.fieldnames is None:
        fail("'" + filename + "' is empty.")
    for col in required_columns:
        if col not in reader.fieldnames:
            fail("Missing column '" + col + "'. Header should be: assignment,group,score,weight")

    row_number = 1 
    for row in reader:
        row_number += 1
        name = row['assignment'].strip()
        group = row['group'].strip()

        if group.lower() != 'formative' and group.lower() != 'summative':
            fail("Row " + str(row_number) + ": group must be Formative or Summative, not '" + group + "'.")

     
        try:
            score = float(row['score'])
            weight = float(row['weight'])
        except:
            fail("Row " + str(row_number) + ": score and weight must be numbers (example: 85 or 72.5).")

        assignments.append({
            'assignment': name,
            'group': group,
            'score': score,
            'weight': weight
        })
    file.close()

    if len(assignments) == 0:
        fail("'" + filename + "' has no assignment rows.")
    return assignments


def evaluate_grades(data):
    print("\n--- Processing Grades ---")

 
    for a in data:
        if not 0 <= a['score'] <= 100:
            fail(f"invalid score {a['score']:g} for '{a['assignment']}' "
                 "(must be between 0 and 100).")

    total_w = sum(a['weight'] for a in data)
    formative = [a for a in data if a['group'].strip().lower() == 'formative']
    summative = [a for a in data if a['group'].strip().lower() == 'summative']
    formative_weight = sum(a['weight'] for a in formative)
    summative_weight = sum(a['weight'] for a in summative)

    errors = []
    if any(a['weight'] < 0 for a in data):
        errors.append("Weights cannot be negative.")
    if total_w != 100:
        errors.append(f"Total weight is {total_w:g}, expected 100.")
    if summative_weight != 40:
        errors.append(f"Summative weight is {summative_weight:g}, expected 40.")
    if formative_weight != 60:
        errors.append(f"Formative weight is {formative_weight:g}, expected 60.")
    if errors:
        fail(" ".join(errors))

  
    formative_points = sum(a['score'] * a['weight'] / 100 for a in formative)
    summative_points = sum(a['score'] * a['weight'] / 100 for a in summative)
    total_grade = formative_points + summative_points
    gpa = (total_grade / 100) * 5.0

 
    formative_percentage = formative_points / formative_weight * 100
    summative_percentage = summative_points / summative_weight * 100
    passed = formative_percentage >= 50 and summative_percentage >= 50


    failed = [a for a in formative if a['score'] < 50]
    if failed:
        top = max(a['weight'] for a in failed)
        resubmit = ", ".join(a['assignment'] for a in failed if a['weight'] == top)
    else:
        resubmit = "None"


    print(f"{'Assignment':<38}{'Category':<10}{'Grade (%)':>10}{'Weight':>8}{'Final weight':>14}")
    for a in data:
        category = 'FA' if a['group'].strip().lower() == 'formative' else 'SA'
        final_weight = a['score'] * a['weight'] / 100
        print(f"{a['assignment']:<38}{category:<10}{a['score']:>10g}{a['weight']:>8g}{final_weight:>14g}")
    print(f"{'Formatives (60)':<38}{'':<10}{'':>10}{'':>8}{formative_points:>14g}")
    print(f"{'Summatives (40)':<38}{'':<10}{'':>10}{'':>8}{summative_points:>14g}")
    print(f"{'GPA':<38}{gpa:g}")
    print()
    print(f"{'Status':<38}{'PASSED' if passed else 'FAILED'}")
    print(f"{'Available for resubmission':<38}{resubmit}")


if __name__ == "__main__":
    evaluate_grades(load_csv_data())
