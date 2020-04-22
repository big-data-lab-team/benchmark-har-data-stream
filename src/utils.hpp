#include <iostream> 

template<int input_size>
void parse_line(std::string line, double* features){
	std::string delimiter = "\t";
	int prev_token = 0;
	for(int i = 0; i < input_size; ++i){
		int new_token = line.find(delimiter, prev_token);
		std::string data = line.substr(prev_token, new_token); 
		prev_token = new_token+delimiter.size();
		features[i] = std::stod(data);
	}
}
