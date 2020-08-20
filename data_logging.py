#data_logging.py
import pandas as pd
import pickle
import subprocess
import numpy as np
from evaluate import *
import os, json


def log_loss(losses, loss_a, loss_u, loss_f, loss_wf, loss_train, loss_validate, dataset):
	if type(loss_a) == int:
		losses['loss_a'].append(loss_a/dataset)
	else:
		losses['loss_a'].append(loss_a.item()/dataset)
	if type(loss_u) == int:
		losses['loss_u'].append(loss_u/dataset)
	else:
		losses['loss_u'].append(loss_u.item()/dataset)
	if type(loss_f) == int:
		losses['loss_f'].append(loss_f/dataset) 
	else:
		losses['loss_f'].append(loss_f.item()/dataset) 
	if type(loss_wf) == int:
		losses['loss_wf'].append(loss_wf/dataset) 
	else:
		losses['loss_wf'].append(loss_wf.item()/dataset)
	losses['loss_train'].append(loss_train.item()/dataset)
	losses['loss_validate'].append(loss_validate.item()/10000)
	return losses

def log_data(EQUATION, MODEL, KERNEL_SIZE, FILE, PATH, BLOCKS, EPSILON, FILTERS, EPOCHS, BATCH_SIZE, LOSS, AVG_ITER, LOSSES, LOSS_TYPE, NBFUNCS, NPARAMS):
	data = model_metrics(EQUATION, MODEL, FILE, KERNEL_SIZE, PATH, EPSILON, FILTERS, BLOCKS)
	data['AVG IT/S'] = np.round(AVG_ITER, 1)
	data['LOSS'] = np.round(LOSS, 6)
	data['LOSS_TYPE'] = LOSS_TYPE
	data['EPOCHS'] = EPOCHS
	data['BATCH'] = BATCH_SIZE
	data['BLOCKS'] = BLOCKS
	data['FILTERS'] = FILTERS
	data['EPSILON'] = EPSILON
	data['NBFUNCS'] = NBFUNCS
	data['NPARAMS'] = NPARAMS
	
	COLS = ['EQUATION', 'MODEL', 'LOSS_TYPE', 'TIMESTAMP', 'DATASET', 'FOLDER', 'SHAPE', 'BLOCKS', 'K.SIZE', 'FILTERS', 'BATCH', 'EPOCHS', 'AVG IT/S', 'LOSS', 'MAEa', 'MSEa', 'MIEa', 'MAEu', 'MSEu', 'MIEu', 'NBFUNCS', 'NPARAMS']
	try:
		df = pd.read_excel('temp.xlsx', ignore_index=True)
	except:
		df = pd.DataFrame([], columns=COLS)			
	entries = df.to_dict('records')
	entries.append(data)

	df = pd.DataFrame(entries)
	df.to_excel('log_data.xlsx')
	return df

def loss_log(params, losses, df):
	try:
		with open('./losses.pkl', 'rb') as f:
			data = pickle.load(f)
	except:
		data = {}

	entry = {'losses': losses}
	entry['EQUATION'] = params['EQUATION']
	if params['MODEL'] == NetA:
		entry['MODEL'] = 'NetA'
	elif params['MODEL'] == NetB:
		entry['MODEL'] = 'NetB'
	elif params['MODEL'] == NetC:
		entry['MODEL'] = 'NetC'
	elif params['MODEL'] == ResNet:
		entry['MODEL'] = 'ResNet'
		
	entry['KERNEL_SIZE'] = params['KERNEL_SIZE']
	entry['BLOCKS'] = params['BLOCKS']
	entry['FILTERS'] = params['FILTERS']
	entry['EPSILON'] = params['EPSILON']
	entry['EPOCHS'] = params['EPOCHS']
	entry['LOSS_TYPE'] = params['LOSS_TYPE']
	entry['NBFUNCS'] = params['NBFUNCS']
	entry['NPARAMS'] = params['NPARAMS']
	for _ in ['MAEa', 'MSEa', 'MIEa', 'MAEu', 'MSEu', 'MIEu']:
		val = df[_].tolist()
		entry[_] = val[-1]
	data[params['PATH']] = entry

	with open(f'./losses.pkl', 'wb') as f:
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def log_gparams(gparams):
	cwd = os.getcwd()
	os.chdir(gparams['path'])
	with open('parameters.txt', 'w') as f:
		for k, v in gparams.items():
			entry = f"{k}:{v}\n"
			f.write(entry)
	os.chdir(cwd)
