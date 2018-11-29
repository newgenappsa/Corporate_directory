from DBConnection import DatabaseOperation
from corporatedir import corporate_dir
from selenium.common.exceptions import TimeoutException
import datetime

from_ = DatabaseOperation("sales_automation_development","thunderclouds")
to_ = DatabaseOperation("sales_automation_development","event")
people = DatabaseOperation("sales_automation_development","test_people")
people_names = DatabaseOperation("sales_automation_development","test_people_names")
now = datetime.datetime.now()
older_than = now - datetime.timedelta(21)
mycol = from_.retrieve_info()
my_people = people.retrieve_info()


def update_organisation(id):
    number = my_people.count_documents({"organisation_id": id})
    doc = mycol.find_one({"_id":id})
    doc["person_count"] = number
    from_.save_or_update({"_id":id},doc)


def save_in_people(details,organisation_id):
    emails,names = [],[]
    for detail_dict in details:
        print(detail_dict)
        if "email" in detail_dict.keys():
            info = {}
            info["organisation_id"] = organisation_id
            info["email"] = detail_dict["email"]
            info["email_type"] = "personal"
            info["status"] = True
            print(info)
            people.save_in_db(info)
        if "name" in detail_dict.keys():
            for name in detail_dict["name"]:
                if type(name) == str and name!= "":
                      info = {}
                      info["organisation_id"] = organisation_id
                      info["name"] = name
                      info["status"] = True
                      print(info)
                      people_names.save_in_db(info)
    update_organisation(organisation_id)

def process_doc(col):
    details,dict = [],{}
    try:
         company_name = col["name"]
         print("----",company_name,"------")
         dict["name"] = company_name
         details = corporate_dir(company_name)
         col['corp_processed_at'] = now
         from_.save_or_update({'_id': col['_id']},col)
    except KeyError:
          print("KeyError 'name'")
          return
    try:
        dict["domain"] = col["domain"]
    except KeyError:
        return
    if len(details)>0:
        print("save")
        dict["corporate Info"] = details
        to_.save_in_db(dict)
        save_in_people(details,col["_id"])



processed_count = list(mycol.find({"corp_processed_at": {"$lt": older_than}}))
never_processed = list(mycol.find({"corp_processed_at":{'$exists': 0}})[15:])
if len(never_processed)>0:
    for col in never_processed:
        process_doc(col)
for col in processed_count:
    process_doc(col)
