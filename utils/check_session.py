from flask import render_template, redirect, url_for, session

def check_session_and_render(path, template, **params):
  if 'user_is_logged' not in session or session['user_is_logged'] == None:
    return redirect(url_for('login', next_page = url_for(path)))
  else:
    return render_template(template, **params)