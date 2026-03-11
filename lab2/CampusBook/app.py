import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'campus-book-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campusbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    books = db.relationship('Book', backref='seller', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20))
    category = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    condition = db.Column(db.String(20))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order = db.relationship('Order', backref='book', uselist=False)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    contact_message = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    book = db.relationship('Book')


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    book = db.relationship('Book')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    search = request.args.get('search')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', 'newest')
    
    query = Book.query.filter_by(status='available')
    
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(db.or_(
            Book.title.ilike(f'%{search}%'),
            Book.author.ilike(f'%{search}%')
        ))
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    
    if sort == 'price_asc':
        query = query.order_by(Book.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Book.price.desc())
    else:
        query = query.order_by(Book.created_at.desc())
    
    books = query.paginate(page=page, per_page=12, error_out=False)
    categories = ['教材', '文学', '专业课', '考研', '公务员', '其他']
    return render_template('index.html', books=books, categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'error')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('用户名或密码错误', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        current_user.phone = request.form.get('phone')
        if request.form.get('new_password'):
            current_user.set_password(request.form.get('new_password'))
        db.session.commit()
        flash('个人信息已更新', 'success')
    return render_template('profile.html')


@app.route('/book/new', methods=['GET', 'POST'])
@login_required
def new_book():
    if request.method == 'POST':
        file = request.files.get('image')
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            isbn=request.form.get('isbn'),
            category=request.form.get('category'),
            price=float(request.form.get('price')),
            description=request.form.get('description'),
            condition=request.form.get('condition'),
            seller_id=current_user.id,
            image_url=filename
        )
        db.session.add(book)
        db.session.commit()
        flash('书籍发布成功', 'success')
        return redirect(url_for('index'))
    categories = ['教材', '文学', '专业课', '考研', '公务员', '其他']
    conditions = ['全新', '九成新', '八成新', '七成新', '六成新及以下']
    return render_template('new_book.html', categories=categories, conditions=conditions)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.seller_id != current_user.id:
        flash('无权编辑此书籍', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            book.image_url = filename
        
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.isbn = request.form.get('isbn')
        book.category = request.form.get('category')
        book.price = float(request.form.get('price'))
        book.description = request.form.get('description')
        book.condition = request.form.get('condition')
        db.session.commit()
        flash('书籍信息已更新', 'success')
        return redirect(url_for('book_detail', book_id=book.id))
    
    categories = ['教材', '文学', '专业课', '考研', '公务员', '其他']
    conditions = ['全新', '九成新', '八成新', '七成新', '六成新及以下']
    return render_template('edit_book.html', book=book, categories=categories, conditions=conditions)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.seller_id != current_user.id:
        flash('无权删除此书籍', 'error')
        return redirect(url_for('index'))
    
    CartItem.query.filter_by(book_id=book.id).delete()
    db.session.delete(book)
    db.session.commit()
    flash('书籍已删除', 'success')
    return redirect(url_for('index'))


@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.book.price for item in cart_items if item.book.status == 'available')
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/cart/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    book = Book.query.get_or_404(book_id)
    if book.seller_id == current_user.id:
        flash('不能购买自己的书籍', 'error')
        return redirect(url_for('book_detail', book_id=book_id))
    
    existing = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if existing:
        flash('书籍已在购物车中', 'info')
        return redirect(url_for('book_detail', book_id=book_id))
    
    if book.status != 'available':
        flash('书籍已下架', 'error')
        return redirect(url_for('book_detail', book_id=book_id))
    
    cart_item = CartItem(user_id=current_user.id, book_id=book_id)
    db.session.add(cart_item)
    db.session.commit()
    flash('已加入购物车', 'success')
    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        flash('无权操作', 'error')
        return redirect(url_for('cart'))
    db.session.delete(cart_item)
    db.session.commit()
    flash('已从购物车移除', 'success')
    return redirect(url_for('cart'))


@app.route('/order/create', methods=['POST'])
@login_required
def create_order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('购物车为空', 'error')
        return redirect(url_for('cart'))
    
    contact_message = request.form.get('contact_message', '')
    
    for item in cart_items:
        if item.book.status == 'available':
            order = Order(
                buyer_id=current_user.id,
                book_id=item.book.id,
                total_price=item.book.price,
                contact_message=contact_message
            )
            item.book.status = 'sold'
            db.session.add(order)
    
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('订单创建成功', 'success')
    return redirect(url_for('orders'))


@app.route('/orders')
@login_required
def orders():
    buy_orders = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_at.desc()).all()
    sell_orders = Order.query.join(Book).filter(Book.seller_id == current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', buy_orders=buy_orders, sell_orders=sell_orders)


@app.route('/order/<int:order_id>/confirm', methods=['POST'])
@login_required
def confirm_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.buyer_id != current_user.id:
        flash('无权操作', 'error')
        return redirect(url_for('orders'))
    order.status = 'completed'
    db.session.commit()
    flash('已确认收货', 'success')
    return redirect(url_for('orders'))


@app.route('/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.buyer_id != current_user.id:
        flash('无权操作', 'error')
        return redirect(url_for('orders'))
    order.book.status = 'available'
    order.status = 'cancelled'
    db.session.commit()
    flash('订单已取消', 'success')
    return redirect(url_for('orders'))


@app.route('/messages')
@login_required
def messages():
    received = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).all()
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    return render_template('messages.html', received=received, sent=sent)


@app.route('/message/send/<int:book_id>', methods=['POST'])
@login_required
def send_message(book_id):
    book = Book.query.get_or_404(book_id)
    if book.seller_id == current_user.id:
        flash('不能给自己发消息', 'error')
        return redirect(url_for('book_detail', book_id=book_id))
    
    content = request.form.get('content')
    if not content:
        flash('消息内容不能为空', 'error')
        return redirect(url_for('book_detail', book_id=book_id))
    
    message = Message(
        sender_id=current_user.id,
        receiver_id=book.seller_id,
        content=content,
        book_id=book_id
    )
    db.session.add(message)
    db.session.commit()
    flash('消息已发送', 'success')
    return redirect(url_for('book_detail', book_id=book_id))


@app.route('/message/<int:message_id>/read', methods=['POST'])
@login_required
def mark_as_read(message_id):
    message = Message.query.get_or_404(message_id)
    if message.receiver_id != current_user.id:
        flash('无权操作', 'error')
        return redirect(url_for('messages'))
    message.is_read = True
    db.session.commit()
    return jsonify({'success': True})


@app.route('/my-books')
@login_required
def my_books():
    books = Book.query.filter_by(seller_id=current_user.id).order_by(Book.created_at.desc()).all()
    return render_template('my_books.html', books=books)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
