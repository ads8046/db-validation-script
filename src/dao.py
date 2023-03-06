# Author: Atharva Shivankar
# DAO operations and data validation module (Image URL validation)

from db_utils import *
import requests as req
import validators as vd
from validators import ValidationFailure
import csv


def is_valid_url(url_string):
    result = vd.url(url_string)
    if isinstance(result, ValidationFailure):
        return False
    return result


def extract_record():
    sql_get_img_uri = """
        SELECT monument_id, url 
        FROM image 
        ORDER BY monument_id 
        DESC LIMIT 300;
    """
    query_res = exec_get_all(sql_get_img_uri)
    return query_res
    

def update_url_record(id, url):
    data = (url, id)
    update_sql = """
        UPDATE image 
        SET url = %s
        WHERE monument_id = %s
        RETURNING monument_id;
    """
    query_res = exec_commit_get_one(update_sql, data)
    return query_res
    
    
def encode_bad_img_url(id_url_tuple):
    # Example reference Object: 119771-1622222+-+Chen,+Alex+-+Coppini_1955_Austin_GeorgeWashington.jpg
    # https://monuments-and-memorials.s3.us-east-2.amazonaws.com/images/119771-1622222+-+Chen,+Alex+-+Coppini_1955_Austin_GeorgeWashington.jpg
    # https://monuments-and-memorials.s3.us-east-2.amazonaws.com/images/119771-1622222%2B-%2BChen%2C%2BAlex%2B-%2BCoppini_1955_Austin_GeorgeWashington.jpg
    # https://monuments-and-memorials.s3.us-east-2.amazonaws.com/images/119771-1622222%2B-%2BChen%2C%2BAlex%2B-%2BCoppini_1955_Austin_GeorgeWashington.jpg
    
    # bad_url = "https://monuments-and-memorials.s3.us-east-2.amazonaws.com/images/119771-1622222+-+Chen,+Alex+-+Coppini_1955_Austin_GeorgeWashington.jpg"
    
    try:
        is_modified = False
        
        monument_id = id_url_tuple[0]
        image_url = id_url_tuple[1].strip()
        
        resp = req.get(image_url)
        
        if (resp.status_code != 200 and is_valid_url(image_url)):
                image_url = image_url.replace('+', '%2B').replace(',', '%2C')
                is_modified = True

        return is_modified, monument_id, image_url
    
    except Exception:
        print(f"An exception occurred for the record with monument id: {id_url_tuple[0]}")


def write_to_csv(updated_records_lst):
    field_names = ['is_modified', 'monument_id', 'updated_image_url']
    with open('updated_records.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, field_names)
        writer.writeheader()
        writer.writerows(updated_records_lst)
    
    
def validate_url_encoding():
    query_data = extract_record()
    sanitized_lst = list(map(encode_bad_img_url, query_data))
    updated_records = list()
    
    for e in sanitized_lst:
        is_modified = e[0]
        monument_id = e[1]
        image_url = e[2]
        if is_modified:
            update_url_record(monument_id, image_url)
            record_dict = {'is_modified': is_modified, 'monument_id': monument_id, 'updated_image_url': image_url}
            updated_records.append(record_dict)
    
    write_to_csv(updated_records)
    return "SUCCESS: Records were successfully sanitized and updated in the DB."