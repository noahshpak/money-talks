import pprint
# takes in file w/ copied request headers.
def parsefile(filename):
    with open('requestheaders.txt', 'r') as f:
        headers, cookies = {}, {}
        for line in f:
            data = line.strip().split(': ')
            if len(data) > 1:
                if data[0] == 'Cookie':
                    cookie_data = data[1].split('; ')
                    cookie_dict = { d.split('=',1)[0]:d.split('=',1)[1] for d in cookie_data }
                    cookies = cookie_dict
                    
                else:
                    key = data[0].lower().replace('-', '_')
                    headers[key] = data[1]
                    
    return [headers,cookies]

