import argparse
from DoubleLinkedList import DoubleLinkedList

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS583 HW0', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-n', '--n', default=5, type=int, help="Size of the square matrices.")
    parser.add_argument('-s', '--s', default=10, type=int, help="Scalar to multiply.")
    args = parser.parse_args()  
    matrix_size = args.n
    scalar = args.s

    # Addition
    print('---------- Addition')
    matrix1, matrix2 = DoubleLinkedList(matrix_size), DoubleLinkedList(matrix_size)

    print('Matrix 1:')
    matrix1.traverse()

    print('\nMatrix 2:')
    matrix2.traverse()

    matrix_sum = matrix1.add(matrix2)
    print('\nResult of Summation:')
    matrix_sum.traverse()

    # Scalar Multiplication
    print('\n---------- Scalar Multiplication')
    print(f'Scalar: {scalar}')

    matrix3 = DoubleLinkedList(matrix_size)
    print('\nMatrix 3:')
    matrix3.traverse()

    matrix3.scalar_multiply(scalar)
    print('\nResult of Scalar Multiplication:')
    matrix3.traverse()

    # Transpose
    print('\n---------- Transpose Operation')
    matrix4 = DoubleLinkedList(matrix_size)
    print('Matrix 4:')
    matrix4.traverse()

    matrix4.transpose()
    print('\nResult of Transpose:')
    matrix4.traverse()

    print('\nExecution complete.')