create index search_enrollments_by_enrollments_student_id on
enrollments(student_id);

create index search_enrollments_by_enrollments_course_id on
enrollments(course_id);

create index search_courses_by_department_number_semester on
courses (department, number, semester);

create index search_courses_by_semester on
courses (semester);

create index search_satisfies_by_course_id on
satisfies (course_id);
