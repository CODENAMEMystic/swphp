# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for


crud = Blueprint('crud', __name__)


# [START list]
@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    orders, next_page_token = get_model().list(cursor=token)
    inventorys, next_page_token = get_model().glist(cursor=token)

    return render_template(
        "list.html",
        inventorys=inventorys,
        next_page_token=next_page_token)
# [END list]

@crud.route('/orders', methods=['GET', 'POST'])
def glist():
		
	token = request.args.get('page_token', None)
	if token:
		token = token.encode('utf-8')

	orders, next_page_token = get_model().list(cursor=token)
	

	return render_template(
		"orderView.html",
		orders=orders,
		next_page_token=next_page_token)


    
        

@crud.route('/<id>')
def view(id):
    order = get_model().read(id)
    return render_template("view.html", action="REVIEW", order=order)
    
@crud.route('/<id>/review')
def review(id):
    order = get_model().read(id)
    return render_template("view2.html", action="REVIEW", order=order)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        orders = get_model().create(data)
        
        return redirect(url_for('.view', id=orders['id']))

    return render_template("form.html", action="CREATE AN", orders={})
# [END add]

@crud.route('/<id>/add2', methods=['GET', 'POST'])
def add2(id):
    order = get_model().read(id)
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        orders = get_model().create(data)
        
        return redirect(url_for('.view', id=orders['id']))

    return render_template("form2.html", action="CREATE AN", orders={}, order=order)


# [END login]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    order = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        order = get_model().update(data, id)

        return redirect(url_for('.view', id=order['id']))

    return render_template("form.html", action="EDIT", orders=order)

@crud.route('/<id>/editI', methods=['GET', 'POST'])
def editI(id):
    inventory = get_model().readI(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        inventory = get_model().updateI(data, id)

        return redirect("/m/"+id+"/editI")

    return render_template("inventoryform.html", action="EDIT", inventory=inventory)
    
@crud.route('/<id>/editO', methods=['GET', 'POST'])
def editO(id):
    order = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        order = get_model().update(data, id)

        return redirect("/m/orders")

    return render_template("form.html", action="EDIT", orders=order)

@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
    
@crud.route('/<id>/deleteO')
def deleteO(id):
    get_model().delete(id)
    return redirect('m/orders')