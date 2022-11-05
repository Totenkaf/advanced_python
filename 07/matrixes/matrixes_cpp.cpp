#include<iostream>
#include<vector>
#include<cstdlib>
#include<stack>

class Matrix {
public:
    Matrix()
    : num_rows(0), num_cols(0)
    {}

    Matrix(int _num_rows, int _num_cols)
    : num_rows(_num_rows), num_cols(_num_cols), 
    matrix(std::move(std::vector<int>(_num_rows*_num_cols, 0)))
    {}

    int get_num_rows() const;
    int get_num_cols() const;
    void print_as_matrix();
    void initialize();
    void fill_with_random_int(int edge);

    int& operator[](size_t index);
    const int& operator[](size_t index) const;

private:
    int num_rows;
    int num_cols;
    std::vector<int> matrix;
};

int& Matrix::operator[](size_t index) {
    return matrix[index];
}

const int& Matrix::operator[](size_t index) const {
    return matrix[index];
}

int Matrix::get_num_cols() const {
    return num_cols;
}

int Matrix::get_num_rows() const {
    return num_rows;
}

void Matrix::print_as_matrix() {
    for (size_t i = 0; i < num_rows; ++i) {
        for (size_t j = 0; j < num_cols; ++j) {
            std::cout << matrix[i * num_cols + j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
    return;
}

void Matrix::fill_with_random_int(int edge){
    for (size_t i = 0; i < num_rows; ++i) {
        for (size_t j = 0; j < num_cols; ++j) {
            matrix[i * num_cols + j] = rand() % edge;
        }
    }
}


Matrix multiply_two_matrix(const Matrix& matrix_1, const Matrix& matrix_2) {
    if (matrix_1.get_num_cols() != matrix_2.get_num_rows()) {
        return Matrix(0, 0);
    }
    Matrix result_matrix = Matrix(matrix_1.get_num_rows(), matrix_2.get_num_cols());
    for (size_t i = 0; i < matrix_1.get_num_rows(); i++) {
        for (size_t j = 0; j < matrix_2.get_num_cols(); j++) {
            for (size_t k = 0; k < matrix_1.get_num_cols(); k++) {
                result_matrix[i * matrix_2.get_num_cols() + j] += (matrix_1[i * matrix_1.get_num_cols() + k] * matrix_2[k * matrix_2.get_num_cols() + j]);
            } 
        }
    }
    return result_matrix;
}

std::vector<Matrix> fill_matrix_chain(std::vector<int> matrix_chain_pattern, int edge) {
    std::vector<Matrix> filled_matrix_chain;

    for (size_t i = 1; i < matrix_chain_pattern.size(); ++i) {
        Matrix matrix = Matrix(matrix_chain_pattern[i-1], matrix_chain_pattern[i]);
        matrix.fill_with_random_int(edge);
        filled_matrix_chain.push_back(matrix); 
    }
    return filled_matrix_chain;
}

void print_matrix_chain(std::vector<Matrix>& filled_matrix_chain) {
    for (size_t i = 0; i < filled_matrix_chain.size(); ++i) {
    filled_matrix_chain[i].print_as_matrix();
    }
    
}

Matrix multiply_matrix_chain(std::vector<Matrix>& matrix_chain_list) {
    std::stack<Matrix> matrix_stack;
    Matrix result;

    matrix_stack.push(matrix_chain_list[0]);
    for (size_t i = 1; i < matrix_chain_list.size(); ++i) {
        Matrix tmp_result = matrix_stack.top();
        matrix_stack.pop();
        result = multiply_two_matrix(tmp_result, matrix_chain_list[i]);
        matrix_stack.push(result);
    }
    return result;
}


extern "C" {
    int multiply_matrix_chain_command(int* arr, int arr_len, int edge, int* c_arr) {
        std::vector<int> matrix_chain_pattern;
        for (size_t i = 0; i < arr_len; ++i) {
            matrix_chain_pattern.push_back(arr[i]);
        }
        
        std::vector<Matrix> filled_matrix_chain = fill_matrix_chain(matrix_chain_pattern, edge);
        Matrix result_multiple = multiply_matrix_chain(filled_matrix_chain);
        result_multiple.print_as_matrix();

        int c_arr_size = result_multiple.get_num_cols() * result_multiple.get_num_rows();
        return c_arr_size;
    }
}


// Matrix cpp_multiply_matrix_chain_command(std::vector<int> matrix_chain_pattern, int edge) {
//     std::vector<int> matrix_chain_pattern;
//     std::vector<Matrix> filled_matrix_chain = fill_matrix_chain(matrix_chain_pattern, edge);
//     Matrix result_multiple = multiply_matrix_chain(filled_matrix_chain);
//     return result_multiple;
// }

// int main(int argc, const char** argv) {
//     srand(time(NULL));
//     const int edge = 10;
//     std::vector<int> matrix_chain_pattern = {2, 4, 3, 3};
//     Matrix result = cpp_multiply_matrix_chain_command(matrix_chain_pattern, edge);       
//     result.print_as_matrix();

//     int arr_len = 4;
//     int arr[4] = {2, 4, 3, 3};
//     multiply_matrix_chain_command(arr, arr_len, edge);
//     return 0;
// }