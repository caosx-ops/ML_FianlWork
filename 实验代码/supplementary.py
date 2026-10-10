import json, numpy as np
from pathlib import Path
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split,StratifiedKFold,cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import classification_report,accuracy_score
X,y=load_digits(return_X_y=True);ix=np.arange(len(y));itr,ite=train_test_split(ix,test_size=.25,random_state=42,stratify=y)
xt,yt=X[itr],y[itr];xte,yte=X[ite],y[ite]
old=json.loads(Path('實驗結果/raw_predictions.json').read_text(encoding='utf-8')); assert old['y_test']==yte.tolist()
cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
rows=[]
for ratio in [None,.8,.9,.95,.99]:
 steps=[('scale',StandardScaler())]
 if ratio: steps += [('pca',PCA(n_components=ratio,svd_solver='full'))]
 steps += [('svc',SVC(C=10,gamma=.01))]
 model=Pipeline(steps);scores=cross_val_score(model,xt,yt,cv=cv,n_jobs=1);model.fit(xt,yt)
 rows.append(dict(ratio=ratio,cv_mean=float(scores.mean()),cv_std=float(scores.std()),folds=scores.tolist(),dimensions=int(model.named_steps['pca'].n_components_) if ratio else 64))
 if ratio in [None,.99]:
  pred=model.predict(xte);oi=0 if ratio is None else 1
  rows[-1]['verified_original']=bool(np.array_equal(pred,old['results'][oi]['predictions']))
  rows[-1]['test_accuracy']=float(accuracy_score(yte,pred))
  if ratio is None: baseline=pred
model=Pipeline([('scale',StandardScaler()),('pca',PCA(n_components=.95,svd_solver='full')),('svc',SVC())]);model.fit(xt,yt)
ph=442/450;n=450;z=1.96;ctr=(ph+z*z/(2*n))/(1+z*z/n);half=z*np.sqrt(ph*(1-ph)/n+z*z/(4*n*n))/(1+z*z/n)
result={'controlled_ablation':rows,'default_pca_verified':bool(np.array_equal(model.predict(xte),old['results'][2]['predictions'])),'default_pca_dimensions':int(model.named_steps['pca'].n_components_),'class_report':classification_report(yte,baseline,output_dict=True),'wilson_95':[ctr-half,ctr+half],'total_class_counts':np.bincount(y).tolist(),'train_class_counts':np.bincount(yt).tolist(),'test_class_counts':np.bincount(yte).tolist(),'zero_variance_columns':int(np.sum(xt.var(axis=0)==0)),'errors_test_indices':ite[baseline!=yte].tolist()}
Path('论文素材/word_revision/supplementary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
