from pymongo import MongoClient
import random
MONGODB_URL = "mongodb+srv://Hoanh:MyPass123@cluster0.nx6irmd.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGODB_URL)
db = client['finance_tracker']
transactions = db['transactions']


# db.command("ping")

# print("Kết nối database thành công!")
# print("Database:", db.name)
# print("Collection:", transactions.name)

# #insert one
# print("Inserting one transaction...")


# my_transaction = {
#     "type": "Wave",
#     "amount": 500000,
#     "unit": "VND",
#     "date": "2024-10-01",
# }

# transactions.insert_one(my_transaction)
# print("inssert done")


# # insert many
# # transaction.insert_many(list[dict])

# TYPE = ['in', 'out']
# UNIT = ['VND', 'USD']

# multi_transactions = []
# for i in range(10):
#     take_trans = {
#         "type": random.choice(TYPE),
#         "amount": random.randint(10000, 1000000),
#         "unit": random.choice(UNIT),
#         "date": f"2024-10-{random.randint(1,30):02d}",
#     }
#     multi_transactions.append(take_trans)

# # print multi_transactions
# # print(multi_transactions)

# # insert many
# result = transactions.insert_many(multi_transactions)

# print(len(result.inserted_ids), "transactions inserted.")
# print("Generated IDs:", result.inserted_ids)

# # embedded documents
# my_emb_transaction = {
#     "type": "Wave",
#     "amount": 500000,
#     "unit": "VND",
#     "date": "2024-10-01",
#     "details":[
#         {
#         "item": "Groceries",
#         "quantity": 10,
#         "discount": 5000
#         },
#         {
#         "item": "Snacks",
#         "quantity": 5,
#         "discount": 2000
#         }
#     ]
# }

# transactions.insert_one(my_emb_transaction)
# print("inssert done")

print("="*60)
print("READ DATA")
print("="*60)

# # GET ALL DOCUMENTS IN TRANSACTIONS COLLECTION
# all_trans = transactions.find()
# all_trans = list(all_trans)
# print(f"Retrieved {len(all_trans)} docs")

# for trans in all_trans[:3]:
#     print(f"Transaction ID: {trans.get('_id', 'unknown')}")
#     print(f"Transaction Type: {trans.get('type', 'others')}")
#     print(f"Transaction Unit: {trans.get('unit', '-----')}")
#     print('-'*20)

# #get documents with type "in"
# all_trans_in = transactions.find({"type":"in"})
# all_trans_in = list(all_trans_in)
# print(f"Retrieved {len(all_trans_in)} docs with type = in")

#get documents with type "out", great than 50 USD, LESS THAN 500 USD
all_trans_out = transactions.find({"type":"out", "amount":{"$gt":50}, "unit":"USD"})
all_trans_out = list(all_trans_out)
print(f"Retrieved {len(all_trans_out)} docs with type = out")
for trans in all_trans_out[:3]:
    print(f"Transaction ID: {trans.get('_id', 'unknown')}")
    print(f"Transaction Type: {trans.get('type', 'others')}")
    print(f"Transaction Unit: {trans.get('unit', '-----')}")
    print(f"Transaction Amount: {trans.get('amount', '-----')}")
    print('-'*20)