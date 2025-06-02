import os
import sys
import asyncio
import random
import aiohttp
import logging
from typing import List
from src.types.models import Customer
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

FIRST_NAMES = [
            "Leia", "Sadie", "Jose", "Sara", "Frank",
            "Dewey", "Tomas", "Joel", "Lukas", "Carlos"
        ]
LAST_NAMES = [
            "Liberty", "Ray", "Harrison", "Ronan", "Drew",
            "Powell", "Larsen", "Chan", "Anderson", "Lane"
        ]

class CustomerSimulator:
    def __init__(self, base_url: str = os.getenv("BASE_URL")):
        self.base_url = f"{base_url}/customers"
        self.next_id = 1
        self.setup_logging()

    def setup_logging(self):
        # Create outputs directory if it doesn't exist
        outputs_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(outputs_dir, exist_ok=True)
        
        # Setup logging with timestamp in filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join(outputs_dir, f"customer_simulation_{timestamp}.log")
        
        # Configure logging
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        print(f"Logging to: {log_filename}")

    def generate_customers(self, count: int = 2) -> List[Customer]:
        customers = []
        generated_names = set()
        
        while len(customers) < count:
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            if full_name not in generated_names:
                customer = Customer(
                    firstName=first_name,
                    lastName=last_name,
                    age=random.randint(10, 90),
                    id=self.next_id
                )
                self.next_id += 1
                customers.append(customer)
                generated_names.add(full_name)
        return customers

    async def send_post_request(self, customers: List[Customer]) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                json=[customer.model_dump() for customer in customers]
            ) as response:
                result = await response.json()
                
                # Log POST request with customer details
                self.logger.info(f"POST request completed - Total users sent: {len(customers)} - Users sent: [{customers}]")
                
                return result

    async def send_get_request(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url) as response:
                result = await response.json()
                
                # Log GET request
                self.logger.info(f"GET request completed - Total users: {len(result['customers'])} - Users received: [{result['customers']}]")
                
                return result

    async def run_simulation(self, post_requests: int = 3, get_requests: int = 3):
        self.logger.info(f"Starting simulation with {post_requests} POST requests and {get_requests} GET requests")
        self.logger.info("")

        post_tasks = []
        for _ in range(post_requests):
            customers = self.generate_customers(random.randint(2, 5))
            post_tasks.append(self.send_post_request(customers))

        get_tasks = [self.send_get_request() for _ in range(get_requests)]

        all_tasks = post_tasks + get_tasks
        random.shuffle(all_tasks)
        await asyncio.gather(*all_tasks)
        
        self.logger.info("")
        self.logger.info("The execution is finished")

if __name__ == "__main__":
    simulator = CustomerSimulator()
    
    post_count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    get_count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    if post_count > 10 or get_count > 10:
        print(f"Error: Request counts cannot exceed 10. POST count: {post_count}, GET count: {get_count}")
        sys.exit(1)
    
    print(f"Running simulation with {post_count} POST requests and {get_count} GET requests")
    asyncio.run(simulator.run_simulation(post_requests=post_count, get_requests=get_count))