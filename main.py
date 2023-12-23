import numpy as np
import pandas as pd
import json
import math


MAX_COURSE_CAPACITY = 210

groups_sheet = pd.read_csv("DataSheets/groups.csv")
rooms_sheet = pd.read_csv("DataSheets/rooms.csv")
subjects_sheet = pd.read_csv("DataSheets/subjects.csv")
teachers_sheet = pd.read_csv("DataSheets/teachers.csv")

subject_teacher = {}
subjects = {}
groups = {}
rooms = {}


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


def extract_rooms():
    for room in rooms_sheet.iterrows():
        room_id = room[1]["id "]
        room_id = room_id.replace(" ", "")
        rooms[room_id] = {
            "capacity": int(room[1]["nr_persons"]) if not math.isnan(room[1]["nr_persons"]) else None,
            "laboratory": True if room[1]["is_lab_cab"] == "1" else False
        }


def process_data():
    group_teachers()
    format_subjects()
    group_groups()
    extract_groups()
    extract_rooms()

    with open("subject_teacher.json", "w") as f:
        f.write(json.dumps(subject_teacher, indent=4))
        f.close()

    with open("subjects.json", "w") as f:
        f.write(json.dumps(subjects, indent=4))
        f.close()

    with open("groups.json", "w") as f:
        f.write(json.dumps(groups, indent=4))
        f.close()

    with open("rooms.json", "w") as f:
        f.write(json.dumps(rooms, indent=4))
        f.close()


def get_groups(
        subject_id,
        language
):
    local_groups = {
        "course": [],
        "course_hours": 0,
        "seminar": [],
        "seminar_hours": 0,
        "laboratory": [],
        "laboratory_hours": 0
    }

    if subjects[subject_id]["course"] is not None:
        local_groups["course"] = subjects[subject_id]["course"]["groups"][language]
        local_groups["course_hours"] = subjects[subject_id]["course"]["hours_w"]
    if subjects[subject_id]["seminar"] is not None:
        local_groups["seminar"] = subjects[subject_id]["seminar"]["groups"][language]
        local_groups["seminar_hours"] = subjects[subject_id]["seminar"]["hours_w"]
    if subjects[subject_id]["laboratory"] is not None:
        local_groups["laboratory"] = subjects[subject_id]["laboratory"]["groups"][language]
        local_groups["laboratory_hours"] = subjects[subject_id]["laboratory"]["hours_w"]

    return local_groups


def get_course_groups(
        subject_id,
        language
):
    return get_groups(subject_id, language)["course"]


def main():
    process_data()

    for subject_id in subjects.keys():
        speciality_groups = {
            "ro": [],
            "ru": [],
            "fr": [],
            "eng": []
        }
        for language in ["ro", "ru", "fr", "eng"]:
            course_groups = get_course_groups(subject_id, language)
            # Phase 1: place each group in standalone group
            for course_group in course_groups:
                speciality_groups[language].append(([course_group], groups[course_group]["count"]))

            # Phase 2: merge groups with same speciality
            temp_dict = {}
            for gr in speciality_groups[language]:
                if groups[gr[0][0]]["speciality"] not in temp_dict.keys():
                    temp_dict[groups[gr[0][0]]["speciality"]] = []
                temp_dict[groups[gr[0][0]]["speciality"]].append(gr)
            speciality_groups[language] = []

            for key in temp_dict.keys():
                speciality_groups[language].append(
                    (
                        [temp_dict[key][i][0][0] for i in range(len(temp_dict[key]))],
                        sum(temp_dict[key][i][1] for i in range(len(temp_dict[key])))
                    )
                )

            # Phase 3: merge groups with the lowest number of students
            while True:
                change_happened = False
                min_1, min_2 = MAX_COURSE_CAPACITY, MAX_COURSE_CAPACITY
                min_1_index, min_2_index = None, None
                for gr in speciality_groups[language]:
                    if gr[1] < min_1:
                        min_1 = gr[1]
                        min_1_index = speciality_groups[language].index(gr)
                    elif gr[1] < min_2:
                        min_2 = gr[1]
                        min_2_index = speciality_groups[language].index(gr)

                if min_1_index is not None and min_2_index is not None:
                    if speciality_groups[language][min_1_index][1] + speciality_groups[language][min_2_index][1] <= MAX_COURSE_CAPACITY:
                        speciality_groups[language][min_1_index] = (
                            speciality_groups[language][min_1_index][0] + speciality_groups[language][min_2_index][0],
                            speciality_groups[language][min_1_index][1] + speciality_groups[language][min_2_index][1]
                        )
                        speciality_groups[language].pop(min_2_index)
                        change_happened = True

                # print(min_1_index, min_1, min_2_index, min_2)

                if not change_happened:
                    break

            print(subject_id, language, speciality_groups[language])

        # TODO: Remove break
        # break


if __name__ == "__main__":
    main()
