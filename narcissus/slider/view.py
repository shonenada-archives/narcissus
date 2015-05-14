from flask import Blueprint, render_template


slider_app = Blueprint('slider', __name__)


@slider_app.route('/slider')
def slider_index():
    return render_template('slider.html')
