#include <fstream>
#include <iostream> 
#include <cmath>
#include "utils.hpp"

using namespace std;


class functions{
	public:
	static void* malloc(int const size){
		return std::malloc(size);
	}
	static void free(void* p){
		std::free(p);
	}
	static double log(double const x){
		return std::log(x);
	}
	static double log2(double const x){
		return std::log2(x);
	}
	static double exp(double const x){
		return std::exp(x);
	}
	static double sqrt(double const x){
		return std::sqrt(x);
	}
	static bool isnan(double const x){
		return std::isnan(x);
	}
	//TODO: we need a rand_uniform and a log functions (log == ln)
	static double rand_uniform(void){
		return static_cast<double>(rand())/static_cast<double>(RAND_MAX);
	}
	static double random(void){
		return (static_cast<double>(std::rand()) / static_cast<double>(RAND_MAX));
	}
	template<class T>
	static int round(T const x){
		return std::round(x);
	}
	template<class T>
	static int floor(T const x){
		return std::floor(x);
	}
};

#include CLASSIFIER_INITIALIZATION_FILE

template<int label_count>
class Evaluation{
	double counts[label_count+1][label_count+1];
	double fading_factor;
	public:
		Evaluation(double const fading_factor){
			this->fading_factor = fading_factor;
			for(int i = 0; i < label_count; ++i)
				for(int j = 0; j < label_count; ++j)
						counts[i][j] = 0;
		}
		void count(int const prediction, int const label){
			for(int i = 0; i <= label_count; ++i)
				for(int j = 0; j <= label_count; ++j)
					counts[i][j] *= fading_factor;

			counts[prediction][label] += 1;
			counts[label_count][label] += 1;
			counts[prediction][label_count] += 1;
			counts[label_count][label_count] += 1;
		}
		double accuracy(void) const{
			double right = 0;
			for(int i = 0; i < label_count; ++i)
				right += counts[i][i];
			double const total = counts[label_count][label_count];
			return right / total;
		}
		double f1(void) const{
			double score_sum = 0;
			double real_label_count = static_cast<double>(label_count);
			for(int i = 0; i < label_count; ++i){
				if(counts[i][label_count] != 0 && counts[label_count][i] != 0){
					double const precision = counts[i][i] / counts[i][label_count];
					double const recall = counts[i][i] / counts[label_count][i];
					if(precision != 0 || recall != 0 && !(isnan(precision) && isnan(recall))){
						double const score = 2 * ((precision * recall) / (precision + recall));
						score_sum += score;
					}
				}
				else{
					real_label_count -= 1;
				}
			}
			if(real_label_count == 0)
				return 0;
			return score_sum / real_label_count;
		}
};

template<int feature_count, class func, class C, class E>
int process_file(string const filename, C* classifier, E* evaluator){
	ifstream myfile, statm;
	string line;
	myfile.open (filename);
	if(!myfile.is_open()){
		return 1;
	}
	statm.open("/proc/self/statm");
	if(!myfile.is_open()){
		return 2;
	}
	cout << "File processed: " << filename << endl;
	int line_count = 1;
	//Start reading the file
	while (getline (myfile,line) ) {
		double features[feature_count+1]; //+1 because we need the label
		parse_line<feature_count+1>(line, features);
		int label = func::round(features[feature_count]);
		int const prediction = classifier->predict(features);
		evaluator->count(prediction, label);
		classifier->train(features, label);
		line_count += 1;
		if(line_count%10 == 0){
			cout << "Accuracy: " << line_count << "~" << evaluator->accuracy() << endl;
			cout << "F1: " << line_count << "~" << evaluator->f1() << endl;
		}
		if(line_count%40 == 0){
			//rewind cursor
			statm.seekg(0, ios::beg);
			cout << "Memory: " << line_count << "~";
			char letter = 'A';
			while(letter != ' '){
				statm.read(&letter, 1);
				if(letter != ' ')
					cout << letter;
			}
			cout << endl;
		}
	}
	myfile.close();
	return 0;
}

int main(int argc, char** argv){

	if(argc < 2){
		cout << "usage: " << argv[0] << " <file1> <parameter classifier ...>" << endl;
		return 0;
	}
	char* filename = argv[1];
	Evaluation<3> evaluator;
	auto classifier = get_classifier(argc-2, argv+2);
	if(classifier != nullptr)
		process_file<3, functions>(filename, classifier, &evaluator);
	return 0;
}

//#define INPUT_SIZE 120
//#define FEATURES_COUNT (3*3)
//#define WINDOW_SIZE 50
//void parse_line(string line, double* features){
	//std::string delimiter = "\t";
	//int prev_token = 0;
	//for(int i = 0; i < INPUT_SIZE; ++i){
		//int new_token = line.find(delimiter, prev_token);
		//std::string data = line.substr(prev_token, new_token); // token is "scott"
		//prev_token = new_token+delimiter.size();
		//features[i] = std::stod(data);
	//}
//}
//void extract_features(double window[][INPUT_SIZE], double* features, int *label){
	//int const starting_input = 2;
	//int labels[33] = {0};
	//for(int f = starting_input; f < starting_input+3; ++f){
		//int const ff = f-starting_input; //index to access features based on f
		//for(int i = 0; i < WINDOW_SIZE; ++i){
			//features[ff*3] += window[i][f]; //sum
			//features[ff*3+1] = features[ff*3+1] < window[i][f] ? window[i][f] : features[ff*3+1]; //Max
			//features[ff*3+2] = features[ff*3+2] > window[i][f] ? window[i][f] : features[ff*3+2]; //min
			//labels[static_cast<int>(window[i][119])] += 1;
		//}
		//features[ff*3] /= WINDOW_SIZE; //turn the sum into average
	//}
	//int label_max = 0;
	//for(int i = 1; i < 33; ++i)
		//if(labels[i] > labels[label_max])
			//label_max = i;
	//*label = label_max;
//}
//void discretize_feature(double* features){
	//double schmi[][4] = {
		//{-29.084, -19.0646, -9.04526, 10.9935},
		//{0, 8.988, 17.976, 35.952},
		//{-60.032, -47.3277, -34.6234, -9.2149},
		//{-11.7437, -2.57032, 6.60306, 24.9498},
		//{2.2894, 18.7538, 35.2182, 68.147},
		//{-40.94, -30.705, -20.47, 0},
		//{-16.8507, -9.13749, -1.42424, 14.0023},
		//{4.1023, 17.4012, 30.7002, 57.298},
		//{-61.453, -46.0898, -30.7265, 0}
	//};
	//for(int f = 0; f < FEATURES_COUNT; ++f){
		//if(features[f] < schmi[f][0]){
			//features[f] = 0;
		//}
		//else{
			//bool done = false;
			//for(int i = 0; i < 3; ++i){
				//if(features[f] >= schmi[f][i] && features[f] < schmi[f][i+1]){
					//features[f] = i+1;
					//done = true;
					//break;
				//}
			//}
			//if(!done)
				//features[f] = 4;
		//}
	//}
//}

//class loutre{
	//public:
		//static void extract_features(double window[][INPUT_SIZE], double* features, int *label){
			//int const starting_input = 2;
			//int labels[33] = {0};
			//for(int f = starting_input; f < starting_input+3; ++f){
				//int const ff = f-starting_input; //index to access features based on f
				//for(int i = 0; i < WINDOW_SIZE; ++i){
					//features[ff*3] += window[i][f]; //sum
					//features[ff*3+1] = i == 0 || features[ff*3+1] < window[i][f] ? window[i][f] : features[ff*3+1]; //Max
					//features[ff*3+2] = i == 0 || features[ff*3+2] > window[i][f] ? window[i][f] : features[ff*3+2]; //min
					//labels[static_cast<int>(window[i][119])] += 1;
				//}
				//features[ff*3] /= WINDOW_SIZE; //turn the sum into average
			//}
			//int label_max = 0;
			//for(int i = 1; i < 33; ++i)
				//if(labels[i] > labels[label_max])
					//label_max = i;
			//*label = label_max;
			//discretize_feature(features);
		//}
	//static void discretize_feature(double* features){
		//double schmi[FEATURES_COUNT][4] = {
			//{-29.084, -19.0646, -9.04526, 10.9935},
			//{0, 8.988, 17.976, 35.952},
			//{-60.032, -47.3277, -34.6234, -9.2149},
			//{-11.7437, -2.57032, 6.60306, 24.9498},
			//{2.2894, 18.7538, 35.2182, 68.147},
			//{-40.94, -30.705, -20.47, 0},
			//{-16.8507, -9.13749, -1.42424, 14.0023},
			//{4.1023, 17.4012, 30.7002, 57.298},
			//{-61.453, -46.0898, -30.7265, 0}
		//};
		//for(int f = 0; f < FEATURES_COUNT; ++f){
			//if(features[f] < schmi[f][0]){
				//features[f] = 0;
			//}
			//else{
				//bool done = false;
				//for(int i = 0; i < 3; ++i){
					//if(features[f] >= schmi[f][i] && features[f] < schmi[f][i+1]){
						//features[f] = i+1;
						//done = true;
						//break;
					//}
				//}
				//if(!done)
					//features[f] = 4;
			//}
		//}
	//}
//};
