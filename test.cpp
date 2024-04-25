#include <iostream>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        std::cerr << "Error: invalid arguments.\n"
                  << "Correct usage: ./test <message> <#repeats>" << std::endl;
        return 1;
    }

    int n_repeats = atoi(argv[2]);

    for (int i = 0; i < n_repeats; i++) {
        std::cout << argv[1] << std::endl;
    }

    return 0;
}