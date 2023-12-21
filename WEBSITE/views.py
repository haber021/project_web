from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from WEBSITE.models import Note  # Fix the import statement
from WEBSITE import db
import json

views = Blueprint('views', __name__)

# ... (rest of the code remains unchanged)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_content = request.form.get('note')

        if len(note_content) < 1:
            flash('note is too short', category='error')
        else:
            current_date_time = datetime.utcnow()
            new_note = Note(data=current_date_time, content=note_content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note added!', category='success')
    
    # Retrieve all the notes for the current user from the database
    user_notes = Note.query.filter_by(user_id=current_user.id).all()

    return render_template("home.html", user=current_user, notes=user_notes)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})