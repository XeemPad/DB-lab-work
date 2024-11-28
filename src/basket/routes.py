from flask import Blueprint, session, redirect, url_for, render_template, current_app, request
from database.sql_provider import SQLProvider
import os
from cache.wrapper import fetch_from_cache
from database.select import select_dict
from basket.model_route import model_route_transaction_order


basket_blueprint = Blueprint('basket_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@basket_blueprint.route('/', methods=['GET'])
def basket_index():
    db_config = current_app.config['db_config']
    cache_config = current_app.config['cache_config']
    cache_select_dict = fetch_from_cache('items_cached', cache_config)(select_dict)
    _sql = provider.get('all_goods.sql')
    products = cache_select_dict(db_config, _sql)
    current_basket = session.get('basket',{}) # get basket or return default={}
    print("basketonload:",session.get('basket',{}))
    current_basket = form_basket(current_basket)
    return render_template('basket_dynamic.html', products=products, basket=current_basket)

@basket_blueprint.route('/', methods=['POST'])
def basket_main():
    db_config = current_app.config['db_config']
    print("BASKET=", session.get('basket', []))
    if request.form.get('buy'):
        # adding to basket
        if not 'basket' in session:
            session['basket'] = dict()
        _sql = provider.get('one_good.sql', e_prod_id=int(request.form['product_display']))
        product = select_dict(db_config, _sql)[0]
        print(product)
        current_basket = session.get('basket', {})

        # сессия поддерживает сериализацию через json, поэтому ключ может быть только строчкой
        # сессия не запоминает изменения значений по ключу, только добавление или удалени
        # поэтому нужно вручную указывать изменение сессии

        if str(product['prod_id']) in current_basket:
            prid = product['prod_id']
            amount = int(session['basket'][str(prid)])
            session['basket'][str(prid)] = str(amount+1)
            session.modified = True
        else:
            print("NEW PRODUCT")
            prid = product['prod_id']
            session['basket'][str(prid)] = '1'
            print(session['basket'])
            session.modified = True

    if request.form.get('product_display_plus'):
        # increasing count in basket
        _sql = provider.get('one_good.sql', e_prod_id=int(request.form['product_display']))
        product = select_dict(db_config, _sql)[0]
        amount = int(session['basket'][str(product['prod_id'])])
        session['basket'][str(product['prod_id'])] = str(amount + 1)
        session.modified = True

    if request.form.get('product_display_minus'):
        # decreasing count in basket
        _sql = provider.get('one_good.sql', e_prod_id=int(request.form['product_display']))
        product = select_dict(db_config, _sql)[0]
        amount = int(session['basket'][str(product['prod_id'])])
        if amount == 1:
            session['basket'].pop(str(product['prod_id']))
        else:
            session['basket'][str(product['prod_id'])] = str(amount-1)
        session.modified = True

    return redirect(url_for('basket_bp.basket_index'))

@basket_blueprint.route('/clear_basket')
def clear_basket():
    if session.get('basket',{}):
        session.pop('basket')
    return redirect(url_for('basket_bp.basket_index'))

@basket_blueprint.route('/save_order')
def save_order():
    print("a")
    if not session.get('basket',{}):
        return redirect(url_for('basket_bp.basket_index'))
    if not session.get('user_id',""):
        return render_template("error.html", message="Вы не авторизованы на сайте, авторизируйтесь для регистрации заказа")
    print("Order success")
    current_basket = session.get('basket', {})
    user_id = session.get('user_id', -1)
    result = model_route_transaction_order(current_app.config['db_config'], provider, current_basket, user_id)
    if result.status:
        clear_basket()
        return render_template("order_finish.html", order_id = result.result[0])
    else:
        return render_template("error.html", message="Заказ не был создан")


def form_basket(current_basket : dict):
    basket = []
    for k,v in current_basket.items():
        _sql = provider.get('one_good.sql', e_prod_id=k)
        product = select_dict(current_app.config['db_config'], _sql)[0]
        product['amount'] = v
        basket.append(product)
    return basket




