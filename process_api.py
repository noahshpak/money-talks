import pprint, fileinput, json, requests, urllib2, time, sys
from tqdm import tqdm
from datetime import datetime
from ParseRequestsHeaders import parse

# USAGE

# go to chrome, login to Venmo, open dev tools, go to network, filter for api
# when you hover over it, link should look like https://venmo.com/api/v5/users/{user_id}/feed
# right click > Copy Request Headers > paste these into a file called requestheaders.txt in this directory

noah_venmo_id = 1002948

bonds = []
user_data = {}

# TODO
# get rid of duplicate bonds -- need to create a class and define equality

try:
    res = parse.parsefile('requestheaders.txt')
    headers, cooks = res[0], res[1]
except IndexError as e:
    print "You probably forgot to copy your own request headers"
    sys.exit(1)



def bond(source, target, message, created_at):
    return dict(source=source, target=target, title=message, about=created_at)

def fetch_neighbors(user):
    ids = []
    url = 'https://venmo.com/api/v5/users/{user}/feed'.format(user=user)
    req = requests.get(url, cookies=cooks, headers=headers)
    try:
        data = req.json()['data']
        ids = process(data)
    except (KeyError, UnicodeEncodeError) as e:
        print "Your O AUTH Token has expired.  Refresh Venmo and copy it again from Chrome into the text file"
    return ids

# TODO(noah) -- finish this
# def fetch_prev_neighbors(user):
#     ids = []
#     url = 'https://venmo.com/api/v5/users/{user}/feed'.format(user=user)
#     graph = {user: []}
#
#     req = requests.get(url, cookies=cooks, headers=headers)
#     data = req.json()['data']
#     ids = process(data)
#     graph[user] = ids
#
#     visited, stack, depth = set(), [user], 1
#     while
#     try:
#         prev = req.json()['paging']['previous']
#         req = requests.get(prev, cookies=cooks, headers=headers)
#         data = req.json()['data']
#         ids = process(data)
#     except (KeyError, UnicodeEncodeError) as e:
#         print e.message

def fetch_all_users():
    for user in tqdm(xrange(7000, 100000)):
        url = 'https://venmo.com/api/v5/users/{user}/feed'.format(user=user)
        req = requests.get(url, cookies=cooks)
        print req.text
        try:
            data = req.json()['data']
            ids = process(data)
            user_data[url] = data
            if user % 50 == 0 and bonds:
                pprint.pprint(bonds)
                save(bonds, user_data) # this call saves this data
        except KeyError as e:
            print e.message
        time.sleep(1)
    save(bonds, user_data)

# TODO(noah)
def bfs_fetch(user):
    neighbors = fetch_prev_neighbors(user)

def dfs_fetch(user):
    # creating the graph of from { elem1 : [ neighbors ], elem2 : [ neighbors ] ... }

    max_depth = 55
    url = 'https://venmo.com/api/v5/users/{user}/feed'.format(user=user)
    graph = {user: []}

    req = requests.get(url, cookies=cooks)
    try:
        data = req.json()['data']
        ids = process(data)
        graph[user] = ids

        visited, stack, depth = set(), [user], 1
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                depth += 1
                try:
                    print "Visiting + {vertex}".format(vertex=vertex)
                except UnicodeEncodeError as e:
                    pass

                visited.add(vertex)
                if vertex in graph:
                    if depth < max_depth:
                        stack.extend(graph[vertex] - visited)
                else:
                    neighbors = fetch_neighbors(vertex)
                    graph[vertex] = neighbors
                    if depth < max_depth:
                        stack.extend(graph[vertex] - visited)



        save(bonds, [])
        return visited


    except KeyError as e:
        print "Your O AUTH Token has expired."
        print "Refresh Venmo and copy it again from Chrome into the text file"
        sys.exit(1)
    time.sleep(1)


def save(bonds,user_data):
    with open('data/bonds' + str(datetime.now()).split(' ')[1] + '.txt', 'w') as f:
        f.write(str(bonds))
    if user_data:
        with open("data/all_data" + str(datetime.now()).split(' ')[1] + '.txt', 'w') as f:
            f.write(str(user_data))

# grabs the data we want
# If you want to grab other items, here's where you can modify
def process(data):
    ids = []
    try:
        for d in data:
            source = d['actor']['name']
            ids.append(d['actor']['id'])
            created_at = d['created_time']
            date_object = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
            date = date_object.strftime("%d/%m/%y")
            message = d['message']
            targets = d['transactions']
            for t in targets:
                target = t['target']['name']
                print "{actor}-->{target}".format(actor=source,target=target)
                ids.append(t['target']['id'])
                bonds.append(bond(source, target, message, date))
    except (TypeError, KeyError) as e:
        print(e.message)
    return set(ids)

def crawl():
    for i in range(1):
        dfs_fetch(noah_venmo_id)
        time.sleep(5)

if __name__ == '__main__':
    crawl()
    pprint.pprint(user_data)
    pprint.pprint("----------------------------------------------")
    pprint.pprint(bonds)
    pprint.pprint(len(bonds))
