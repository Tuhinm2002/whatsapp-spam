import torch.nn as nn
import torch 
import torch.functional as F

# from myclass import CNN,ClassificationBase

class ClassificationBase(nn.Module):
    def training_step(self,batch):
        img,labels=batch
        out=self(img)
        loss=F.cross_entropy(out,labels)
        return loss
    
    def validation_step(self,batch):
        img,labels=batch
        out=self(img)
        loss=F.cross_entropy(out,labels)
        acc=accuracy(out,labels)
        return {'val_loss':loss.detach(), 'val_acc':acc}
    
    def validation_epoch_end(self,outputs):
        batch_losses=[x['val_loss'] for x in outputs]
        epoch_loss=torch.stack(batch_losses).mean()
        batch_acc=[x['val_acc'] for x in outputs]
        epoch_acc=torch.stack(batch_acc).mean()
        return {'val_loss':epoch_loss.item(),'val_acc':epoch_acc.item()}
    
    def epoch_end(self,epoch,result):
        print("Epoch [{}], val_loss:{:.4f}, val_acc:{:.4f} ".format(epoch,result['val_loss'],result['val_acc']))
     

def accuracy(outputs, labels):
    _,preds=torch.max(outputs,dim=1)
    return torch.tensor(torch.sum(preds==labels).item())/len(preds)

class CNN(ClassificationBase):
    def __init__(self):
        super().__init__()
        self.network=nn.Sequential(nn.Conv2d(3,32,kernel_size=3,padding=1),
                                  nn.ReLU(),
                                  nn.Conv2d(32,64,kernel_size=3,padding=1,stride=1),
                                  nn.ReLU(),
                                  nn.MaxPool2d(2,2),

                                  nn.Conv2d(64,128,kernel_size=3,padding=1,stride=1),
                                  nn.ReLU(),
                                  nn.Conv2d(128,128,kernel_size=3,padding=1,stride=1),
                                  nn.ReLU(),
                                  nn.MaxPool2d(2,2),

                                  nn.Conv2d(128,256,kernel_size=3,padding=1,stride=1),
                                  nn.ReLU(),
                                  nn.Conv2d(256,256,kernel_size=3,padding=1,stride=1),
                                  nn.ReLU(),
                                  nn.MaxPool2d(2,2),
                                   
                                   nn.Flatten(),
                                   nn.Linear(256*4*4,1024),
                                   nn.ReLU(),
                                   nn.Linear(1024,512),
                                   nn.ReLU(),
                                   nn.Linear(512,2)
                                  )
    def forward(self,xb):
        return self.network(xb)
    
