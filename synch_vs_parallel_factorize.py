import multiprocessing
import time

def divisors(num):
    divisors = []
    for i in range(1, num + 1):
        if num % i == 0:
            divisors.append(i)    
    return divisors

def factorize(numbers):
    result = []
    for num in numbers:        
        result.append(divisors(num))
    return result

def parallel_factorize(numbers):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(divisors, numbers)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
    numbers = [76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]  # вхідні числа
    
    start_time = time.time()
    result = factorize(numbers)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nСинхронний час виконання: {execution_time:.4f} секунд")
    
    start_time = time.time()
    results = parallel_factorize(numbers)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nПаралельний час виконання: {execution_time:.4f} секунд")
        
    print("\n",results)
    