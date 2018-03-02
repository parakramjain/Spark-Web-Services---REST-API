# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:13:27 2018

@author: Parakram.Jain
"""
# spark-submit --jars /usr/hdp/current/phoenix-client/phoenix-client.jar,/usr/hdp/current/phoenix-client/lib/phoenix-spark-4.7.0.2.5.3.0-37.jar,/usr/hdp/current/hbase-client/lib/hbase-client-1.1.2.2.5.3.0-37.jar,/usr/hdp/current/hbase-client/lib/hbase-common-1.1.2.2.5.3.0-37.jar,/usr/hdp/current/hbase-client/lib/hbase-hadoop2-compat-1.1.2.2.5.3.0-37.jar --master yarn --executor-memory 14G --executor-cores 5 --num-executors 16 --conf spark.driver.maxResultSize=10G --conf spark.sql.shuffle.partitions=2 server.py
# spark-submit --class org.apache.spark.examples.SparkPi --master spark://localhost:7077 server.py

# for MS Azure
# spark-submit --class org.apache.spark.examples.SparkPi --master yarn server.py
# spark-submit --class org.apache.spark.examples.SparkPi --master yarn --num-executors 16 --executor-memory 8G --driver-memory 10G --executor-cores 4 server.py
# curl -X GET http://localhost:5333/getsitelist
# curl -X GET http://localhost:5333/getsitedetails
# curl -X GET http://localhost:5334/getmch2list
# curl -X POST http://localhost:5444/getfilteredsitelist/D034
# curl -X GET  http://localhost:5333/getMCH2details/M0227
# python -m SimpleHTTPServer 8000
#####################################
#### Import packages
#####################################

import cherrypy
from paste.translogger import TransLogger
from app import create_app


#@main.route("/<int:site_id>", methods=["GET"])
#def get_site_data(site_id):
#    return json.dumps([123])

    # Mount the WSGI callable object (app) on the root directory
app = create_app()
app_logged = TransLogger(app)


def run_server(app):
 
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)
 
    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')
 
    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5334,
        'server.socket_host': '0.0.0.0'
    })
 
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
        
run_server(app)    
