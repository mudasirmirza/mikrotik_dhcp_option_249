
from bottle import route, run, template, request, error, abort, default_app


TITLE = "Mikrotik DHCP option 249 route"

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{title or 'No title'}}</title>
</head>

<body>

<div class="jumbotron" style="padding: 0px 0px 0px 0px; margin-bottom: 10px;">
    <div class="container-fluid">
        <h1>Mikrotik</h1>
            <p>
                Make DHCP option 249 routes
            </p>
    </div>
</div>

<div class="bs-example">
    <form action="/mikrotik" method="POST">
        <textarea name="route" ROWS=20 COLS=70 placeholder="10.6.40.0/22-10.6.32.1,10.6.44.0/22-10.6.38.1"></textarea>
        </br>
        <INPUT TYPE=SUBMIT name="submit" VALUE="Submit">
    </form>
</div>

</body>
</html>
"""


@error(404)
def error404(error):
    return 'Error: %s' % error


@route('/', method='GET')
@route('/mikrotik', method='POST')
def index():
    if request.method == "GET":
        return template(HTML_CODE, title=TITLE)

    if request.method == "POST":
        try:
            form_data = request.forms.get('route')
        except Exception, e:
            abort(404, e)
        if form_data:
            route_dict = {}
            for i in form_data.split(","):
                subnet = i.split('-')[0]
                gateway = i.split('-')[1]
                route_dict[subnet] = gateway
            return routes2hex(route_dict)
        return "Empty data provided, please try again"


def ip2hex(cidr, router):
    addr, mask = cidr.split("/")
    mask = int(mask)
    addr = [("%2s" % hex(int(i))[2:]).replace(" ", "0") for i in addr.split(".") if i != "0"]
    parts = mask/8 - len(addr)
    if mask%8 > 0:
        parts += 1
    if parts > 0:
        for i in range(int(parts)):
            addr.append("00")

    r = []
    for i in router.split("."):
        r.append(("%2s" % hex(int(i))[2:]).replace(" ", "0"))

    addr.insert(0, hex(mask)[2:])
    return "".join(addr), "".join(r)


def routes2hex(routes):
    routers = []
    for cidr, router in routes.items():
        a,r = ip2hex(cidr, router)
        routers.append(a)
        routers.append(r)

    return "0x%s" % ("".join(routers).upper())

#application = default_app()
run(host='127.0.0.1', port=8090, debug=True, reloader=True)
