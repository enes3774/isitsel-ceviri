

#bu script kaydedilen hand ve body pointleri alıp normalizasyon,eksik frameleri çıkarma, eksik tespit edilen noktaları
#kendi weighted algorithm ile kapatma ve bilek ile el verilerini alarak eli tam olarak bilek noktasına koyuyor
import codecs
import math
import re
import os
import json
import h5py
import subprocess

import numpy
import os
import re

def walkDir(dname, filt=r".*"):
  result = []
  for root, dnames, fnames in os.walk(dname):
    for fname in fnames:
      if re.search(filt, fname):
        foo = root + "/" + fname
        foo = re.sub(r"[/\\]+", "/", foo)
        result.append(foo)
  return result

def selectPoints(points, keepThis):
  points2 = []
  for i in keepThis:
    points2.append(points[3 * i + 0])
    points2.append(points[3 * i + 1])
    points2.append(points[3 * i + 2])
  return points2


def noNones(l):
  l2 = []
  for i in l:
    if not i is None:
      l2.append(i)
  return l2





def prune(Xx, Xy, Xw, watchThis, threshold, dtype):
  id_list=[]
  T = Xw.shape[0]
  N = Xw.shape[1]
  Yx = numpy.zeros((T, N), dtype=dtype)
  Yy = numpy.zeros((T, N), dtype=dtype)
  Yw = numpy.zeros((T, N), dtype=dtype)
  for t in range(T):
    sum0 = 0
    sum1 = 0.0
    for i in watchThis:
      sum0 = sum0 + 1
      sum1 = sum1 + Xw[t, i]
    Ew = sum1 / sum0
    if Ew >= threshold:
      for i in range(N):
        Yx[t, i] = Xx[t, i]
        Yy[t, i] = Xy[t, i]
        Yw[t, i] = Xw[t, i]
      if N==0:
        id_list.append(t)
    else:
        id_list.append(t)
  return Yx, Yy, Yw,id_list



def interpolation(Xx, Xy, Xw, threshold, dtype):
  T = Xw.shape[0]
  N = Xw.shape[1]
  Yx = numpy.zeros((T, N), dtype=dtype)
  Yy = numpy.zeros((T, N), dtype=dtype)
  for t in range(T):
    for i in range(N):
      a1 = Xx[t, i]
      a2 = Xy[t, i]
      p = Xw[t, i]
      sumpa1 = p * a1
      sumpa2 = p * a2
      sump = p
      delta = 0
      while sump < threshold:
        change = False
        delta = delta + 1
        t2 = t + delta
        if t2 < T:
          a1 = Xx[t2, i]
          a2 = Xy[t2, i]
          p = Xw[t2, i]
          sumpa1 = sumpa1 + p * a1
          sumpa2 = sumpa2 + p * a2
          sump = sump + p
          change = True
        t2 = t - delta
        if t2 >= 0:
          a1 = Xx[t2, i]
          a2 = Xy[t2, i]
          p = Xw[t2, i]
          sumpa1 = sumpa1 + p * a1
          sumpa2 = sumpa2 + p * a2
          sump = sump + p
          change = True
        if not change:
          break
      if sump <= 0.0:
        sump = 1e-10
      Yx[t, i] = sumpa1 / sump
      Yy[t, i] = sumpa2 / sump
  return Yx, Yy, Xw

def convList2Array(lst): 
  T, dim = lst[0].shape
  a = []
  for t in range(T):
    a_t = []
    for i in range(dim):
      for j in range(len(lst)):
        a_t.append(lst[j][t, i])
    a.append(a_t)
  return numpy.asarray(a)
def normalization(Xx, Xy):
  T, n = Xx.shape
  sum0 = T * n
  sum1Xx = numpy.sum(numpy.sum(Xx))
  sum2Xx = numpy.sum(numpy.sum(Xx * Xx))
  sum1Xy = numpy.sum(numpy.sum(Xy))
  sum2Xy = numpy.sum(numpy.sum(Xy * Xy))
  mux = sum1Xx / sum0
  muy = sum1Xy / sum0
  sum0 = 2 * sum0
  sum1 = sum1Xx + sum1Xy
  sum2 = sum2Xx + sum2Xy
  mu = sum1 / sum0
  sigma2 = (sum2 / sum0) - mu * mu
  if sigma2 < 1e-10:
    simga2 = 1e-10
  sigma = math.sqrt(sigma2)
  return (Xx - mux) / sigma, (Xy - muy) / sigma
      

import numpy as np
def loadData(dname,vid_id):

  fnames = walkDir(dname = dname, filt = r"\.json$")
  fnames.sort()
  frames = []
  id_list=[]
  ids_of_val_poses=[]
  
  for i,fname in enumerate(fnames):
      
    p = re.search(r"([^\\/]+)_(\d+)_keypoints\.json$", fname)
    print(fname)
    with open(fname) as json_data:
      data = json.load(json_data)
    if len(data["people"]) == 0:
      id_list.append(i)
      continue
      
    i = int(p.group(2))
    while len(frames) < i + 1:
      frames.append(None)
    
    theTallest = data["people"][0]
    
    idxsPose = [0, 1, 2, 3, 4, 5, 6, 7]
    idxsHand = range(21)    

    if theTallest is None:
      points = 3 * (len(idxsPose) + 2 * len(idxsHand)) * [0.0]
    else:
      pointsP = theTallest["pose_keypoints_2d"]
      pointsLH = theTallest["hand_left_keypoints_2d"]
      pointsRH = theTallest["hand_right_keypoints_2d"]
      pointsP = selectPoints(pointsP, idxsPose)
      pointsLH = selectPoints(pointsLH, idxsHand)
      pointsRH = selectPoints(pointsRH, idxsHand)
      points = pointsP + pointsLH + pointsRH

    if not points[0] == 0.0:
      frames[i] = points
      ids_of_val_poses.append(i)
    else:
      id_list.append(i)
  data=numpy.asarray(noNones(frames))
     #////////////////////////////////////////////////şimdi intrpolation ve prune kısmı//////////////
  """   
  X=data[:,:3*8].copy()
    
  Xx = X[0:X.shape[0], 0:(X.shape[1]):3]
  Xy = X[0:X.shape[0], 1:(X.shape[1]):3]
  Xw = X[0:X.shape[0], 2:(X.shape[1]):3]
  dtype="float32"
  Xx, Xy, Xw = interpolation(Xx, Xy, Xw, 0.99, dtype)
  X=convList2Array([Xx, Xy, Xw])
  data[:,:3*8]=X
  for i in range(42):
        data_ = np.array(data[:,3*(i+8)])
        non_zero_indices = np.nonzero(data_)[0]
        interpolated_values = np.interp(range(len(data_)), non_zero_indices, data_[non_zero_indices])
        data[:,3*(i+8)]=interpolated_values
        data_ = np.array(data[:,3*(i+8)+1])
        non_zero_indices = np.nonzero(data_)[0]
        interpolated_values = np.interp(range(len(data_)), non_zero_indices, data_[non_zero_indices])
        data[:,3*(i+8)+1]=interpolated_values
  """
  X=data.copy()
    
  Xx = X[0:X.shape[0], 0:(X.shape[1]):3]
  Xy = X[0:X.shape[0], 1:(X.shape[1]):3]
  Xw = X[0:X.shape[0], 2:(X.shape[1]):3]
  dtype="float32"
  Xx, Xy, Xw = interpolation(Xx, Xy, Xw, 0.99, dtype)
  
  a=(Xx[:,8]-Xx[:,4])
  b=(Xx[:,29]-Xx[:,7])
  c=(Xy[:,8]-Xy[:,4])
  d=(Xy[:,29]-Xy[:,7])
  for i in range(21):
      Xx[:,i+8]-=a
  for i in range(21):
      Xx[:,i+29]-=b
  for i in range(21):
      Xy[:,i+8]-=c
  for i in range(21):
      Xy[:,i+29]-=d
  Xx, Xy = normalization(Xx, Xy)
  """
  X=convList2Array([Xx, Xy, Xw])
  data=X
 """
  
  os.makedirs(f"processed_poses/{vid_id}", exist_ok=True)
  X=convList2Array([Xx, Xy])
  for i,ids in enumerate(ids_of_val_poses):
      filename=f'processed_poses/{vid_id}/{vid_id}_{str(ids).zfill(12)}_keypoints.txt'
      
      with open(filename, 'w') as f:
        list_=list(X[i])
        for j in range(len(list_)):
            f.write("%e\t" % list_[j])
        
    
     
      
         
  return data,id_list,ids_of_val_poses


data_lists=os.listdir("pose_results")
# Process and save hand data
for vid_id in data_lists:
 
  
  dnameIn = f"pose_results/{vid_id}"
  fnameOut = f"output_jsons/{vid_id}"
  
  
  recs = {}
  for fname in walkDir(dnameIn, filt=r"\.[jJ][sS][oO][nN]$"):
    dname = re.sub(r"(.*)[/\\].*", r"\1", fname)
    key = re.sub(r".*[/\\]", "", dname)
    recs[key] = dname
  
  #hf = h5py.File(fnameOut, "w")
  for key in recs:
    print(key)
    data, id_list,ids_of_val_poses= loadData(recs[key], vid_id)
    #hf.create_dataset(key, data=data, dtype="float32")    
  #hf.close()