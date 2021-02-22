from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt

def plotconfusionmatrix(y_test,pred,file_loc,p=0.5,normalize=True):
    
    y_test_pos,y_test_neg = np.bincount(y_test)
    y_pred= np.where(pred<p,0,1 )
    cfn_matrix = confusion_matrix(y_test,y_pred)
    cfn_norm_matrix = np.array([[1.0 / y_test_pos,1.0/y_test_pos],[1.0/y_test_neg,1.0/y_test_neg]])
    norm_cfn_matrix = cfn_matrix * cfn_norm_matrix

    #colsum=cfn_matrix.sum(axis=0)
    #norm_cfn_matrix = cfn_matrix / np.vstack((colsum, colsum)).T

    fig = plt.figure(figsize=(15,5))
    ax = fig.add_subplot(1,2,1)
    #sns.heatmap(cfn_matrix,cmap='magma',linewidths=0.5,annot=True,ax=ax,annot=True)
    sns.heatmap(cfn_matrix, annot = True,fmt='g',cmap='rocket')
    #tick_marks = np.arange(len(y_test))
    #plt.xticks(tick_marks, np.unique(y_test), rotation=45)
    plt.title('Confusion Matrix',color='b')
    plt.ylabel('Real Classes')
    plt.xlabel('Predicted Classes')
    #plt.savefig('/content/drive/My Drive/Colab Notebooks/NLP/cm_' +label +  '.png')
    plt.savefig(file_loc +  'cm.png')

    if normalize:    
       ax = fig.add_subplot(1,2,2)
       sns.heatmap(norm_cfn_matrix,cmap=plt.cm.Blues,linewidths=0.5,ax=ax,annot=True)

       plt.title('Normalized Confusion Matrix',color='b')
       plt.ylabel('Real Classes')
       plt.xlabel('Predicted Classes')
       plt.savefig(file_loc+ 'cm_norm.png')
       #plt.savefig('/content/drive/My Drive/Colab Notebooks/NLP/cm_norm' +label +  '.png')
       plt.show()
    
    print('---Classification Report---')
    print(classification_report(y_test,pred))
    

