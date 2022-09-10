#include <cassert>
#include <map>
#include <mondrian_coarse.hpp>
#include <metrics.hpp>

#define RESET   "\033[0m"
#define BLACK   "\033[30m"      /* Black */
#define RED     "\033[31m"      /* Red */
#define GREEN   "\033[32m"      /* Green */
#define YELLOW  "\033[33m"      /* Yellow */
#define BLUE    "\033[34m"      /* Blue */
#define MAGENTA "\033[35m"      /* Magenta */
#define CYAN    "\033[36m"      /* Cyan */
#define WHITE   "\033[37m"      /* White */

typedef  CoarseMondrianForest<double, functions, SAMPLING_OBJECT, FEATURES_COUNT, LABEL_COUNT, SIZE> Classifier;

void helper(void){
	cout << "Usage: <parameter>:<value>" << endl;
	cout << "Parameters:" << endl;
	cout << "\tlifetime: a double higher than 0." << endl;
	cout << "\tbase_measure: a double higher than 0." << endl;
	cout << "\tdiscount_factor: a double higher than 0." << endl;
	cout << "\ttree_management: cobble, optimistic_cobble, robur, phoenix, pausing_phoenix. (default:phoenix)" << endl;
	cout << "\tdont_delete: don't allow tree deletion in the forest, yes or no." << endl;
	cout << "\ttree_count: the number of tree to use." << endl;
	cout << "\tsize_limit: An integer. The value of the limit. The type of limit is defined by the tree_management, so size_limit is either a depth or a node limit.-1 means maximum limit." << endl;
	cout << "\tprint_nodes: print a lot of debug data about nodes, yes or no." << endl;
	cout << "\tsplit_trigger: none, positiven total_count, sfe." << endl;
	cout << "\t\t- none=no split." << endl;
	cout << "\t\t- positive=split if forced extend is positive." << endl;
	cout << "\t\t- total_count=split with probability (forced extend / total data point)." << endl;
	cout << "\t\t- sfe=split with probability (forced extend / sum of forced extend on the path)." << endl;
	cout << "\tfe_distribution: zeroed, 5050." << endl;
	cout << "\t\t- zeroed=after a split, forced extend is reset." << endl;
	cout << "\t\t- 5050=After a split, forced extend is split equally between the node and the new sibling." << endl;
	cout << "\t\t- proportional=after a split, forced extend is split proportionnaly of the count." << endl;
	cout << "\t\t- decrement=after a split, forced extend decrement by 1 on node." << endl;
}
Classifier* get_classifier(int seed, int argc, char** argv){
	std::map<std::string, double> parameters;
	parameters["lifetime"] = -1;
	parameters["base_measure"] = -1;
	parameters["discount_factor"] = -1;
	parameters["tree_count"] = -1;
	parameters["size_limit"] = -1;
	parameters["enable_tree_change"] = NO;
	parameters["print_nodes"] = -1;
	parameters["split_trigger"] = SPLIT_TRIGGER_NONE;
	parameters["fe_distribution"] = FE_DISTRIBUTION_ZERO;
	parameters["reset_once"] = 1.0;
	parameters["generate_full_point"] = 1.0;
	parameters["fe_parameter"] = 1.0;
	parameters["fading_count"] = 1.0;
	parameters["split_helper"] = SPLIT_HELPER_NONE;
	parameters["extend_type"] = EXTEND_ORIGINAL;
	parameters["trim_type"] = TRIM_NONE;
	parameters["maximum_trim_size"] = 1.0;
	parameters["threshold_overfit"] = 1.0;
	parameters["tree_count_target"] = TREE_COUNT_TARGET_DISABLED;
	parameters["maximum_tree_count"] = -1;
	parameters["step_tree_change"] = 500;
	parameters["last_data_point"] = -1;
	parameters["stats_type"] = TYPE_SLIDING;
	for(int i = 0; i < argc; ++i){
		string arg(argv[i]);
		int const pos = arg.find(":");
		//Parameter is "name:", so we skip
		if(pos+1 >= arg.size() || pos < 0)
			continue;
		string const name = arg.substr(0, pos);
		string const value = arg.substr(pos+1);
		if(parameters.count(name) == 0){
			cout << "Parameter" << RED << " « " << name << " » " << RESET << "doesn't exists." << endl;
		}
		if(name == "lifetime" || name == "base_measure" || name == "discount_factor" || name == "tree_count" || name == "size_limit" || name == "fe_parameter" || name == "fading_count" || name == "maximum_trim_size" || name == "maximum_tree_count" || name == "step_tree_change" || name == "last_data_point"){
			parameters[name] = stod(value);
		}
		else if(name == "tree_count_target"){
			if(value == "best")
				parameters[name] = TREE_COUNT_TARGET_BEST;
			else
				parameters[name] = stod(value);
		}
		else if(name == "threshold_overfit"){
			if(value == "z-test")
				parameters[name] = THRESHOLD_Z_TEST;
			else if(value == "t-test")
				parameters[name] = THRESHOLD_T_TEST;
			else if(value == "sum-std")
				parameters[name] = THRESHOLD_SUM_STD;
			else if(value == "sum-var")
				parameters[name] = THRESHOLD_SUM_VAR;
			else if(value == "delta-sum-std")
				parameters[name] = THRESHOLD_DELTA_ACC_STD;
			else
				parameters[name] = stod(value);
		}
		else if(name == "stats_type"){
			if(value == "sliding"){
				parameters[name] = TYPE_SLIDING;
			}
			else if(value == "fading"){
				parameters[name] = TYPE_FADING;
			}
		}
		else if(name == "enable_tree_change"){
			if(value == "yes")
				parameters[name] = YES;
			else if(value == "no")
				parameters[name] = NO;
		}
		else if(name == "print_nodes"){
			if(value == "yes")
				parameters[name] = 1;
			else if(value == "no")
				parameters[name] = -1;
		}
		else if(name == "split_trigger"){
			if(value == "none")
				parameters[name] = SPLIT_TRIGGER_NONE;
			else if(value == "positive")
				parameters[name] = SPLIT_TRIGGER_POSITIVE;
			else if(value == "total_count")
				parameters[name] = SPLIT_TRIGGER_TOTAL;
			else if(value == "sfe")
				parameters[name] = SPLIT_TRIGGER_SFE;
		}
		else if(name == "fe_distribution"){
			if(value == "zeroed")
				parameters[name] = FE_DISTRIBUTION_ZERO;
			else if(value == "5050")
				parameters[name] = FE_DISTRIBUTION_SPLIT;
			else if(value == "proportional")
				parameters[name] = FE_DISTRIBUTION_PROPORTIONAL;
			else if(value == "decrement")
				parameters[name] = FE_DISTRIBUTION_DECREMENT;
		}
		else if(name == "split_helper"){
			if(value == "none")
				parameters[name] = SPLIT_HELPER_NONE;
			else if(value == "avg")
				parameters[name] = SPLIT_HELPER_AVG;
			else if(value == "weighted")
				parameters[name] = SPLIT_HELPER_WEIGHTED;
		}
		else if(name == "extend_type"){
			if(value == "original")
				parameters[name] = EXTEND_ORIGINAL;
			else if(value == "none")
				parameters[name] = EXTEND_NONE;
			else if(value == "barycenter")
				parameters[name] = EXTEND_BARYCENTER;
		}
		else if(name == "trim_type"){
			if(value == "none")
				parameters[name] = TRIM_NONE;
			else if(value == "random")
				parameters[name] = TRIM_RANDOM;
			else if(value == "fading_score")
				parameters[name] = TRIM_FADING;
			else if(value == "count")
				parameters[name] = TRIM_COUNT;
			else if(value == "chop")
				parameters[name] = TRIM_CHOP;
		}
		else if(name == "reset_once"){
			if(value == "yes")
				parameters[name] = 1;
			else if(value == "no")
				parameters[name] = -1;
		}
		else if(name == "generate_full_point"){
			if(value == "yes")
				parameters[name] = 1;
			else if(value == "no")
				parameters[name] = -1;
		}
	}
	bool stop = false;
	if(parameters["lifetime"] < 0){
		cout << RED << "lifetime " << RESET << "parameter is missing" << endl;
		stop = true;
	}
	if(parameters["base_measure"] < 0){
		cout << RED << "base_measure " << RESET << "parameter is missing" << endl;
		stop = true;
	}
	if(parameters["discount_factor"] < 0){
		cout << RED << "discount_factor " << RESET << "parameter is missing" << endl;
		stop = true;
	}
	if(parameters["tree_count"] < 0){
		cout <<  RED << "tree_count " << RESET << "parameter is missing" << endl;
		stop = true;
	}

	if(stop){
		helper();
		return nullptr;
	}
	srand(seed);
	return new Classifier
		(parameters["lifetime"], parameters["base_measure"], parameters["discount_factor"],
		 static_cast<int>(parameters["tree_count"]),
		 static_cast<int>(parameters["size_limit"]),
		 static_cast<int>(parameters["enable_tree_change"]),
		 parameters["print_nodes"] > 0,
		 static_cast<int>(parameters["fe_distribution"]),
		 static_cast<int>(parameters["split_trigger"]),
		 parameters["generate_full_point"] > 0,
		 parameters["reset_once"] > 0,
		 parameters["fe_parameter"],
		 parameters["fading_count"],
		 static_cast<int>(parameters["split_helper"]),
		 static_cast<int>(parameters["extend_type"]),
		 static_cast<int>(parameters["trim_type"]),
		 parameters["maximum_trim_size"],
		 static_cast<int>(parameters["tree_count_target"]),
		 static_cast<int>(parameters["maximum_tree_count"]),
		 parameters["threshold_overfit"],
		 static_cast<int>(parameters["step_tree_change"]),
		 static_cast<int>(parameters["last_data_point"]),
		 static_cast<int>(parameters["stats_type"])
		 );
}

