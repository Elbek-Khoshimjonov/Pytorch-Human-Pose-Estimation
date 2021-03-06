from os import environ
environ["CUDA_VISIBLE_DEVICES"] = "0,1"

import torch
import builder
import trainer

import os
import time
import argparse
from opts import opts


opts = opts().parse()
torch.set_default_tensor_type('torch.DoubleTensor' if opts.usedouble else 'torch.FloatTensor')
Builder = builder.Builder(opts)

Model = Builder.Model()
Optimizer = Builder.Optimizer(Model)
Loss = Builder.Loss()
Metrics = Builder.Metric()
TrainDataLoader, ValDataLoader = Builder.DataLoaders()
Epoch = Builder.Epoch()


# gpus = [ int(id) for id in opts.gpuid.split(",")]

Model = torch.nn.DataParallel(Model.cuda())


# opts.saveDir = os.path.join(opts.saveDir, os.path.join(opts.model, 'logs_{}'.format(datetime.datetime.now().isoformat())))
File = os.path.join(opts.saveDir, 'log.txt')

Trainer = trainer.Trainer(Model, Optimizer, Loss, Metrics, File, None, opts)

if opts.test:
	Trainer.test(ValDataLoader)
	exit()

Trainer.train(TrainDataLoader, ValDataLoader, Epoch, opts.nEpochs)
