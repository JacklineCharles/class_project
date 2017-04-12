from flask import Flask, render_template, request, redirect, url_for, flash, g, session, json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Ideas, Comments
from sqlalchemy import update
from flaskext.markdown import Markdown
Markdown(app)

engine = create_engine('sqlite:///userideas.db')
Base.metadata.bind = engine

DBdbsession = sessionmaker(bind = engine)
dbsession = DBdbsession()
app.secret_key = "my_key"


# Landing page
@app.route('/')
def main():
    return render_template('index.html')
    
# Sign Up
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('signup.html')

    elif request.method == 'POST':
        name = request.form['inputName']
        username = request.form['inputUserName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        newUser = User(name = name, username = username, email = email, password = password)
        dbsession.add(newUser)
        dbsession.commit()
        return redirect(url_for('sign_in'))
    
# Sign In
@app.route('/signin', methods = ['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('signin.html')

    elif request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        checkUser = dbsession.query(User).filter_by(email = email).first()
        if not checkUser:
            flash("Invalid email!")
            return render_template("signin.html")
        elif check_password_hash(checkUser.password, password):
            g.user = checkUser
            session['user'] = email
            userEmail = session['user']
            user_id_set = dbsession.query(User.id).filter_by(email = userEmail).first()
            user_id = user_id_set[0]
            return redirect(url_for('user_home'))
        else: 
            flash("Invalid credentials!")
            return render_template("signin.html")

# Home Page
@app.route('/home')
def user_home():
    if session.get('user'):
        ideas = dbsession.query(Ideas).all()        
        return render_template('userHome.html', ideas=ideas)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

# Log Out
@app.route('/logout')
def log_out():
    session.pop('user', None)
    return redirect('/')

# View Your Profile
@app.route('/profile')
def profile():
    if session.get('user'):
        userEmail = session['user']
        user_id_set = dbsession.query(User.id).filter_by(email = userEmail).first()
        user_id = user_id_set[0]
        ideas = dbsession.query(Ideas).filter_by(user_id = user_id)
        # print(type(ideas))
        return render_template('user.html', ideas=ideas)
        
    else:
        return render_template('error.html',error = 'Unauthorized Access')

# Add new Idea
@app.route('/newidea', methods = ['GET', 'POST'])
def new_idea():
    if session.get('user'):
        if request.method == 'GET':
            return render_template('newIdea.html')
        elif request.method == 'POST':
            userEmail = session['user']
            user_id_set = dbsession.query(User.id).filter_by(email = userEmail).first()
            user_id = user_id_set[0]
            name = request.form['name']
            description = request.form['description']
            newIdea = Ideas(name = name, description = description, user_id = user_id)
            user = dbsession.query(User).filter_by(id = user_id).first()
            dbsession.add(newIdea)
            dbsession.commit()
            flash("new Idea created!")
            return redirect(url_for('user_home'))

# Edit Idea
@app.route('/edit/<int:idea_id>/', methods = ['GET','POST'])
def edit_idea(idea_id):
    if session.get('user'):
        if request.method == 'GET':
            editedIdea = dbsession.query(Ideas).filter_by(id = idea_id).one()
            return render_template('editIdea.html', idea = editedIdea)
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            editedIdea = update(Ideas).where(Ideas.id == idea_id).values(name = name, description = description)
            dbsession.execute(editedIdea)
            dbsession.commit()
            flash("Idea has been edited")
            return redirect(url_for('profile'))
        else:
            return render_template('editIdea.html', idea_id = id, idea = editedIdea)

@app.route('/comment/<int:idea_id>/', methods = ['GET', 'POST'])
def comment(idea_id):
    if session.get('user'):
        idea = dbsession.query(Ideas).filter_by(id = idea_id).first()
        return render_template('idea.html', idea = idea)
    else:
        return redirect(url_for('register'))


@app.route('/upvote/<int:idea_id>/', methods = ['GET', 'POST'])
def up_vote(idea_id):
    if session.get('user'):
        idea = dbsession.query(Ideas).filter_by(id = idea_id)
        upvote_set = dbsession.query(Ideas.upvotes).filter_by(id = idea_id).first()
        oldupvotes = upvote_set[0]
        newupvotes = oldupvotes+1
        upvotes = update(Ideas).where(Ideas.id == idea_id).values(upvotes = newupvotes)
        dbsession.execute(upvotes)
        dbsession.commit()
        return redirect(url_for('comment', idea_id = idea_id))
    else:
        return render_template('error.html', error = "You are not authorised to see this")

@app.route('/downvote/<int:idea_id>/', methods = ['GET', 'POST'])
def down_vote(idea_id):
    if session.get('user'):
        idea = dbsession.query(Ideas).filter_by(id = idea_id)
        downvote_set = dbsession.query(Ideas.downvotes).filter_by(id = idea_id).first()
        olddownvotes = downvote_set[0]
        newdownvotes = olddownvotes+1
        downvotes = update(Ideas).where(Ideas.id == idea_id).values(downvotes = newdownvotes)
        dbsession.execute(downvotes) 
        dbsession.commit()
        return redirect(url_for('comment', idea_id = idea_id))
    else:
        return render_template('error.html', error = "You are not authorised to see this")

# Delete Idea
@app.route('/delete/<int:idea_id>/', methods = ['GET', 'POST'])
def delete_idea(idea_id):
    if session.get('user'):
        deletedIdea = dbsession.query(Ideas).filter_by(id = idea_id).one()
        dbsession.delete(deletedIdea)
        dbsession.commit()
        flash("Idea has been deleted")
        return redirect(url_for('profile'))
    else:
        return render_template('error.html', error = "You cannot perform this action")

if __name__ == '__main__':
    app.run(debug = True)
