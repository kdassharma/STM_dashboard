from flask import Flask, redirect, url_for
# url_for is good for dynamically creating a url of a function
# redirect simply redirects you to the built url

app = Flask(__name__)
# to make the server reload itself if the code changes
app.debug = True

# decorator, tells the app which url should call the function
# here the / url is bound to this function, so when the home page of the server is opened in the browser,
# the output of this function will be outputted
# @app.route('/')

# now the route argument was switched to /hello
# using the routing technique to access this page without having to navigate from home
# @app.route('/hello')

# now we're able to pass a var using <>, can even restrict the type with <int:>
@app.route('/hello/<varName>')
def hello(varName):
    return 'hello %s!!!' % varName

# canonical url, will return this whether the url is /hi/ or /hi
@app.route('/hi/')
def hi():
    return "<b>hi there admin!</b>"


@app.route('/user/<name>')
def user(name):
    if name == "admin":
        return redirect(url_for('hi'))
    else:
        return redirect(url_for('hello', varName=name))


if __name__ == '__main__':
    # runs the app on the local dev server
    app.run()



# this does the same as @app.route
# app.add_url_rule(‘/’, ‘hello’, helloInternet)