import asyncio
import logging

from flask import Flask, render_template, request
from twscrape import AccountsPool, API
from twscrape.logger import set_log_level

loop = asyncio.get_event_loop()
app = Flask(__name__)
pool = AccountsPool('../accounts.db')
api = API(pool)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    if 'Mac OS X' in user_agent or 'iOS' in user_agent:
        return render_template('index.html', show_install=True)
    else:
        return render_template('index.html', show_install=False)


@app.route('/api/nab-tweet/<int:tweet_id>')
async def get_tweet(tweet_id):
    tweet = await api.tweet_details(tweet_id)
    types = []
    media = []
    if tweet.media:
        for m in tweet.media:
            if m.type == "animated_gif" or m.type == "video":
                types.append(m.type)
                #  Get the highest bitrate video, ignore if bitrate is None
                m.videoInfo.variants.sort(key=lambda x: x.bitrate if x.bitrate is not None else 0, reverse=True)
                media.append(m.videoInfo.variants[0].url)
            elif m.type == "photo":
                types.append('jpg')
                # Append :orig to the end of the url to get the highest quality image
                media.append(m.url + ':orig')

    return {
        'username': tweet.user.username,
        'text': tweet.rawContent,
        'types': types,
        'media': media
    }


async def setup_accounts():
    global api
    await pool.login_all()
    api = API(pool)


if __name__ == '__main__':
    set_log_level('DEBUG')
    loop.run_until_complete(setup_accounts())
    app.run(host='0.0.0.0')

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)