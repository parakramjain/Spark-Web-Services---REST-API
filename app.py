# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:04:02 2018

@author: Parakram.Jain
"""

from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('flask_cors').level = logging.DEBUG

from flask import Flask
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Row
#from pyspark.sql.functions import lit, concat, round, col

#Code for cross domain message exchange
from flask_cors import CORS
CORS(main)

######################################
conf = SparkConf().setAppName("Get Site Dataframe")
conf.setMaster("local")
sc = SparkContext.getOrCreate(conf)
sqlContext = SQLContext(sc)

raw_RDD = sc.textFile("sample.csv").map(lambda line: line.split(","))
header = raw_RDD.first()
raw_RDD1 = raw_RDD.filter(lambda line: line != header)
schema = Row('ship_site', 'rcv_site_num',	'lead_time',	'schd_delv_qty',	'first_cost',	'sales',	'ship_lat',	'ship_long',	'rcv_site_num',	'rcv_lat','rcv_long',	'mch_2_cd')
raw_RDD2 = raw_RDD1.map(lambda r: schema(*r))
raw_df = sqlContext.createDataFrame(raw_RDD2)

### get article for MCH_2_CD
#artcl_mch_query = "select artcl_num, mch_2_cd from supply_chain.artcl_mch"
#artcl_mch_df = sqlContext.sql(artcl_mch_query)

						   
@main.route('/')
def hello():
    return "Hello Supply Chain from Spark Server!"

@main.route("/<int:site_id>", methods=["GET"])
def get_site_data(site_id):
    return1 = raw_df.collect()
    return json.dumps(return1)

@main.route("/getmch2list", methods=["GET"])
def get_mch2_data_post():
    return_mch2_list = raw_df.select('mch_2_cd').distinct().collect()
    return json.dumps(return_mch2_list)

@main.route("/getMCH2details/<string:mch2_id>", methods=["GET"])
def get_mch2_details_post(mch2_id):
    return_mch2_details = raw_df.filter(raw_df.mch_2_cd == mch2_id).collect()
    return json.dumps(return_mch2_details)

@main.route("/getMCH2details/<string:mch2_id>/<string:site_id>", methods=["GET"])
def get_mch2_site_details_post(mch2_id, site_id):
    return_mch2_details = raw_df.filter(raw_df.ship_site == site_id).filter(raw_df.mch_2_cd == mch2_id).collect()
    return json.dumps(return_mch2_details)

@main.route("/getMCH2details/<string:mch2_id>/<string:site_id>/<string:artcl_id>", methods=["GET"])
def get_mch2_site_artcl_details_post(mch2_id, site_id, artcl_id):
    return_mch2_details = raw_df.filter(raw_df.ship_site == site_id).filter(raw_df.mch_2_cd == mch2_id).collect()
    return json.dumps(return_mch2_details)	
	
@main.route("/getartcllist/<string:mch2_id>", methods=["GET"])
def get_artcl_data_post(mch2_id):
	# return_artcl_list = artcl_mch_df.filter(artcl_mch_df.mch_2_cd == mch2_id).select('artcl_num').distinct().collect()
    return_artcl_list = raw_df.filter(raw_df.mch2 == mch2_id).select('artcl_num').distinct().collect()
    return json.dumps(return_artcl_list)

@main.route("/getsitelist", methods=["GET"])
def get_site_data_post():
    return_site_list = raw_df.select('ship_site').distinct().collect()
    return json.dumps(return_site_list)

@main.route("/getsitedetails", methods=["GET"])
def get_site_detail_post():
    return_site_list = raw_df.collect()
    return json.dumps(return_site_list)

	
@main.route("/getfilteredsitelist/<string:site_id>", methods=["GET"])
def get_site_filtered_data_post(site_id):
    site_raw_df = raw_df.filter(raw_df.ship_site == site_id)
    return_site_list = site_raw_df.collect()
    return json.dumps(return_site_list)
	
def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app

