import pandas as pd
import json


groups_sheet = pd.read_csv("DataSheets/groups.csv")
rooms_sheet = pd.read_csv("DataSheets/rooms.csv")
subjects_sheet = pd.read_csv("DataSheets/subjects.csv")
teachers_sheet = pd.read_csv("DataSheets/teachers.csv")

subject_teacher = {}
subjects = {}
groups = {}


def group_teachers():
    for teacher in teachers_sheet.iterrows():
        if teacher[1]["subject"] not in subject_teacher.keys():
            subject_teacher[teacher[1]["subject"]] = {
                "course": None,
                "seminar": None,
                "laboratory": None,
            }

        subject_types = teacher[1]["type"].split(",")

        if "TEOR" in subject_types:
            subject_teacher[teacher[1]["subject"]]["course"] = teacher[1]["id"]
        if "PRACT" in subject_types:
            subject_teacher[teacher[1]["subject"]]["seminar"] = teacher[1]["id"]
        if "LAB" in subject_types:
            subject_teacher[teacher[1]["subject"]]["laboratory"] = teacher[1]["id"]


def format_subjects():
    for subject in subjects_sheet.iterrows():
        if subject[1]["id"] not in subjects.keys():
            subjects[subject[1]["id"]] = {
                "name": subject[1]["unitate_curs"],
                "semester": [],
                "course": None,
                "seminar": None,
                "laboratory": None
            }

        subject_semesters = subject[1]["semestru"].split(",")
        for subject_semester in subject_semesters:
            if subject_semester != "":
                subjects[subject[1]["id"]]["semester"].append(int(subject_semester))

        if subject[1]["teorie"] != 0:
            hours_week = int(subject[1]["teorie"])
            hours_week = int(hours_week / 15) if hours_week % 15 == 0 else int(hours_week / 12)
            subjects[subject[1]["id"]]["course"] = {
                "teacher": subject_teacher[subject[1]["id"]]["course"],
                "groups": {
                    "ro": [],
                    "ru": [],
                    "fr": [],
                    "eng": []
                },
                "hours_w": hours_week
            }
        else:
            subjects[subject[1]["id"]]["course"] = None

        if subject[1]["practica"] != 0:
            hours_week = int(subject[1]["practica"])
            hours_week = int(hours_week / 15) if hours_week % 15 == 0 else int(hours_week / 12)
            subjects[subject[1]["id"]]["seminar"] = {
                "teacher": subject_teacher[subject[1]["id"]]["seminar"],
                "groups": {
                    "ro": [],
                    "ru": [],
                    "fr": [],
                    "eng": []
                },
                "hours_w": hours_week
            }
        else:
            subjects[subject[1]["id"]]["seminar"] = None

        if subject[1]["lab"] != 0:
            hours_week = int(subject[1]["lab"])
            hours_week = int(hours_week / 15) if hours_week % 15 == 0 else int(hours_week / 12)
            subjects[subject[1]["id"]]["laboratory"] = {
                "teacher": subject_teacher[subject[1]["id"]]["laboratory"],
                "groups": {
                    "ro": [],
                    "ru": [],
                    "fr": [],
                    "eng": []
                },
                "hours_w": hours_week
            }
        else:
            subjects[subject[1]["id"]]["laboratory"] = None


def group_groups():
    for group in groups_sheet.iterrows():
        group_id = group[1]["id"]
        group_language = group[1]["language"]
        group_subject_ids = group[1]["subject_ids"]
        group_subject_ids = group_subject_ids.replace(" ", "")
        group_subject_ids = group_subject_ids.split(",")
        # print(group_id, group_language, group_subject_ids)
        for group_subject_id in group_subject_ids:
            if group_subject_id != "":
                group_subject_id = int(group_subject_id)
                if subjects[group_subject_id]["course"] is not None:
                    subjects[group_subject_id]["course"]["groups"][group_language].append(group_id)
                if subjects[group_subject_id]["seminar"] is not None:
                    subjects[group_subject_id]["seminar"]["groups"][group_language].append(group_id)
                if subjects[group_subject_id]["laboratory"] is not None:
                    subjects[group_subject_id]["laboratory"]["groups"][group_language].append(group_id)


def extract_groups():
    for group in groups_sheet.iterrows():
        group_speciality = group[1]["speciality"]
        if group[1]["id"] not in groups.keys():
            groups[group[1]["id"]] = {
                "language": group[1]["language"],
                "speciality": group_speciality[0:group_speciality.index("-")],
                "group": group_speciality,
                "count": group[1]["nr_persoane"]
            }


def main():
    group_teachers()
    format_subjects()
    group_groups()
    extract_groups()

    with open("subject_teacher.json", "w") as f:
        f.write(json.dumps(subject_teacher, indent=4))
        f.close()

    with open("subjects.json", "w") as f:
        f.write(json.dumps(subjects, indent=4))
        f.close()

    with open("groups.json", "w") as f:
        f.write(json.dumps(groups, indent=4))
        f.close()


if __name__ == "__main__":
    main()
