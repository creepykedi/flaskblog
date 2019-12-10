from flask import request, render_template, Blueprint
from flaskblog.unpackaged.models import Post


# users is just name
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    # first page is default, only accepts int as page num
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title='Home')

@main.route('/about')
def about():
    return render_template('about.html', title='About')