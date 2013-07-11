import hackbright_app
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")

@app.route("/add_project")
def add_project():
    return render_template("add_project.html")

@app.route("/add_grade")
def add_grade():
    return render_template("add_grade.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    grades = hackbright_app.get_grades_by_student(row[0], row[1])

    return render_template("student_info.html", first_name = row[0],
                                            last_name = row[1],
                                            github = row[2],
                                            grades = grades)

@app.route("/new_student")
def make_student():
    hackbright_app.connect_to_db()
    first = request.args.get("first")
    last = request.args.get("last")
    github = request.args.get("github")
    hackbright_app.make_new_student(first, last, github)
    return redirect("/student?github="+github)

@app.route("/project")
def get_project():
    hackbright_app.connect_to_db()
    project_name = request.args.get("name")
    grades = hackbright_app.get_grades_by_project(project_name)

    return render_template("project_info.html", name = project_name,
                                                grades = grades)

@app.route("/new_project")
def make_project():
    hackbright_app.connect_to_db()
    ptitle = request.args.get("ptitle")
    description = request.args.get("description")
    max_score = request.args.get("max_score")
    hackbright_app.make_new_project(ptitle, description, max_score)
    return redirect("/project?name="+ptitle)

@app.route("/new_grade")
def make_grade():
    hackbright_app.connect_to_db()
    grade = request.args.get("grade")
    ptitle = request.args.get("title")
    github = request.args.get("github")
    hackbright_app.update_grade(grade, ptitle, github)
    return redirect("/student?github="+github)


if __name__ == "__main__":
    app.run(debug=True)
