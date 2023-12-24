import numpy as np
import pandas as pd
import json
import math


MAX_COURSE_CAPACITY = 210

groups_sheet = pd.read_csv("DataSheets/groups.csv")
rooms_sheet = pd.read_csv("DataSheets/rooms.csv")
subjects_sheet = pd.read_csv("DataSheets/subjects.csv")
teachers_sheet = pd.read_csv("DataSheets/teachers.csv")

course_code = [
    "mon_per_1", "mon_per_2", "mon_per_3", "mon_per_4", "mon_per_5", "mon_per_6", "mon_per_7",
    "tue_per_1", "tue_per_2", "tue_per_3", "tue_per_4", "tue_per_5", "tue_per_6", "tue_per_7",
    "wed_per_1", "wed_per_2", "wed_per_3", "wed_per_4", "wed_per_5", "wed_per_6", "wed_per_7",
    "thu_per_1", "thu_per_2", "thu_per_3", "thu_per_4", "thu_per_5", "thu_per_6", "thu_per_7",
    "fri_per_1", "fri_per_2", "fri_per_3", "fri_per_4", "fri_per_5", "fri_per_6", "fri_per_7",
    "sat_per_1", "sat_per_2", "sat_per_3", "sat_per_4", "sat_per_5", "sat_per_6", "sat_per_7"
]

subject_teacher = {}
subjects = {}
groups = {}
rooms = {}

teacher_table = [{}, {}]
group_table = [{}, {}]


def group_teachers() -> None:
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


def format_subjects() -> None:
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


def group_groups() -> None:
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


def extract_groups() -> None:
    for group in groups_sheet.iterrows():
        group_speciality = group[1]["speciality"]
        if group[1]["id"] not in groups.keys():
            groups[group[1]["id"]] = {
                "language": group[1]["language"],
                "speciality": group_speciality[0:group_speciality.index("-")],
                "group": group_speciality,
                "count": group[1]["nr_persoane"]
            }


def extract_rooms() -> None:
    for room in rooms_sheet.iterrows():
        room_id = room[1]["id "]
        room_id = room_id.replace(" ", "")
        rooms[room_id] = {
            "capacity": int(room[1]["nr_persons"]) if not math.isnan(room[1]["nr_persons"]) else None,
            "laboratory": True if room[1]["is_lab_cab"] == "1" else False
        }


def format_teacher_table() -> None:
    for teacher in teachers_sheet.iterrows():
        teacher_id = teacher[1]["id"]
        teacher_table[0][teacher_id] = {}
        teacher_table[1][teacher_id] = {}
        for course in course_code:
            if teacher[1][course] != 0:
                teacher_table[0][teacher_id][course] = {}
                teacher_table[1][teacher_id][course] = {}


def format_group_table() -> None:
    for group in groups:
        group_table[0][group] = []
        group_table[1][group] = []


def process_data() -> None:
    group_teachers()
    format_subjects()
    group_groups()
    extract_groups()
    extract_rooms()
    format_teacher_table()
    format_group_table()

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

    with open("teacher_table_sem1.json", "w") as f:
        f.write(json.dumps(teacher_table[0], indent=4))
        f.close()

    with open("teacher_table_sem2.json", "w") as f:
        f.write(json.dumps(teacher_table[1], indent=4))
        f.close()


def get_groups(
        subject_id,
        language
) -> dict:
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


def get_course_groups() -> dict:
    grs = {}

    for subject_id in subjects.keys():
        grs[subject_id] = {}
        speciality_groups = {
            "ro": [],
            "ru": [],
            "fr": [],
            "eng": []
        }
        for language in ["ro", "ru", "fr", "eng"]:
            course_groups = get_groups(subject_id, language)["course"]
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

                if not change_happened:
                    break

            # print(subject_id, language, speciality_groups[language])
            grs[subject_id][language] = speciality_groups[language]

    return grs


def order_teachers() -> dict:
    teachers_hours = {}
    for teacher in teachers_sheet.iterrows():
        teacher_hours = 0
        for course in course_code:
            teacher_hours += teacher[1][course]
        teachers_hours[teacher[1]["id"]] = teacher_hours
    teachers_hours = dict(sorted(teachers_hours.items(), key=lambda item: item[1], reverse=False))
    return teachers_hours


def main():
    process_data()

    ordered_teachers = order_teachers()
    for teacher in ordered_teachers.keys():
        teacher_subject = None
        teacher_subject_type = []
        for subject in subject_teacher.keys():
            if subject_teacher[subject]["course"] == teacher:
                teacher_subject = subject
                teacher_subject_type.append("course")
            if subject_teacher[subject]["seminar"] == teacher:
                teacher_subject = subject
                teacher_subject_type.append("seminar")
            if subject_teacher[subject]["laboratory"] == teacher:
                teacher_subject = subject
                teacher_subject_type.append("laboratory")
        # print(teacher, ordered_teachers[teacher], teacher_subject, teacher_subject_type)
        for semester in subjects[teacher_subject]["semester"]:
            semester = (semester + 1) % 2
            for s_type in ["course", "seminar", "laboratory"]:
                if subjects[teacher_subject][s_type] is not None:
                    for lang in subjects[teacher_subject][s_type]["groups"].keys():
                        if s_type != "course":
                            for group in subjects[teacher_subject][s_type]["groups"][lang]:
                                for course in teacher_table[semester][teacher].keys():
                                    if course not in group_table[semester][group] and teacher_table[semester][teacher][course] == {}:
                                        group_table[semester][group].append(course)
                                        teacher_table[semester][teacher][course] = {
                                            "subject": teacher_subject,
                                            "group": group,
                                            "type": s_type,
                                            "language": lang,
                                        }
                                        break
                        else:
                            for group in get_course_groups()[teacher_subject][lang]:
                                for course in teacher_table[semester][teacher].keys():
                                    if course not in group_table[semester][group[0][0]] and teacher_table[semester][teacher][course] == {}:
                                        group_table[semester][group[0][0]].append(course)
                                        teacher_table[semester][teacher][course] = {
                                            "subject": teacher_subject,
                                            "group": group[0],
                                            "type": s_type,
                                            "language": lang,
                                        }
                                        break

    with open("teacher_table_sem1.json", "w") as f:
        f.write(json.dumps(teacher_table[0], indent=4))
        f.close()

    with open("teacher_table_sem2.json", "w") as f:
        f.write(json.dumps(teacher_table[1], indent=4))
        f.close()


if __name__ == "__main__":
    main()
