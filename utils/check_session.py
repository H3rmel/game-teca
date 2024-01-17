from flask import render_template, redirect, url_for, session


"""
    Check if the user is logged in and render a template.

    Args:
        path (str): The path of the current page.
        template (str): The name of the template to render.
        **params: Additional keyword arguments to pass to the template.

    Returns:
        If the user is not logged in, redirects to the login page with the current path as the next page.
        If the user is logged in, renders the specified template with the given parameters.

"""
def check_session_and_render(path, template, **params):
    if 'user_is_logged' not in session or session['user_is_logged'] == None:
        return redirect(url_for('login', next_page=url_for(path)))
    else:
        return render_template(template, **params)
