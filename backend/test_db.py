from app.utils.db import get_db, serialize_mongo_document
def test_mongo_connection():
    db = get_db()
    # Thử thêm một document vào collection 'test_collection'
    test_collection = db.test_collection
    test_collection.delete_many({"name": "Test User"})
    # test_document = {"name": "Test User", "email": "test@example.com"}
    # inserted_id = test_collection.insert_one(test_document).inserted_id
    
    # # Lấy document vừa thêm
    # result = test_collection.find_one({"_id": inserted_id})
    # print("Document:", serialize_mongo_document(result))

if __name__ == "__main__":
    test_mongo_connection()