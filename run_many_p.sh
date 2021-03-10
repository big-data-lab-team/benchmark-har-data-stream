for ((i = 4; i >= 1; i=i-1))
do
	sbatch --time=01:00:00 --account=rrg-glatard --mem=4G global_script.sh $i;
done
