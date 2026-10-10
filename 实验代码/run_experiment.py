import json, platform, time
from pathlib import Path
import numpy as np
import sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

SEED=42
X,y=load_digits(return_X_y=True)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=SEED,stratify=y)
cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=SEED)

def evaluate(name, estimator):
    start=time.perf_counter(); estimator.fit(X_train,y_train); train_s=time.perf_counter()-start
    start=time.perf_counter(); pred=estimator.predict(X_test); infer_s=time.perf_counter()-start
    p,r,f,_=precision_recall_fscore_support(y_test,pred,average='macro',zero_division=0)
    return {'name':name,'accuracy':accuracy_score(y_test,pred),'macro_precision':p,'macro_recall':r,'macro_f1':f,'train_seconds':train_s,'test_inference_seconds':infer_s,'predictions':pred.tolist(),'confusion_matrix':confusion_matrix(y_test,pred).tolist()}

# Baseline: scale pixels, then tune RBF-SVM C and gamma with training-only CV.
base=Pipeline([('scale',StandardScaler()),('svc',SVC(kernel='rbf'))])
base_grid=GridSearchCV(base,{'svc__C':[1,10,100], 'svc__gamma':['scale',.001,.01,.1]},cv=cv,scoring='accuracy',n_jobs=-1,refit=True)
base_grid.fit(X_train,y_train)
base_result=evaluate('StandardScaler + RBF-SVM',base_grid.best_estimator_)
base_result['best_params']=base_grid.best_params_; base_result['cv_best_accuracy']=base_grid.best_score_

# Proposed adaptation: preserve 95% training variance in a compact PCA space, then tune RBF-SVM.
prop=Pipeline([('scale',StandardScaler()),('pca',PCA(svd_solver='full')),('svc',SVC(kernel='rbf'))])
prop_grid=GridSearchCV(prop,{'pca__n_components':[.80,.90,.95,.99], 'svc__C':[1,10,100], 'svc__gamma':['scale',.001,.01,.1]},cv=cv,scoring='accuracy',n_jobs=-1,refit=True)
prop_grid.fit(X_train,y_train)
prop_result=evaluate('StandardScaler + PCA + RBF-SVM',prop_grid.best_estimator_)
prop_result['best_params']=prop_grid.best_params_; prop_result['cv_best_accuracy']=prop_grid.best_score_
prop_result['retained_components']=int(prop_grid.best_estimator_.named_steps['pca'].n_components_)
prop_result['retained_variance']=float(prop_grid.best_estimator_.named_steps['pca'].explained_variance_ratio_.sum())

# Ablation: same preprocessing and classifier family, fixed 95% PCA, compare parameter search vs default SVC settings.
default_pca=Pipeline([('scale',StandardScaler()),('pca',PCA(n_components=.95,svd_solver='full')),('svc',SVC(kernel='rbf'))])
abl=evaluate('PCA(95%) + default RBF-SVM (C=1)',default_pca)

out={'dataset':{'name':'Optical Recognition of Handwritten Digits (scikit-learn load_digits)','samples':int(len(y)),'features':int(X.shape[1]),'classes':int(len(np.unique(y))),'image_shape':[8,8],'pixel_range':[float(X.min()),float(X.max())],'source':'https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html'},'protocol':{'test_size':.25,'random_state':SEED,'stratified':True,'train_samples':int(len(y_train)),'test_samples':int(len(y_test)),'cv':'5-fold stratified; shuffle=True; random_state=42','selection':'All hyperparameter selection performed on training split only; held-out test evaluated once per final configuration.'},'software':{'python':platform.python_version(),'scikit_learn':sklearn.__version__,'numpy':np.__version__},'results':[base_result,prop_result,abl]}
# Do not include prediction vectors in public metrics summary; save detailed raw predictions separately.
Path('實驗結果').mkdir(exist_ok=True)
raw={'y_test':y_test.tolist(),'results':[{'name':z['name'],'predictions':z['predictions'],'confusion_matrix':z['confusion_matrix']} for z in out['results']]}
Path('實驗結果/raw_predictions.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf-8')
for z in out['results']: z.pop('predictions')
Path('實驗結果/metrics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
