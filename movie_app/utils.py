from collections import Counter


def format_output(data, request):
    rdata = data.json()
    host = request.get_host()
    path = request.path
    valNext = None
    valPrev = None
    if rdata['next'] != None:
        valNext = rdata['next'].split('?')[1]
    if rdata['previous'] != None:
        if len(rdata['previous'].split('?')) == 1:
            rdata['previous'] = 'http://'+host+path
    if rdata['previous'] != None and len(rdata['previous'].split('?')) > 1:
        valPrev = rdata['previous'].split('?')[1]
    if valNext:
        rdata['next'] = 'http://'+host+path+'?'+valNext
    if valPrev:
        rdata['previous'] = 'http://'+host+path+'?'+valPrev

    return rdata


def validateMovies(movies):
    for x in movies:
        keys = set(x.keys())
        if len(keys) > 4:
            return False
        if 'uuid' not in keys:
            return False
        if 'genres' not in keys:
            return False
        if 'name' not in keys:
            return False
        if 'description' not in keys:
            return False
    return True


def getGenreField(vals):
    d = []

    for x in vals:
        for y in x['movies']:
            d.extend(y['genres'].split(','))

    c = Counter(d).most_common()
    st = []
    for x in c:
        if len(st) < 3:
            st.append(x[0])

    return ','.join(st)
