#include <perceptron.hpp>
#include <cmath>

template<class feature_type, int label_count, int feature_count, int layer_count>
class MLPClassifier{
	MultiLayerPerceptron<layer_count, 600000, functions>* mlp = nullptr;
	int last_layer_size;
	int total_weight_count;
	double min_err = 1000;
	int counter = 0;
	public:
	MLPClassifier(int* layer_size, double learning_rate=0.1){
		mlp = new MultiLayerPerceptron<layer_count, 600000, functions>(layer_size, learning_rate);
		last_layer_size = layer_size[layer_count-1];
		total_weight_count = 0;
		for(int i = 1; i < layer_count; ++i)
			total_weight_count += layer_size[i]*(layer_size[i-1]+1); //+1 for the bias
		read_weights("weights");
	}
	inline bool train(feature_type const* features, int const label){
		double output[last_layer_size];
		mlp->feed_forward(features, output);
		double real_output[last_layer_size] = {0};
		real_output[label] = 1;
		double err = mlp->backpropagate(real_output);
		if(err < min_err)
			min_err = err;
		//for(int i = 0; i < label_count; ++i)
			//cout << output[i] << ",";
		//cout << endl;
		//cout << "Target " << label << " : " << output[label] << endl;
		//if(counter%5000 == 0)
			//cout << "Error: " << err << " ---- " << min_err << endl;
		counter += 1;
		return true;
	}
	inline int predict(feature_type const* features){
		double output[last_layer_size];
		mlp->feed_forward(features, output);

		//From the output find the highest
		int hightest = 0;
		for(int i = 1; i < label_count; ++i)
			if(output[i] > output[hightest])
				hightest = i;
		return hightest;
	}
	void write_weights(string const& filename) const{
		double* weights = mlp->get_weights();
		std::fstream fs;
		fs.open (filename, std::fstream::in | std::fstream::out | std::fstream::app);
		for(int i = 0; i < total_weight_count; ++i)
			fs << weights[i] << ",";
		fs.close();
	}
	void read_weights(string const& filename){
		//fs.open (filename, std::fstream::in | std::fstream::out | std::fstream::app);
		//for(int i = 0; i < total_weight_count; ++i)
			//fs << weights[i] << ",";
		double canard[] = {3.09372,2.64706,0.957192,-4.00386,1.96192,-4.62183,-0.563898,2.73559,1.40348,-1.42138,-0.609386,2.41573,-0.617025,-1.25334,0.607784,-4.08512,1.11791,-3.83275,0.834552,-2.5713,3.35343,3.71347,2.55581,4.98832,-9.33862,-1.27034,-0.508105,-1.80839,-2.59674,-1.93553,-0.563294,-2.03332,-2.57357,-0.262566,0.393646,-0.368088,-4.28198,-0.762297,-0.0893055,-0.824291,-3.69923,-0.880634,-0.0214339,-0.864253,-3.64234,-0.806187,-0.178513,-0.922197,-3.68912,-0.17037,-0.169086,-0.404388,-4.33697,-1.55952,0.332851,-1.49536,-3.04702,-1.18205,-0.157432,-0.742201,-3.37288,-1.33449,-0.351154,-1.42101,-3.15277,-1.35194,-0.195729,-1.27483,-3.19444,-1.26809,-0.452023,-1.29999,-3.22244,-1.2403,-0.360179,-1.3023,-3.26155,-1.00984,-0.237314,-1.08211,-3.4785,-4.53428,5.94569,-0.932277,-4.06729,-0.477767,0.295282,-0.641042,-4.07838,-0.808857,0.232409,-0.870326,-3.72567,-1.09815,-0.283895,-1.20729,-3.3857,-1.09859,-0.206312,-1.08491,-3.43318,-0.986684,0.148834,-0.893047,-3.59822,-1.07834,-0.243457,-1.12794,-3.43133,-0.840518,-0.0367938,-0.94816,-3.69342,-0.557524,-0.153038,-0.525468,-4.11233,-0.488206,0.209485,-0.594932,-4.06865,-0.201191,0.306814,-0.0932591,-4.63299,-0.153047,0.559317,-0.302505,-4.66467,-1.30287,-0.145215,-1.31508,-3.23038,-1.39867,-0.495435,-1.38376,-3.05396,-0.573467,0.105542,-0.493914,-4.05649,3.05733,4.03159,-4.17498,-5.72604,8.83035,-6.5516,-4.02315,-4.88544,-7.83955,-0.0719084,9.42943,-4.92304};
		mlp->set_weights(canard);

	}
	double err(void) const{
		return min_err;
	}
	~MLPClassifier(){
		write_weights("weights");
	}
};
MLPClassifier<double, LABEL_COUNT, FEATURES_COUNT, LAYER_COUNT>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	if(argc < (1+LAYER_COUNT-2)){
		cout << "Need " << (1+LAYER_COUNT-2) << " parameters." << endl;
		cout << "usage: <learning_rate> ";
		for(int i = 1; i < LAYER_COUNT-1; ++i)
			cout << "<size hidden layer " << i << "> ";
		cout << endl;
		return nullptr;
	}

	double learning_rate = stod(argv[0]);
	int layer_size[LAYER_COUNT];
	layer_size[0] = FEATURES_COUNT;
	layer_size[LAYER_COUNT-1] = LABEL_COUNT;
	for(int i = 1; i < LAYER_COUNT-1; ++i){
		layer_size[i] = stoi(argv[i]);	
	}
	return new MLPClassifier<double, LABEL_COUNT, FEATURES_COUNT, LAYER_COUNT>(layer_size, learning_rate);
}

