import os
import sys
from utils import *
from PIL import Image
from scipy.misc import imresize
input_path = "dataset/Webscope_I4/ydata-tvsum50-v1_1/video"
FPS = 3
def generate_video_dataset():
	for video in os.listdir(input_path):
		if video[0]==".":
			continue
		print("working on video: " + str(video))
		video_dir = input_path + "/" + video
		if not os.path.isdir("dataset/video_frames/Webscope_I4/" + video.split('.')[0]):
			os.mkdir("dataset/video_frames/Webscope_I4/" + video.split('.')[0])
		convert_video_to_frames(video_dir, "dataset/video_frames/Webscope_I4/" + video.split('.')[0])
		print("Video done: " + str(video))

		for frame in os.listdir("dataset/video_frames/Webscope_I4/" + video.split('.')[0]):
			if frame[0] == '.':
				continue
			dirr = "dataset/video_frames/Webscope_I4/" + video.split('.')[0] + "/" + frame
			image = np.asarray(Image.open(dirr))
			image = imresize(image,(224,224,3))
			Image.fromarray(image).save("dataset/video_frames/Webscope_I4/" + video.split('.')[0] + "/" + frame)

		print("Resized all frames of video: " + str(video))

def get_frame_importance(file_dir):
  f = open(file_dir,"r")
  video_to_frame_importance = dict()
  for video_imp in f:
    tab_separated_values = video_imp.split('\t')
    scores = tab_separated_values[2].split(',')
    i=0
    final_scores=list()
    while(i<len(scores)):
      for j in range(0, FPS*2):
        final_scores.append((int(scores[i])-1))
      i += 60
    video_to_frame_importance[tab_separated_values[0]]=final_scores
  print video_to_frame_importance
  return video_to_frame_importance

if __name__=='__main__':
	get_frame_importance(("dataset/Webscope_I4/ydata-tvsum50-v1_1/data/ydata-tvsum50-anno.tsv"))