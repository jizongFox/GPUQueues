#!/usr/bin/env bash
labeled_sample_num=4000
save_dir=cifar10/labeled_sample_${labeled_sample_num}/augment_img
EMA_decay=0.999

declare -a StringArray=(
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacherbaseline  Dataset.augment=strong Dataset.labeled_sample_num=${labeled_sample_num}  Trainer.max_epoch=${max_epoch} Dataset.dataset_name=${dataset} RegScheduler.max_value=0  Trainer.EMA_decay=${EMA_decay}  "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_0.1      Dataset.augment=strong Dataset.labeled_sample_num=${labeled_sample_num}  Trainer.max_epoch=${max_epoch} Dataset.dataset_name=${dataset} RegScheduler.max_value=0.1  Trainer.EMA_decay=${EMA_decay} "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_1        Dataset.augment=strong Dataset.labeled_sample_num=${labeled_sample_num}  Trainer.max_epoch=${max_epoch} Dataset.dataset_name=${dataset} RegScheduler.max_value=1  Trainer.EMA_decay=${EMA_decay}  "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_10       Dataset.augment=strong Dataset.labeled_sample_num=${labeled_sample_num}  Trainer.max_epoch=${max_epoch} Dataset.dataset_name=${dataset} RegScheduler.max_value=10  Trainer.EMA_decay=${EMA_decay} "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_20       Dataset.augment=strong Dataset.labeled_sample_num=${labeled_sample_num}  Trainer.max_epoch=${max_epoch} Dataset.dataset_name=${dataset} RegScheduler.max_value=20  Trainer.EMA_decay=${EMA_decay} "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_50       Dataset.augment=strong Dataset.labeled_sample_num=${labeled_sample_num}  Trainer.max_epoch=${max_epoch} Dataset.dataset_name=${dataset} RegScheduler.max_value=50  Trainer.EMA_decay=${EMA_decay} "
)
# you may have to run this script somewhere else beside this repo
gpuqueue "${StringArray[@]}" --available_gpus 0 1
