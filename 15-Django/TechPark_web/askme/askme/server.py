def application(environ, start_response):
    status = '200 OK'
    output = '<html><body>'
    output += '<h1>GET Parameters</h1>'
    output += '<ul>'

    query = environ['QUERY_STRING'].split('&')
    query_dict = {i.split('=')[0]: i.split('=')[1] for i in query if len(i) != 0}
    for key, value in query_dict.items():
        print("HOCHU_CHETVERKU", f'<li>{key} = {value}</li>')
        output += f'<li>{key} = {value}</li>'

    output += '</ul>'
    output += '<h1>POST Parameters</h1>'
    output += '<ul>'

    query = environ['wsgi.input'].read().decode('utf-8').split('&')
    query_dict = {i.split('=')[0]: i.split('=')[1] for i in query if len(i) != 0}
    for key, value in query_dict.items():
        output += '<li>{} = {}</li>'.format(key, value)

    output += '</ul>'
    output += '</body></html>'
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [str.encode(output)]
