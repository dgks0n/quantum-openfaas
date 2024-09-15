import motor.motor_asyncio
from decouple import config
import asyncio
import json

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable
dbClient = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Create new Database called qfaas
database = dbClient.qfaas

# drop all collections if they exist
async def drop_exising_collections():
    existing_collections = await database.list_collection_names()
    for collection in existing_collections:
        await database.drop_collection(collection)

# Create all required collections
async def initialize_database():
    await drop_exising_collections()
    collection_names = ["backends", "functions", "jobs", "providers", "users"]

    for collectionName in collection_names:
        await database.create_collection(collectionName)
        print(f"Collection {collectionName} created")

    print("All collections created successfully in the database qfaas")

    # seed users data
    users = database["users"]
    with open('users.json') as file:
        users_data = json.load(file)
        await users.insert_many(users_data)

        print("Users data seeded successfully")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(initialize_database())
