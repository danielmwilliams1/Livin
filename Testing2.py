def find_sum(n):
  if n==1:
    return 1
  return n + find_sum

if __name__ == "__main__":
  print(find_sum(8))