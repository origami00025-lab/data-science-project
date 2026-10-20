"""Reproduce descriptive Iris analysis from the checked-in UCI data."""
from pathlib import Path
import json,hashlib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
df=pd.read_csv(ROOT/'data/iris.csv')
FEATURES=['sepal_length','sepal_width','petal_length','petal_width']
assert len(df)==150 and not df.isna().any().any()
assert (df[FEATURES]>0).all().all()
assert df.species.value_counts().eq(50).all()
classes=['Iris-setosa','Iris-versicolor','Iris-virginica']
palette=['#00778b','#b85d29','#7454a1'];markers=['o','^','s']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.hashsalt':'iris-project-v1'})
fig,ax=plt.subplots(figsize=(9,5.8),layout='constrained')
for species,color,marker in zip(classes,palette,markers):
 s=df[df.species==species]
 ax.scatter(s.petal_length,s.petal_width,c=color,marker=marker,label=species.replace('Iris-',''),s=45,alpha=.8,edgecolor='white',linewidth=.4)
ax.set(xlabel='Petal length (cm)',ylabel='Petal width (cm)',title='Petal measurements separate setosa in this sample')
ax.grid(alpha=.15);ax.set_axisbelow(True);ax.legend(title='Species')
fig.savefig(ROOT/'figures/petal_scatter.svg',metadata={'Date':None});plt.close(fig)
medians=df.groupby('species')[FEATURES].median().reindex(classes)
fig,axes=plt.subplots(1,4,figsize=(12,4.5),layout='constrained',sharey=True)
for ax,feature in zip(axes,FEATURES):
 for y,(species,color) in enumerate(zip(classes,palette)):
  v=medians.loc[species,feature];ax.scatter(v,y,color=color,s=90);ax.annotate(f'{v:.2f}',(v,y),xytext=(7,0),textcoords='offset points',va='center',fontsize=10)
 ax.set_xlim(0,8.5);ax.set_xlabel('Length or width (cm)');ax.set_title(feature.replace('_',' ').capitalize(),fontsize=11);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
axes[0].set_yticks(range(3),[x.replace('Iris-','') for x in classes]);axes[0].invert_yaxis()
fig.suptitle('Median measurements show larger petal differences than sepal widths',fontsize=14)
fig.savefig(ROOT/'figures/species_medians.svg',metadata={'Date':None});plt.close(fig)
medians.to_csv(ROOT/'results/species_medians.csv',float_format='%.3f')
summary={'observations':len(df),'per_species':df.species.value_counts().sort_index().to_dict(),'missing_cells':int(df.isna().sum().sum()),'duplicate_rows':int(df.duplicated().sum()),'petal_length_ranges':df.groupby('species').petal_length.agg(['min','max']).to_dict('index'),'medians_cm':medians.to_dict('index'),'dataset_sha256':hashlib.sha256((ROOT/'data/iris.csv').read_bytes()).hexdigest(),'versions':{'pandas':pd.__version__,'numpy':np.__version__,'matplotlib':matplotlib.__version__}}
(ROOT/'results/summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
