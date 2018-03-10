from bottle import get, static_file, route, template, request, run, view
from datetime import datetime
import html


def reader(filename):
    raw_data = []
    with open(filename, mode='r', encoding='utf-8') as f:
        news = f.readlines()
        n = []
        for line in news:
            if line.find('\n') == 0:
                raw_data.append(n)
                n = []
                continue
            else:
                n.append(line)

    news_data = []
    for i in range(0, len(raw_data)):
        n = dict(
            date = raw_data[i][0],
            caption = raw_data[i][1],
            author = raw_data[i][2],
            url = raw_data[i][3],
            text = ''.join(raw_data[i][4:len(raw_data[0])])
            )
        news_data.append(n)

    return news_data


def searcher(data, query):
    result = []
    q = query.lower()
    for item in data:
        if item['author'].lower().find(q) != -1 or \
           item['caption'].lower().find(q) != -1 or \
           item['text'].lower().find(q) != -1:
            r = item
            result.append(r)

    for item in result:
        for key in item:
            if key == 'date' or key == 'url':
                continue
            else:
                item[key] = html.escape(item[key], quote=True)
                if item[key].lower().find(q) == -1:
                    continue
                else:
                    item[key] = (item[key])[:item[key].lower().find(q)] + "<span class='search'>" + \
                                (item[key])[item[key].lower().find(q):item[key].lower().find(q) + len(query)] + \
                                "</span>" + (item[key])[item[key].lower().find(q) + len(query):len(item[key])]

    return result


@get('/views/css/<filepath:re:.*\.css>')
def css(filepath):
    return static_file(filepath, root="views/css")


@get("/views/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="views/img")


@route('/')
def main_view():
    news_data = reader('news.txt')

    return template('main.html', news=news_data)
 

@route('/search', method=['GET', 'POST'])
@view('search.html')
def search_view():
    if request.method == 'GET':
        return {
            'process': False,
            'query': None,
            'result': None,
        }

    else:
        # q = request.POST['query']
        # q = request.forms.query
        q = request.POST.getunicode('query')

        if not q:
            return {
                'process': False,
                'query': q,
                'result': None,
            }
        else:
            news_data = reader('news.txt')

            result = searcher(news_data, q)

            return {
                'process': True,
                'query': q,
                'result': result,
            }
                

run(host='localhost', port=8080)