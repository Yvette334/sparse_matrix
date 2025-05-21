from sparse import read, add, sub, mult, force_mult, save

def main():
    print("Matrix Calculator")
    print("1: Addition")
    print("2: Subtract")
    print("3: Multiply")
    choice = input("Enter from (1-3): ")

    first_file = input("First file: ")
    second_file = input("Second file: ")
    output = input("Save result to: ")

    try:
        print("Loading matrices...")
        matrix_a = read(first_file)
        matrix_b = read(second_file)

        print("Processing...")
        if choice == '1':
            result = add(matrix_a, matrix_b)
            print("Addition completed.")
        elif choice == '2':
            result = sub(matrix_a, matrix_b)
            print("Subtraction completed.")
        elif choice == '3':
            print("Multiplying matrices (this may take a moment for large matrices)...")
            result = force_mult(matrix_a, matrix_b)
            print("Multiplication completed.")
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
            return

        print("Saving result...")
        save(result, output)
        print(f"Operation completed! Result saved to {output}")
    
    except ValueError as error:
        print(f"Error: {error}")
    except FileNotFoundError:
        print("Error: Could not find one of the input files")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")

if __name__ == "__main__":
    main()
