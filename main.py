from flask import Flask, request, jsonify, Response, send_from_directory
import logging
import pathlib
import os
import time

# from commons import LOG_LOCATION
# from components.logs.log_even import LogEvent

# TODO: how to format time in logging

logging.basicConfig(
  filename='log.txt',
  level=logging.INFO,
  format='%(asctime)s = %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route("/")
def hello():
  logging.info('Web has been access with data ? ')
  return "Hello Flask on IIS!"

@app.route("/main")
def main():
  logging.info('Main has been access?')
  return "Hello MAIN!"

@app.route("/about")
def about():
  logging.info('About has been access?')
  return "Hello ABOUT!"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
           logging.error(f"Error getting JSON data from request...")
           logging.error(f"Request data: {request.data}")
           logging.error(f"Request headers: {request.headers}")
           return "Error getting JSON data from request", 400
        logging.info(f"Request Data: {data}")

    return Response(status=200)

# how to read log file and return via http
@app.route("/logs")
def download_file():
   try:
      path_ = pathlib.Path(".").parent.resolve()
      # logging.info( path_ )
      # return Response(status=200)      
      return send_from_directory( path_ , "log.txt", as_attachment=False)
   except Exception as e:
      logging.error( repr(e) )


# inverts file line(s) and writes to a new file
def line_inverter(import_file_name, export_file_name, prefix_string):
    
    # tries to open import file in reading mode
    f1 = open(import_file_name, "r")
    
    # tries to create export file in append mode
    f2 = open(export_file_name, "a")
    
    
    # creates a list with each line in a separate index
    line_list = f1.readlines()
    
    # reverses line order
    line_list.reverse()
    
    # closes import file, since all data is stored in line_list
    f1.close()
    
    
    # loops through line_list to modify individual indices
    for line in line_list:
        
        # strips the "\n" from the string
        line = line.strip("\n")
        
        # concatenates prefix_string and a character from the line_list
        x = prefix_string + line
        
        # appends the line to the new file
        f2.write(x)
        
    # once the loop is finished, close the new file
    f2.close()

# TODO: how to reverse line in file
@app.route("/last")
def last():
   try:
      os.remove( "revert.txt" )
      time.sleep( 0.2 )
      line_inverter("log.txt", "revert.txt", "\n")
      path_ = pathlib.Path(".").parent.resolve()
      return send_from_directory(path_, "revert.txt", as_attachment=False)
      #  , mimetype="text/xml" )
   except Exception as e:
      logging.error( repr(e) )

# @app.route("/logs", method=["GET"])
# def get_logs():
#    if request.method == "GET":
#       log_file = open(LOG_LOCATION, 'r')
#       logs = [LogEvent().from_line(log) for log in log_file.readlines()]
#       return jsonify([log.as_json() for log in logs ])

if __name__ == '__main__':
  app.run(debug=True)