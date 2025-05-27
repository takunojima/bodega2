from flask import render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm
from app import db
import requests
from urllib.parse import urlencode

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/line/login')
def line_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    params = {
        'response_type': 'code',
        'client_id': current_app.config['LINE_CHANNEL_ID'],
        'redirect_uri': current_app.config['LINE_CALLBACK_URL'],
        'state': 'random_state',  # セキュリティのため、実際の実装ではランダムな文字列を生成して使用
        'scope': 'profile openid'
    }
    
    line_auth_url = f"https://access.line.me/oauth2/v2.1/authorize?{urlencode(params)}"
    return redirect(line_auth_url)

@bp.route('/line/callback')
def line_callback():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    error = request.args.get('error')
    if error:
        flash('LINE認証でエラーが発生しました')
        return redirect(url_for('auth.login'))
    
    code = request.args.get('code')
    
    # アクセストークンを取得
    token_response = requests.post(
        'https://api.line.me/oauth2/v2.1/token',
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': current_app.config['LINE_CALLBACK_URL'],
            'client_id': current_app.config['LINE_CHANNEL_ID'],
            'client_secret': current_app.config['LINE_CHANNEL_SECRET']
        }
    )
    
    token_data = token_response.json()
    
    if 'error' in token_data:
        flash('LINEログインに失敗しました')
        return redirect(url_for('auth.login'))
    
    # ユーザープロフィールを取得
    profile_response = requests.get(
        'https://api.line.me/v2/profile',
        headers={'Authorization': f"Bearer {token_data['access_token']}"}
    )
    
    profile_data = profile_response.json()
    
    # ユーザーを検索または作成
    user = User.query.filter_by(line_id=profile_data['userId']).first()
    if not user:
        # 新規ユーザーを作成
        user = User(
            username=profile_data.get('displayName', 'LINEユーザー'),
            line_id=profile_data['userId'],
            line_access_token=token_data['access_token']
        )
        db.session.add(user)
        db.session.commit()
    else:
        # 既存ユーザーのアクセストークンを更新
        user.line_access_token = token_data['access_token']
        db.session.commit()
    
    login_user(user)
    return redirect(url_for('main.index')) 