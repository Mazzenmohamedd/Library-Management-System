from transaction import TransactionManager

manager = TransactionManager()

# تسجيل عملية استعارة
manager.log_transaction("test_user@example.com", "0195153448", "borrow")
print("Logged borrow transaction.")

# تسجيل عملية إرجاع
manager.log_transaction("test_user@example.com", "0195153448", "return")
print("Logged return transaction.")
