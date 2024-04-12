from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from app.forms import CustomerRegForm, LoginForm
from app.models import Customer, Goods, Orders, OrderLineItem
import config
import random
import datetime

app = Flask(__name__)
# 从config模块中加载配信息
app.config.from_object(config)
# 创建SQLAlchemy对象db
db = SQLAlchemy(app)


# 注册实现
@app.route('/reg', methods=['GET', 'POST'])
def register():
    form = CustomerRegForm()
    if request.method == 'POST':
        if form.validate():
            # 从表单上取出数据添加到Customer数据模型对象中
            new_customer = Customer()
            new_customer.id = form.userid.data
            new_customer.name = form.name.data
            new_customer.password = form.password.data
            new_customer.address = form.address.data
            new_customer.birthday = form.birthday.data
            new_customer.phone = form.phone.data

            db.session.add(new_customer)
            db.session.commit()

            print('Registrar successful')
            return render_template('customer_reg_success.html', form=form)
        # else:
        #     return render_template('customer_reg.html', form=form)

    return render_template('customer_reg.html', form=form)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            c = db.session.query(Customer).filter_by(id=form.userid.data).first()
            if c is not None and c.password == form.password.data:
                print('Login successful')
                customer = {}
                customer['id'] = c.id
                customer['name'] = c.name
                customer['password'] = c.password
                customer['address'] = c.address
                customer['phone'] = c.phone
                customer['birthday'] = c.birthday
                # customer保持到HTTP Session
                session['customer'] = customer

                return redirect(url_for('main'))
            else:
                flash('El cuenta de usuario y la contraseña que ingresó son incorrectos.')
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/main')
def main():
    if 'customer' not in session.keys():
        flash('Aún no has iniciado sesión. Por favor, inicia sesión.')
        return redirect(url_for('login'))
    return render_template('main.html')


# 显示商品列表
@app.route('/list')
def show_goods_list():
    if 'customer' not in session.keys():
        flash('Aún no has iniciado sesión. Por favor, inicia sesión.')
        return redirect(url_for('login'))

    goodslist = db.session.query(Goods).all()
    return render_template('goods_list.html', list=goodslist)


# 显示商品详细
@app.route('/detail')
def show_goods_detail():
    if 'customer' not in session.keys():
        flash('Aún no has iniciado sesión. Por favor, inicia sesión.')
        return redirect(url_for('login'))

    goodsid = request.args['id']
    goods = db.session.query(Goods).filter_by(id=goodsid).first()

    return render_template('goods_detail.html', goods=goods)


# 添加购物车
@app.route('/add')
def add_cart():
    if 'customer' not in session.keys():
        flash('Aún no has iniciado sesión. Por favor, inicia sesión.')
        return redirect(url_for('login'))

    goodsid = int(request.args['id'])
    goodsname = request.args['name']
    goodsprice = float(request.args['price'])

    # 判断Session中是否有购物车数据
    if 'cart' not in session.keys():
        session['cart'] = []  # 购物车是一个列表结构

    cart = session['cart']
    # 声明flag标志,如果0表示购物车中没有当前商品,1表示购物车总有当前商品
    flag = 0
    for item in cart:
        if item[0] == goodsid:  # item[0]保存在购物车的商品id
            item[3] += 1  # item[3]保存在购物车的商品数量,对当前数量+1
            flag = 1
            break

    if flag == 0:
        # 第一次添加商品到购物车数量是1
        cart.append([goodsid, goodsname, goodsprice, 1])

    session['cart'] = cart

    print(cart)

    flash('Se han agregado los productos【' + goodsname + '】cart')
    return redirect(url_for('show_goods_list'))


# 查看购物车
@app.route('/cart')
def show_cart():
    if 'customer' not in session.keys():
        flash('Aún no has iniciado sesión. Por favor, inicia sesión.')
        return redirect(url_for('login'))

    if 'cart' not in session.keys():
        return render_template('cart.html', list=[], total=0.0)

    cart = session['cart']
    list = []
    total = 0.0
    for item in cart:
        # 购物车每一个元素[商品id, 商品名称, 商品价格, 商品数量]
        # 添加一个小计
        subtotal = item[2] * item[3]
        total += subtotal
        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)

    return render_template('cart.html', list=list, total=total)


# 提交订单
@app.route('/submit_order', methods=['POST'])
def submit_order():
    # 从表单中取出数据添加到Orders模式对象中
    orders = Orders()
    # 生成订单id,规则当前时间戳+一位随机数
    n = random.randint(0, 9)
    d = datetime.datetime.today()
    orderid = str(int(d.timestamp() * 1e6)) + str(n)
    orders.id = orderid
    orders.orderdate = d.strftime('%Y-%m-%d %H:%M:%S')
    orders.status = 1  # 1 待付款 0 已付款

    db.session.add(orders)
    # 购物车每一个元素[商品id, 商品名称, 商品价格, 商品数量] Cada artículo en el carrito [ID, Nombre, Precio, Cantidad
    cart = session['cart']
    total = 0.0
    for item in cart:
        quantity = request.form['quantity_' + str(item[0])]
        try:
            quantity = int(quantity)
        except:
            quantity = 0

        # 小计 Subtotal
        subtotal = item[2] * quantity
        total += subtotal

        order_line_item = OrderLineItem()
        order_line_item.quantity = quantity
        order_line_item.goodsid = item[0]
        order_line_item.orderid = orderid
        order_line_item.subtotal = subtotal

        db.session.add(order_line_item)

    orders.total = total
    # 提交事务 Enviar la transacción
    db.session.commit()

    # 清除购物车 Vaciar el carrito de compras
    session.pop('cart', None)

    return render_template('order_finish.html', orderid=orderid)