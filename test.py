import gtg
import numpy as np

chunk_result =np.load('EM32_Building_Lobby_1_M6_s3_Babble_0dB-0_0.npy')
cen_freq = np.load('central_freq.npy')
gtg.gtgplot(chunk_result, cen_freq, 64000, 16000)#just for debug