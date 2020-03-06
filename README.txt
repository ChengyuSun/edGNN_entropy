if you want to run the program quickly,there's two part of parameters you need to set and run.

part1:
preprocess
dortmund(alternative)
--dataset
MUTAG(alternative)
--out_folder
./preprocessed_data/MUTAG(alternative)


part2:
run_model
--dataset
ptc_fr(alternative)
--config_fpath
../core/models/config_files/config_edGNN_graph_class_mutag.json(alternative)
--data_path
./preprocessed_data/MUTAG/(alternative)
--n-epochs
40
--gpu(alternative)


if you want more details,please read README_original.md in the same folder.