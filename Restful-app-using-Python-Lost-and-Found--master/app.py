#import libraries
from flask import Flask, render_template
from RestApiFunctions import app


#Run Server
if __name__== '__main__':
     app.run(host='0.0.0.0', port=5000)