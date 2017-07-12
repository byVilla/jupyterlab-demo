from __future__ import print_function
from invoke import task, run
import os

env_name = 'jupyterlab-demo'
demofolder = 'demofiles'

@task
def environment(ctx, clean=False, env_name=env_name):
	if clean:
		print('deleting environment')
		ctx.run('source deactivate; conda remove -n {} --all'.format(env_name))
	# Create a new environment
	print('creating environment')
	ctx.run('conda env create -f environment.yml -n {0!s};\
		source activate {0!s};\
		ipython kernel install --name {0!s} --display-name {0!s} --sys-prefix;\
		jupyter labextension install @jupyterlab/google-drive@0.3.1;\
		jupyter lab clean && jupyter lab build;\
		jupyter labextension install @jupyterlab/nbwidgets@0.21;\
		jupyter labextension install @jupyter-widgets/jupyterlab-manager;\
		jupyter labextension install bqplot-jupyterlab'.format(env_name), pty=True)

@task
def demofiles(ctx, clean=False, demofolder=demofolder):
	print('cleaning demofiles')
	if clean:
		ctx.run('rm -rf {}'.format(demofolder))
	print('creating demofolder')
	ctx.run('mkdir {}'.format(demofolder))
	old_pwd = os.getcwd()
	os.chdir(demofolder)
	#list of repos used in demo
	print('cloning repos into demofolder')
	reponames = ['jakevdp/PythonDataScienceHandbook',
	'swissnexSF/Urban-Data-Challenge',
	'altair-viz/altair',
	'QuantEcon/QuantEcon.notebooks',
	'theandygross/TCGA',
	'aymericdamien/TensorFlow-Examples']
	for repo in reponames:
		ctx.run('git clone https://github.com/{}.git'.format(repo))
		assert os.path.isdir(repo.split('/')[1]), '{} failed download'.format(repo)

@task
def clean(ctx, env_name=env_name, demofolder=demofolder):
	ctx.run('source deactivate;\
		conda remove --name {0!s} --all;\
		rm -rf {1!s}'.format(env_name, demofolder))