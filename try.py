@app.route('/one/<username>', methods=['GET', 'POST'])
@login_required
def one(username):
    user = User.query.filter_by(username=username).first_or_404()
    FacultyU = Faculty.query.get(user.Faculty_id)
    DepartmentU = Department.query.get(user.Department_id)
    Year = "Весна 2020"
    Course = 1
    #БАКАЛАВРЫ
    deg = Degree.query.get(1)

    D = Direction.query.join(Profile, (Profile.Direction_id == Direction.id)).filter(Profile.Department_id == DepartmentU.id, Direction.Degree_id == deg.id)
    P = Profile.query.join(Direction, (Direction.id == Profile.Direction_id)).filter(Profile.Department_id == DepartmentU.id, Direction.Degree_id == deg.id)
    G = groupStud.query.join(Profile, (Profile.id == groupStud.Profile_id)).join(Direction, (Direction.id == Profile.Direction_id)).filter(Profile.Department_id == DepartmentU.id, Direction.Degree_id == deg.id, groupStud.id.like("6%"))

    form = OneForm()

    form.Direction_id.choices = [(d.id, d.name) for d in D.all()]
    form.Profile_id.choices = [(d.id, d.name) for d in P.all()]
    form.Group_id.choices = [(d.id) for d in G.all()]

"""    if form.validate_on_submit1():
        forms = Form(NumForm = '1',
                    user_id = user.username,
                    Faculty_id = FacultyU.id,
                    Department_id = DepartmentU.id,
                    Degree_id = Degree.id,
                    Year = Year,
                    Direction_id = form.Direction_id.data,
                    Profile_id = form.Profile_id.data,
                    Course = Course,
                    Group_id = form.Group_id.data,
                    NumStudents = form.NumStudents.data)
        db.session.add(forms)
        db.session.commit()
        return render_template('index.html', title='Home Page')"""

"    return render_template('one.html', FacultyU = FacultyU, DepartmentU = DepartmentU, Year = Year, Course = Course, deg = deg, title='one', form=form)"
