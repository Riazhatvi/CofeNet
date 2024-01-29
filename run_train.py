# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_ndTF4ptXVTksSPES4eTVUNfkEx9mcRo
"""

import sys
!git clone https://github.com/cofe-ai/CofeNet.git
sys.path.insert(0, '/content/CofeNet')

# Commented out IPython magic to ensure Python compatibility.
!pip install absl-py==0.13.0 \
  boto3==1.17.112 \
  botocore==1.20.112 \
  cachetools==4.2.2 \
  certifi==2021.5.30 \
  charset-normalizer==2.0.2 \
  click==8.0.1 \
  future==0.18.2 \
  google-auth==1.33.0 \
  google-auth-oauthlib==0.4.4 \
  grpcio==1.38.1 \
  idna==3.2 \
  importlib-metadata==4.6.1 \
  jmespath==0.10.0 \
  joblib==1.0.1 \
  Markdown==3.3.4 \
  numpy==1.21.0 \
  oauthlib==3.1.1 \
  protobuf==3.17.3 \
  pyasn1==0.4.8 \
  pyasn1-modules==0.2.8 \
  pynvml==11.0.0 \
  python-dateutil==2.8.2 \
  pytorch-crf==0.7.2 \
  pytorch-transformers==1.2.0 \
  regex==2021.7.6 \
  requests==2.26.0 \
  requests-oauthlib==1.3.0 \
  rsa==4.7.2 \
  s3transfer==0.4.2 \
  sacremoses==0.0.45 \
  scikit-learn==0.23.2 \
  scipy==1.7.0 \
  sentencepiece==0.1.96 \
  six==1.16.0 \
  tensorboard==2.4.0 \
  tensorboard-plugin-wit==1.8.0 \
  threadpoolctl==2.2.0 \
  torch==1.2.0 \
  tqdm==4.61.2 \
  typing-extensions==3.10.0.0 \
  urllib3==1.26.6 \
  Werkzeug==2.0.1 \
  zipp==3.5.0 \
  pandas==1.3.5 \
  pytz==2022.5
!tensorboard --bind_all --logdir /content/CofeNet/log
!pip install pynvml
!pip install pytorch_transformers
!pip install torchcrf
!pip install --upgrade pip
!pip install --upgrade setuptools
# %pip install pytorch-crf

# Train Cofe for polnear - Example with BERT model
!python /content/CofeNet/run_train.py --exp_name pn_bert_cofe --trn_name v1 --eval_per_step 500 --max_epoch 6 --batch_size 15 --bert_learning_rate 5e-5 --gpu 0

# Evaluate the trained model
!python /content/CofeNet/run_eval.py --exp_name pn_bert_cofe --gpu 0

# -*- coding: utf-8 -*-
import argparse
from utils import get_gpus_meminfo, get_best_device, cuda_is_available
from exe.trainer import Trainer
from utils import set_global_rand_seed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_name", type=str, default='pn_bert_cofe')
    parser.add_argument("--trn_name", type=str, default='v1')

    parser.add_argument("--gpu", type=int, default=None)
    parser.add_argument("--use_cpu", default=False, action='store_true')

    parser.add_argument('--show_per_step', type=int, default=10)
    parser.add_argument("--eval_per_step", type=int, default=250)
    parser.add_argument("--min_eval_step", type=int, default=100)
    parser.add_argument("--eval_type", type=str, default='bio_f1', choices=["bio_f1", "exact_f1_avg"])
    parser.add_argument('--max_mod_saved_num', type=int, default=2)
    parser.add_argument("--do_not_save_mod", default=False, action='store_true')

    parser.add_argument('--random_seed', type=int, default=2021)
    parser.add_argument('--optim', type=str, default="Adam", choices=["Adam", "AdamW", "Adadelta", "RMSprop", "Adagrad"])

    parser.add_argument("--max_epoch", type=int, default=15)
    parser.add_argument("--learning_rate", type=float, default=1e-3)
    parser.add_argument('--weight_decay', type=float, default=0.0)
    parser.add_argument("--bert_learning_rate", type=float, default=1e-4)  # 5e-5
    parser.add_argument('--bert_weight_decay', type=float, default=0.0)
    parser.add_argument("--fix_bert", default=False, action='store_true')
    parser.add_argument("--batch_size", type=int, default=32)

    # Parse only the relevant arguments
    args, _ = parser.parse_known_args()

    # select the good gpu/cpu
    if not args.use_cpu and cuda_is_available():
        if (args.gpu is None) or (args.gpu not in get_gpus_meminfo()[0]):
            args.gpu = get_best_device()
    else:
        args.gpu = None

    if args.gpu is None:
        print('device: CPU')
    else:
        print('device: GPU %d' % args.gpu)

    Trainer(vars(args)).train()

if __name__ == "__main__":
    main()

