from typing import List
from src.types.models import Customer
import json
from src.clients.redis_connection import r

class CustomerService:
    def _read_customers(self) -> List[Customer]:
        try:
            customers_data = r.get("customers")
            if customers_data is None:
                return []
            customers_data = json.loads(customers_data)
            return [Customer(**customer_data) for customer_data in customers_data]
        except Exception as e:
            print(f"Error reading customers: {e}")
            return []

    def _write_customers(self, customers: List[Customer]) -> None:
        try:
            customers_data = [customer.model_dump() for customer in customers]
            r.set("customers", json.dumps(customers_data))
        except Exception as e:
            print(f"Error writing customers: {e}")

    def insert_customer_in_order(self, customer: Customer) -> None:
        customers = self._read_customers()
        insert_pos = 0
        for i, existing_customer in enumerate(customers):
            if (customer.lastName, customer.firstName) < (existing_customer.lastName, existing_customer.firstName):
                break
            insert_pos = i + 1
        
        customers.insert(insert_pos, customer)
        self._write_customers(customers)

    def add_customers(self, new_customers: List[Customer]) -> None:
        inserted_customers = []
        failed_customers = []
        for customer in new_customers:
            if self.validate_customer(customer):
                self.insert_customer_in_order(customer)
                inserted_customers.append(customer)
            else:
                failed_customers.append(customer)
        return {
            "inserted": inserted_customers,
            "failed": failed_customers
        }

    def validate_customer(self, customer: Customer) -> bool:
        customer_dict = customer.model_dump(exclude_unset=True)
        customers = self._read_customers()

        required_fields = ["firstName", "lastName", "age", "id"]
        for field in required_fields:
            if field not in customer_dict or customer_dict[field] is None:
                print(f"Customer is missing required field: {field}")
                return False

        if customer_dict['age'] < 18:
            print(f"Customer has invalid age: {customer_dict['age']}")
            return False
        
        if any(existing.id == customer_dict['id'] for existing in customers):
            print(f"Customer with ID {customer_dict['id']} already exists")
            return False

        if any((existing.lastName, existing.firstName) == (customer_dict['lastName'], customer_dict['firstName']) for existing in customers):
            print(f"Customer with name {customer_dict['lastName']}, {customer_dict['firstName']} already exists")
            return False
        
        return True

    def get_customers(self) -> List[Customer]:
        return self._read_customers()

    def get_name_lists(self) -> tuple[List[str], List[str]]:
        customers = self._read_customers()
        first_names = [customer.firstName for customer in customers]
        last_names = [customer.lastName for customer in customers]
        return first_names, last_names 
    
    def delete_all_customers(self) -> None:
        try:
            self._write_customers([])
        except Exception as e:
            print(f"Error deleting customers: {e}")