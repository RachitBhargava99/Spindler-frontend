from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, session
from flask_login import current_user, login_required
import requests
from PIL import Image
from io import BytesIO
from frontend.dashboard.utils import sorted_search
import asyncio
from datetime import datetime

dash = Blueprint('dash', __name__)


# View Function - Homepage / Search Results
@dash.route('/', methods=['GET'])
def home():
    if (request.args.get('q') is not None):
        data = {
            "q": f"{request.args.get('q')}",
            "center": f"{request.args.get('center', type=str, default='')}",
            "description": "",
            "description_508": "",
            "keywords": "",
            "location": f"{request.args.get('location', type=str, default='')}",
            "media_type": "image",
            "nasa_id": f"{request.args.get('nasa-id', type=str, default='')}",
            "photographer": f"{request.args.get('photographer', type=str, default='')}",
            "secondary_creator": "",
            "title": "",
            "year_start": f"{request.args.get('start-year', type=str, default='')}",
            "year_end": f"{request.args.get('end-year', type=str, default='')}",
            "user_id": current_user.user_id if current_user.is_authenticated else -1,
            "page": f"{request.args.get('page', type=int, default=1)}"
        }
        if session.get('query') == data:
            print("Yay")
            searches = session['recent_results']
        else:
            raw_searches = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['SEARCH_URL'],
                                         json=data)
            searches = raw_searches.json()
##            session['query'] = data
##            session['recent_results'] = searches

        start_page = (request.args.get('page', type=int, default=1) - 1) * 40
        end_page = (request.args.get('page', type=int, default=1)) * 40
        focus = searches['data'][start_page:end_page]
        pn = request.args.get('page', type=int, default=1)
        max = (searches['num_ret'] - 1) // 40 + 2

        async def get_image_ratio(data):
            file = requests.get(data['links'][0]['href']).content
            image = Image.open(BytesIO(file))
            width, height = image.size
            data['image_ratio'] = height / width

        async def runner():
            tasks = []
            for each in focus:
                tasks.append(asyncio.ensure_future(get_image_ratio(each)))
            await asyncio.gather(*tasks)

        start_time = datetime.now()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner())
        loop.close()
        end_time = datetime.now()
        print(end_time - start_time)

        curr_params = ''

        print(searches)

        for each in request.args:
            if each != 'page':
                curr_params += str(each) + '=' + request.args.get(each) + '&'

        sorted_focus = sorted_search(focus)

        sorted_list = sorted_focus[0] + sorted_focus[1] + sorted_focus[2] + sorted_focus[3]

        cuts = [len(sorted_focus[0]), len(sorted_focus[0]) + len(sorted_focus[1]), len(sorted_focus[0]) + len(sorted_focus[1]) + len(sorted_focus[2])]

        login_info = {'status': False}

        if current_user.is_authenticated:
            login_info['status'] = True
            login_info['name'] = current_user.name

        return render_template('courses.html', searches=sorted_list, cuts=cuts, pre_data=data, pn=pn,
                               max=max, curr_params=curr_params, p_list=list(
                range((pn - 2 if pn > 3 else 1), (pn + 3 if pn + 3 <= max else max))), login_info=login_info)
    else:
        raw_searches = requests.get(current_app.config['ENDPOINT_ROUTE'] + current_app.config['MOST_SEARCH_URL'])
        searches = raw_searches.json()['list']
        login_info = {'status': False}

        if current_user.is_authenticated:
            login_info['status'] = True
            login_info['name'] = current_user.name

        return render_template('index.html', searches=searches, login_info=login_info)


# View Function - Dashboard
@login_required
@dash.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template('dash.html')


# View Function - Search History
@login_required
@dash.route('/search_history', methods=['GET'])
def search_history():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['SEARCH_HISTORY_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    return render_template('search_history.html', searches=data['data'])


# View Function - Now Streaming
@login_required
@dash.route('/stream', methods=['GET'])
def streamer():
    if (request.args.get('q') is not None):
        data = {
            "q": f"{request.args.get('q')}",
            "center": f"{request.args.get('center', type=str, default='')}",
            "location": f"{request.args.get('location', type=str, default='')}",
            "media_type": "image",
            "keywords": "",
            "photographer": "",
            "auth_token": current_user.auth_token
        }
        requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['NEW_STREAM_URL'], json=data)
        flash("New Stream Added Successfully!", 'success')
    raw_stream = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ALL_STREAM_URL'],
                               json={
                                   'auth_token': current_user.auth_token
                               })
    all_streams = raw_stream.json()
    print(all_streams)
    return render_template('stream.html', streams=all_streams['data'], name=current_user.name)


# View Function - Remove a Stream - id required
@login_required
@dash.route('/stream/remove/<int:id>', methods=['GET'])
def remove_stream(id):
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['REMOVE_STREAM_URL'],
                                 json={
                                     'ss_id': id,
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 1:
        flash("Stopped streaming successfully!", 'success')
    else:
        flash(data['error'], 'danger')
    return redirect(url_for('dash.streamer'))


# View Function - Add to Favorites - id required
@login_required
@dash.route('/fav/add/<int:id>', methods=['GET'])
def add_fav(id):
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['ADD_FAV_URL'],
                                 json={
                                     'result_id': id,
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 1:
        flash("Added to Favorites Successfully!", 'success')
    else:
        flash(data['error'], 'danger')
    return redirect(url_for('dash.show_fav'))


# View Function - Show All Favorites
@login_required
@dash.route('/fav/show', methods=['GET'])
def show_fav():
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['SHOW_FAV_URL'],
                                 json={
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 1:
        return render_template('fav.html', searches=data['data'])
    flash(data['error'], 'danger')
    return redirect(url_for('dash.home'))


# View Function - Remove from Favorites - id required
@login_required
@dash.route('/fav/rem/<int:id>', methods=['GET'])
def remove_fav(id):
    request_data = requests.post(current_app.config['ENDPOINT_ROUTE'] + current_app.config['REMOVE_FAV_URL'],
                                 json={
                                     'res_id': id,
                                     'auth_token': current_user.auth_token
                                 })
    data = request_data.json()
    if data['status'] == 1:
        flash("Removed from Favorites Successfully!", 'success')
    else:
        flash(data['error'], 'danger')
    return redirect(url_for('dash.show_fav'))
